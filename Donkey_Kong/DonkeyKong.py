import mcpi.minecraft as minecraft
import mcpi.block as block
import mcpi.minecraftstuff as minecraftstuff
import time

mc = minecraft.Minecraft.create()
pos = mc.player.getTilePos()

#define constants
BOARD_ROWS = 3
MINECART_DELAY = 2
BOARD_WIDTH = 2
BOARD_HEIGHT = 30
BOARD_LENGTH = 15

#define variables
level = 1
numLives = 3
radius = 40
score = 0
done = False
timer = 60

#define functions
def clearArea(radius):
    position = mc.player.getTilePos()
    mc.setBlocks(position.x - radius,
                 position.y,
                 position.z - radius,
                 position.x + radius,
                 position.y + radius,
                 position.z + radius,
                 block.AIR)

def buildBoard(filename, originx, originy, originz):
    f = open(filename, "r")
    lines = f.readlines()

    coords = lines[0].split(",")
    sizex = int(coords[0])
    sizey = int(coords[1])
    sizez = int(coords[2])

    lineidx = 1

    for y in range(sizey):
        mc.postToChat("print:" + str(y))
        lineidx = lineidx + 1

        for x in range(sizex):
            line = lines[lineidx]
            lineidx = lineidx + 1
            data = line.split(",")

            for z in range(sizez):
                blockid = int(data[z])
                mc.setBlock(originx + x, originy + y, originz + z, blockid)

def checkWin():
    events = mc.events.pollBlockHits()
    for e in events:
        pos = e.pos
        if block.DIAMOND_BLOCK.data == mc.getBlockWithData(pos).data:
            mc.postToChat("Congratulations! You reached the treasured and beat the level")

def Level_1():
    clearArea(radius)
    buildBoard("lEVEL 1",pos.x+1, pos.y, pos.z+1)
    while not done:
        checkWin()

def Level_2():
    clearArea(radius)
    buildBoard("lEVEL 2",pos.x+1, pos.y, pos.z+1)
    while not done:
        checkWin()

def Level_3():
    clearArea(radius)
    buildBoard("lEVEL 3",pos.x+1, pos.y, pos.z+1)
    while not done:
        checkWin()

Level_1()