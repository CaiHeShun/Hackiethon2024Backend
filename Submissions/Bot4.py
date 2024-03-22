# bot code goes here
from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *
from Game.playerActions import defense_actions, attack_actions, projectile_actions
from Game.gameSettings import HP, LEFTBORDER, RIGHTBORDER, LEFTSTART, RIGHTSTART, PARRYSTUN


# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Boomerang, Bear Trap

# TODO FOR PARTICIPANT: Set primary and secondary skill here
PRIMARY_SKILL = TeleportSkill
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
CANCEL = ("skill_cancel", )

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
        
        x_distance = get_distance(player, enemy)
        y_distance = abs(get_pos(player)[1] - get_pos(enemy)[1])

        # If the enemy has uppercut that's not on cooldown, evade them
        if not primary_on_cooldown(enemy) and get_primary_skill(enemy) == "uppercut":
            # We're in uppercut range from both sides, move away
            if x_distance == 1:
                return BACK
            elif x_distance == -1:
                return FORWARD

        # Turn Super Saiyan - Damage 2X
        if not primary_on_cooldown(player):
            return PRIMARY
        
        # If not on cooldown and travel range less than or equal to range of Hadoken, activate Hadoken
        if not secondary_on_cooldown(player) and abs(x_distance) <= seco_range(player) and y_distance == 0:
            return SECONDARY     
        
        # Enemy is out of range, chase them
        # Enemy is behind us, move back
        elif x_distance > 0:
            return BACK
        
        # Enemy is forward of us, move forward.
        elif x_distance < 0:
            return FORWARD


        # IF ENEMY IS STUNNED, SAFE TO MOVE IN.
        if get_stun_duration(enemy) >= 3 and abs(x_distance) > 3:
            return JUMP_FORWARD
        elif get_stun_duration(enemy) >= 1 and abs(x_distance) > 1:
            return FORWARD
        
        # If we're lower health than the enemy
        if get_hp(enemy) > get_hp(player) and x_distance < -1:
            return FORWARD
        if get_hp(enemy) > get_hp(player) and x_distance > 1:
            return BACK
            
        # COMBO ATTACK 
        if get_last_move(player) == "light" and get_past_move(player, 2) == "light":
            # If they're in range, block is ready, and the enemy has no shield
            if not heavy_on_cooldown() and abs(x_distance) == 1 and get_block_status(enemy) == 0:
                return HEAVY
            # If they're in range, block is ready, 
            elif heavy_on_cooldown() and abs(x_distance) == 1 and get_block_status(enemy) > 0:
                return LIGHT
            # Not in range, move forward
            elif x_distance < -1:
                return FORWARD
            # Not in range, move backwards
            elif x_distance > 1:
                return BACK
        