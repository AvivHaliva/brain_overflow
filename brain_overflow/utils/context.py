import os 
from pathlib import Path

class Context:
	def __init__(self, *args):
		self.dir = Path('/'.join(str(arg) for arg in args))
		os.makedirs(self.dir, exist_ok=True)

	def get_path(self, file_name):
		return self.dir / file_name

	def save(self, file_name, data, type='w'):
		file_path = self.get_path(file_name)
		with open(file_path, type) as f:
			f.write(data)
		return str(file_path)


