from server import run_server
from client import upload_sample
from web import run_webserver
from utils import reader
from parsers import run_parser_command, parse

import click

@click.group()
def cli():
	pass

cli.add_command(run_server)
cli.add_command(run_webserver)
cli.add_command(reader.read)
cli.add_command(upload_sample)

cli.add_command(run_parser_command)
cli.add_command(parse)

