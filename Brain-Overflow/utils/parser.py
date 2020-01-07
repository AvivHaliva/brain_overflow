import pathlib
import importlib
import sys

class Parser:
	def __init__(self):
		self.supported_parsers = {}
		self.load_parsers('/home/user/Brain-Overflow/Brain-Overflow/utils/parsers/')

	def load_parsers(self, root):
		root = pathlib.Path(root).absolute()
		sys.path.insert(0, str(root.parent))
		for path in root.iterdir():
			if path.name.startswith('parse_') and path.suffix == '.py':
				m = importlib.import_module(f'{root.name}.{path.stem}', package=root.name)
				for f in dir(m):
					if f.startswith('parse_'):
						try:
							parse_f = getattr(m, f)
							self.supported_parsers[parse_f.field] = parse_f
						except:
							pass
	
