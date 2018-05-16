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
    global lives
    if block.WATER_STATIONARY.id == mc.getBlockWithData(mc.player.getTilePos()).id:
        mc.player.setTilePos(startPos)
        lives= lives-1
        if lives > 1:
            mc.postToChat("YOU HAVE " + str(lives) + " LIVES REMAINING")
        elif lives

def setTimer():
    global timer
    if done == False:
        time.sleep(1)
        timer = timer - 1
        mc.postToChat("timer = " + str(timer))


def setReplay():
    global position
    pos = mc.player.getTilePos()
    replay = [pos.x + 1, pos.y, pos.z]
    gameOver = [pos.x - 1, pos.y, pos.z]
    mc.setBlock(replay, block.GREEN_WOOL)
    mc.setBlock(gameOver, block.RED_WOOL)
    position.append(replay)
    position.append(gameOver)

def replayDecision():
    global done
    global bootyFound
    global empty_blocks
    global PlayerValue
    global position
    events = mc.events.pollBlockHits()
    for e in events:
        pos = e.pos
        while len(position) > 0:
            for choice in position:
                if block.GREEN_WOOL.data == mc.getBlockWithData(pos).data:
                    position = []
                    mc.postToChat("Play")
                    done = False
                    empty_blocks = Num_Cols * Num_Rows
                    PlayerValue = [[0, 0, 0],
                                   [0, 0, 0],
                                   [0, 0, 0]]
                    game()
                elif  block.RED_WOOL.data == mc.getBlockWithData(pos).data:
                    mc.postToChat("Don't Play Again")
                    clearArea(radius)
                    quit()

def setBoard():
    global done
    global timer
    done = False
    clearArea(radius)
    if level == 1:
        buildBoard("lEVEL 1", pos.x+1, pos.y, pos.z+1)
    elif level == 2:
        timer = 90
        mc.player.setTilePos(startPos)
        buildBoard("Level 2(V2)", pos.x + 1, pos.y, pos.z + 1)
    elif level == 3:
        timer = 120
        mc.player.setTilePos(startPos)
        buildBoard("Level 3(V2)", pos.x + 1, pos.y, pos.z + 1)
def youLost():
    global done
    if lives == 0 or timer ==0:
        mc.postToChat("YOU LOST, PUTTING YOU AT THE START")
        replayFinal()
def replayFinal():
    if level == 4:
        clearArea(50)
        mc.player.setTilePos(startPos)
        while done == True:
            time.sleep(2)
            mc.postToChat("Do you want to play again")

def BarrelRoll():
    while lives > 0:
        mc.setBlock()

while lives > 0:
    setBoard()
    while not done:
        setTimer()
        checkWin()
        inWater()
        replayFinal()
        youLost()