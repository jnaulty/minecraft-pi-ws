from mcpi.minecraft import Minecraft
import mcpi.block as block

#=================================
#Helper functions
#================================

def message(msg):
    mc.postToChat(msg)

def getCurPos():
    return mc.player.getTilePos()


def getPlayerPos():
    # returns x, y, z
    return mc.player.getTilePos()

def setPlayerPos(x, y, z):
    mc.player.setPos(x, y, z)

def setCam():
    # birds eye view position
    entity = mc.getPlayerEntityIds()
    mc.camera.setFollow(entity[0])


def checkBlock(location, BLOCK):
    # return Boolean if location has block.block
    #location = (x, y, z)
    # block = mcpi block type in CAPS
    if mc.getBlock(location.x, location.y, location.z) == BLOCK:
        return True
    else:
        return False


def check_block_dir(BLOCK):
    # BLOCKS =takes block type: block.TYPE
    # direction: forward, left, right, behind
    space_dict = {'u': 0, 'l': 0, 'r': 0, 'd': 0}
    pos = cur_pos()
    fwd = mc.getBlock(pos.x, pos.y, pos.z + 1)
    left = mc.getBlock(pos.x + 1, pos.y, pos.z)
    right = mc.getBlock(pos.x - 1, pos.y, pos.z)
    back = mc.getBlock(pos.x, pos.y, pos.z - 1)
    for key in space_dict:
        if key == 'u' and fwd == BLOCK:
            space_dict['u'] += 1
        elif key == 'l'and left == BLOCK:
            space_dict['l'] += 1
        elif key == 'r'and right == BLOCK:
            space_dict['r'] += 1
        elif key == 'd' and back == BLOCK:
            space_dict['d'] += 1
    return space_dict




#================================
#Setup World
#===============================

def build_maze(layer):
    """
    Takes in a text generated maze.
    Clears a space in front of player position
    moves player to middle of maze on x-axis
    builds maze
    clears entrance to maze
    """
    # get player position
    # may also use origin = mc.player.getTilePos()
    # then use origin.x, origin.y, origin.z to set
    x, y, z = mc.player.getTilePos()
    if isinstance(layer, str):
        lines = layer.split("\n")
    else:
        lines = layer
    x_origin = x
    z_origin = z
    z_lines = len(lines)
    x_lines = len(lines[0])
    midline = x_lines // 2
    # clear space for maze
    mc.setBlocks(x, y, z, x + x_lines, y + 30, z + z_lines, block.AIR)
    # put player outside of maze in middle
    mc.player.setTilePos(midline, y, z - 1)

    for line in lines:
        x_origin = 0
        for char in line:
            if char == "1" or char == 1:
                # set block where 1 goes
                mc.setBlocks(x_origin, y, z, x_origin, y +
                             2, z,  block.DIAMOND_BLOCK)
                # add one to the origin along x-axis
            else:
                char == "0" or char == 0
                mc.setBlocks(x_origin, y, z, x_origin, y + 2, z, block.AIR)
            x_origin += 1
        # add one to the origin along z-axis
        z += 1
    new_pos = getCurPos()
    new_pos.z += 1
    # make a doorway to maze
    if not checkBlock(new_pos, block.AIR):
        mc.setBlocks(new_pos.x, new_pos.y, new_pos.z + 1,
                     new_pos.x, new_pos.y + 2, new_pos.z + 1, block.AIR)


def build_world():
    x, y, z = getPlayerPos()
    x_origin = x
    z_origin = z
    # clear space for maze
    mc.setBlocks(x, y, z, x + 20, y + 30, z + 30, block.AIR)
    # put player outside of maze in middle
    mc.player.setTilePos(x/2, y, z - 1)
    

if __name__ == "__main__":

    mc = Minecraft.create()
    mc.setBlocks(-100, -1, -100, 100, 0, 100, 2)
    mc.setBlocks(-100, 1, -100, 100, 100, 100, 0)
    mc.postToChat("Begin Building Maze")
    from gen_maze import maze
    data = maze(20, 20)
    message("Welcome TCDisruptSF 2016")
    mc.player.setPos(0, 0, 0)
    build_maze(data)
    pos = getCurPos()
    setCam()
    mc.player.setPos(pos.x + .5, pos.y, pos.z + 2.5)
    
    #build_world()
