from db.mongo_db import MongoDB

supported_db_drivers = {'mongodb://': MongoDB}

def find_driver(url):
	for scheme, cls in supported_db_drivers.items():
		if url.startswith(scheme):
			return cls(url)
	raise ValueError(f'invalid url: {url}')