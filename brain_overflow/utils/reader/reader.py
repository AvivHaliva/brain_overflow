import click
import pathlib
import importlib
import sys

class Reader():
	def __init__(self, path, file_format):
		self.supported_parsers ={}
		self.load_file_readers()
		self.file_reader = self.get_file_reader(file_format)(path)
		self.user = self.file_reader.get_user_info()

	def __str__(self):
		pass

	def __repr__(self):
		pass
		#return 'reader = Reader(<file>, <file_reader>).for example: reader = Reader('sample.mind',BinaryReader)'

	def __iter__(self):
		try:
			snapshot = self.file_reader.get_next_snapshot()
			while snapshot:
				yield snapshot
				snapshot = self.file_reader.get_next_snapshot()
		except Exception as e:
			print(e)
		finally:
			self.file_reader.file.close()
			return 

	def load_file_readers(self):
		root = (pathlib.Path(__file__).parent / 'file_readers').absolute()
		sys.path.insert(0, str(root.parent))
		for path in root.iterdir():
			if path.name.endswith('_reader.py'):
				m = importlib.import_module(f'{root.name}.{path.stem}', package=root.name)
				for att in dir(m):
					if att.endswith('Reader'):
						file_reader = getattr(m, att)
						self.supported_parsers[file_reader.file_format] = file_reader

	def get_file_reader(self, file_format):
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

