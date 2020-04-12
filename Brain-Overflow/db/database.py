from . import db_drivers_handler

class DataBase:
	def __init__(self, url):
		self.db_driver = db.db_drivers_handler.find_driver(url)

	def save_user(self, user_data):
		try:
			self.db_driver.save_user(user_data)
		except:
			pass
			#TODO

	def get_user_info(self, user_id):
		user = self.db_driver.get_user_info(user_id)
		if user is None:
			raise LookupError()
		return user


	def get_snapshot(self, user_id, snapshot_id):
		snapshot = self.db_driver.get_snapshot(user_id, snapshot_id)
		if snapshot is None:
			raise LookupError()
		return snapshot

	def get_all_user_snapshots(self, user_id):
		snapshots = self.db_driver.get_all_user_snapshots(user_id)
		if snapshots is None:
			raise LookupError()
		return snapshots

	def get_all_users(self):
		return self.db_driver.get_all_users()

	def save_snapshot_data(self, data):
		try:
			self.db_driver.save_snapshot_data(data)
		except:
			pass
			#TODO

