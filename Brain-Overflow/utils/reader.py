import click
import pathlib
import importlib
import sys

class Reader():
	def __init__(self, path, file_format):
		self.supported_parsers = {}
		self.load_file_parsers('/home/user/Brain-Overflow/Brain-Overflow/utils/file_readers/')
		self.file_parser = self.get_file_parser(file_format)(path)
		self.user = self.file_parser.get_user_info()

	def __str__(self):
		pass

	def __repr__(self):
		pass
		#return 'reader = Reader(<file>, <file_parser>).for example: reader = Reader('sample.mind',BinaryReader)'

	def __iter__(self):
		try:
			snapshot = self.file_parser.get_next_snapshot()
			while snapshot:
				yield snapshot
				snapshot = self.file_parser.get_next_snapshot()
		except Exception as e:
			print(e)
		finally:
			self.file_parser.file.close()
			return 

	def load_file_parsers(self, root):
		root = pathlib.Path(root).absolute()
		sys.path.insert(0, str(root.parent))
		for path in root.iterdir():
			if path.name.endswith('_reader.py'):
				m = importlib.import_module(f'{root.name}.{path.stem}', package=root.name)
				for att in dir(m):
					if att.endswith('Reader'):
						file_parser = getattr(m, att)
						self.supported_parsers[file_parser.file_format] = file_parser

	def get_file_parser(self, file_format):
		try:
			return self.supported_parsers[file_format.lower()]
		except Exception as e:
			print(e)
			print(file_format)
		finally:
			pass

@click.command()
@click.argument("path")
@click.argument("file_format")
def read(path, file_format):
	#TODO - change
	reader = Reader(path, file_format)
	print(reader.user)
	for snapshot in reader:
		print(snapshot)

