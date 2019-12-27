import pathlib
import importlib
import sys

class Parser:
	def __init__(self):
		self.supported_parsers = {}

	def load_parsers(self, root):
		root = pathlib.Path(root).absolute()
		sys.path.insert(0, str(root.parent))
		for path in root.iterdir():
			if path.name.startswith('parse_') and path.suffix == 'py':
				m = importlib.import_module(f'{root.name}.{path.stem}', package=root.name)
				for f in dir(m):
					parse_f = getattr(m, f)
					self.supported_parsers[parse_f.field] = parse_f
