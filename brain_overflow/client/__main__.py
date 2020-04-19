import click
from . import client

@click.group()
def cli():
    pass

@cli.command('upload-sample')
@click.argument('path', type=click.Path(exists=True))
@click.option('-h', '--host',default='127.0.0.1', show_default=True, type=str, help='server ip')
@click.option('-p', '--port', default=8000, show_default=True, type=int, help='server port')
@click.argument('file_format', type=str)
def upload_sample_command(path, host, port, file_format):
	""" reads a sample from specified PATH in the specified FILE_FORMAT
		and uploads it to the server = (host, port)"""
	client.upload_sample(path, host, port, file_format)

cli.add_command(upload_sample_command)

if __name__ == '__main__':
    cli(prog_name='client')
