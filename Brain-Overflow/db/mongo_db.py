import pymongo

class MongoDB:
	def __init__(self, url):
		client = pymongo.MongoClient(url)
		self.db = client['BrainOverflowDB']

	def create_user(self, **kwargs):
		users = self.db['users'] 
		result = users.insert_one(kwargs)

	def get_user_info(self, user_id):
		users = self.db['users']
		user = users.find_one({'user_id':user_id}, {'_id':False})
		return user

	def get_user_snapshots(self, user_id):
		snapshots = self.db['snapshots']
		return list(snapshots.find(
			{'user_id':user_id}, 
			{'_id':False, 'snapshot_id':True, 'datetime':True})
		)

	def get_all_users(self):
		users = self.db.users
		return list(users.find(
			{},
			{'_id':False, 'user_id':True, 'name':True}
			))

	def update_user(self, **kwargs):
		pass

	def create_snapshot(self, **kwargs):
		pass

	def get_snapshot(self, **kwargs):
		pass

	def get_all_snapshots(self, **kwargs):
		pass


		
