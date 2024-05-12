#!/usr/bin/env python3

import yaml
import typer # Import Typer for command-line interface creation
from rich.console import Console # Import Console from Rich for better terminal output formatting
from rich.syntax import Syntax
from pyfiglet import Figlet
from common import config
from utils import logger
from AWS.core import app as aws

revise_version = "0.1"

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
    figlet = Figlet(font='standard')    
    print(figlet.renderText("Revise.cli"))
    console.print("A CLI to find improvement opportunities in your AWS account...")
    console.rule(align="left")
    console.print("- version: " + revise_version)
    console.print("- github: https://github.com/micheleliabe/revise.cli")
    console.print("- documentation: pending")
    console.print("- license: MIT")
    console.print("- author: Michel Eliabe Moreira Dias")
    console.print("- support: micheldias.cloud@gmail.com")
    console.print()

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
