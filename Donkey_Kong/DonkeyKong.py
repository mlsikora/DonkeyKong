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
lives = 3
radius = 40
score = 0
startPos = pos
done = False
timer = 60

buildLevel = ["lEVEL 1", "Level 2", "level 3"]

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
    global level
    global done
    events = mc.events.pollBlockHits()
    for e in events:
        pos = e.pos
        if block.DIAMOND_BLOCK.id == mc.getBlockWithData(pos).id:
            mc.postToChat("Congratulations! You reached the treasured and beat the level")
            level = level + 1
            done = True

def inWater():
    if block.WATER_STATIONARY.id == mc.getBlockWithData(mc.player.getTilePos()).id:
        mc.player.setTilePos(startPos)

def setBoard():
    global done
    done = False
    clearArea(radius)
    if level == 1:
        buildBoard(buildLevel[0], pos.x+1, pos.y, pos.z+1)
    elif level == 2:
        buildBoard(buildLevel[1], pos.x + 1, pos.y, pos.z + 1)
    elif level == 3:
        buildBoard(buildLevel[0], pos.x + 1, pos.y, pos.z + 1)


while lives > 0:
    setBoard()
    while not done:
        checkWin()
        inWater()

