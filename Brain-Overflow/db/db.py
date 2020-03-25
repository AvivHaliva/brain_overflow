import db_drivers_handler

class DataBase:
	def __init__(self, url):
		self.db_driver = db_drivers_handler.find_driver(url)

	def create_user(self, **kwargs):
		self.db_driver.create_user(**kwargs)

	def get_user_info(self, user_id):
		user = self.db_driver.get_user_info(user_id)
		if user is None:
			raise LookupError()
		return user

	def get_user_snapshots(self, user_id):
		snapshots = self.db_driver.get_user_snapshots(user_id)
		#TODO - add logic -> what if user doesn't exist or have 0 snapshots?
		return snapshots

	def get_all_users(self):
		return self.db_driver.get_all_users()

	def update_user(self, **kwargs):
		pass

	def create_snapshot(self, **kwargs):
		pass

	def get_snapshot(self, **kwargs):
		pass

	def get_all_snapshots(self, **kwargs):
		pass