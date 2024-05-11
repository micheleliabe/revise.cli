import json
import boto3

from utils.logger import log
from rich.console import Console
from rich.table import Table, box
from AWS.finder import EC2Finder
from AWS.finder import S3Finder

# Initialize Rich Console for better terminal output formatting
console = Console()

class AWSRecommendations():

    def __init__(self, title: str, description: str, documentation: str, data: list):
        """
        Initialize a new recommendation object.

        Args:
            title (str): The title of the recommendation.
            description (str): A brief description of the recommendation.
            documentation (str): The documentation for the recommendation.
            data (list): A list of items that were found.
        """
        self.title = title
        self.description = description
        self.documentation = documentation
        self.data = data

    # Function to display data in a tabular format with a title and optional recommendation
    def show_recommendations(self):

        if self.data == []:
            return

        # Create a Rich Table with specified title and formatting
        table = Table(
            title=f"[bold purple]{self.title}", show_header=True, show_lines=True, box=box.ROUNDED,
            title_justify='left'
        )

        # Extract column names from the data
        columns = self.data[0].keys()

        # Add columns to the table
        for column in columns:
            table.add_column(column)

        # Add rows to the table
        for region in self.data:
            row = []
            # Populate each row with values from the region dictionary
            for key, value in region.items():
                row.append(value)
            table.add_row(*row)

        console.print()
        console.print()

        # Print the table using Rich Console
        console.print(table)

        # Print recommendation if provided
        if self.description:
            console.print(
                f"\n [yellow]Recommendation: \n  [white]- {self.description}")

            console.print(
                f"\n [yellow]Documentation: \n  [white]- {self.documentation}")

        # Add a newline after printing the table
        console.print()
        console.print()
        console.print()
        console.print()


class AWSRegionsIterator:
    """
    Iterates over a set of AWS regions and executes a given function for each region.
    """

    def __init__(self, regions_string):
        """
        Initializes the AWSRegionsIterator with a string of region names.

        Args:
            regions_string (str): A space-separated string of AWS region names.
        """
        self.regions = regions_string.split(" ")
        self.regions = set(self.regions)

    def execute(self, func, operation, *args):
        """
        Executes the given function for each AWS region and returns the results.

        Args:
            func (callable): The function to be executed for each region.
            *args: Additional arguments to be passed to the function.

        Returns:
            list: A list of results from executing the function for each region.
        """
        results = []
        for region in self.regions:
            log.info(f"{operation} on {region} started!")

            with console.status(f"{operation} on {region}", spinner="aesthetic"):
                data = func(region, *args)

            log.info(f"{operation} on {region} finished!")

            if data:
                for region_itens in data:
                    log.debug(
                        f"{region_itens}")
                    results.append(region_itens)
        return results


class AWSCostChecker:
    def __init__(self, regions):
        """
        Initializes the AWSCostChecker with a list of AWS regions.

        Args:
            regions (str): A space-separated string of AWS region names.
        """
        self.regions_iterator = AWSRegionsIterator(regions)
        self.ec2_finder = EC2Finder()

    def get_gp2_volumes(self):
        """
        Retrieves information about all GP2 volumes across the specified AWS regions.

        Returns:
            list: A list of data about the GP2 volumes.
        """
        data = self.regions_iterator.execute(
            self.ec2_finder.get_gp2_volumes, "GET - GP2 volumes")

        recommendation = AWSRecommendations(
            "Upgrade to EBS gp3 Volumes for Cost Savings and Better Performance!",
            "We recommend migrating your AWS EBS gp2 volumes to gp3. gp3 volumes offer lower costs and enhanced performance. Refer to our documentation for guidance on transitioning.",
            "https://aws.amazon.com/blogs/storage/migrate-your-amazon-ebs-volumes-from-gp2-to-gp3-and-save-up-to-20-on-costs/",
            data
        )

        recommendation.show_recommendations()
        return data

    def get_volumes_on_stopped_instances(self):
        """
        Retrieves information about all volumes attached to stopped instances across the specified AWS regions.

        Returns:
            list: A list of data about the volumes attached to stopped instances.
        """
        data = self.regions_iterator.execute(
            self.ec2_finder.get_volumes_on_stopped_instances, "GET - Volumes on stopped instances")

        recommendation_text = """To avoid unnecessary charges for Amazon EBS storage when your (Amazon EC2) instances are stopped, consider the following steps:

    1. Take snapshots of unused EBS volumes to preserve data.
    2. Delete active EBS volumes that are not currently needed.
    3. Utilize EBS snapshots, which are billed at a lower rate, to retain stored information for future use.
    4. When necessary, replace EBS volumes with the stored snapshots to reduce costs while maintaining data availability.
"""

        recommendation = AWSRecommendations(
            "EBS Charges for Stopped EC2 Instances",
            recommendation_text,
            "https://aws.amazon.com/blogs/storage/migrate-your-amazon-ebs-volumes-from-gp2-to-gp3-and-save-up-to-20-on-costs/",
            data
        )

        recommendation.show_recommendations()
        return data

    def get_detached_volumes(self):
        """
        Retrieves information about all detached volumes across the specified AWS regions.

        Returns:
            list: A list of data about the detached volumes.
        """
        data = self.regions_iterator.execute(
            self.ec2_finder.get_detached_volumes, "GET - Detached volumes")

        recommendation = AWSRecommendations(
            "Unused EBS Volumes",
            "AWS suggests taking snapshots of detached volumes and then deleting them to reduce costs.",
            "https://docs.aws.amazon.com/pt_br/ebs/latest/userguide/ebs-detaching-volume.html",
            data
        )

        recommendation.show_recommendations()
        return data

    def get_detached_ips(self):
        """
        Retrieves information about all detached IP addresses across the specified AWS regions.

        Returns:
            list: A list of data about the detached IP addresses.
        """

        data = self.regions_iterator.execute(
            self.ec2_finder.get_detached_ips, "GET - Detached IP addresses")

        recommendation = AWSRecommendations(
            "Unused Elastic IPs",
            "Release detached IPs",
            "https://aws.amazon.com/blogs/aws/new-aws-public-ipv4-address-charge-public-ip-insights/",
            data
        )

        recommendation.show_recommendations()
        return data

    def get_old_snapshots(self, retention):
        """
        Retrieves information about all old snapshots across the specified AWS regions.

        Returns:
            list: A list of data about the old snapshots.
        """
        data = self.regions_iterator.execute(
            self.ec2_finder.get_old_snapshots, "GET - Old snapshots", retention)

        recommendation = AWSRecommendations(
            "Old Snapshots",
            "Remove old snapshots and establish retention policies.",
            "https://docs.aws.amazon.com/pt_br/ebs/latest/userguide/automating-snapshots.html",
            data
        )

        recommendation.show_recommendations()
        return data


class AWSSecurityChecker:
    def __init__(self, regions):
        """
        Initializes the AWSSecurityChecker with a list of AWS regions.

        Args:
            regions (str): A space-separated string of AWS region names.
        """
        self.regions_iterator = AWSRegionsIterator(regions)
        self.ec2_finder = EC2Finder()
        self.s3_finder = S3Finder()

    def get_security_groups_public_egress(self):
        """
        Retrieves information about all public egress rules in the specified AWS regions.

        Returns:
            list: A list of data about the public egress rules.
        """
        data = self.regions_iterator.execute(
            self.ec2_finder.get_security_groups_public_egress, "GET - Security groups with public egress rules")

        recommendation = AWSRecommendations(
            "Security Groups with Public Egress Rules",
            "Remove public egress rules to improve security.",
            "https://docs.aws.amazon.com/pt_br/vpc/latest/userguide/security-group-rules.html",
            data
        )

        recommendation.show_recommendations()
        return data

    def get_buckets_not_public_acess_block(self):
        """
        Retrieves information about all buckets that are not public access blocked in the specified AWS regions.

        Returns:
            list: A list of data about the buckets that are not public access blocked.
        """
        log.info(f"GET - Buckets not public access block started!")
        with console.status(f"GET - Buckets not public access block", spinner="aesthetic"):        
            data = self.s3_finder.get_buckets_not_public_acess_block()
        log.info(f"GET - Buckets not public access block on account finished!")

        recommendation = AWSRecommendations(
            "Buckets that are not public access blocked",
            "Check if public access blocking can be enabled on the bucket",
            "https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html",
            data
        )

        recommendation.show_recommendations()
        return data