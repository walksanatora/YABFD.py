import YABFD as BF

###realm function example
#classes are easier to work with because they can share values in/out easier
class ExampleCustomRealmFunc:
	def __init__(self):
		self.value=0
	def set(self,realms: list[list], realmptr: int, ptr: int):
		self.value=realms[realmptr]['cells'][ptr]['v']
#instantiate
t=ExampleCustomRealmFunc()

#generate a memory space with 5 cells
testspace = BF.util.generateMemSpace(5)
#make the realm function be the custom classes set function
testspace['func'] = t.set

#add 3 to the first cell copy the value to the class
#then add 2 more afterwards to show that they are seperate values
mem = BF.evaluate(
		'+++_++',
		realms=[testspace]
	)
#print some extra information
print("memory output:")
print(BF.util.memToList(mem))
print(t.value)
del t
del mem

###realm switching + linking example
#increment cell value to 1
#then open a portal and increment the value by 2
mem = BF.evaluate(
	'+@++',
	realms=[BF.util.generateMemSpace(5),BF.util.generateMemSpace(5)]
)
print("memory output:")
print(BF.util.memToList(mem))
del mem

###pointer example
# creates a pointer to 0:0 at 0:2 then increments by 2
# then heads to realm 1 and links 1:0 to 0:0 and increments by two more
# then unlinks to add 2 more
# also shows how it can re-convert list back to usable memory
mem = BF.evaluate(
	"*>>$++>+@$++^++",
	realms=[BF.util.generateMemSpace(5),BF.util.generateMemSpace(5)]
)
l = BF.util.memToList(mem)
recov = BF.util.listToMem(l)
print("memory output:")
print(l)
print(recov)

del mem
del l
del recov

### show how if statments can be made
# this example will print "aaa" if you input "a" but it will echo back your input once if it is not a "a"
print("IF example:")
mem = BF.evaluate(
	'+[-[---<]>>-]<->,{=...}(.)',
	realms=[BF.util.generateMemSpace(5)]
)
print(BF.util.memToList(mem))