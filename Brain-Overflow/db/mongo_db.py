import pymongo

#TODO - make sure user id in the queries is INT

class MongoDB:
	def __init__(self, url):
		client = pymongo.MongoClient(url)
		self.db = client['BrainOverflowDB']

	def save_user(self, data):
		users = self.db['users'] 
		users.update_one(
			{'user_id': data['user_id']},
			{'$set':data}, 
			upsert=True)

	def get_user_info(self, user_id):
		users = self.db['users']
		user = users.find_one({'user_id':user_id}, {'_id':False})
		return user

	def get_snapshot(self, user_id, snapshot_id):
		snapshots = self.db['snapshots']
		availabe_results = snapshots.find_one({'user_id' : user_id, 'snapshot_id' : snapshot_id},
			{'_id':False, 'snapshot_id':False, 'timestamp':False}).keys()
		timestamp = snapshots.find_one({'user_id' : user_id, 'snapshot_id' : snapshot_id},
			{'_id':False, 'timestamp':True})

		snapshot_metadata = {
			'user_id': user_id,
			'snapshot_id' : snapshot_id,
			'timestamp' : timestamp,
			'availabe_results' : availabe_results
		}

		return snapshot_metadata

	def get_all_user_snapshots(self, user_id):
		snapshots = self.db['snapshots']
		return list(snapshots.find(
			{'user_id': user_id}, 
			{'_id':False, 'snapshot_id':True, 'timestamp':True})
		)

	def get_all_users(self):
		users = self.db.users
		return list(users.find(
			{},
			{'_id':False, 'user_id':True, 'user_name':True}
			))


	def save_snapshot_data(self, data):
		snapshots = self.db['snapshots']
		#TODO add snapshot_id to filter
		snapshots.update_one({'user_id': data['user_id'] , 'timestamp':data['timestamp']},
			{'$set':data},
			upsert=True)




		
