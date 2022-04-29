def DoNothing(realms: list[list], realmptr: int, ptr: int):
    return

def PrintInt(realms: list[list],realmptr: int, ptr:int):
	print(realms[realmptr]['cells'][ptr]['v'])

def generateMemSpace(cells: int = 255) -> list[dict]:
    return {"cells": [{"t": "i", "v": 0} for _ in range(cells)], "func": PrintInt}


def intListToMemSpace(il: list[int]) -> list[dict]:
    mem = []
    for v in il:
        mem.append({"t": "i", "v": v})
    return mem



def memToList(mem):
    output = []
    for cells in mem:
        tmpOut = []
        for cell in cells["cells"]:
            if cell['t'] == 'i':
                tmpOut.append(cell["v"])
            else:
                tmpOut.append(mem[cell["r"]]["cells"][cell["c"]]["v"])
        output.append(tmpOut)
    return output
