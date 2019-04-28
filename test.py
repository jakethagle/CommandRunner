from CommandRunner import CommandRunner

def test_local_command():
	c = CommandRunner()
	c.invoke_command("ls")

def test_remote_command():
	c = CommandRunner("192.168.1.200", "frosty")
	c.invoke_command("ls")

def main():
	test_local_command()
	test_remote_command()

if __name__ == "__main__":
	main()
