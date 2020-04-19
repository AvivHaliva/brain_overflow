import pytest
import unittest
from brain_overflow.client import upload_sample

class TestClient(unittest.TestCase):
	def test_no_server_exit_grcefully(self):
		with self.assertRaises(SystemExit) as cm:
			upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gz')
		self.assertEqual(cm.exception.code, 1)

	def test_no_such_file_exit_grcefully(self):
		with self.assertRaises(SystemExit) as cm:
			upload_sample(host='127.0.0.1', port=8000, path='no_such_file.gz')
		self.assertEqual(cm.exception.code, 1)

	def test_no_exception_is_raised(self):
	    try:
	        upload_sample(host='127.0.0.1', port=8000, path='no_such_file.gz')
	    except SystemExit:
	    	pass
	    except Exception:
	        self.fail("myFunc() raised Exception unexpectedly!")

	def test_reader_results(self):
		upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gz')



	 

