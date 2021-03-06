import mcpi.minecraft as minecraft
import mcpi.block as block
import mcpi.minecraftstuff as minecraftstuff
from mcpi.vec3 import Vec3
import _thread
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
wait = 1
complete = False
pause = 2
threads = []
L1_Offset = [10, 10, 6]
L2_Offset = [2, 16, 6]
L3_Offset = [20, 19, 8]
radius = 40
finished = False
position = []
score = 0
startPos = pos
done = False
timer = 60

#define functions

def instructions():  #displays instructions before game begins
    mc.postToChat("type /gamemode 1. Next press E on keyboard and select a sword from inventory")
    time.sleep(wait)
    mc.postToChat("type /gamemode 2. Jump up the structures and hit the diamond block at the top to complete the level.")
    time.sleep(wait)
    mc.postToChat("You have 3 lives to complete all 3 levels. Do not fall in the water, do not switch gamemode, do not let timer run out.")
    time.sleep(wait)

def clearArea(radius):  #clears area around player
    position = mc.player.getTilePos()
    mc.setBlocks(position.x - radius,
                 position.y,
                 position.z - radius,
                 position.x + radius,
                 position.y + radius,
                 position.z + radius,
                 block.AIR)

def buildBoard(filename, originx, originy, originz): #builds the board from csv file
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

def checkWin():   #checks to see if the player hits diamond block at top of board and wins
    global level
    global done
    global complete
    events = mc.events.pollBlockHits()
    for e in events:
        pos = e.pos
        if block.DIAMOND_BLOCK.id == mc.getBlockWithData(pos).id:
            mc.postToChat("Congratulations! You reached the treasured and beat the level")
            level = level + 1
            done = True
            complete = True
            time.sleep(1)


def inWater():   #checks to see if player fell off board into the water
    global lives
    global timer
    if (block.WATER_STATIONARY.id == mc.getBlockWithData(mc.player.getTilePos()).id) or (block.SANDSTONE_SLAB.id == mc.getBlockWithData(mc.player.getTilePos()).id):
        mc.player.setTilePos(startPos)
        lives= lives-1
        if level== 1:
            timer = 60
        elif level == 2:
            timer = 120
        elif level == 3:
            timer = 150
        if lives > 1 or lives == 0:
            mc.postToChat("YOU HAVE " + str(lives) + " LIVES REMAINING")
        elif lives == 1:
            mc.postToChat("YOU HAVE " + str(lives) + " LIFE REMAINING")



def setTimer():   #sets timer up. If timer hits 0 player loses
    global timer
    while not done:
        if timer > 0 and finished == False:
            time.sleep(1)
            timer = timer - 1
            mc.postToChat("timer = " + str(timer))
        elif timer == 0:
            mc.postToChat("YOU LOST, PUTTING YOU AT THE START")


def setReplay():  #sets up the replay blocks
    global position
    pos = mc.player.getTilePos()
    replay = [pos.x + 1, pos.y, pos.z]
    gameOver = [pos.x - 1, pos.y, pos.z]
    mc.setBlock(replay, block.GREEN_WOOL)
    mc.setBlock(gameOver, block.RED_WOOL)
    position.append(replay)
    position.append(gameOver)

def replayDecision():  #waits till player makes a replay choice
    global done
    global finished
    global level
    global lives
    global timer
    global position
    events = mc.events.pollBlockHits()
    for e in events:
        pos = e.pos
        while len(position) > 0:
            for choice in position:
                if block.GREEN_WOOL.data == mc.getBlockWithData(pos).data:
                    position = []
                    mc.postToChat("Play")
                    level = 1
                    lives = 3
                    timer = 60
                    done = False
                    finished = False
                    game()
                elif block.RED_WOOL.data == mc.getBlockWithData(pos).data:
                    mc.postToChat("Don't Play Again")
                    clearArea(radius)
                    quit()

def setBoard():   #sets the board depending on what level player is on
    global done
    global timer
    done = False
    clearArea(radius)
    if level == 1:
        buildBoard("lEVEL 1", pos.x+1, pos.y, pos.z+1)
    elif level == 2:
        timer = 120
        mc.player.setTilePos(startPos)
        buildBoard("Level 2(V2)", pos.x + 1, pos.y, pos.z + 1)
    elif level == 3:
        timer = 180
        mc.player.setTilePos(startPos)
        buildBoard("Level 3(V2)", pos.x + 1, pos.y, pos.z + 1)

def replayFinal():  #runs replay setup and then decision and clears board
    global finished
    if level == 4 or lives == 0 or timer ==0:
        finished = True
        mc.player.setTilePos(startPos)
        clearArea(radius)
        setReplay()
        mc.postToChat("Do you want to play again")
        while finished:
            replayDecision()

def BarrelRoll():  #gives the path for barrels to roll down on each levels board
        if level == 1:
            mc.setBlock(startPos.x + L1_Offset[0], startPos.y + L1_Offset[1], startPos.z + L1_Offset[2], block.SANDSTONE_SLAB.id)
            sandPos = Vec3(startPos.x + L1_Offset[0], startPos.y + L1_Offset[1], startPos.z + L1_Offset[2])
            sandBlock = [minecraftstuff.ShapeBlock(0, 0, 0, block.SANDSTONE_SLAB.id)]
            barrel = minecraftstuff.MinecraftShape(mc, sandPos, sandBlock)
            for n in range(0,2):
                for n in range(1, 7):
                    if level == 1:
                        time.sleep(pause)
                        barrel.moveBy(-1, 0, 0)
                    else:
                        mc.setBlock(barrel.position, block.AIR.id)
                for n in range(0, 2):
                    if level == 1:
                        time.sleep(pause)
                        barrel.moveBy(-1, -1, 0)
                    else:
                        mc.setBlock(barrel.position, block.AIR.id)
                for n in range(0, 1):
                    if level == 1:
                        time.sleep(pause)
                        barrel.moveBy(0, 0, -1)
                    else:
                        mc.setBlock(barrel.position, block.AIR.id)
                for n in range(0, 6):
                    if level == 1:
                        time.sleep(pause)
                        barrel.moveBy(1, 0, 0)
                    else:
                        mc.setBlock(barrel.position, block.AIR.id)
                for n in range(0, 2):
                    if level == 1:
                        time.sleep(pause)
                        barrel.moveBy(1, -1, 0)
                    else:
                        mc.setBlock(barrel.position, block.AIR.id)
                for n in range(0, 1):
                    if level == 1:
                        time.sleep(pause)
                        barrel.moveBy(0, 0, -1)
                    else:
                        mc.setBlock(barrel.position, block.AIR.id)

        if level == 2:
            mc.setBlock(startPos.x + L2_Offset[0], startPos.y + L2_Offset[1], startPos.z + L2_Offset[2],
                        block.SANDSTONE_SLAB.id)
            sandPos = Vec3(startPos.x + L2_Offset[0], startPos.y + L2_Offset[1], startPos.z + L2_Offset[2])
            sandBlock = [minecraftstuff.ShapeBlock(0, 0, 0, block.SANDSTONE_SLAB.id)]
            barrel = minecraftstuff.MinecraftShape(mc, sandPos, sandBlock)
            for n in range (0,2):
                for n in range (0,12):
                    if level == 2:
                        time.sleep(pause)
                        barrel.moveBy(1, 0, 0)
                    else:
                        mc.setBlock(barrel.position, block.AIR.id)
                for n in range(0, 3):
                    if level == 2:
                        time.sleep(pause)
                        barrel.moveBy(1, -1, 0)
                    else:
                        mc.setBlock(barrel.position, block.AIR.id)
                for n in range(0,1):
                    if level == 2:
                        time.sleep(pause)
                        barrel.moveBy(0, 0, -1)
                    else:
                        mc.setBlock(barrel.position, block.AIR.id)
                for n in range(0, 12):
                    if level == 2:
                        time.sleep(pause)
                        barrel.moveBy(-1,0,0)
                    else:
                        mc.setBlock(barrel.position, block.AIR.id)
                for n in range(0, 3):
                    if level == 2:
                        time.sleep(pause)
                        barrel.moveBy(-1, -1, 0)
                    else:
                        mc.setBlock(barrel.position, block.AIR.id)
                for n in range(0,1):
                    if level == 2:
                        time.sleep(pause)
                        barrel.moveBy(0, 0, -1)
                    else:
                        mc.setBlock(barrel.position, block.AIR.id)
            for n in range(0,12):
                if level == 2:
                    time.sleep(pause)
                    barrel.moveBy(1,0,0)
                else:
                    mc.setBlock(barrel.position, block.AIR.id)
        if level == 3:
            mc.setBlock(startPos.x + L3_Offset[0], startPos.y + L3_Offset[1], startPos.z + L3_Offset[2],
                        block.SANDSTONE_SLAB.id)
            sandPos = Vec3(startPos.x + L3_Offset[0], startPos.y + L3_Offset[1], startPos.z + L3_Offset[2])
            sandBlock = [minecraftstuff.ShapeBlock(0, 0, 0, block.SANDSTONE_SLAB.id)]
            barrel = minecraftstuff.MinecraftShape(mc, sandPos, sandBlock)
            for n in range(0,1):
                for n in range(0,15):
                    if level == 3:
                        time.sleep(pause)
                        barrel.moveBy(-1, 0, 0)
                    else:
                        mc.setBlock(barrel.position, block.AIR.id)
                for n in range(0,3):
                    if level == 3:
                        time.sleep(pause)
                        barrel.moveBy(-1, -1, 0)
                    else:
                        mc.setBlock(barrel.position, block.AIR.id)
                for n in range(0,1):
                    if level == 3:
                        time.sleep(pause)
                        barrel.moveBy(0, 0, -1)
                    else:
                        mc.setBlock(barrel.position, block.AIR.id)
                for n in range(0,15):
                    if level == 3:
                        time.sleep(pause)
                        barrel.moveBy(1, 0, 0)
                    else:
                        mc.setBlock(barrel.position, block.AIR.id)
                for n in range(0,3):
                    if level == 3:
                        time.sleep(pause)
                        barrel.moveBy(1, -1, 0)
                    else:
                        mc.setBlock(barrel.position, block.AIR.id)
                for n in range(0,1):
                    if level == 3:
                        time.sleep(pause)
                        barrel.moveBy(0, 0, -1)
                    else:
                        mc.setBlock(barrel.position, block.AIR.id)


                for n in range(0,10):
                    if level == 3:
                        time.sleep(pause)
                        barrel.moveBy(-1, 0, 0)
                    else:
                        mc.setBlock(barrel.position, block.AIR.id)
                for n in range(0,1):
                    if level == 3:
                        time.sleep(pause)
                        barrel.moveBy(-1, 1, 0)
                    else:
                        mc.setBlock(barrel.position, block.AIR.id)
                for n in range(0,1):
                    if level == 3:
                        time.sleep(pause)
                        barrel.moveBy(-1, 0, 0)
                    else:
                        mc.setBlock(barrel.position, block.AIR.id)
                for n in range(0,1):
                    if level == 3:
                        time.sleep(pause)
                        barrel.moveBy(-1, -1, 0)
                    else:
                        mc.setBlock(barrel.position, block.AIR.id)
                for n in range(0,2):
                    if level == 3:
                        time.sleep(pause)
                        barrel.moveBy(-1, 0, 0)
                    else:
                        mc.setBlock(barrel.position, block.AIR.id)
                for n in range(0,3):
                    if level == 3:
                        time.sleep(pause)
                        barrel.moveBy(-1, -1, 0)
                    else:
                        mc.setBlock(barrel.position, block.AIR.id)
                for n in range(0,1):
                    if level == 3:
                        time.sleep(pause)
                        barrel.moveBy(0, 0, -1)
                    else:
                        mc.setBlock(barrel.position, block.AIR.id)
                for n in range(0,15):
                    if level == 3:
                        time.sleep(pause)
                        barrel.moveBy(1, 0, 0)
                    else:
                        mc.setBlock(barrel.position, block.AIR.id)
                for n in range(0,3):
                    if level == 3:
                        time.sleep(pause)
                        barrel.moveBy(1, -1, 0)
                    else:
                        mc.setBlock(barrel.position, block.AIR.id)
                for n in range(0,1):
                    if level == 3:
                        time.sleep(pause)
                        barrel.moveBy(0, 0, -1)
                    else:
                        mc.setBlock(barrel.position, block.AIR.id)
                for n in range(0,12):
                    if level == 3:
                        time.sleep(pause)
                        barrel.moveBy(-1, 0, 0)
                    else:
                        mc.setBlock(barrel.position, block.AIR.id)
                for n in range(0,1):
                    if level == 3:
                        time.sleep(pause)
                        barrel.moveBy(-1, 1, 0)
                    else:
                        mc.setBlock(barrel.position, block.AIR.id)
                for n in range(0,1):
                    if level == 3:
                        time.sleep(pause)
                        barrel.moveBy(-1, 0, 0)
                    else:
                        mc.setBlock(barrel.position, block.AIR.id)
                for n in range(0,4):
                    if level == 3:
                        time.sleep(pause)
                        barrel.moveBy(-1, -1, 0)
                    else:
                        mc.setBlock(barrel.position, block.AIR.id)
                for n in range(0,1):
                    if level == 3:
                        time.sleep(pause)
                        barrel.moveBy(0, 0, -1)
                    else:
                        mc.setBlock(barrel.position, block.AIR.id)
                for n in range(0,16):
                    if level == 3:
                        time.sleep(pause)
                        barrel.moveBy(1, 0, 0)
                    else:
                        mc.setBlock(barrel.position, block.AIR.id)
                for n in range(0,1):
                    if level == 3:
                        mc.setBlock(barrel.position, block.AIR.id)

#creates new threads for each new barrel roll
def rolldat():
    global threads
    global complete
    while not complete:
        _thread.start_new_thread(BarrelRoll, ())
        if level == 1:
            time.sleep(10)
        elif level == 2:
            time.sleep(18)
        elif level == 3:
            time.sleep(22)
    complete = False
    _thread.exit_thread()

#game loop without instructions. Has functions like checking if player is in water etc.
def game():
    while lives > 0:
        setBoard()
        _thread.start_new_thread(rolldat, ())
        _thread.start_new_thread(setTimer, ())
        while not done:
            checkWin()
            inWater()
            replayFinal()

#Main game loop. Made in tis format for replay functionality, by putting the main game loop as a function.
instructions()
game()
