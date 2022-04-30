import YABFD
from os.path import exists
import sys
executor = YABFD.Brainfuck()

if len(sys.argv) < 2:
	print (f"usage:\n{sys.argv[0]} <code.bf>")
	exit(1)
elif exists(sys.argv[1]):
	executor.execute(sys.argv[1])
else:
	print(f"evaulating sys.argv[1:] as brainfuck ({sys.argv[1:]})")
	executor.evaluate(sys.argv[1:])
