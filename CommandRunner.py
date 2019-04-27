import subprocess

class CommandRunner(object):
	'''
	A simple wrapper for invoking shell commands from a python scripts.
	If an ip is defined we will try to connect over ssh, otherwise it runs locally
	This relies on ssh/.config to be accurate and uses ssh keys
	'''
	# ----------------------------------------------
	def __init__(self, host=None, user=None):
		self.host = host
		self.user = user
		self.proc = None
		self.is_remote_target = True if host and user else False
		print(self.is_remote_target)

	# ----------------------------------------------
	def open(method):
		def open_process(self, *args, **kwargs):
			self.proc = subprocess.Popen(['/bin/bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf8")
			return method(self, *args, **kwargs)
		return open_process

	# ----------------------------------------------
	@open
	def invoke_command(self, command):
		try:

			if self.proc is None:
				raise Exception("Unable to open process")

			parsed_command = self._build_command(command)
			out, err = self.proc.communicate(parsed_command, 10)

			print("stdout: \n----------------------------\n%s" % out)
			print("stderr: \n----------------------------\n%s" % err)

		except Exception as e:
			print (e)


	# ----------------------------------------------
	def _build_command(self, command=None):
		if not command:
			raise Exception("No Command Specified")
		commands = ["bash"]
		if self.is_remote_target:
			commands = ["ssh {}@{} bash".format(self.user, self.host)]
		commands.append("set -e; {}".format(command))

		return "\n".join(commands)

	# ----------------------------------------------
	def _build_remote_command(self, command=None):
		return """
			ssh {}@{} bash
			set -e; {}
		""".format(self.user, self.host, command)

def main():
	c = CommandRunner("192.168.1.200", "frosty")
	c = CommandRunner()
	c.invoke_command("ls")

if __name__ == "__main__":
	main()
