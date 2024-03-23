# bot code goes here
from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *
from Game.playerActions import defense_actions, attack_actions, projectile_actions
from Game.gameSettings import HP, LEFTBORDER, RIGHTBORDER, LEFTSTART, RIGHTSTART, PARRYSTUN


# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Boomerang, Bear Trap

# TODO FOR PARTICIPANT: Set primary and secondary skill here
PRIMARY_SKILL = Meditate
SECONDARY_SKILL = Hadoken

#constants, for easier move return
#movements
JUMP = ("move", (0,1))
FORWARD = ("move", (1,0))
BACK = ("move", (-1,0))
JUMP_FORWARD = ("move", (1,1))
JUMP_BACKWARD = ("move", (-1, 1))

# attacks and block
LIGHT = ("light",)
HEAVY = ("heavy",)
BLOCK = ("block",)

PRIMARY = get_skill(PRIMARY_SKILL)
SECONDARY = get_skill(SECONDARY_SKILL)

# no move, aka no input
NOMOVE = "NoMove"
# for testing
moves = SECONDARY,
moves_iter = iter(moves)

# TODO FOR PARTICIPANT: WRITE YOUR WINNING BOT
class Script:
    def __init__(self):
        self.primary = PRIMARY_SKILL
        self.secondary = SECONDARY_SKILL
        
    # DO NOT TOUCH
    def init_player_skills(self):
        return self.primary, self.secondary
    
    # MAIN FUNCTION that returns a single move to the game manager
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):

        distance = get_distance(player, enemy)
        x_distance = get_pos(player)[0] - get_pos(enemy)[0]

        print(distance)
        print(x_distance)
        y_distance = abs(get_pos(player)[1] - get_pos(enemy)[1])

        # If meditate is not on cooldown, and our player is less than 80 HP.
        if not primary_on_cooldown(player) and get_hp(player) <= 80:
            return PRIMARY

        # If Hadoken is not on cooldown, and enemy is within 6 units, and not airborne
        if not secondary_on_cooldown(player) and (distance < 6) and y_distance == 0:
            return SECONDARY
        
        # If Hadoken is on cooldown, decide between a HEAVY ATTACK or moving away
        elif secondary_on_cooldown(player) and (distance <= 1) and y_distance == 0:
            if get_last_move(player) == "light" and get_past_move(player, 2) == "light":
                if get_block_status(enemy) == 0:
                    return HEAVY
                elif get_block_status(enemy) > 0 and x_distance > 0:
                    return BACK
                else:
                    return FORWARD
            # If Hadoken is on cooldown, decide between a LIGHT ATTACK or moving away
            elif get_last_move(player) == "light" and get_past_move(player, 2) != "light":
                if get_block_status(enemy) == 0:
                    return LIGHT
                elif get_block_status(enemy) > 0 and x_distance > 0:
                    return BACK
                else:
                    return FORWARD
            
            elif get_last_move(player) == "move":
                
        
        # If Hadoken is on cooldown, and enemy is not within 1 unit, retreat either forward or backwards.
        elif distance > 1 and y_distance == 0:
            if x_distance > 0:
                return FORWARD
            else:
                return BACK


     
        
