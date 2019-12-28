import datetime as dt

class User:
	def __init__(self, id, name, birth_date, gender):
		self.id = id
		self.name = name
		self.birth_date = birth_date
		#TODO - gender?
		#TODO - create a dict instead {'m':'male', 'f':'female'} etc.
		self.gender = gender

	def __str__(self):
		#TODO - move the date format to somewhere else
		return 'user {0}: {1}, born {2} ({3})'.format(self.id, self.name, self.birth_date_to_str(), self.gender)

	def birth_date_to_str(self):
		return dt.datetime.fromtimestamp(self.birth_date/1000.0).strftime('%d %B %Y')
		#TODO - fix birthdate error! 1970?
	def __repr__(self):
		pass