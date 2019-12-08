from server import run_server
from client import upload_thought
from web import run_webserver

import click

@click.group()
def cli():
	pass

cli.add_command(run_server)
cli.add_command(upload_thought)
cli.add_command(run_webserver)