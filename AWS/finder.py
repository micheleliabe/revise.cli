import datetime
import boto3
import sys

from datetime import datetime, timedelta


class EC2Finder:

    def get_gp2_volumes(self, region: str):
        """
        Retrieves information about all GP2 volumes in the specified AWS region.

        Args:
            region (str): The AWS region to retrieve the GP2 volumes from.

        Returns:
            list: A list of dictionaries containing information about the GP2 volumes.
        """
        client = boto3.client('ec2', region_name=region)

        try:

            response = client.describe_volumes(
                Filters=[
                    {
                        "Name": 'volume-type',
                        "Values": ["gp2"]
                    }
                ]
            )

            return [
                {
                    'Region': region,
                    'VolumeId': volume['VolumeId'],
                    'VolumeType': volume['VolumeType']
                }
                for volume in response.get('Volumes')
            ]

        except Exception as e:
            print(f"Error retrieving GP2 volumes in {region}: {e}")
            sys.exit()

    def get_volumes_on_stopped_instances(self, region: str):
        """
        Retrieves information about all volumes attached to stopped instances in the specified AWS region.

        Args:
            region (str): The AWS region to retrieve the volumes from.

        Returns:
            list: A list of dictionaries containing information about the volumes.
        """
        # Initialize EC2 client for the specified region
        client = boto3.client('ec2', region_name=region)

        try:
            # Get stopped instances
            response = client.describe_instances(
                Filters=[
                    {
                        'Name': 'instance-state-name',
                        'Values': ['stopped']
                    }
                ]
            )

            # relevant information for each volume
            volumes = []
            for reservation in response.get("Reservations"):
                for instance in reservation["Instances"]:
                    for device in instance["BlockDeviceMappings"]:
                        volumes.append({
                            "region": region,
                            "instance": instance["InstanceId"],
                            "device": device["DeviceName"],
                            "volume": device["Ebs"]["VolumeId"]
                        })
            return volumes

        except Exception as e:
            print(
                f"Error retrieving volumes on stopped instances in {region}: {e}")
            sys.exit()

    def get_detached_volumes(self, region: str):
        """
        Retrieves information about all detached volumes in the specified AWS region.

        Args:
            region (str): The AWS region to retrieve the detached volumes from.

        Returns:
            list: A list of dictionaries containing information about the detached volumes.
        """
        # Initialize EC2 client for the specified region
        client = boto3.client('ec2', region_name=region)

        try:
            # Get all volumes
            response = client.describe_volumes()

            # relevant information for each volume
            volumes = []
            for volume in response.get("Volumes"):
                if volume["State"] == "available":
                    volumes.append({
                        "region": region,
                        "volume": volume["VolumeId"],
                        "AvailabilityZone": volume["AvailabilityZone"],
                        "VolumeType": volume["VolumeType"],
                        "Size": str(volume["Size"])
                    })
            return volumes

        except Exception as e:
            print(f"Error retrieving detached volumes in {region}: {e}")
            sys.exit()

    def get_detached_ips(self, region: str):
        """
        Retrieves information about all detached IP addresses in the specified AWS region.

        Args:
            region (str): The AWS region to retrieve the detached IP addresses from.

        Returns:
            list: A list of dictionaries containing information about the detached IP addresses.
        """
        # Initialize EC2 client for the specified region
        client = boto3.client('ec2', region_name=region)

        try:
            # Get all IP addresses
            response = client.describe_addresses()

            # Extract relevant information for each unused Elastic IPs
            not_used_ips = []
            for address in response.get('Addresses', []):
                # Check if Elastic IP is not associated with any network interface
                if "NetworkInterfaceId" not in address and address is not None:
                    not_used_ips.append({
                        "Region": region,
                        "Address": address['PublicIp'],
                        "AllocationId": address['AllocationId']
                    })

            return not_used_ips
        except Exception as e:
            print(f"Error retrieving detached IP addresses in {region}: {e}")

    def get_old_snapshots(self, region: str, retention):
        """
        Retrieves information about all old snapshots in the specified AWS region.

        Args:
            region (str): The AWS region to retrieve the old snapshots from.

        Returns:
            list: A list of dictionaries containing information about the old snapshots.
        """
        # Initialize EC2 client for the specified region
        client = boto3.client('ec2', region_name=region)

        try:
            # Get all snapshots
            response = client.describe_snapshots(
                OwnerIds=['self'])

            # Extract relevant information for each old snapshot
            old_snapshots = []
            for snapshot in response.get('Snapshots', []):
                # Check if snapshot is older
                if snapshot['StartTime'].date() < datetime.now().date() - timedelta(days=retention):
                    old_snapshots.append({
                        "Region": region,
                        "SnapshotId": snapshot['SnapshotId'],
                        "StartTime": str(snapshot['StartTime'].date())
                    })

            return old_snapshots

        except Exception as e:
            print(f"Error retrieving old snapshots in {region}: {e}")
            sys.exit()

    def get_security_groups_public_egress(self, region: str):
        """
        Retrieves information about all public egress rules in the specified AWS region.

        Args:
            region (str): The AWS region to retrieve the public egress rules from.

        Returns:
            list: A list of dictionaries containing information about the public egress rules.
        """
        # Initialize EC2 client for the specified region
        client = boto3.client('ec2', region_name=region)

        try:

            # Describe security groups with IP permission CIDR as "0.0.0.0/0" (internet access)
            response = client.describe_security_groups(Filters=[
                {
                    "Name": "ip-permission.cidr",
                    "Values": ["0.0.0.0/0"]
                }
            ])

            # Extract relevant information for each security group
            security_groups = []
            for item in response["SecurityGroups"]:
                security_groups.append({
                    "Region": region,
                    "GroupId": item['GroupId'],
                    "GroupName": item["GroupName"],
                    "VpcId": item["VpcId"]
                })

            return security_groups

        except Exception as e:
            print(f"Error retrieving public egress rules in {region}: {e}")

class S3Finder:
    def get_buckets_not_public_acess_block(self):
        """
        Retrieves information about all buckets that do not have public access block enabled in the specified AWS region.

        Args:
            region (str): The AWS region to retrieve the buckets from.

        Returns:
            list: A list of dictionaries containing information about the buckets.
        """
        # Initialize S3 client for the specified region
        client = boto3.client('s3')

        try:
            # Get all buckets
            response = client.list_buckets()

            # Extract relevant information for each bucket
            buckets = []
            public_buckets = []
            
            for bucket in response["Buckets"]:
                buckets.append(bucket["Name"])

            for bucket in buckets:
                try:
                    client.get_public_access_block(
                        Bucket=bucket
                    )
                    continue
                except:
                    public_buckets.append({"Bucket": bucket, "Public": "True"})

            return public_buckets

        except Exception as e:
            print(f"Error retrieving buckets not public access block in {region}: {e}")
            sys.exit()