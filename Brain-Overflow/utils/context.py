class Context:
	def __init__(self, dir):
		self.dir = dir

	def path(self, file_name):
		return self.dir / file_name

	def save(self, file_name, data):
		with open(self.path(file_name), 'w') as file:
			file.write(data)

