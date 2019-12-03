import datetime
import struct
import time

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
THOUGHT_STR_FORMAT = '[{0}] user {1}: {2}'
FORMAT = 'lli'
EXTENDED_FORMAT = FORMAT+'{0}s'

class Thought:
	def __init__(self, user_id, timestamp, thought):
		self.user_id = user_id
		# support ts both as datetime and as int
		if isinstance(timestamp, datetime.datetime):
			self.timestamp = timestamp
		else:
			self.timestamp = datetime.datetime.fromtimestamp(timestamp)
		self.thought = thought

	def __repr__(self):
		return f'Thought(user_id={self.user_id!r}, timestamp={self.timestamp!r}, thought={self.thought!r})'

	def __str__(self):
		return str((THOUGHT_STR_FORMAT.format(
			self.timestamp.strftime(TIME_FORMAT),
			self.user_id,
			self.thought)))

	def __eq__(self, other):
		return isinstance(other, Thought) \
		and self.user_id == other.user_id \
		and self.timestamp == other.timestamp \
		and self.thought == other.thought

	def serialize(self):
		# returns bytes representing this thought
		ts = time.mktime(self.timestamp.timetuple())
		form = EXTENDED_FORMAT.format(len(self.thought.encode()))
		thought_serialized = struct.pack(form, self.user_id, int(ts), len(self.thought), self.thought.encode())
		return thought_serialized

	def deserialize(data):
		# given some bytes, decodes them 
		# and construct a new thought instance accordingly
		user_id, timestamp, thought_size = struct.unpack(FORMAT, data[:struct.calcsize(FORMAT)])
		user_id, timestamp, thought_size, thought = struct.unpack(EXTENDED_FORMAT.format(thought_size), data)
		return Thought(user_id, timestamp, thought.decode())


