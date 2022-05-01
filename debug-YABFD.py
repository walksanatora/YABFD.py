import YABFD
from os.path import exists
import sys
executor = YABFD.Brainfuck()

if len(sys.argv) < 2:
	print (f"usage:\n{sys.argv[0]} <code.bf>")
	exit(1)
elif exists(sys.argv[1]):
	try:
		with open(sys.argv[1],'r') as f:
			data = f.read()
			executor.setup(data)
			while executor.codeptr < len(executor.code):
				print(f"""\ncode: {executor.code}
{"".join([" "for _ in range(executor.codeptr+6)])}^
l:{executor.cellptr} v:{executor.cells[executor.cellptr]['v']} p: {executor.ptrvalue}
""")
				executor.step()
	except BaseException as e:
		import traceback
		traceback.print_exc()
		print(f"""code: {executor.code}
{"".join([" "for _ in range(executor.codeptr+6)])}^
instruction: {executor.code[executor.codeptr]}
codeptr: {executor.codeptr}
cellptr: {executor.cellptr}
cell: {executor.cells[executor.cellptr]['v']}
maps:\tbrace: {executor.bracemap}
\tcurly: {executor.curlymap}
\tpar: {executor.parmap}
""")
else:
	print(f'evaulating sys.argv[1:] as brainfuck ({" ".join(sys.argv[1:])}')
	executor.evaluate(" ".join(sys.argv[1:]))
