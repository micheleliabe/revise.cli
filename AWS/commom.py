import boto3

class RegionsFinder:
    def get_available_regions(self):
        """
        Retrieves a list of all available AWS regions.

        Returns:
            list: A list of strings containing the names of all available AWS regions.
        """
        client = boto3.client("account")
        response = None
        try:
            # Get regions enabled for the account
            response = client.list_regions(
                RegionOptStatusContains=['ENABLED', 'ENABLED_BY_DEFAULT']
            )

        except Exception as error:
            raise error

        # Extract region names from the response
        regions = [region['RegionName'] for region in response.get('Regions', [])]

        return regions