# Import necessary libraries
import typer
from typing_extensions import Annotated
from rich.console import Console
from common import config

from AWS.recommendations import AWSSecurityChecker, AWSCostChecker


# Initialize Rich Console for better terminal output formatting
console = Console()

# Create a Typer application instance
app = typer.Typer()

config = config.load_configs()

# Define a command to fetch AWS cost recommendations


@app.command()
def costs(regions: Annotated[str, typer.Option(help='A string with the list of regions to scan. Exemple: "us-east-1 us-east-2 sa-east-1"')] = "all"):
    """
    Retrieves cost recommendations for the specified AWS regions.
    """
    aws_cost_checker = AWSCostChecker(regions)
    aws_cost_checker.get_gp2_volumes()


@app.command()
def get(resource, regions: Annotated[str, typer.Option(help='A string with the list of regions to scan. Exemple: "us-east-1 us-east-2 sa-east-1"')] = "all"):
    match resource:
        case "gp2-volumes":
            aws_cost_checker = AWSCostChecker(regions)
            aws_cost_checker.get_gp2_volumes()

        case "volumes-on-stopped-instances":
            aws_cost_checker = AWSCostChecker(regions)
            aws_cost_checker.get_volumes_on_stopped_instances()

        case "detached-volumes":
            aws_cost_checker = AWSCostChecker(regions)
            aws_cost_checker.get_detached_volumes()

        case "detached-ips":
            aws_cost_checker = AWSCostChecker(regions)
            aws_cost_checker.get_detached_ips()

        case "old-snapshots":
            aws_cost_checker = AWSCostChecker(regions)
            snapshot_retention = config["finders"]["aws"]["costs"]["oldSnapshots"]["daysOfRetention"]
            aws_cost_checker.get_old_snapshots(snapshot_retention)

        case "public-egress-rules":
            aws_security_checker = AWSSecurityChecker(regions)
            aws_security_checker.get_security_groups_public_egress()
        case _:
            console.print("Invalid")


@app.command()
def fix(regions: Annotated[str, typer.Option(help='A string with the list of regions to scan. Exemple: "us-east-1 us-east-2 sa-east-1"')] = "all",
        resource: Annotated[str, typer.Argument(help='Resources to fix. Exemple detached-volumes, not-used-ips')] = None):
    pass
