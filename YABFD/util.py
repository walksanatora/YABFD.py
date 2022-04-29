def DoNothing(realms: list[list], realmptr: int, ptr: int):
    return

def PrintInt(realms: list[list],realmptr: int, ptr:int):
	print(realms[realmptr]['cells'][ptr]['v'])

def generateMemSpace(cells: int = 255) -> list[dict]:
    return {"cells": [{"t": "i", "v": 0} for _ in range(cells)], "func": PrintInt}


def listToMem(l:list[list]):
    output = []
    for realms in l:
        tmp_output=[]
        for value in realms:
            if type(value) == type(1):
                tmp_output.append({'t':'i','v':value})
            elif type(value) == type('str'):
                v = value.lstrip('$')
                v = v.split(':')
                tmp_output.append({'t':'l','v':0,'r':v[0],'c':v[1]})
        output.append(tmp_output)
    return output


def memToList(mem):
    output = []
    for cells in mem:
        tmpOut = []
        for cell in cells["cells"]:
            if cell['t'] == 'i':
                tmpOut.append(cell["v"])
            else:
                tmpOut.append(f"${cell['r']}:{cell['c']}")
        output.append(tmpOut)
    return output
