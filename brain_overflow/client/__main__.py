import click
from . import client

@click.group()
def cli():
    pass

@cli.command('upload_sample')
@click.argument('path', type=click.Path(exists=True))
@click.option('-h', '--host',default='127.0.0.1')
@click.option('-p', '--port', default='8000')
@click.argument('file_format', default='protobuf')
def upload_sample_command(path, address, file_format):
	client.upload_sample(path, host, port, file_format)

cli.add_command(upload_sample_command)

if __name__ == '__main__':
    cli(prog_name='client')
