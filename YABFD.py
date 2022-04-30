import YABFD
from os.path import exists
import sys
if len(sys.argv) < 2:
	print (f"usage:\n{sys.argv[0]} <code.bf>")
	exit(1)
elif exists(sys.argv[1]):
	executor = YABFD.Brainfuck()
	executor.execute(sys.argv[1])
else:
	print(f"file: '{sys.argv[1]}' does not exist")