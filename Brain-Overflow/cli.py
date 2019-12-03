import functools
import inspect
import sys

USAGE_MESSAGE = 'USAGE: python example.py <command> [<key>=<value>]*'

class CommandLineInterface:
	supported_functions_args = {}
	supported_functions_code = {}

	def command(self, f):
		func = f.__name__
		func_args = inspect.getfullargspec(f)[0]
		self.supported_functions_args[func] = func_args
		self.supported_functions_code[func] = f
		@functools.wraps(f)
		def wrapper(*args, **kwargs):
			return f(*args, **kwargs)
		return wrapper

	def print_usage_message(self):
		print(USAGE_MESSAGE)
		sys.exit(1)

	def main(self):
		cli_args = sys.argv
		if len(cli_args) < 2 :
			return self.print_usage_message()
		func = cli_args[1]
		#validate the function is supported in the interface
		if func not in self.supported_functions_args:
			return self.print_usage_message()
		#validate the number of args passed to the function
		required_args_num = len(self.supported_functions_args[func])
		if len(cli_args) < required_args_num + 2 :
			return self.print_usage_message()
		cli_args = cli_args[2:2 + required_args_num]
		#validate args format and value and store them
		args = []
		for kwarg in cli_args:
			var_and_value = kwarg.split('=')
			#wrong format
			if len(var_and_value) < 2 :
				return self.print_usage_message()
			var = var_and_value[0]
			value = var_and_value[1]
			#unsupported argument
			if var not in self.supported_functions_args[func]:
				return self.print_usage_message()
			args.append(value)

		#call the function with the extracted args
		self.supported_functions_code[func](*args)
		sys.exit(0)









        


