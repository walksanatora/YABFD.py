import YABFD as BF
mem = BF.evaluate(
		'*>$++*>$<%>>$',
		realms=[BF.util.generateMemSpace(5)]
	)
print('\n\n')
print(mem)
print(BF.util.memToList(mem))