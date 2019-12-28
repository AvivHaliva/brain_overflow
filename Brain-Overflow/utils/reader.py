import click
import utils

class Reader():
	#TODO - maybe change to fantory?
	def __init__(self, path, file_format):
		self. path = path
		if file_format == 'binary':
			self.reader = utils.BinaryReader(path)
		elif file_format == 'protobuf':
			self.reader = utils.ProtobufReader(path)
		else:
		#TODO - raise error
			return

	def __str__(self):
		return str(self.reader)

	def __iter__(self):
		return self.reader.__iter__()


@click.command()
@click.argument("path")
@click.argument("file_format")
def read(path, file_format):
	reader = Reader(path, file_format)
	print(reader)
	for snapshot in reader:
		print(snapshot)


