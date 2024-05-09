#!/usr/bin/python3

import yaml

# Import Typer for command-line interface creation
import typer

# Import Console from Rich for better terminal output formatting
from rich.console import Console
from rich.syntax import Syntax


from common import config
from utils import logger


from AWS.core import app as aws


# Initialize Rich Console for better terminal output formatting
console = Console()

# Create a Typer application instance
app = typer.Typer()


# Load Revise.cli configs from config file
config = config.load_configs()
config_yaml = yaml.dump(config)

if config["logs"]["enabled"] == False:
    logger.disable_logging()


app.add_typer(aws, name="aws")


@app.command()
def version():
    """
    GET Revise CLI version.
    """
    console.print("Revise.cli, version: 0.1")


@app.command()
def info():
    """
    GET Revise CLI Documentation.
    """
    console.print("Revise.cli documentation available in:")

    console.print(
        "https://github.com/micheleliabe/revise/blob/master/readme.md")


@app.command()
def config():
    """
    GET Revise CLI configurations.
    """
    console.print("Revise config:")
    console.print()
    synstax = Syntax(config_yaml, "yaml", theme="github-dark")
    console.print(synstax)


    # Entry point of the script
if __name__ == "__main__":
    app()
