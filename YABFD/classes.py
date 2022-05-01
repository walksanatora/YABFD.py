import sys

from . import getch

def noop(**kwargs): return

class Realm:
    cells:list[dict]
    def __init__(self,cells=[]):
        self.cells=cells
    def func(self,Brainfuck):
        print(Brainfuck.realms[Brainfuck.realmptr].cells[Brainfuck.cellptr])

class Brainfuck:
    code:str
    bracemap: dict[int,int]
    curlymap: dict[int,int]
    parmap: dict[int,int]
    realms: list[Realm]
    codeptr: int
    cellptr: int
    realmptr: int
    cells: list[dict]
    def __init__(self):
        pass

    def printChar(self,char):
        sys.stdout.write(char)

    def getChar(self):
        return ord(getch.getch())

    def evalInstruction(self,command:str)->None:
        match command:
                case ">":
                    self.cellptr += 1
                    if self.cellptr == len(self.cells):
                        self.cellptr = 0

                case "<":
                    self.cellptr = len(self.cells)-1 if self.cellptr <= 0 else self.cellptr - 1

                case "+":
                    if self.cells[self.cellptr]["t"] == "i":
                        self.cells[self.cellptr]["v"] = (
                            self.cells[self.cellptr]["v"] + 1 if self.cells[self.cellptr]["v"] < 255 else 0
                        )
                    else:
                        self.realms[self.cells[self.cellptr]["r"]].cells[self.cells[self.cellptr]["c"]]["v"] = (
                            self.realms[self.cells[self.cellptr]["r"]].cells[self.cells[self.cellptr]["c"]]["v"]
                            + 1
                            if self.realms[self.cells[self.cellptr]["r"]].cells[self.cells[self.cellptr]["c"]][
                                "v"
                            ]
                            < 255
                            else 0)

                case "-":
                    if self.cells[self.cellptr]["t"] == "i":
                        self.cells[self.cellptr]["v"] = (
                            self.cells[self.cellptr]["v"] - 1 if self.cells[self.cellptr]["v"] > 0 else 255
                        )
                    else:
                        self.realms[self.cells[self.cellptr]["r"]].cells[self.cells[self.cellptr]["c"]]["v"] = (
                            self.realms[self.cells[self.cellptr]["r"]].cells[self.cells[self.cellptr]["c"]]["v"]
                            - 1
                            if self.realms[self.cells[self.cellptr]["r"]].cells[self.cells[self.cellptr]["c"]][
                                "v"
                            ]
                            > 0
                            else 255)

                case "[":
                    if self.cells[self.cellptr]["t"] == "i":
                        if self.cells[self.cellptr]["v"] == 0:
                            self.codeptr = self.bracemap[self.codeptr]

                    else:  # really cursed one liner to get a cell from another realm
                        if (
                            self.realms[self.cells[self.cellptr]["r"]].cells[self.cells[self.cellptr]["c"]][
                                "v"
                            ]
                            != 0
                        ):
                            self.codeptr = self.bracemap[self.codeptr]

                case "]":
                    if self.cells[self.cellptr]["t"] == "i":
                        if self.cells[self.cellptr]["v"] != 0:
                            self.codeptr = self.bracemap[self.codeptr]
                    else:
                        if (
                            self.realms[self.cells[self.cellptr]["r"]].cells[self.cells[self.cellptr]["c"]]["v"]
                            != 0
                        ):
                            self.codeptr = self.bracemap[self.codeptr]

                case ".":
                    if self.cells[self.cellptr]["t"] == "i":
                        self.printChar(chr(self.cells[self.cellptr]["v"]))
                    else:
                        self.printChar(
                            chr(
                                self.realms[self.cells[self.cellptr]["r"]].cells[self.cells[self.cellptr]["c"]][
                                    "v"
                                ]
                            )
                        )
                    self.printedChar=True

                case ",":
                    if self.cells[self.cellptr]["t"] == "i":
                        self.cells[self.cellptr]["v"] = self.getChar()
                    else:
                        self.realms[self.cells[self.cellptr]["r"]].cells[self.cells[self.cellptr]["c"]][
                            "v"
                        ] = self.getChar()

                case "|":
                    if self.cells[self.cellptr]["t"] == "i":
                        self.cells[self.cellptr]["v"] = self.realmptr
                    else:
                        self.realms[self.cells[self.cellptr]["r"]].cells[self.cells[self.cellptr]["c"]][
                            "v"
                        ] = self.realmptr

                case "@":
                    realmtgt = 0
                    if self.cells[self.cellptr]["t"] == "i":
                        realmtgt = self.cells[self.cellptr]["v"]
                    else:
                        realmtgt = self.realms[self.cells[self.cellptr]["r"]].cells[
                            self.cells[self.cellptr]["c"]
                        ]["v"] = self.realmptr
                    try:
                        cells = self.realms[realmtgt].cells
                        self.realmptr = realmtgt
                        self.cellptr = 0
                    except IndexError:
                        cells = self.realms[0].cells
                        self.realmptr = 0
                        self.cellptr = 0

                case "_":
                    self.realms[self.realmptr].func(self)

                case "{":
                    bracket=self.codeptr
                    self.codeptr+=1
                    ins=self.code[self.codeptr]
                    skip=True
                    match ins:
                        case '0':
                            if self.cells[self.cellptr]["t"] == "i":
                                if self.cells[self.cellptr]["v"] == 0:
                                    skip=False
                            else:  # really cursed one liner to get a cell from another realm
                                if (
                                self.realms[self.cells[self.cellptr]["r"]].cells[self.cells[self.cellptr]["c"]][
                                    "v"
                                ]
                                == 0
                                ):
                                    skip = False
                        case '@':
                            if self.cells[self.cellptr]["t"] == "i":
                                if self.cells[self.cellptr]["v"] == self.realmptr:
                                    skip=False
                            else:  # really cursed one liner to get a cell from another realm
                                if (
                                self.realms[self.cells[self.cellptr]["r"]].cells[self.cells[self.cellptr]["c"]][
                                    "v"
                                ]
                                == self.realmptr
                                ):
                                    skip = False
                        case '*':
                            if self.cells[self.cellptr]['t'] == 'l':
                                skip=False
                        case '=':
                            left=0
                            right=0
                            if self.cells[self.cellptr-1]["t"] == "i":
                                left=self.cells[self.cellptr-1]["v"]
                            else:
                                left=self.realms[self.cells[self.cellptr]["r"]].cells[self.cells[self.cellptr]["c"]-1]["v"]
                            if self.cells[self.cellptr-1]["t"] == "i":
                                right=self.cells[self.cellptr]["v"]
                            else:
                                right=self.realms[self.cells[self.cellptr]["r"]].cells[self.cells[self.cellptr]["c"]]["v"]
                            if left==right:
                                skip=False
                        case '<':
                            left=0
                            right=0
                            if self.cells[self.cellptr-1]["t"] == "i":
                                left=self.cells[self.cellptr-1]["v"]
                            else:
                                left=self.realms[self.cells[self.cellptr]["r"]].cells[self.cells[self.cellptr]["c"]-1]["v"]
                            if self.cells[self.cellptr-1]["t"] == "i":
                                right=self.cells[self.cellptr]["v"]
                            else:
                                right=self.realms[self.cells[self.cellptr]["r"]].cells[self.cells[self.cellptr]["c"]]["v"]
                            if left<right:
                                skip=False
                        case '>':
                            left=0
                            right=0
                            if self.cells[self.cellptr-1]["t"] == "i":
                                left=self.cells[self.cellptr-1]["v"]
                            else:
                                left=self.realms[self.cells[self.cellptr]["r"]].cells[self.cells[self.cellptr]["c"]-1]["v"]
                            if self.cells[self.cellptr-1]["t"] == "i":
                                right=self.cells[self.cellptr]["v"]
                            else:
                                right=self.realms[self.cells[self.cellptr]["r"]].cells[self.cells[self.cellptr]["c"]]["v"]
                            if left>right:
                                skip=False
                    if skip:
                        self.codeptr=self.curlymap[bracket]

                case "}":
                    if self.code[self.codeptr+1] == '(':
                        self.codeptr=self.parmap[self.codeptr+1]

                case "*":
                    self.ptrvalue=[self.realmptr,self.cellptr]
                    self.ptrlocation=True

                case "%":
                    if self.cells[self.cellptr]["t"] == "i":
                        self.ptrvalue = self.cells[self.cellptr]["v"]
                    else:
                        self.ptrvalue = self.realms[self.cells[self.cellptr]["r"]].cells[
                            self.cells[self.cellptr]["c"]
                        ]["v"]
                    self.ptrlocation=False

                case "$":
                    if self.ptrlocation:
                        self.cells[self.cellptr]["t"] = 'l'
                        self.cells[self.cellptr]['r'] = self.ptrvalue[0]
                        self.cells[self.cellptr]['c'] = self.ptrvalue[1]
                    else:
                        self.cells[self.cellptr]['t'] = 'i'
                        self.cells[self.cellptr]['v'] = self.ptrvalue

                case '^':
                    if self.cells[self.cellptr]['t'] == 'l':
                        self.cells[self.cellptr]['v'] = self.realms[self.cells[self.cellptr]["r"]].cells[self.cells[self.cellptr]["c"]]["v"]
                        self.cells[self.cellptr]['t'] = 'i'

    def setup(self,code:str, **kwargs: dict):
        #remove unused charachters
        self.code = self.cleanup(list(code))

        code = self.code

        #generate links for the pairs of brackets,braces,parenthesis
        self.bracemap = self.buildbracemap(code)
        self.curlymap = self.buildcurlymap(code)
        self.parmap = self.buildparmap(code)

        #set to a default value if argument not provided
        self.realms = [Realm([{'t':'i','v':0} for _ in range(255)])] if not 'realms' in kwargs.keys() else kwargs['realms']
        self.codeptr = 0 if not 'codeptr' in kwargs.keys() else kwargs['codeptr']
        self.cellptr = 0 if not 'cellptr' in kwargs.keys() else kwargs['cellptr']
        self.realmptr = 0 if not 'realmptr' in kwargs.keys() else kwargs['realmptr']
        self.cells = self.realms[self.realmptr].cells

        #stuff for linking and copying values
        self.ptrvalue=0
        self.ptrlocation=False

        #print a newline afterwards if we printed anything
        self.printedChar=False

    def evaluate(self):
        while self.codeptr < len(self.code):
            command = self.code[self.codeptr]
            self.evalInstruction(command)
            self.codeptr +=1
        if self.printedChar: print('')
        return self.realms

    def step(self):
        command = self.code[self.codeptr]
        self.evalInstruction(command)
        self.codeptr +=1

    def cleanup(self,code: str):
        return "".join(
            filter(
                lambda x: x in [".", ",", "[", "]", "<", ">", "+", "-", "@", "|", "_","{","0","*","=","}","(",")","%","$","^"], code
            )
        )

    def buildbracemap(self,code: str):
        temp_bracestack, bracemap = [], {}

        for position, command in enumerate(code):
            if command == "[":
                temp_bracestack.append(position)
            if command == "]":
                start = temp_bracestack.pop()
                bracemap[start] = position
                bracemap[position] = start
        return bracemap

    def buildcurlymap(self,code: str):
        temp_bracestack, bracemap = [], {}

        for position, command in enumerate(code):
            if command == "{":
                temp_bracestack.append(position)
            if command == "}":
                start = temp_bracestack.pop()
                bracemap[start] = position
                bracemap[position] = start
        return bracemap

    def buildparmap(self,code: str):
        temp_bracestack, bracemap = [], {}

        for position, command in enumerate(code):
            if command == "(":
                temp_bracestack.append(position)
            if command == ")":
                start = temp_bracestack.pop()
                bracemap[start] = position
                bracemap[position] = start
        return bracemap
