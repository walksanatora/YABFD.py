import YABFD

print('create enviroment')
BF = YABFD.Brainfuck()
print('done')

###realm function example
#classes are easier to work with because they can share values in/out easier
#add 3 to the first then print the value
#then add 2 more afterwards to show that they are seperate values
print('\nrealm function example')
BF.setup(
		'+++_++',
		realms=[YABFD.util.generateMemSpace(5)]
	)
BF.evaluate()
#print some extra information
print("memory output:")
print(YABFD.util.memToList(BF.realms))

###realm switching
#increment cell value to 1
#then open a portal
#put the value of the current realm into the cell
#add 2
print('\nrealm switching example')
BF.setup(
	'+@|++',
	realms=[YABFD.util.generateMemSpace(5),YABFD.util.generateMemSpace(5)]
)
BF.evaluate()
print("memory output:")
print(YABFD.util.memToList(BF.realms))

###pointer example
# creates a pointer to 0:0 at 0:2 then increments by 2
# then heads to realm 1 and links 1:0 to 0:0 and increments by two more
# then unlinks to add 2 more
# also shows how it can re-convert list back to usable memory
print('\npointer example, and usage across realms')
BF.setup(
	"*>>$++>+@$++^++",
	realms=[YABFD.util.generateMemSpace(5),YABFD.util.generateMemSpace(5)]
)
BF.evaluate()
l = YABFD.util.memToList(BF.realms)
recov = YABFD.util.listToMem(l)
print("memory output:")
print('origional:',BF.realms)
print('list:',l)
print('recovered:',recov)

del l
del recov

### show how if statments can be made
# this example will print "aaa" if you input "a" but it will echo back your input once if it is not a "a"
# also shows how you can copy values to another location
print("\nIF example, prints input 6 times if it is 'a' or once if anything else:")
BF.setup(
	'+[-[---<]>>-]<-%[-]<<$>,{=......}(.)',
	realms=[YABFD.util.generateMemSpace(5)]
)
BF.evaluate()
print(YABFD.util.memToList(BF.realms))
