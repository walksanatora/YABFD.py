# stolen code from https://github.com/pocmo/Python-Brainfuck big thanks to them
#!/usr/bin/python
#
# Brainfuck Interpreter
# Copyright 2011 Sebastian Kaspari
#
# Usage: ./brainfuck.py [FILE]

import sys

from . import getch
from .util import *

class Brainfuck:

    def __init__(self):
        pass

    def printChar(self,char):
        sys.stdout.write(char)

    def getChar(self):
        return ord(getch.getch())

    def execute(self, filename: str):
        f = open(filename, "r")
        self.evaluate(f.read())
        f.close()


    def evaluate(self, code: str, **kwargs: dict) -> list[list[dict]]:
        #remove unused charachters
        code = self.cleanup(list(code))

        #generate links for the pairs of brackets,braces,parenthesis
        bracemap = self.buildbracemap(code)
        curlymap = self.buildcurlymap(code)
        parmap = self.buildparmap(code)

        #set to a default value if argument not provided
        realms = [generateMemSpace(255)] if not 'realms' in kwargs.keys() else kwargs['realms']
        codeptr = 0 if not 'codeptr' in kwargs.keys() else kwargs['codeptr']
        cellptr = 0 if not 'cellptr' in kwargs.keys() else kwargs['cellptr']
        realmptr = 0 if not 'realmptr' in kwargs.keys() else kwargs['realmptr']
        cells = realms[realmptr]['cells']

        #stuff for linking and copying values
        ptrvalue=0
        ptrlocation=False

        #print a newline afterwards if we printed anything
        printedChar=False

        while codeptr < len(code):
            command = code[codeptr]
            match command:
                case ">":
                    cellptr += 1
                    if cellptr == len(cells):
                        cellptr = 0

                case "<":
                    cellptr = len(cells)-1 if cellptr <= 0 else cellptr - 1

                case "+":
                    if cells[cellptr]["t"] == "i":
                        cells[cellptr]["v"] = (
                            cells[cellptr]["v"] + 1 if cells[cellptr]["v"] < 255 else 0
                        )
                    else:
                        realms[cells[cellptr]["r"]]["cells"][cells[cellptr]["c"]]["v"] = (
                            realms[cells[cellptr]["r"]]["cells"][cells[cellptr]["c"]]["v"]
                            + 1
                            if realms[cells[cellptr]["r"]]["cells"][cells[cellptr]["c"]][
                                "v"
                            ]
                            < 255
                            else 0)

                case "-":
                    if cells[cellptr]["t"] == "i":
                        cells[cellptr]["v"] = (
                            cells[cellptr]["v"] - 1 if cells[cellptr]["v"] > 0 else 255
                        )
                    else:
                        realms[cells[cellptr]["r"]]["cells"][cells[cellptr]["c"]]["v"] = (
                            realms[cells[cellptr]["r"]]["cells"][cells[cellptr]["c"]]["v"]
                            - 1
                            if realms[cells[cellptr]["r"]]["cells"][cells[cellptr]["c"]][
                                "v"
                            ]
                            > 0
                            else 255)

                case "[":
                    if cells[cellptr]["t"] == "i":
                        if cells[cellptr]["v"] == 0:
                            codeptr = bracemap[codeptr]
                    else:  # really cursed one liner to get a cell from another realm
                        if (
                            realms[cells[cellptr]["r"]]["cells"][cells[cellptr]["c"]][
                                "v"
                            ]
                            != 0
                        ):
                            codeptr = bracemap[codeptr]

                case "]":
                    if cells[cellptr]["t"] == "i":
                        if cells[cellptr]["v"] != 0:
                            codeptr = bracemap[codeptr]
                    else:
                        if (
                            realms[cells[cellptr]["r"]]["cells"][cells[cellptr]["c"]]["v"]
                            != 0
                        ):
                            codeptr = bracemap[codeptr]

                case ".":
                    if cells[cellptr]["t"] == "i":
                        self.printChar(chr(cells[cellptr]["v"]))
                    else:
                        self.printChar(
                            chr(
                                realms[cells[cellptr]["r"]]["cells"][cells[cellptr]["c"]][
                                    "v"
                                ]
                            )
                        )
                    printedChar=True

                case ",":
                    if cells[cellptr]["t"] == "i":
                        cells[cellptr]["v"] = self.getChar()
                    else:
                        realms[cells[cellptr]["r"]]["cells"][cells[cellptr]["c"]][
                            "v"
                        ] = self.getChar()

                case "|":
                    if cells[cellptr]["t"] == "i":
                        cells[cellptr]["v"] = realmptr
                    else:
                        realms[cells[cellptr]["r"]]["cells"][cells[cellptr]["c"]][
                            "v"
                        ] = realmptr

                case "@":
                    realmtgt = 0
                    if cells[cellptr]["t"] == "i":
                        realmtgt = cells[cellptr]["v"]
                    else:
                        realmtgt = realms[cells[cellptr]["r"]]["cells"][
                            cells[cellptr]["c"]
                        ]["v"] = realmptr
                    try:
                        cells = realms[realmtgt]['cells']
                        realmptr = realmtgt
                        cellptr = 0
                    except IndexError:
                        cells = realms[0]['cells']
                        realmptr = 0
                        cellptr = 0

                case "_":
                    realms[realmptr]['func'](realms,realmptr,cellptr)

                case "{":
                    bracket=codeptr
                    codeptr+=1
                    ins=code[codeptr]
                    skip=True
                    match ins:
                        case '0':
                            if cells[cellptr]["t"] == "i":
                                if cells[cellptr]["v"] == 0:
                                    skip=False
                            else:  # really cursed one liner to get a cell from another realm
                                if (
                                realms[cells[cellptr]["r"]]["cells"][cells[cellptr]["c"]][
                                    "v"
                                ]
                                == 0
                                ):
                                    skip = False
                        case '@':
                            if cells[cellptr]["t"] == "i":
                                if cells[cellptr]["v"] == realmptr:
                                    skip=False
                            else:  # really cursed one liner to get a cell from another realm
                                if (
                                realms[cells[cellptr]["r"]]["cells"][cells[cellptr]["c"]][
                                    "v"
                                ]
                                == realmptr
                                ):
                                    skip = False
                        case '*':
                            if cells[cellptr]['t'] == 'l':
                                skip=False
                        case '=':
                            left=0
                            right=0
                            if cells[cellptr-1]["t"] == "i":
                                left=cells[cellptr-1]["v"]
                            else:
                                left=realms[cells[cellptr]["r"]]["cells"][cells[cellptr]["c"]-1]["v"]
                            if cells[cellptr-1]["t"] == "i":
                                right=cells[cellptr]["v"]
                            else:
                                right=realms[cells[cellptr]["r"]]["cells"][cells[cellptr]["c"]]["v"]
                            if left==right:
                                skip=False
                        case '<':
                            left=0
                            right=0
                            if cells[cellptr-1]["t"] == "i":
                                left=cells[cellptr-1]["v"]
                            else:
                                left=realms[cells[cellptr]["r"]]["cells"][cells[cellptr]["c"]-1]["v"]
                            if cells[cellptr-1]["t"] == "i":
                                right=cells[cellptr]["v"]
                            else:
                                right=realms[cells[cellptr]["r"]]["cells"][cells[cellptr]["c"]]["v"]
                            if left<right:
                                skip=False
                        case '>':
                            left=0
                            right=0
                            if cells[cellptr-1]["t"] == "i":
                                left=cells[cellptr-1]["v"]
                            else:
                                left=realms[cells[cellptr]["r"]]["cells"][cells[cellptr]["c"]-1]["v"]
                            if cells[cellptr-1]["t"] == "i":
                                right=cells[cellptr]["v"]
                            else:
                                right=realms[cells[cellptr]["r"]]["cells"][cells[cellptr]["c"]]["v"]
                            if left>right:
                                skip=False
                    if skip:
                        codeptr=curlymap[bracket]

                case "}":
                    if code[codeptr+1] == '(':
                        codeptr=parmap[codeptr+1]

                case "*":
                    ptrvalue=[realmptr,cellptr]
                    ptrlocation=True

                case "%":
                    ptrvalue=0
                    if cells[cellptr]["t"] == "i":
                        ptrvalue = cells[cellptr]["v"]
                    else:
                        ptrvalue = realms[cells[cellptr]["r"]]["cells"][
                            cells[cellptr]["c"]
                        ]["v"]
                    ptrlocation=False

                case "$":
                    if ptrlocation:
                        cells[cellptr]["t"] = 'l'
                        cells[cellptr]['r'] = ptrvalue[0]
                        cells[cellptr]['c'] = ptrvalue[1]
                    else:
                        cells[cellptr]['t'] = 'i'
                        cells[cellptr]['v'] = ptrvalue

                case '^':
                    if cells[cellptr]['t'] == 'l':
                        cells[cellptr]['v'] = realms[cells[cellptr]["r"]]["cells"][cells[cellptr]["c"]]["v"]
                        cells[cellptr]['t'] = 'i'

            codeptr +=1
        if printedChar: print('')
        return realms


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
