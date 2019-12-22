from server import run_server
from client import upload_thought
from client import upload_sample
from web import run_webserver
from utils import reader

import click

@click.group()
def cli():
	pass

cli.add_command(run_server)
cli.add_command(upload_thought)
cli.add_command(run_webserver)
cli.add_command(reader.read)
cli.add_command(upload_sample)