from audioop import avg
from cgitb import handler
from doctest import FAIL_FAST
from logging import critical
from multiprocessing import context
from pydoc import cli
import random as rand
import pickle, os, sys, math, pygame
from types import TracebackType
from select import select
from tkinter import Y
from pygame import display
pygame.font.init()
pygame.mixer.init()

######################################
########### Pygame Variables #########

WIDTH, HEIGHT = 500, 600

from pygame.locals import *
pygame.init()
pygame.display.set_caption('First')
screen = pygame.display.set_mode((WIDTH, HEIGHT))

font = pygame.font.Font('alagard.ttf', 20)
big_font = pygame.font.Font('alagard.ttf', 40)
intermediate_font = pygame.font.Font('alagard.ttf', 18)
small_font = pygame.font.Font('alagard.ttf', 15)
description_font = pygame.font.Font('alagard.ttf', 13)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (204,119,34)
GRAY = (128, 128, 128)
INTERMEDIATE_GRAY = (175, 175, 175)
LIGHT_GRAY = ( 210, 210, 210)
VERY_LIGHT_GRAY = ( 230, 230, 230)
GREEN = ( 0, 128, 0)
FIRE = (255, 100, 20)
METAL = ( 50, 50, 50)

FPS = 60

#####################################
########### Import Sound ############

attack_sfx = pygame.mixer.Sound(os.path.join('Assets', 'attack_sfx.wav'))
crit_attack_sfx = pygame.mixer.Sound(os.path.join('Assets', 'crit_attack_sfx.wav'))
death_sfx = pygame.mixer.Sound(os.path.join('Assets', 'death_sfx.wav'))
rest_regen_sfx = pygame.mixer.Sound(os.path.join('Assets', 'rest_regen_sfx.wav'))
parry_attack_sfx = pygame.mixer.Sound(os.path.join('Assets', 'parry_attack_sfx.wav'))
dodge_sfx = pygame.mixer.Sound(os.path.join('Assets', 'dodge_sfx.wav'))
status_update_sfx = pygame.mixer.Sound(os.path.join('Assets', 'status_update_sfx.wav'))
consumable_sfx = pygame.mixer.Sound(os.path.join('Assets', 'consumable_sfx.wav'))
regen_sfx = pygame.mixer.Sound(os.path.join('Assets', 'regen_sfx.wav'))
warcry_sfx = pygame.mixer.Sound(os.path.join('Assets', 'warcry_sfx.wav'))
multistrike_sfx = pygame.mixer.Sound(os.path.join('Assets', 'multistrike_sfx.wav'))

def play_town_music():
	pygame.mixer.music.load((os.path.join('Assets', 'Locations_Medieval Tavern Song.wav')))
	pygame.mixer.music.set_volume(0.5)
	pygame.mixer.music.play()

def play_dungeon_music():
	pygame.mixer.music.load((os.path.join('Assets', 'Exploration_Dark (loop).wav')))
	pygame.mixer.music.set_volume(0.5)
	pygame.mixer.music.play()

def play_battle_music():
	roll = rand.randint(1,2)

	if roll == 1:
		pygame.mixer.music.load((os.path.join('Assets', 'intro_main_battle_music.ogg')))
		pygame.mixer.music.set_volume(0.5)
		pygame.mixer.music.play()
		pygame.mixer.music.queue((os.path.join('Assets', 'main_battle_music.ogg')))

	if roll == 2:	
		pygame.mixer.music.load((os.path.join('Assets', 'Music_4_HeroicFight_Intro_FullTrack.wav')))
		pygame.mixer.music.set_volume(0.5)
		pygame.mixer.music.play()
		pygame.mixer.music.queue((os.path.join('Assets', 'Music_4_HeroicFight_Loop_FullTrack.wav')))
	
def play_defeat_music():
	pygame.mixer.music.load((os.path.join('Assets', 'defeat_music.wav')))
	pygame.mixer.music.set_volume(0.5)
	pygame.mixer.music.play()
	
def play_victory_music():
	pygame.mixer.music.load((os.path.join('Assets', 'victory_music.wav')))
	pygame.mixer.music.set_volume(0.4)
	pygame.mixer.music.play()

#####################################
########### Import Image ############

BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'gray_wall.jpg')), (WIDTH, HEIGHT))

def BACKGROUND():
	screen.fill(LIGHT_GRAY)

CROSSEDSWORDS_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'crossedswords.png')), ( 30, 30))
SHIELD_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'shield.png')), ( 30, 30))
SKULL_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'skull.png')), ( 30, 30))
SHIELD_DEFLECT_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'shield_deflect.png')), ( 30, 30))
RIPOSTE_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'riposte.png')), ( 30, 30))
DODGE_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'dodge.png')), ( 30, 30))
ARROW_UP_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'arrow.png')), ( 30, 30))
ARROW_DOWN_IMAGE = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'arrow.png')), ( 30, 30)), 180)
EYE_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'eye_icon.png')), ( 40, 40))
LEFT_ARROW_IMAGE = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'arrow.png')), ( 25, 35)), 90)
RIGHT_ARROW_IMAGE = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'arrow.png')), ( 25, 35)), 270)
DUNGEON_RETURN_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'return_icon.png')), ( 30, 30))
DUNGEON_NEXT_FLOOR_TRUE_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'next_floor_true.png')), ( 30, 30))
DUNGEON_NEXT_FLOOR_FALSE_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'next_floor_false.png')), ( 30, 30))
ATTACKER_IMAGE = pygame.image.load(os.path.join('Assets', 'attacker.png'))
DEFENDER_IMAGE = pygame.image.load(os.path.join('Assets', 'defender.png'))
DEATH_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'death_icon.png')), ( 100, 100))
CHECK_PARTY_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'dungeon_check_party.png')), ( 50, 50))
DUNGEON_CONSUMABLE_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'dungeon_consumable.png')), ( 50, 50))
CHECK_LOOT_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'dungeon_check_loot.png')), ( 50, 50))
UPGRADE_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'upgrade.png')), ( 40, 40))
TRAINING_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'training.png')), ( 40, 40))
BUY_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'buy.png')), ( 22, 22))
SELL_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'dungeon_check_loot.png')), ( 25, 25))

## Consumables images ##

#Health Pot

SMALL_HEALTH_POTION_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'small_health_potion.png')), ( 40, 40))
BUY_SMALL_HEALTH_POTION_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'small_health_potion.png')), ( 20, 20))
MEDIUM_HEALTH_POTION_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'medium_health_potion.png')), ( 40, 40))
BUY_MEDIUM_HEALTH_POTION_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'medium_health_potion.png')), ( 20, 20))
LARGE_HEALTH_POTION_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'large_health_potion.png')), ( 40, 40))
BUY_LARGE_HEALTH_POTION_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'large_health_potion.png')), ( 20, 20))

#Mana Pot

SMALL_MANA_POTION_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'small_mana_potion.png')), ( 40, 40))
BUY_SMALL_MANA_POTION_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'small_mana_potion.png')), ( 20, 20))
MEDIUM_MANA_POTION_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'medium_mana_potion.png')), ( 40, 40))
BUY_MEDIUM_MANA_POTION_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'medium_mana_potion.png')), ( 20, 20))
LARGE_MANA_POTION_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'large_mana_potion.png')), ( 40, 40))
BUY_LARGE_MANA_POTION_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'large_mana_potion.png')), ( 20, 20))

## Weapons images ##

#Two_handed Swords
TH_SWORD_1_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'th_sword_1.png')), ( 50, 50))
TH_SWORD_2_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'th_sword_2.png')), ( 50, 50))
TH_SWORD_3_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'th_sword_3.png')), ( 50, 50))
TH_SWORD_4_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'th_sword_4.png')), ( 50, 50))
TH_SWORD_5_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'th_sword_5.png')), ( 50, 50))
TH_SWORD_6_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'th_sword_6.png')), ( 50, 50))
TH_SWORD_7_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'th_sword_7.png')), ( 50, 50))


## Armor image ##

#Warrior Armor

#Helmet
WAR_HELMET_1_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'war_helmet_1.png')), ( 50, 50))
WAR_HELMET_2_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'war_helmet_2.png')), ( 50, 50))
WAR_HELMET_3_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'war_helmet_3.png')), ( 50, 50))
WAR_HELMET_4_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'war_helmet_4.png')), ( 50, 50))
WAR_HELMET_5_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'war_helmet_5.png')), ( 50, 50))
WAR_HELMET_6_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'war_helmet_6.png')), ( 50, 50))
WAR_HELMET_7_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'war_helmet_7.png')), ( 50, 50))

#Chest
WAR_CHEST_1_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'war_chest_1.png')), ( 50, 50))
WAR_CHEST_2_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'war_chest_2.png')), ( 50, 50))
WAR_CHEST_3_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'war_chest_3.png')), ( 50, 50))
WAR_CHEST_4_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'war_chest_4.png')), ( 50, 50))
WAR_CHEST_5_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'war_chest_5.png')), ( 50, 50))
WAR_CHEST_6_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'war_chest_6.png')), ( 50, 50))
WAR_CHEST_7_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'war_chest_7.png')), ( 50, 50))

#Legs
WAR_LEGS_1_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'war_legs_1.png')), ( 50, 50))
WAR_LEGS_2_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'war_legs_2.png')), ( 50, 50))
WAR_LEGS_3_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'war_legs_3.png')), ( 50, 50))
WAR_LEGS_4_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'war_legs_4.png')), ( 50, 50))
WAR_LEGS_5_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'war_legs_5.png')), ( 50, 50))
WAR_LEGS_6_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'war_legs_6.png')), ( 50, 50))
WAR_LEGS_7_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'war_legs_7.png')), ( 50, 50))

#Feet
WAR_FEET_1_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'war_feet_1.png')), ( 50, 50))
WAR_FEET_2_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'war_feet_2.png')), ( 50, 50))
WAR_FEET_3_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'war_feet_3.png')), ( 50, 50))
WAR_FEET_4_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'war_feet_4.png')), ( 50, 50))
WAR_FEET_5_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'war_feet_5.png')), ( 50, 50))
WAR_FEET_6_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'war_feet_6.png')), ( 50, 50))
WAR_FEET_7_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'war_feet_7.png')), ( 50, 50))

#Gloves
WAR_GLOVES_1_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'war_gloves_1.png')), ( 50, 50))
WAR_GLOVES_2_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'war_gloves_2.png')), ( 50, 50))
WAR_GLOVES_3_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'war_gloves_3.png')), ( 50, 50))
WAR_GLOVES_4_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'war_gloves_4.png')), ( 50, 50))
WAR_GLOVES_5_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'war_gloves_5.png')), ( 50, 50))
WAR_GLOVES_6_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'war_gloves_6.png')), ( 50, 50))
WAR_GLOVES_7_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'war_gloves_7.png')), ( 50, 50))
###

#Items
TEMPLATE_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'template_img.png')), ( 20, 20))
SOULGEM_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'soulgem.png')), ( 20, 20))
###

## Alex skill tree image ##

ENRAGED_REGEN_ICON_COLOR = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'enraged_regen.png')), ( 50, 50))
ENRAGED_REGEN_ICON_GRAY = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'enraged_regen_gray.png')), ( 50, 50))
MULTISTRIKE_ICON_COLOR = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'multistrike.png')), ( 50, 50))
MULTISTRIKE_ICON_GRAY = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'multistrike_gray.png')), ( 50, 50))
WARCRY_ICON_COLOR = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'warcry.png')), ( 50, 50))
WARCRY_ICON_GRAY = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'warcry_gray.png')), ( 50, 50))
ALEX_RIPOSTE_ICON_COLOR = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'riposte.png')), ( 50, 50))
ALEX_RIPOSTE_ICON_GRAY = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'riposte.png')), ( 50, 50))
ALEX_DMG_UP_ICON_COLOR = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'dmg_up.png')), ( 50, 50))
ALEX_ARMOR_UP_ICON_COLOR = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'armor_up.png')), ( 50, 50))
ALEX_HP_UP_ICON_COLOR = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'hp_up.png')), ( 50, 50))
ALEX_CRIT_UP_ICON_COLOR = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'crit_up.png')), ( 50, 50))
ALEX_DEF_ROLL_UP_ICON_COLOR = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'def_roll_up.png')), ( 50, 50))
ALEX_CRIT_DEF_ROLL_UP_ICON_COLOR = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'crit_def_roll_up.png')), ( 50, 50))

######################################
###### Battle screen emplacement ##### OLD
'''
FIRST_EMPLACEMENT_ALLY = ( 15, 75)
SECOND_EMPLACEMENT_ALLY = ( 15, 200)
THIRD_EMPLACEMENT_ALLY = ( 15, 325)
FOURTH_EMPLACEMENT_ALLY = ( 15, 450)

FIRST_EMPLACEMENT_ENY = ( 450, 75)
SECOND_EMPLACEMENT_ENY = ( 450, 200)
THIRD_EMPLACEMENT_ENY = ( 450, 325)
FOURTH_EMPLACEMENT_ENY = ( 450, 450)
'''
######################################
###### Battle screen emplacement #####

IN_BATTLE_BAND = pygame.Rect( 200, 0, 100, 18)

SKILL_BAND = pygame.Rect( 0, 475, 500, 125)
SKILL_TOP_LINE = pygame.Rect( 0, 474, 500, 1)

FIRST_EMPLACEMENT_ALLY = pygame.Rect( 10, 25, 160, 100)
FIRST_EMPLACEMENT_ALLY_LINING = pygame.Rect( 9, 24, 162, 102)
FIRST_EMPLACEMENT_ALLY_NAME_BACKGROUND = pygame.Rect( 15, 30, 150, 20)
FIRST_EMPLACEMENT_ALLY_HP_BACKGROUND = pygame.Rect( 19, 54, 142, 17)
FIRST_EMPLACEMENT_ALLY_MP_BACKGROUND = pygame.Rect( 19, 74, 142, 17)
FIRST_EMPLACEMENT_ALLY_SPECIAL_BACKGROUND = pygame.Rect ( 29, 94, 122, 17)
FIRST_EMPLACEMENT_ALLY_RAGE_1 = pygame.Rect( 30, 95, 20, 15)
FIRST_EMPLACEMENT_ALLY_RAGE_2 = pygame.Rect( 55, 95, 20, 15)
FIRST_EMPLACEMENT_ALLY_RAGE_3 = pygame.Rect( 80, 95, 20, 15)
FIRST_EMPLACEMENT_ALLY_RAGE_4 = pygame.Rect( 105, 95, 20, 15)
FIRST_EMPLACEMENT_ALLY_RAGE_5 = pygame.Rect( 130, 95, 20, 15)

SECOND_EMPLACEMENT_ALLY = pygame.Rect( 10, 135, 160, 100)
SECOND_EMPLACEMENT_ALLY_LINING = pygame.Rect( 9, 134, 162, 102)
SECOND_EMPLACEMENT_ALLY_NAME_BACKGROUND = pygame.Rect( 15, 140, 150, 20)
SECOND_EMPLACEMENT_ALLY_HP_BACKGROUND = pygame.Rect( 19, 164, 142, 17)
SECOND_EMPLACEMENT_ALLY_MP_BACKGROUND = pygame.Rect( 19, 184, 142, 17)

THIRD_EMPLACEMENT_ALLY = pygame.Rect( 10, 245, 160, 100)
THIRD_EMPLACEMENT_ALLY_LINING = pygame.Rect( 9, 244, 162, 102)
THIRD_EMPLACEMENT_ALLY_NAME_BACKGROUND = pygame.Rect( 15, 250, 150, 20)
THIRD_EMPLACEMENT_ALLY_HP_BACKGROUND = pygame.Rect( 19, 274, 142, 17)
THIRD_EMPLACEMENT_ALLY_MP_BACKGROUND = pygame.Rect( 19, 294, 142, 17)

FOURTH_EMPLACEMENT_ALLY = pygame.Rect( 10, 355, 160, 100)
FOURTH_EMPLACEMENT_ALLY_LINING = pygame.Rect( 9, 354, 162, 102)
FOURTH_EMPLACEMENT_ALLY_NAME_BACKGROUND = pygame.Rect( 15, 360, 150, 20)
FOURTH_EMPLACEMENT_ALLY_HP_BACKGROUND = pygame.Rect( 19, 384, 142, 17)
FOURTH_EMPLACEMENT_ALLY_MP_BACKGROUND = pygame.Rect( 19, 404, 142, 17)


FIRST_EMPLACEMENT_ENY = pygame.Rect( 330, 25, 160, 100)
FIRST_EMPLACEMENT_ENY_LINING = pygame.Rect( 329, 24, 162, 102)
FIRST_EMPLACEMENT_ENY_NAME_BACKGROUND = pygame.Rect( 335, 30, 150, 20)
FIRST_EMPLACEMENT_ENY_HP_BACKGROUND = pygame.Rect( 339, 54, 142, 17)
FIRST_EMPLACEMENT_ENY_MP_BACKGROUND = pygame.Rect( 339, 74, 142, 17)

SECOND_EMPLACEMENT_ENY = pygame.Rect( 330, 135, 160, 100)
SECOND_EMPLACEMENT_ENY_LINING = pygame.Rect( 329, 134, 162, 102)
SECOND_EMPLACEMENT_ENY_NAME_BACKGROUND = pygame.Rect( 335, 140, 150, 20)
SECOND_EMPLACEMENT_ENY_HP_BACKGROUND = pygame.Rect( 339, 164, 142, 17)
SECOND_EMPLACEMENT_ENY_MP_BACKGROUND = pygame.Rect( 339, 184, 142, 17)

THIRD_EMPLACEMENT_ENY = pygame.Rect( 330, 245, 160, 100)
THIRD_EMPLACEMENT_ENY_LINING = pygame.Rect( 329, 244, 162, 102)
THIRD_EMPLACEMENT_ENY_NAME_BACKGROUND = pygame.Rect( 335, 250, 150, 20)
THIRD_EMPLACEMENT_ENY_HP_BACKGROUND = pygame.Rect( 339, 274, 142, 17)
THIRD_EMPLACEMENT_ENY_MP_BACKGROUND = pygame.Rect( 339, 294, 142, 17)

FOURTH_EMPLACEMENT_ENY = pygame.Rect( 330, 355, 160, 100)
FOURTH_EMPLACEMENT_ENY_LINING = pygame.Rect( 329, 354, 162, 102)
FOURTH_EMPLACEMENT_ENY_NAME_BACKGROUND = pygame.Rect( 335, 360, 150, 20)
FOURTH_EMPLACEMENT_ENY_HP_BACKGROUND = pygame.Rect( 339, 384, 142, 17)
FOURTH_EMPLACEMENT_ENY_MP_BACKGROUND = pygame.Rect( 339, 404, 142, 17)

######################################
########## Buttons / Band ############


#General Buttons
GAME_NAME_BAND = pygame.Rect( 50, 25, 400, 60)
TOP_BAND = pygame.Rect( 50, 15, 400, 30)
TOP_LEFT_BAND = pygame.Rect( 10, 10, 100, 30)
TOP_RIGHT_BAND = pygame.Rect( 340, 10, 150, 30)
ABILITY_BAND = pygame.Rect( 0, 550, WIDTH, 50)
#

#Start Menu Buttons
NEW_GAME_BUTTON = pygame.Rect(175, 200, 150, 30)
LOAD_GAME_BUTTON = pygame.Rect(175, 300, 150, 30)
CREDITS_BUTTON = pygame.Rect(175, 400, 150, 30)
#

#Main Menu Buttons
FIGHT_BUTTON = pygame.Rect(175, 100, 150, 30)
SHOP_BUTTON = pygame.Rect(175, 200, 150, 30)
GO_HOME_BUTTON = pygame.Rect(175, 300, 150, 30)
TRAINING_GROUND_BUTTON = pygame.Rect(175, 400, 150, 30)
SAVE_BUTTON = pygame.Rect(175, 500, 150, 30)
#

#Shop Buttons
BUY_BUTTON = pygame.Rect(175, 100, 150, 30)
SELL_BUTTON = pygame.Rect(175, 200, 150, 30)
UPGRADE_BUTTON = pygame.Rect(175, 300, 150, 30)
#


#Buy Buttons
BUY_SWITCH_NUMBER_OF_STACKS_BUTTON = pygame.Rect( 440, 55, 45, 30)
BUY_PAGE_LEFT_BUTTON = pygame.Rect( 200, 80, 35, 25)
BUY_PAGE_RIGHT_BUTTON = pygame.Rect( 265, 80, 35, 25)
BUY_SWITCH_STORAGE_CONSUMABLE_BUTTON = pygame.Rect( 310, 80, 115, 25)

BUY_ITEM_NUM_ONE_BUTTON = pygame.Rect( 450, 120, 25, 25)
BUY_ITEM_NUM_TWO_BUTTON = pygame.Rect( 450, 160, 25, 25)
BUY_ITEM_NUM_THREE_BUTTON = pygame.Rect( 450, 200, 25, 25)
BUY_ITEM_NUM_FOUR_BUTTON = pygame.Rect( 450, 240, 25, 25)
BUY_ITEM_NUM_FIVE_BUTTON = pygame.Rect( 450, 280, 25, 25)
BUY_ITEM_NUM_SIX_BUTTON = pygame.Rect( 450, 320, 25, 25)
BUY_ITEM_NUM_SEVEN_BUTTON = pygame.Rect( 450, 360, 25, 25)
BUY_ITEM_NUM_EIGHT_BUTTON = pygame.Rect( 450, 400, 25, 25)
BUY_ITEM_NUM_NINE_BUTTON = pygame.Rect( 450, 440, 25, 25)
BUY_ITEM_NUM_TEN_BUTTON = pygame.Rect( 450, 480, 25, 25)

BUY_ITEM_NUM_ONE_BAND = pygame.Rect( 25, 120, 400, 25)
BUY_ITEM_NUM_TWO_BAND = pygame.Rect( 25, 160, 400, 25)
BUY_ITEM_NUM_THREE_BAND = pygame.Rect( 25, 200, 400, 25)
BUY_ITEM_NUM_FOUR_BAND = pygame.Rect( 25, 240, 400, 25)
BUY_ITEM_NUM_FIVE_BAND = pygame.Rect( 25, 280, 400, 25)
BUY_ITEM_NUM_SIX_BAND = pygame.Rect( 25, 320, 400, 25)
BUY_ITEM_NUM_SEVEN_BAND = pygame.Rect( 25, 360, 400, 25)
BUY_ITEM_NUM_EIGHT_BAND = pygame.Rect( 25, 400, 400, 25)
BUY_ITEM_NUM_NINE_BAND = pygame.Rect( 25, 440, 400, 25)
BUY_ITEM_NUM_TEN_BAND = pygame.Rect( 25, 480, 400, 25)
#

#Loot Buttons
LOOT_PAGE_LEFT_BUTTON = pygame.Rect( 200, 70, 35, 25)
LOOT_PAGE_RIGHT_BUTTON = pygame.Rect( 265, 70, 35, 25)

LOOT_ITEM_NUM_ONE_BAND = pygame.Rect( 50, 120, 400, 25)
LOOT_ITEM_NUM_TWO_BAND = pygame.Rect( 50, 160, 400, 25)
LOOT_ITEM_NUM_THREE_BAND = pygame.Rect( 50, 200, 400, 25)
LOOT_ITEM_NUM_FOUR_BAND = pygame.Rect( 50, 240, 400, 25)
LOOT_ITEM_NUM_FIVE_BAND = pygame.Rect( 50, 280, 400, 25)
LOOT_ITEM_NUM_SIX_BAND = pygame.Rect( 50, 320, 400, 25)
LOOT_ITEM_NUM_SEVEN_BAND = pygame.Rect( 50, 360, 400, 25)
LOOT_ITEM_NUM_EIGHT_BAND = pygame.Rect( 50, 400, 400, 25)
LOOT_ITEM_NUM_NINE_BAND = pygame.Rect( 50, 440, 400, 25)
LOOT_ITEM_NUM_TEN_BAND = pygame.Rect( 50, 480, 400, 25)
#

#Upgrade Buttons
HELMET_UPGRADE_BUTTON = pygame.Rect(225, 150, 50, 50)
CHEST_UPGRADE_BUTTON = pygame.Rect(225, 225, 50, 50)
LEGS_UPGRADE_BUTTON = pygame.Rect(225, 300, 50, 50)
FEET_UPGRADE_BUTTON = pygame.Rect(225, 375, 50, 50)
GLOVES_UPGRADE_BUTTON = pygame.Rect(150, 225, 50, 50)
WEAPON_MAIN_HAND_UPGRADE_BUTTON = pygame.Rect(150, 300, 50, 50)
WEAPON_OFF_HAND_UPGRADE_BUTTON = pygame.Rect(300, 300, 50, 50)
WEAPON_TWO_HANDED_UPGRADE_BUTTON = pygame.Rect(300, 225, 50, 50)
UPGRADE_DESCRIPTION_BAND = pygame.Rect(0, 480, WIDTH, 120)
#

#Home Buttons
CHECK_PARTY_BUTTON = pygame.Rect(175, 100, 150, 30)
CHECK_INVENTORY_BUTTON = pygame.Rect(175, 200, 150, 30)
REST_BUTTON = pygame.Rect(175, 300, 150, 30)
MANAGE_TEAM_BUTTON = pygame.Rect(175, 400, 150, 30)
GODDESS_BUTTON = pygame.Rect(175, 500, 150, 30)
#

#Goddess Buttons
GODDESS_LEVEL_UP_BUTTON = pygame.Rect(175, 100, 150, 30)
GODDESS_SKILL_BUTTON = pygame.Rect(175, 200, 150, 30)
GODDESS_BLESSING_BUTTON = pygame.Rect(175, 300, 150, 30)

OFFERING_CONVERT_SOUL_BUTTON = pygame.Rect(350, 80, 55, 30)

OFFERING_FIRST_BUTTON = pygame.Rect(225, 275, 50, 50)
#

#Check Party Buttons
FIRST_MEMBER_BUTTON = pygame.Rect(410, 95, 40, 40)
SECOND_MEMBER_BUTTON = pygame.Rect(410, 205, 40, 40)
THIRD_MEMBER_BUTTON = pygame.Rect(410, 320, 40, 40)
FOURTH_MEMBER_BUTTON = pygame.Rect(410, 435, 40, 40)
#

#Character Sheet Buttons
UPPER_LEFT_ARROW_BUTTON = pygame.Rect(5, 3, 35, 25)
UPPER_RIGHT_ARROW_BUTTON = pygame.Rect(WIDTH - 40, 3, 35, 25)
LOWER_LEFT_ARROW_BUTTON = pygame.Rect(165, 565, 35, 25)
LOWER_RIGHT_ARROW_BUTTON = pygame.Rect(300, 565, 35, 25)
STATS_COLUMN_BUTTON = pygame.Rect( 0, 30, 125, 30)
SKILL_COLUMN_BUTTON = pygame.Rect( 125, 30, 125, 30)
TITLE_COLUMN_BUTTON = pygame.Rect( 250, 30, 125, 30)
RECORDS_COLUMN_BUTTON = pygame.Rect( 375, 30, 125, 30)
FIRST_COLUMN_SEPARATOR = pygame.Rect( 124, 30, 3, 30)
SECOND_COLUMN_SEPARATOR = pygame.Rect( 249, 30, 3, 30)
THIRD_COLUMN_SEPARATOR = pygame.Rect( 374, 30, 3, 30)
#

#Update Status Buttons
YES_LVL_UP_BUTTON = pygame.Rect(125, 400, 75, 30)
NO_LVL_UP_BUTTON = pygame.Rect(300, 400, 75, 30)
#

#Manage Team Buttons
ALLY_BAND = pygame.Rect(50, 100, 100, 30)
PARTY_BAND = pygame.Rect(350, 100, 100, 30)

ARROW_UP_BUTTON = pygame.Rect(WIDTH//2 - 15, 200, 30, 30)
ARROW_DOWN_BUTTON = pygame.Rect(WIDTH//2 - 15, 250, 30, 30)
ADD_BUTTON = pygame.Rect(WIDTH//2 - 85//2, 350, 85, 30)
REMOVE_BUTTON = pygame.Rect(WIDTH//2 - 85//2, 400, 85, 30)
#

#Mastery Tree Buttons
FIRST_ROW_MIDDLE_ABILITY_BUTTON = pygame.Rect(WIDTH//2 - 25, 75, 50, 50)
SECOND_ROW_LEFT_ABILITY_BUTTON = pygame.Rect(WIDTH//3 - 25, 150, 50, 50)
SECOND_ROW_MIDDLE_ABILITY_BUTTON = pygame.Rect(WIDTH//2 - 25, 150, 50, 50)
SECOND_ROW_RIGHT_ABILITY_BUTTON = pygame.Rect(WIDTH//3 * 2 - 25, 150, 50, 50)
THIRD_ROW_LEFT_ABILITY_BUTTON = pygame.Rect(WIDTH//3 - 25, 225, 50, 50)
THIRD_ROW_MIDDLE_ABILITY_BUTTON = pygame.Rect(WIDTH//2 - 25, 225, 50, 50)
THIRD_ROW_RIGHT_ABILITY_BUTTON = pygame.Rect(WIDTH//3 * 2 - 25, 225, 50, 50)
FOURTH_ROW_LEFT_ABILITY_BUTTON = pygame.Rect(WIDTH//3 - 25, 300, 50, 50)
FOURTH_ROW_MIDDLE_ABILITY_BUTTON = pygame.Rect(WIDTH//2 - 25, 300, 50, 50)
FOURTH_ROW_RIGHT_ABILITY_BUTTON = pygame.Rect(WIDTH//3 * 2 - 25, 300, 50, 50)
FIFTH_ROW_LEFT_ABILITY_BUTTON = pygame.Rect(WIDTH//3 - 25, 375, 50, 50)
FIFTH_ROW_MIDDLE_ABILITY_BUTTON = pygame.Rect(WIDTH//2 - 25, 375, 50, 50)
FIFTH_ROW_RIGHT_ABILITY_BUTTON = pygame.Rect(WIDTH//3 * 2 - 25, 375, 50, 50)
SIXTH_ROW_LEFT_ABILITY_BUTTON = pygame.Rect(WIDTH//3 - 25, 450, 50, 50)
SIXTH_ROW_MIDDLE_ABILITY_BUTTON = pygame.Rect(WIDTH//2 - 25, 450, 50, 50)
SIXTH_ROW_RIGHT_ABILITY_BUTTON = pygame.Rect(WIDTH//3 * 2 - 25, 450, 50, 50)

DESCRIPTION_BAND = pygame.Rect(0, 520, WIDTH, 80)
#

#Floor Selection Buttons
FIRST_FLOOR_BUTTON = pygame.Rect( 175, 100, 150, 30)
SECOND_FLOOR_BUTTON = pygame.Rect( 175, 200, 150, 30)
THIRD_FLOOR_BUTTON = pygame.Rect( 175, 300, 150, 30)
FOURTH_FLOOR_BUTTON = pygame.Rect( 175, 400, 150, 30)
FIFTH_FLOOR_BUTTON = pygame.Rect( 175, 500, 150, 30)
#

#Dungeon Buttons
DUNGEON_CHECK_PARTY_BUTTON = pygame.Rect( 445, 215, 50, 50)
DUNGEON_USE_CONSUMABLES_BUTTON = pygame.Rect( 445, 275, 50, 50)
DUNGEON_CHECK_LOOT_BUTTON = pygame.Rect( 445, 335, 50, 50)
DUNGEON_EXPLORE_BUTTON = pygame.Rect( 75, 490, 125, 30)
DUNGEON_FARM_BUTTON = pygame.Rect( 300, 490, 125, 30)
DUNGEON_NEXT_FLOOR_BUTTON = pygame.Rect( 75, 550, 125, 30)
DUNGEON_RETURN_BUTTON = pygame.Rect( 300, 550, 125, 30)
DUNGEON_BOTTOM_BAND = pygame.Rect( 0, 470, WIDTH, 130)
#

#Pre Battle Buttons
PRE_BATTLE_FIGHT_BUTTON = pygame.Rect( 75, 490, 125, 30)
PRE_BATTLE_AMBUSH_BUTTON = pygame.Rect( 75, 550, 125, 30)
PRE_BATTLE_FLEE_BUTTON = pygame.Rect( 300, 490, 125, 30)
PRE_BATTLE_AVOID_BUTTON = pygame.Rect( 300, 550, 125, 30)
PRE_BATTLE_BOTTOM_BAND = pygame.Rect( 0, 470, WIDTH, 130)
#

#Choose Consumable
CONSUMABLE_EMPLACEMENT_ONE = pygame.Rect( 80, 100, 42, 42)
CONSUMABLE_EMPLACEMENT_TWO = pygame.Rect( 180, 100, 42, 42)
CONSUMABLE_EMPLACEMENT_THREE = pygame.Rect( 280, 100, 42, 42)
CONSUMABLE_EMPLACEMENT_FOUR = pygame.Rect( 380, 100, 42, 42)
CONSUMABLE_EMPLACEMENT_FIVE = pygame.Rect( 80, 200, 42, 42)
CONSUMABLE_EMPLACEMENT_SIX = pygame.Rect( 180, 200, 42, 42)
CONSUMABLE_EMPLACEMENT_SEVEN = pygame.Rect( 280, 200, 42, 42)
CONSUMABLE_EMPLACEMENT_EIGHT = pygame.Rect( 380, 200, 42, 42)
CONSUMABLE_EMPLACEMENT_NINE = pygame.Rect( 80, 300, 42, 42)
CONSUMABLE_EMPLACEMENT_TEN = pygame.Rect( 180, 300, 42, 42)
CONSUMABLE_EMPLACEMENT_ELEVEN = pygame.Rect( 280, 300, 42, 42)
CONSUMABLE_EMPLACEMENT_TWELVE = pygame.Rect( 380, 300, 42, 42)
CONSUMABLE_EMPLACEMENT_THIRTEEN = pygame.Rect( 80, 400, 42, 42)
CONSUMABLE_EMPLACEMENT_FOURTEEN = pygame.Rect( 180, 400, 42, 42)
CONSUMABLE_EMPLACEMENT_FIFTEEN = pygame.Rect( 280, 400, 42, 42)
CONSUMABLE_EMPLACEMENT_SIXTEEN = pygame.Rect( 380, 400, 42, 42)
#

#Use Consumable
FIRST_PARTY_MEMBER_BUTTON = pygame.Rect( 40, 100, 250, 85)
SECOND_PARTY_MEMBER_BUTTON = pygame.Rect( 40, 200, 250, 85)
THIRD_PARTY_MEMBER_BUTTON = pygame.Rect( 40, 300, 250, 85)
FOURTH_PARTY_MEMBER_BUTTON = pygame.Rect( 40, 400, 250, 85)
#

#Back Buttons
BACK_BUTTON = pygame.Rect( 400, 540, 75, 30)
BACK_BUTTON_BIS = pygame.Rect( 400, 480, 75, 30)
BACK_BUTTON_BIS_2 = pygame.Rect( 400, 440, 75, 30)
BACK_BUTTON_MIDDLE = pygame.Rect( 210, 565, 80, 30)
BACK_BUTTON_TOP = pygame.Rect( 15, 55, 75, 30)
#


######################
####### Spells #######

def skill_list_reset():
	fighting.playing.skill_list = []

def skill_checker():
	for skill in fighting.playing.learned_skill:
		skill()

######

def can_dark_sphere(user):
	if user.mp >= 6:
		user.skill_list.append(dark_sphere)

def dark_sphere(user):
	dark_sphere_data = "single target"
	user.casting_skill = dark_sphere_use
	return dark_sphere_data

def dark_sphere_use(user,target):
	user.mp -= 6
	crit_multiplier = 1
	ability_string = (f"{user.name} uses Dark Sphere")
	ability_announcer_screen_draw(ability_string)
	crit = is_critical(user)
	if crit == True:
		crit_multiplier = 2
	def_roll = defensive_roll(target)
	if def_roll == 0:
		dodge_screen_draw(target)
	else:
		if def_roll == 0.2:
			parry_screen_draw(target)
		final_dmg = int(( user.magic_dmg * 8 * crit_multiplier - target.armor ) * def_roll)
		if final_dmg < 0:
			final_dmg = 1
		target.hp -= final_dmg
		no_hp_under(target)
		dmg_announcer_screen_draw(target,final_dmg,crit_multiplier)
	claim_kill(user,target)

###

def can_fireball(user):
	if user.mp >= 5:
		user.skill_list.append(fireball)

def fireball(user):
	fireball_data = "single target"
	user.casting_skill = fireball_use
	return fireball_data

def fireball_use(user,target):
	user.mp -= 5
	crit_multiplier = 1
	ability_string = (f"{user.name} uses Fireball !")
	ability_announcer_screen_draw(ability_string)
	crit = is_critical(user)
	if crit == True:
		crit_multiplier = 2
	def_roll = defensive_roll(target)
	if def_roll == 0:
		print(f"{target.name} dodged the fire ball !")
		dodge_screen_draw(target)
	else:
		if def_roll == 0.2:
			print(f"{target.name} parried the fire ball !")
			parry_screen_draw(target)
		final_dmg = int(( user.magic_dmg * 5 * crit_multiplier - target.armor ) * def_roll)
		if final_dmg < 0:
			final_dmg = 1
		target.hp -= final_dmg
		no_hp_under(target)
		dmg_announcer_screen_draw(target,final_dmg,crit_multiplier)
		dmg_announcer(target,final_dmg)
	claim_kill(user,target)

###

def can_icelance(user):
	if user.mp >= 1:
		user.skill_list.append(icelance)

def icelance(user):
	icelance_data = "single target"
	user.casting_skill = icelance_use
	return icelance_data

def icelance_use(user,target):
	user.mp -= 1
	crit_multiplier = 1
	ability_string = (f"{user.name} uses Icelance !")
	ability_announcer_screen_draw(ability_string)
	crit = is_critical(user)
	if crit == True:
		crit_multiplier = 3
	def_roll = defensive_roll(target)
	if def_roll == 0:
		print(f"{target.name} dodged the frozen spear !")
		dodge_screen_draw(target)
	else:
		if def_roll == 0.2:
			print(f"{target.name} parried the frozen spear !")
			parry_screen_draw(target)
		final_dmg = int(( user.magic_dmg * crit_multiplier - target.armor ) * def_roll)
		if final_dmg < 0:
			final_dmg = 1
		target.hp -= final_dmg
		no_hp_under(target)
		dmg_announcer_screen_draw(target,final_dmg,crit_multiplier)
		dmg_announcer(target,final_dmg)
	claim_kill(user,target)

###

def can_warcry():
	if fighting.playing.warcry_cd <= fighting.playing.global_turn_count:
		fighting.playing.skill_list.append(warcry)

def warcry():
	generate_skill_description("Warcry", f"{fighting.playing.name} unleash a Warcry boosting his DMG !")
	generate_skill_icon(WARCRY_ICON_COLOR)
	fighting.playing.warcry_cd = fighting.playing.global_turn_count + 10

	power = int(fighting.playing.dmg * 3 - fighting.playing.dmg)
	fighting.playing.dmg = int(fighting.playing.dmg * 3)
	fighting.playing.rage -= 100

	effect_warcry = {"name" : "Warcry", "icon" : WARCRY_ICON_COLOR, "end" : fighting.playing.global_turn_count + 5, "ticks" : False, "type" : "buff", "sub_type" : "dmg", "scope" : "self", "power" : power}
	fighting.playing.effects.append(effect_warcry)
	warcry_sfx.play()
	warcry_sfx.set_volume(0.5)

###

def enraged_regeneration(user):
	power = int(user.max_hp * 0.05)
	effect_enraged_regen = {"name" : "Enraged Regeneration", "icon" : ENRAGED_REGEN_ICON_COLOR, "description" : f"{user.name} regenerate {power} hp.", "end" : user.global_turn_count + 99999, "ticks" : True, "in_combat" : True, "type" : "regen", "sub_type" : "hp", "scope" : "self", "power" : power}
	user.effects.append(effect_enraged_regen)

###

def can_triple_shining_arrow(user):
	if user.mp >= 5 and user.triple_shining_arrow_cd <= user.global_turn_count:
		user.skill_list.append(triple_shining_arrow)

def triple_shining_arrow(user,eny):
	user.mp -= 5
	ability_string = f"{user.name} use Triple Shining Arrow"
	ability_announcer_screen_draw(ability_string)
	user.triple_shining_arrow_cd = user.global_turn_count + 3
	count = 1
	target_list = []
	dmg_list = []
	crit_multiplier_list = []
	def_roll_list = []
	while count <= 3:
		count += 1
		target = rand.choice(eny)
		crit_multiplier = 1
		def_roll = 1
		crit = is_critical(user)
		if crit == True:
			crit_multiplier = 3
		def_roll = defensive_roll(target)
		if def_roll == 0:
			print(f"{target.name} dodged the arrow !")
			final_dmg = 0
		else:
			if def_roll == 0.2:
				print(f"{target.name} parried the strike !")
			final_dmg = int(( user.dmg * 1 * crit_multiplier - target.armor ) * def_roll)
			if final_dmg < 0:
				final_dmg = 1
			target.hp -= final_dmg
			no_hp_under(target)
		target_list.append(target)
		dmg_list.append(final_dmg)
		crit_multiplier_list.append(crit_multiplier)
		def_roll_list.append(def_roll)
	dmg_announcer_screen_draw_multiple(target_list,dmg_list,crit_multiplier_list,def_roll_list)
	dmg_announcer(target,final_dmg)

###

def can_multistrike():
	if fighting.playing.mp >= 5 and fighting.playing.multistrike_cd <= fighting.playing.global_turn_count:
		fighting.playing.skill_list.append(multistrike)

def multistrike():
	fighting.playing.mp -= 5
	fighting.playing.multistrike_cd = fighting.playing.global_turn_count + 5
	generate_skill_description("Multistrike (Skill)", f"{fighting.playing.name} attacks every enemy in sight !")
	generate_skill_icon(MULTISTRIKE_ICON_COLOR)
	multistrike_sfx.play()
	multistrike_sfx.set_volume(0.5)

	for target in enemy_party.enemy_alive:
		crit_multiplier = 1
		def_roll = 1

		crit = is_critical(fighting.playing)
		if crit == True:
			crit_multiplier = 2

		def_roll = defensive_roll(target)
		if def_roll == 0:
			generate_dodge_animation(target,0)
		else:
			final_dmg = int(( fighting.playing.dmg * 3 * crit_multiplier - target.armor ) * def_roll)
			if final_dmg < 0:
				final_dmg = 1
			if def_roll == 0.2:
				generate_parry_animation(target,final_dmg)
			else:
				if crit:
					generate_crit_dmg_animation(target,final_dmg)
				else:
					generate_dmg_animation(target,final_dmg)
			target.hp -= final_dmg
			no_hp_under(target)

		claim_kill(fighting.playing,target)

###

def attack():
	crit_multiplier = 1

	if fighting.playing.friendly:	#target acquisition
		target = rand.choice(enemy_party.enemy_alive)
		fighting.target.append(target)
	else:
		target = rand.choice(party.party_alive)
		fighting.target.append(target)

	defender_animation(target)

	crit = is_critical(fighting.playing)

		#special ressource management
	if fighting.playing.special_ressource == "rage":
		if crit == True:
			fighting.playing.rage += 40
		else:
			fighting.playing.rage += 20
		if fighting.playing.rage > 100:
			fighting.playing.rage = 100

	if crit == True:
		crit_multiplier = 2

	#Defensive Roll Outcome
	def_roll = defensive_roll(target)
	if def_roll == 0: #crit def roll
		if target.riposte == True: #riposte
			final_dmg = int(( target.dmg * target.riposte_strength ) - fighting.playing.armor)
			fighting.playing.hp -= final_dmg
			if final_dmg < 0:
				final_dmg = 1
			no_hp_under(fighting.playing)
			generate_riposte_animation(target,final_dmg)
			generate_skill_description("Attack (Riposte)",f"{target.name} countered {fighting.playing.name} attack, dealing {final_dmg} dmg.")
			claim_kill(target,fighting.playing)
		else: #dodge
			dodge_sfx.play()
			dodge_sfx.set_volume(0.5)
			generate_dodge_animation(target,0)
			generate_skill_description("Attack (Dodged)",f"{target.name} dodged {fighting.playing.name} attack.")

	else: #regular def roll
		final_dmg = int(( fighting.playing.dmg * crit_multiplier - target.armor ) * def_roll)
		if final_dmg < 0:
			final_dmg = 1

		if def_roll == 0.2: #parry
			parry_attack_sfx.play()
			parry_attack_sfx.set_volume(0.5)
			generate_parry_animation(target,final_dmg)
			generate_skill_description("Attack (Parried)",f"{target.name} parries {fighting.playing.name} attacks but still took {final_dmg} dmg.")
		else: #failed def roll
			if crit:
				crit_attack_sfx.play()
				crit_attack_sfx.set_volume(0.5)
				generate_crit_dmg_animation(target,final_dmg)
				generate_skill_description("Attack (Critical)",f"{fighting.playing.name} deals {final_dmg} dmg to {target.name} !")
			else:
				attack_sfx.play()
				attack_sfx.set_volume(0.5)
				generate_dmg_animation(target,final_dmg)
				generate_skill_description("Attack",f"{fighting.playing.name} deals {final_dmg} dmg to {target.name}.")

		target.hp -= final_dmg
		no_hp_under(target)

	claim_kill(fighting.playing,target)

#####################
##### Inventory #####

class party_inventory:
	town_gold = 0
	town_storage = {}
	consumable = {}
	max_consumable = 16
	dungeon_consumable = {1 : "Small Health Potion", 2 : "Small Health Potion", 3 : "Large Mana Potion", 4 : "Large Health Potion", 5 : "Small Health Potion", 10 : "Small Health Potion", 11 : "Medium Health Potion", 12 : "Small Mana Potion", 15 : "Large Health Potion", 9 : "Small Mana Potion", }

	dungeon_gold = 0
	dungeon_loot = {}

	battle_loot = {}
	battle_gold = 0

	xp_per_ally = 0
	mastery_per_ally = 0

##########################
##### Allies Classes #####

################
##### Alex #####

class Alex_stats:
	name = "Alex"
	emplacement = 1
	xp = 0
	mastery = 0

	level = 1
	base_max_hp = 100
	bonus_max_hp = 0
	max_hp = 100
	hp = 100
	base_max_mp = 5
	bonus_max_mp = 0
	max_mp = 5
	mp = 5
	special_ressource = "rage"
	max_rage = 100
	rage = 0

	base_armor = 5
	bonus_armor = 0
	armor = 5
	resistance = 10
	base_dmg = 20
	bonus_dmg = 0
	bonus_dmg_multiplier = 1
	dmg = 20
	magic_dmg = 10

	crit_chance_base = 20
	crit_chance_bonus = 0
	crit_chance = 20
	defensive_roll_base = 20
	defensive_roll_bonus = 0
	defensive_roll_chance = 20
	crit_defensive_roll_base = 10
	crit_defensive_roll_bonus = 0
	crit_defensive_roll_chance = 10
	riposte = True
	riposte_strength_base = 1
	riposte_strength_bonus = 0
	riposte_strength = 1

	speed_base = 12
	speed_bonus = 0
	speed = 12

	intimidation = 2
	sneak = 10
	stress = 0
	moral = 80

	dead = False
	friendly = True

	global_turn_count = 0
	turn_count = 0
	effects = []
	skill_list = []
	casting_skill = None
	learned_skill = []
	learned_skill_name = []
	passive_skill = []
	passive_skill_name = []
	skills_description = {}
	warcry_cd = 0
	multistrike_cd = 0

	phrase_crit = ["Take this !", "Stay down !", "Give 'em hell !"]

	def behaviour(self):
		if self.skill_list == []:
			self.casting_skill = attack
		elif (warcry in self.skill_list) and self.rage == 100:
			self.casting_skill = warcry
		elif (multistrike in self.skill_list) and enemy_party.number_of_enemy_alive > 2:
			self.casting_skill = multistrike
		else:
			self.casting_skill = attack

#Mastery Tree related

	first_row_middle_passive = False

	second_row_left_passive = False
	second_row_middle_passive = False
	second_row_right_passive = False

	third_row_left_passive = False
	third_row_middle_passive = False
	third_row_right_passive = False

	fourth_row_left_passive = False
	fourth_row_middle_passive = False
	fourth_row_right_passive = False

	fifth_row_left_passive = False
	fifth_row_middle_passive = False
	fifth_row_right_passive = False

	sixth_row_left_passive = False
	sixth_row_middle_passive = False
	sixth_row_right_passive = False

### Mastery Tree Descriptions ###

	first_row_middle_passive_name = "Enraged Regeneration (Passive Skill)"
	first_row_middle_passive_description = "Grant 5% max hp regen per turn while in combat"
	first_row_middle_passive_icon = ENRAGED_REGEN_ICON_COLOR
	first_row_middle_passive_icon_gray = ENRAGED_REGEN_ICON_GRAY

	second_row_left_passive_name = "Dmg Up"
	second_row_left_passive_description = "Increase dmg by 50 (scale with levels)"
	second_row_left_passive_icon = ALEX_DMG_UP_ICON_COLOR
	second_row_left_passive_icon_gray = ALEX_DMG_UP_ICON_COLOR
	second_row_middle_passive_name =  "Armor Up"
	second_row_middle_passive_description = "Increase armor by 10 (scale with levels)"
	second_row_middle_passive_icon = ALEX_ARMOR_UP_ICON_COLOR
	second_row_middle_passive_icon_gray = ALEX_ARMOR_UP_ICON_COLOR
	second_row_right_passive_name = "Hp Up"
	second_row_right_passive_description = "Increase max hp by 200 (scale with levels)"
	second_row_right_passive_icon = ALEX_HP_UP_ICON_COLOR
	second_row_right_passive_icon_gray = ALEX_HP_UP_ICON_COLOR

	third_row_left_passive_name = "Multistrike (Active Skill)"
	third_row_left_passive_description = "A skill that strike every enemy once"
	third_row_left_passive_icon = MULTISTRIKE_ICON_COLOR
	third_row_left_passive_icon_gray = MULTISTRIKE_ICON_GRAY
	third_row_middle_passive_name = "Riposte (Passive Skill)"
	third_row_middle_passive_description = "Convert dodges into attacks"
	third_row_middle_passive_icon = ALEX_RIPOSTE_ICON_COLOR
	third_row_middle_passive_icon_gray = ALEX_RIPOSTE_ICON_GRAY
	third_row_right_passive_name = "Defensive Roll Boost"
	third_row_right_passive_description = "Increase by 20% the success rate of a defensive roll"
	third_row_right_passive_icon = ALEX_DEF_ROLL_UP_ICON_COLOR
	third_row_right_passive_icon_gray = ALEX_DEF_ROLL_UP_ICON_COLOR

	fourth_row_left_passive_name = "Critical Chance Up"
	fourth_row_left_passive_description = "Increase by 30% the performance rate of a critical strike"
	fourth_row_left_passive_icon = ALEX_CRIT_UP_ICON_COLOR
	fourth_row_left_passive_icon_gray = ALEX_CRIT_UP_ICON_COLOR
	fourth_row_middle_passive_name = "Warcry (Active Skill)"
	fourth_row_middle_passive_description = "If at full rage, boost dmg 3x for 5turn"
	fourth_row_middle_passive_icon = WARCRY_ICON_COLOR
	fourth_row_middle_passive_icon_gray = WARCRY_ICON_GRAY
	fourth_row_right_passive_name = "Critical Defensive Roll Boost"
	fourth_row_right_passive_description = "Increase by 10% the success rate of a crit defensive roll"
	fourth_row_right_passive_icon = ALEX_CRIT_DEF_ROLL_UP_ICON_COLOR
	fourth_row_right_passive_icon_gray = ALEX_CRIT_DEF_ROLL_UP_ICON_COLOR

### Equipment Upgrade ###

	armor_type = "Warrior"
	weapon_type = "Two Handed Sword"
	two_handed = True
	weapon = "sword"
	weapon_tier = 0
	helmet_tier = 0
	chest_tier = 0
	legs_tier = 0
	feet_tier = 0
	gloves_tier = 0


### Statistics Tracker ###

	enemy_killed = 0
	dmg_taken = 0
	dmg_inflicted = 0
	goblin_killed = 0
	hobgoblin_killed = 0
	turn_survived_with_10percent_hp = 0
	turn_survived_with_10percent_hp_tracker = 0

### Title Tracker ###

	killer = False			#10 kills
	killer_effect = "(+ 5% DMG)"
	slaughterer = False		#100 kills
	slaughterer_effect = "(+ 5% DMG)"

	survivor = False		#survived 3 consecutive turn with less than 15% hp

	goblin_killer = False	#10 goblin kills
	goblin_bane = False		#100 goblin kills

	hobgoblin_killer = False	#10 hobgoblin kills
	hobgoblin_bane = False		#100 hobgoblin kills
#

###############
### Emeline ###

class Emeline_stats:
	name = "Emeline"
	emplacement = 2
	level = 1
	xp = 0
	mastery = 0
	max_hp = 70
	hp = 70
	max_mp = 20
	mp = 20
	special_ressource = None
	armor = 0
	resistance = 5
	dmg = 10
	magic_dmg = 30

	crit_chance = 10
	defensive_roll_chance = 5
	crit_defensive_roll_chance = 1
	riposte = False
	riposte_strength = 0.75

	speed = 10
	stress = 0
	moral = 80
	dead = False
	friendly = True
	turn_count = 0
	effects = []
	skill_list = []
	casting_skill = None
	learned_skill = [can_icelance, can_fireball]
	learned_skill_name = ["Icelance", "Fireball"]
	passive_skill = []
	passive_skill_name = []
	skills_description = {}
	phrase_crit = ["Serves you right.", "How does it feel ?"]
#

##############
### Azazel ###

class Azazel_stats:
	name = "Azazel"
	emplacement = 3
	level = 1
	xp = 0
	mastery = 0
	max_hp = 70
	hp = 70
	max_mp = 25
	mp = 25
	special_ressource = None
	armor = 0
	resistance = 10
	dmg = 10
	magic_dmg = 20

	crit_chance = 20
	defensive_roll_chance = 5
	crit_defensive_roll_chance = 0
	riposte = False

	speed = 9
	stress = 0
	moral = 80
	dead = False
	friendly = True
	turn_count = 0
	effects = []
	skill_list = []
	casting_skill = None
	learned_skill = [can_dark_sphere]
	learned_skill_name = ["Dark Sphere"]
	passive_skill = []
	passive_skill_name = []
	skills_description = {}
	phrase_crit = ["Take this !", "Stay down !", "Give 'em hell !"]
#

###############
### Ezekiel ###

class Ezekiel_stats:
	name = "Ezekiel"
	emplacement = 4
	level = 1
	xp = 0
	mastery = 0
	max_hp = 80
	hp = 80
	max_mp = 10
	mp = 10
	special_ressource = None
	armor = 2
	resistance = 7
	dmg = 25
	magic_dmg = 5

	crit_chance = 50
	defensive_roll_chance = 20
	crit_defensive_roll_chance = 15
	riposte = True
	riposte_strength = 2

	speed = 15
	stress = 0
	moral = 80
	dead = False
	friendly = True
	turn_count = 0
	effects = []
	skill_list = []
	casting_skill = None
	learned_skill = [can_triple_shining_arrow]
	learned_skill_name = ["Triple Shining Arrow"]
	passive_skill = []
	passive_skill_name = []
	skills_description = {}
	triple_shining_arrow_cd = 0
	phrase_crit = ["Take this !", "Stay down !", "Give 'em hell !"]
#

###############################
##### Party Related Class #####

class party_base:
	available_ally = []
	number_of_ally = 0
	number_of_ally_alive = 0
	party = []
	party_alive = []
	party_dead = []


##############################
##### Monster Classes #####

class goblin:
	def __init__(self,name):
		self.name = "Goblin " + str(name)
	emplacement = None
	specie = "goblin"
	max_hp = 30
	hp = max_hp
	max_mp = 5
	mp = 5
	dmg = 10
	special_ressource = None

	crit_chance = 10
	defensive_roll_chance = 5
	crit_defensive_roll_chance = 1
	riposte = False

	armor = 0
	speed = 5
	moral = 80
	dead = False
	friendly = False
	turn_count = 0
	effects = []
	skill_list = []
	casting_skill = None
	learned_skill = []
	passive_skill = []
	xp = 5
	mastery_xp = 25
	gold = 10
	soul = "Goblin's Soulgem"
	loot_table = ["Goblin's ear jewel"]
	last_attacked_by = None
	killed_by = None

class hobgoblin:
	def __init__(self,name):
		self.name = "Hobgoblin " + str(name)
	emplacement = None
	specie = "hobgoblin"
	max_hp = 75
	hp = max_hp
	max_mp = 5
	mp = 5
	dmg = 20
	special_ressource = None

	crit_chance = 10
	defensive_roll_chance = 10
	crit_defensive_roll_chance = 5
	riposte = False

	armor = 2
	speed = 8
	moral = 80
	dead = False
	friendly = False
	turn_count = 0
	effects = []
	skill_list = []
	casting_skill = None
	learned_skill = []
	passive_skill = []
	xp = 25
	mastery_xp = 125
	gold = 20
	soul = "Hobgoblin's Soulgem"
	loot_table = ["Hobgoblin's nose ring"]


class monsterpedia_base:
	floor_1 = [goblin]
	floor_2 = [goblin,hobgoblin]
	floor_3 = [hobgoblin]

#####################################
##### Enemy Party Related Class #####

class enemy_party_base:
	number_of_enemy = 0
	number_of_enemy_alive = 0
	enemy_list = []
	enemy_dead = []
	enemy_alive = []

##############################
##### Statistics #####

class statistics_base:
    kill_count = [{ "name" : "goblin" , "count" : 0 }, { "name" : "hobgoblin" , "count" : 0 }]
    gold_earned = 0
    dmg_taken = 0
    dmg_inflicted = 0


##############################
##### Achievement #####

class achievement_base:
	goblin_slayer = { "title" : "Goblin Slayer" , "name" : "goblin" , "earned" : False , "counter_goal" : 10 , "bonus" : 0.5 , "description" : "You know where to strike to inflict accrued damages on goblins" }
	hobgoblin_slayer = { "title" : "Hobgoblin Slayer" , "name" : "hobgoblin" , "earned" : False , "counter_goal" : 10 , "bonus" : 0.5 , "description" : "You know where to strike to inflict accrued damages on hobgoblins"}


##############################
##### Shop #####

class shop_database:
	page_1_item_1_name = "Small Health Potion"
	page_1_item_1_cost = 50
	page_1_item_1_icon = BUY_SMALL_HEALTH_POTION_IMAGE
	page_1_item_2_name = "Medium Health Potion"
	page_1_item_2_cost = 250
	page_1_item_2_icon = BUY_MEDIUM_HEALTH_POTION_IMAGE
	page_1_item_3_name = "Large Health Potion"
	page_1_item_3_cost = 1000
	page_1_item_3_icon = BUY_LARGE_HEALTH_POTION_IMAGE

	page_1_item_4_name = "Small Mana Potion"
	page_1_item_4_cost = 50
	page_1_item_4_icon = BUY_SMALL_MANA_POTION_IMAGE
	page_1_item_5_name = "Medium Mana Potion"
	page_1_item_5_cost = 250
	page_1_item_5_icon = BUY_MEDIUM_MANA_POTION_IMAGE
	page_1_item_6_name = "Large Mana Potion"
	page_1_item_6_cost = 1000
	page_1_item_6_icon = BUY_LARGE_MANA_POTION_IMAGE

	'''
	page_1_item_7_name = "Small Mana Potion"
	page_1_item_7_cost = 50
	page_1_item_8_name = "Medium Mana Potion"
	page_1_item_8_cost = 250
	page_1_item_9_name = "Large Mana Potion"
	page_1_item_9_cost = 1000
	page_1_item_10_name = "Small Mana Potion"
	page_1_item_10_cost = 50
	'''

def equipment_database(ally,slot):

	#weapon
	#two handed
	if slot == "two handed weapon":
		if ally.two_handed:
			if ally.weapon == "sword":
				if ally.weapon_tier == 0:
					upgrade_category = "Two Handed Sword"
					upgrade_name = "Fist --> Wood"
					upgrade_cost = 30
					upgrade_description_1 = "0% --> +10% DMG"
					upgrade_description_2 = "0 --> +10 DMG"
					upgrade_description_3 = "0% --> 2% Chance of Crit Def Roll"
				if ally.weapon_tier == 1:
					upgrade_category = "Two Handed Sword"
					upgrade_name = "Wood --> Low Grade Iron"
					upgrade_cost = 150
					upgrade_description_1 = "10% --> +20% DMG"
					upgrade_description_2 = "+10 --> +25 DMG"
					upgrade_description_3 = "2% --> 4% Chance of Crit Def Roll"
				if ally.weapon_tier == 2:
					upgrade_category = "Two Handed Sword"
					upgrade_name = "Low Grade Iron --> High Grade Iron"
					upgrade_cost = 1000
					upgrade_description_1 = "20% --> +30% DMG"
					upgrade_description_2 = "+25 --> +70 DMG"
					upgrade_description_3 = "4% --> 6% Chance of Crit Def Roll"
				if ally.weapon_tier == 3:
					upgrade_category = "Two Handed Sword"
					upgrade_name = "High Grade Iron --> Steel"
					upgrade_cost = 5000
					upgrade_description_1 = "30% --> +40% DMG"
					upgrade_description_2 = "+70 --> +200 DMG"
					upgrade_description_3 = "6% --> 8% Chance of Crit Def Roll"
				if ally.weapon_tier == 4:
					upgrade_category = "Two Handed Sword"
					upgrade_name = "Steel --> Damascus"
					upgrade_cost = 20000
					upgrade_description_1 = "40% --> +50% DMG"
					upgrade_description_2 = "+200 --> +500 DMG"
					upgrade_description_3 = "8% --> 10% Chance of Crit Def Roll"
				if ally.weapon_tier == 5:
					upgrade_category = "Two Handed Sword"
					upgrade_name = "Damascus --> Orichalcum"
					upgrade_cost = 70000
					upgrade_description_1 = "50% --> +70% DMG"
					upgrade_description_2 = "+500 --> +1300 DMG"
					upgrade_description_3 = "10% --> 12% Chance of Crit Def Roll"
				if ally.weapon_tier == 6:
					upgrade_category = "Two Handed Sword"
					upgrade_name = "Orichalcum --> Blessed Orichalcum"
					upgrade_cost = 200000
					upgrade_description_1 = "70% --> +100% DMG"
					upgrade_description_2 = "+1300 --> +3000 DMG"
					upgrade_description_3 = "12% --> 15% Chance of Crit Def Roll"
				if ally.weapon_tier == 7:
					upgrade_category = "Two Handed Sword"
					upgrade_name = "Blessed Orichalcium (MAX)"
					upgrade_cost = "N/A"
					upgrade_description_1 = "+100% DMG"
					upgrade_description_2 = "+3000 DMG"
					upgrade_description_3 = "15% Chance of Crit Def Roll"

			if ally.weapon == "spear":
				pass


	#armor
	if slot == "helmet":
		if ally.armor_type == "Warrior":
			if ally.helmet_tier == 0:
				upgrade_category = "Helmet"
				upgrade_name = "Nothing --> Cooper"
				upgrade_cost = 15
				upgrade_description_1 = "0 --> +2 Armor"
				upgrade_description_2 = "0 --> +5 MP"
				upgrade_description_3 = None
			if ally.helmet_tier == 1:
				upgrade_category = "Helmet"
				upgrade_name = "Cooper --> Crude Iron"
				upgrade_cost = 75
				upgrade_description_1 = "2 --> +5 Armor"
				upgrade_description_2 = "5 --> +10 MP"
				upgrade_description_3 = None
			if ally.helmet_tier == 2:
				upgrade_category = "Helmet"
				upgrade_name = "Crude Iron --> Iron"
				upgrade_cost = 500
				upgrade_description_1 = "5 --> +15 Armor"
				upgrade_description_2 = "10 --> +20 MP"
				upgrade_description_3 = None
			if ally.helmet_tier == 3:
				upgrade_category = "Helmet"
				upgrade_name = "Iron --> Steel"
				upgrade_cost = 2500
				upgrade_description_1 = "15 --> +25 Armor"
				upgrade_description_2 = "20 --> +40 MP"
				upgrade_description_3 = None
			if ally.helmet_tier == 4:
				upgrade_category = "Helmet"
				upgrade_name = "Steel --> Royal Steel"
				upgrade_cost = 10000
				upgrade_description_1 = "25 --> +40 Armor"
				upgrade_description_2 = "40 --> +100 MP"
				upgrade_description_3 = None
			if ally.helmet_tier == 5:
				upgrade_category = "Helmet"
				upgrade_name = "Royal Steel --> Orichalcum"
				upgrade_cost = 35000
				upgrade_description_1 = "40 --> +70 Armor"
				upgrade_description_2 = "100 --> +250 MP"
				upgrade_description_3 = None
			if ally.helmet_tier == 6:
				upgrade_category = "Helmet"
				upgrade_name = "Orichalcum --> Blessed Orichalcum"
				upgrade_cost = 100000
				upgrade_description_1 = "70 --> +100 Armor"
				upgrade_description_2 = "250 --> +500 MP"
				upgrade_description_3 = None
			if ally.helmet_tier == 7:
				upgrade_category = "Helmet"
				upgrade_name = "Blessed Orichalcum (Max)"
				upgrade_cost = "N/A"
				upgrade_description_1 = "+100 Armor"
				upgrade_description_2 = "+500 MP"
				upgrade_description_3 = None

	if slot == "chest":
		if ally.armor_type == "Warrior":
			if ally.chest_tier == 0:
				upgrade_category = "Chest"
				upgrade_name = "Nothing --> Cooper"
				upgrade_cost = 30
				upgrade_description_1 = "0 --> +5 Armor"
				upgrade_description_2 = "0 --> +25 HP"
				upgrade_description_3 = None
			if ally.chest_tier == 1:
				upgrade_category = "Chest"
				upgrade_name = "Cooper --> Crude Iron"
				upgrade_cost = 150
				upgrade_description_1 = "5 --> +15 Armor"
				upgrade_description_2 = "25 --> +75 HP"
				upgrade_description_3 = None
			if ally.chest_tier == 2:
				upgrade_category = "Chest"
				upgrade_name = "Crude Iron --> Iron"
				upgrade_cost = 1000
				upgrade_description_1 = "15 --> +40 Armor"
				upgrade_description_2 = "75 --> +200 HP"
				upgrade_description_3 = None
			if ally.chest_tier == 3:
				upgrade_category = "Chest"
				upgrade_name = "Iron --> Steel"
				upgrade_cost = 5000
				upgrade_description_1 = "40 --> +75 Armor"
				upgrade_description_2 = "200 --> +400 HP"
				upgrade_description_3 = None
			if ally.chest_tier == 4:
				upgrade_category = "Chest"
				upgrade_name = "Steel --> Royal Steel"
				upgrade_cost = 20000
				upgrade_description_1 = "75 --> +125 Armor"
				upgrade_description_2 = "400 --> +700 HP"
				upgrade_description_3 = None
			if ally.chest_tier == 5:
				upgrade_category = "Chest"
				upgrade_name = "Royal Steel --> Orichalcum"
				upgrade_cost = 70000
				upgrade_description_1 = "125 --> +200 Armor"
				upgrade_description_2 = "700 --> +1200 HP"
				upgrade_description_3 = None
			if ally.chest_tier == 6:
				upgrade_category = "Chest"
				upgrade_name = "Orichalcum --> Blessed Orichalcum"
				upgrade_cost = 200000
				upgrade_description_1 = "200 --> +300 Armor"
				upgrade_description_2 = "1200 --> +2000 HP"
				upgrade_description_3 = None
			if ally.chest_tier == 7:
				upgrade_category = "Chest"
				upgrade_name = "Blessed Orichalcum (Max)"
				upgrade_cost = "N/A"
				upgrade_description_1 = "+300 Armor"
				upgrade_description_2 = "+2000 HP"
				upgrade_description_3 = None

	if slot == "legs":
		if ally.armor_type == "Warrior":
			if ally.legs_tier == 0:
				upgrade_category = "Legs"
				upgrade_name = "Nothing --> Cooper"
				upgrade_cost = 25
				upgrade_description_1 = "0 --> +4 Armor"
				upgrade_description_2 = "0 --> +2% Def Roll"
				upgrade_description_3 = None
			if ally.legs_tier == 1:
				upgrade_category = "Legs"
				upgrade_name = "Cooper --> Crude Iron"
				upgrade_cost = 130
				upgrade_description_1 = "4 --> +12 Armor"
				upgrade_description_2 = "2 --> +5% Def Roll"
				upgrade_description_3 = None
			if ally.legs_tier == 2:
				upgrade_category = "Legs"
				upgrade_name = "Crude Iron --> Iron"
				upgrade_cost = 800
				upgrade_description_1 = "12 --> +35 Armor"
				upgrade_description_2 = "5 --> +10% Def Roll"
				upgrade_description_3 = None
			if ally.legs_tier == 3:
				upgrade_category = "Legs"
				upgrade_name = "Iron --> Steel"
				upgrade_cost = 4000
				upgrade_description_1 = "35 --> +65 Armor"
				upgrade_description_2 = "10 --> +15% Def Roll"
				upgrade_description_3 = None
			if ally.legs_tier == 4:
				upgrade_category = "Legs"
				upgrade_name = "Steel --> Royal Steel"
				upgrade_cost = 16000
				upgrade_description_1 = "65 --> +110 Armor"
				upgrade_description_2 = "15 --> +20% Def Roll"
				upgrade_description_3 = None
			if ally.legs_tier == 5:
				upgrade_category = "Legs"
				upgrade_name = "Royal Steel --> Orichalcum"
				upgrade_cost = 60000
				upgrade_description_1 = "110 --> +170 Armor"
				upgrade_description_2 = "20 --> +25% Def Roll"
				upgrade_description_3 = None
			if ally.legs_tier == 6:
				upgrade_category = "Legs"
				upgrade_name = "Orichalcum --> Blessed Orichalcum"
				upgrade_cost = 175000
				upgrade_description_1 = "170 --> +250 Armor"
				upgrade_description_2 = "25 --> +30% Def Roll"
				upgrade_description_3 = None
			if ally.legs_tier == 7:
				upgrade_category = "Legs"
				upgrade_name = "Blessed Orichalcum (Max)"
				upgrade_cost = "N/A"
				upgrade_description_1 = "+250 Armor"
				upgrade_description_2 = "+30% Def Roll"
				upgrade_description_3 = None

	if slot == "feet":
		if ally.armor_type == "Warrior":
			if ally.feet_tier == 0:
				upgrade_category = "Feet"
				upgrade_name = "Nothing --> Cooper"
				upgrade_cost = 10
				upgrade_description_1 = "0 --> +1 Armor"
				upgrade_description_2 = "0 --> +3 Speed"
				upgrade_description_3 = None
			if ally.feet_tier == 1:
				upgrade_category = "Feet"
				upgrade_name = "Cooper --> Crude Iron"
				upgrade_cost = 50
				upgrade_description_1 = "1 --> +5 Armor"
				upgrade_description_2 = "3 --> +10 Speed"
				upgrade_description_3 = None
			if ally.feet_tier == 2:
				upgrade_category = "Feet"
				upgrade_name = "Crude Iron --> Iron"
				upgrade_cost = 350
				upgrade_description_1 = "5 --> +10 Armor"
				upgrade_description_2 = "10 --> +25 Speed"
				upgrade_description_3 = None
			if ally.feet_tier == 3:
				upgrade_category = "Feet"
				upgrade_name = "Iron --> Steel"
				upgrade_cost = 2000
				upgrade_description_1 = "10 --> +20 Armor"
				upgrade_description_2 = "25 --> +50 Speed"
				upgrade_description_3 = None
			if ally.feet_tier == 4:
				upgrade_category = "Feet"
				upgrade_name = "Steel --> Royal Steel"
				upgrade_cost = 7500
				upgrade_description_1 = "20 --> +30 Armor"
				upgrade_description_2 = "50 --> +90 Speed"
				upgrade_description_3 = None
			if ally.feet_tier == 5:
				upgrade_category = "Feet"
				upgrade_name = "Royal Steel --> Orichalcum"
				upgrade_cost = 30000
				upgrade_description_1 = "30 --> +40 Armor"
				upgrade_description_2 = "90 --> +150 Speed"
				upgrade_description_3 = None
			if ally.feet_tier == 6:
				upgrade_category = "Feet"
				upgrade_name = "Orichalcum --> Blessed Orichalcum"
				upgrade_cost = 75000
				upgrade_description_1 = "40 --> +50 Armor"
				upgrade_description_2 = "150 --> +225 Speed"
				upgrade_description_3 = None
			if ally.feet_tier == 7:
				upgrade_category = "Feet"
				upgrade_name = "Blessed Orichalcum (Max)"
				upgrade_cost = "N/A"
				upgrade_description_1 = "+50 Armor"
				upgrade_description_2 = "+225 Speed"
				upgrade_description_3 = None

	if slot == "gloves":
		if ally.armor_type == "Warrior":
			if ally.gloves_tier == 0:
				upgrade_category = "Gloves"
				upgrade_name = "Nothing --> Cooper"
				upgrade_cost = 10
				upgrade_description_1 = "0 --> +1 Armor"
				upgrade_description_2 = "0 --> +2% Critical Chance"
				upgrade_description_3 = None
			if ally.gloves_tier == 1:
				upgrade_category = "Gloves"
				upgrade_name = "Cooper --> Crude Iron"
				upgrade_cost = 50
				upgrade_description_1 = "1 --> +5 Armor"
				upgrade_description_2 = "2 --> +5% Critical Chance"
				upgrade_description_3 = None
			if ally.gloves_tier == 2:
				upgrade_category = "Gloves"
				upgrade_name = "Crude Iron --> Iron"
				upgrade_cost = 350
				upgrade_description_1 = "5 --> +10 Armor"
				upgrade_description_2 = "5 --> +10% Critical Chance"
				upgrade_description_3 = None
			if ally.gloves_tier == 3:
				upgrade_category = "Gloves"
				upgrade_name = "Iron --> Steel"
				upgrade_cost = 2000
				upgrade_description_1 = "10 --> +20 Armor"
				upgrade_description_2 = "10 --> +17% Critical Chance"
				upgrade_description_3 = None
			if ally.gloves_tier == 4:
				upgrade_category = "Gloves"
				upgrade_name = "Steel --> Royal Steel"
				upgrade_cost = 7500
				upgrade_description_1 = "20 --> +30 Armor"
				upgrade_description_2 = "17 --> +25% Critical Chance"
				upgrade_description_3 = None
			if ally.gloves_tier == 5:
				upgrade_category = "Gloves"
				upgrade_name = "Royal Steel --> Orichalcum"
				upgrade_cost = 30000
				upgrade_description_1 = "30 --> +40 Armor"
				upgrade_description_2 = "25 --> +32% Critical Chance"
				upgrade_description_3 = None
			if ally.gloves_tier == 6:
				upgrade_category = "Gloves"
				upgrade_name = "Orichalcum --> Blessed Orichalcum"
				upgrade_cost = 75000
				upgrade_description_1 = "40 --> +50 Armor"
				upgrade_description_2 = "32 --> +40% Critical Chance"
				upgrade_description_3 = None
			if ally.gloves_tier == 7:
				upgrade_category = "Gloves"
				upgrade_name = "Blessed Orichalcum (Max)"
				upgrade_cost = "N/A"
				upgrade_description_1 = "+50 Armor"
				upgrade_description_2 = "+40% Critical Chance"
				upgrade_description_3 = None

	return upgrade_category, upgrade_name, upgrade_cost, upgrade_description_1, upgrade_description_2, upgrade_description_3

def in_shop_draw_window():
	BACKGROUND()
	pygame.draw.rect(screen, GRAY, TOP_BAND)
	context_text = font.render("Shop", 1, BLACK)
	screen.blit(context_text, (TOP_BAND.centerx - context_text.get_width()//2, TOP_BAND.centery - context_text.get_height()//2))

	pygame.draw.rect(screen, GRAY, BUY_BUTTON)
	buy_text = font.render("Buy", 1, BLACK)
	screen.blit(buy_text, ( BUY_BUTTON.centerx - buy_text.get_width()//2, BUY_BUTTON.centery - buy_text.get_height()//2))
	pygame.draw.rect(screen, GRAY, SELL_BUTTON)
	sell_text = font.render("Sell", 1, BLACK)
	screen.blit(sell_text, ( SELL_BUTTON.centerx - sell_text.get_width()//2, SELL_BUTTON.centery - sell_text.get_height()//2))
	pygame.draw.rect(screen, GRAY, UPGRADE_BUTTON)
	upgrade_text = font.render("Blacksmith", 1, BLACK)
	screen.blit(upgrade_text, ( UPGRADE_BUTTON.centerx - upgrade_text.get_width()//2, UPGRADE_BUTTON.centery - upgrade_text.get_height()//2))
	pygame.draw.rect(screen, GRAY, BACK_BUTTON)
	back_text = font.render("Back", 1, BLACK)
	screen.blit(back_text, ( BACK_BUTTON.centerx - back_text.get_width()//2, BACK_BUTTON.centery - back_text.get_height()//2))

	pygame.display.update()

def in_shop():
	click = False
	run = True
	while run:
		clock.tick(60)
		mx, my = pygame.mouse.get_pos()

		if BUY_BUTTON.collidepoint((mx, my)):
			if click:
				in_buying()
			
		if SELL_BUTTON.collidepoint((mx, my)):
			if click:
				in_selling()
			
		if UPGRADE_BUTTON.collidepoint((mx, my)):
			if click:
				pre_upgrade()
			
		if BACK_BUTTON.collidepoint((mx, my)):
			if click:
				run = False

		click = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					run = False
			if event.type == KEYDOWN:
				if event.key == K_SPACE:
					click = True
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True
		
		in_shop_draw_window()

def buy(page,item):
	if page == 1:
		if item == 1:
			item_name = "Small Health Potion"
			item_cost = 50
			item_description = "Restore 50 HP upon use."
			if item_name in inventory.consumable:
				item_owned = inventory.consumable[item_name]
			else:
				item_owned = 0

		elif item == 2:
			item_name = "Medium Health Potion"
			item_cost = 250
			item_description = "Restore 250 HP upon use."
			if item_name in inventory.consumable:
				item_owned = inventory.consumable[item_name]
			else:
				item_owned = 0

		elif item == 3:
			item_name = "Large Health Potion"
			item_cost = 1000
			item_description = "Restore 1000 HP upon use."
			if item_name in inventory.consumable:
				item_owned = inventory.consumable[item_name]
			else:
				item_owned = 0
				
		elif item == 4:
			item_name = "Small Mana Potion"
			item_cost = 50
			item_description = "Restore 10 MP upon use."
			if item_name in inventory.consumable:
				item_owned = inventory.consumable[item_name]
			else:
				item_owned = 0
				
		elif item == 5:
			item_name = "Medium Mana Potion"
			item_cost = 250
			item_description = "Restore 50 MP upon use."
			if item_name in inventory.consumable:
				item_owned = inventory.consumable[item_name]
			else:
				item_owned = 0
				
		elif item == 6:
			item_name = "Large Mana Potion"
			item_cost = 1000
			item_description = "Restore 200 MP upon use."
			if item_name in inventory.consumable:
				item_owned = inventory.consumable[item_name]
			else:
				item_owned = 0


	return item_name,item_cost,item_description,item_owned

def in_buying_draw_window(stack_number,page,item_name,item_cost,item_description,item_owned,animations):
	BACKGROUND()
	pygame.draw.rect(screen, GRAY, TOP_BAND)
	context_text = font.render("Buying", 1, BLACK)
	screen.blit(context_text, (TOP_BAND.centerx - context_text.get_width()//2, TOP_BAND.centery - context_text.get_height()//2))

	gold_available_text = font.render(f"{inventory.town_gold} Gold", 1, BLACK)
	screen.blit(gold_available_text, ( WIDTH//2 - gold_available_text.get_width()//2, BUY_SWITCH_NUMBER_OF_STACKS_BUTTON.centery - gold_available_text.get_height()//2))

	pygame.draw.rect(screen, GRAY, BUY_SWITCH_NUMBER_OF_STACKS_BUTTON)
	switch_text = intermediate_font.render(f"{stack_number}", 1, BLACK)
	screen.blit(switch_text, ( BUY_SWITCH_NUMBER_OF_STACKS_BUTTON.centerx - switch_text.get_width()//2, BUY_SWITCH_NUMBER_OF_STACKS_BUTTON.centery - switch_text.get_height()//2))


	pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_ONE_BAND)
	pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_ONE_BUTTON)
	screen.blit(BUY_IMAGE, ( BUY_ITEM_NUM_ONE_BUTTON.x + 1, BUY_ITEM_NUM_ONE_BUTTON.y + 1))
	if page == 1:
		screen.blit(shop.page_1_item_1_icon, ( BUY_ITEM_NUM_ONE_BAND.x + 5, BUY_ITEM_NUM_ONE_BAND.y + 2))
		item_name_text = intermediate_font.render(f"{shop.page_1_item_1_name}", 1, BLACK)
		screen.blit(item_name_text, ( BUY_ITEM_NUM_ONE_BAND.x + 30, BUY_ITEM_NUM_ONE_BAND.centery - item_name_text.get_height()//2))
		item_cost_text = intermediate_font.render(f"{shop.page_1_item_1_cost}", 1, BLACK)
		screen.blit(item_cost_text, ( BUY_ITEM_NUM_ONE_BAND.right - 5 - item_cost_text.get_width(), BUY_ITEM_NUM_ONE_BAND.centery - item_name_text.get_height()//2))

	pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_TWO_BAND)
	pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_TWO_BUTTON)
	screen.blit(BUY_IMAGE, ( BUY_ITEM_NUM_TWO_BUTTON.x + 1, BUY_ITEM_NUM_TWO_BUTTON.y + 1))
	if page == 1:
		screen.blit(shop.page_1_item_2_icon, ( BUY_ITEM_NUM_TWO_BAND.x + 5, BUY_ITEM_NUM_TWO_BAND.y + 2))
		item_name_text = intermediate_font.render(f"{shop.page_1_item_2_name}", 1, BLACK)
		screen.blit(item_name_text, ( BUY_ITEM_NUM_TWO_BAND.x + 30, BUY_ITEM_NUM_TWO_BAND.centery - item_name_text.get_height()//2))
		item_cost_text = intermediate_font.render(f"{shop.page_1_item_2_cost}", 1, BLACK)
		screen.blit(item_cost_text, ( BUY_ITEM_NUM_TWO_BAND.right - 5 - item_cost_text.get_width(), BUY_ITEM_NUM_TWO_BAND.centery - item_name_text.get_height()//2))
	
	pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_THREE_BAND)
	pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_THREE_BUTTON)
	screen.blit(BUY_IMAGE, ( BUY_ITEM_NUM_THREE_BUTTON.x + 1, BUY_ITEM_NUM_THREE_BUTTON.y + 1))
	if page == 1:
		screen.blit(shop.page_1_item_3_icon, ( BUY_ITEM_NUM_THREE_BAND.x + 5, BUY_ITEM_NUM_THREE_BAND.y + 2))
		item_name_text = intermediate_font.render(f"{shop.page_1_item_3_name}", 1, BLACK)
		screen.blit(item_name_text, ( BUY_ITEM_NUM_THREE_BAND.x + 30, BUY_ITEM_NUM_THREE_BAND.centery - item_name_text.get_height()//2))
		item_cost_text = intermediate_font.render(f"{shop.page_1_item_3_cost}", 1, BLACK)
		screen.blit(item_cost_text, ( BUY_ITEM_NUM_THREE_BAND.right - 5 - item_cost_text.get_width(), BUY_ITEM_NUM_THREE_BAND.centery - item_name_text.get_height()//2))
	
	pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_FOUR_BAND)
	pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_FOUR_BUTTON)
	screen.blit(BUY_IMAGE, ( BUY_ITEM_NUM_FOUR_BUTTON.x + 1, BUY_ITEM_NUM_FOUR_BUTTON.y + 1))
	if page == 1:
		screen.blit(shop.page_1_item_4_icon, ( BUY_ITEM_NUM_FOUR_BAND.x + 5, BUY_ITEM_NUM_FOUR_BAND.y + 2))
		item_name_text = intermediate_font.render(f"{shop.page_1_item_4_name}", 1, BLACK)
		screen.blit(item_name_text, ( BUY_ITEM_NUM_FOUR_BAND.x + 30, BUY_ITEM_NUM_FOUR_BAND.centery - item_name_text.get_height()//2))
		item_cost_text = intermediate_font.render(f"{shop.page_1_item_4_cost}", 1, BLACK)
		screen.blit(item_cost_text, ( BUY_ITEM_NUM_FOUR_BAND.right - 5 - item_cost_text.get_width(), BUY_ITEM_NUM_FOUR_BAND.centery - item_name_text.get_height()//2))

	pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_FIVE_BAND)
	pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_FIVE_BUTTON)
	screen.blit(BUY_IMAGE, ( BUY_ITEM_NUM_FIVE_BUTTON.x + 1, BUY_ITEM_NUM_FIVE_BUTTON.y + 1))
	if page == 1:
		screen.blit(shop.page_1_item_5_icon, ( BUY_ITEM_NUM_FIVE_BAND.x + 5, BUY_ITEM_NUM_FIVE_BAND.y + 2))
		item_name_text = intermediate_font.render(f"{shop.page_1_item_5_name}", 1, BLACK)
		screen.blit(item_name_text, ( BUY_ITEM_NUM_FIVE_BAND.x + 30, BUY_ITEM_NUM_FIVE_BAND.centery - item_name_text.get_height()//2))
		item_cost_text = intermediate_font.render(f"{shop.page_1_item_5_cost}", 1, BLACK)
		screen.blit(item_cost_text, ( BUY_ITEM_NUM_FIVE_BAND.right - 5 - item_cost_text.get_width(), BUY_ITEM_NUM_FIVE_BAND.centery - item_name_text.get_height()//2))

	pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_SIX_BAND)
	pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_SIX_BUTTON)
	screen.blit(BUY_IMAGE, ( BUY_ITEM_NUM_SIX_BUTTON.x + 1, BUY_ITEM_NUM_SIX_BUTTON.y + 1))
	if page == 1:
		screen.blit(shop.page_1_item_6_icon, ( BUY_ITEM_NUM_SIX_BAND.x + 5, BUY_ITEM_NUM_SIX_BAND.y + 2))
		item_name_text = intermediate_font.render(f"{shop.page_1_item_6_name}", 1, BLACK)
		screen.blit(item_name_text, ( BUY_ITEM_NUM_SIX_BAND.x + 30, BUY_ITEM_NUM_SIX_BAND.centery - item_name_text.get_height()//2))
		item_cost_text = intermediate_font.render(f"{shop.page_1_item_6_cost}", 1, BLACK)
		screen.blit(item_cost_text, ( BUY_ITEM_NUM_SIX_BAND.right - 5 - item_cost_text.get_width(), BUY_ITEM_NUM_SIX_BAND.centery - item_name_text.get_height()//2))

	'''
	pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_SEVEN_BAND)
	pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_SEVEN_BUTTON)
	screen.blit(BUY_IMAGE, ( BUY_ITEM_NUM_SEVEN_BUTTON.x + 1, BUY_ITEM_NUM_SEVEN_BUTTON.y + 1))
	if page == 1:
		item_name_text = intermediate_font.render(f"{shop.page_1_item_7_name}", 1, BLACK)
		screen.blit(item_name_text, ( BUY_ITEM_NUM_SEVEN_BAND.x + 5, BUY_ITEM_NUM_SEVEN_BAND.centery - item_name_text.get_height()//2))
		item_cost_text = intermediate_font.render(f"{shop.page_1_item_7_cost}", 1, BLACK)
		screen.blit(item_cost_text, ( BUY_ITEM_NUM_SEVEN_BAND.right - 5 - item_cost_text.get_width(), BUY_ITEM_NUM_SEVEN_BAND.centery - item_name_text.get_height()//2))

	pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_EIGHT_BAND)
	pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_EIGHT_BUTTON)
	screen.blit(BUY_IMAGE, ( BUY_ITEM_NUM_EIGHT_BUTTON.x + 1, BUY_ITEM_NUM_EIGHT_BUTTON.y + 1))
	if page == 1:
		item_name_text = intermediate_font.render(f"{shop.page_1_item_8_name}", 1, BLACK)
		screen.blit(item_name_text, ( BUY_ITEM_NUM_EIGHT_BAND.x + 5, BUY_ITEM_NUM_EIGHT_BAND.centery - item_name_text.get_height()//2))
		item_cost_text = intermediate_font.render(f"{shop.page_1_item_8_cost}", 1, BLACK)
		screen.blit(item_cost_text, ( BUY_ITEM_NUM_EIGHT_BAND.right - 5 - item_cost_text.get_width(), BUY_ITEM_NUM_EIGHT_BAND.centery - item_name_text.get_height()//2))

	pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_NINE_BAND)
	pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_NINE_BUTTON)
	screen.blit(BUY_IMAGE, ( BUY_ITEM_NUM_NINE_BUTTON.x + 1, BUY_ITEM_NUM_NINE_BUTTON.y + 1))
	if page == 1:
		item_name_text = intermediate_font.render(f"{shop.page_1_item_9_name}", 1, BLACK)
		screen.blit(item_name_text, ( BUY_ITEM_NUM_NINE_BAND.x + 5, BUY_ITEM_NUM_NINE_BAND.centery - item_name_text.get_height()//2))
		item_cost_text = intermediate_font.render(f"{shop.page_1_item_9_cost}", 1, BLACK)
		screen.blit(item_cost_text, ( BUY_ITEM_NUM_NINE_BAND.right - 5 - item_cost_text.get_width(), BUY_ITEM_NUM_NINE_BAND.centery - item_name_text.get_height()//2))

	pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_TEN_BAND)
	pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_TEN_BUTTON)
	screen.blit(BUY_IMAGE, ( BUY_ITEM_NUM_TEN_BUTTON.x + 1, BUY_ITEM_NUM_TEN_BUTTON.y + 1))
	if page == 1:
		item_name_text = intermediate_font.render(f"{shop.page_1_item_10_name}", 1, BLACK)
		screen.blit(item_name_text, ( BUY_ITEM_NUM_TEN_BAND.x + 5, BUY_ITEM_NUM_TEN_BAND.centery - item_name_text.get_height()//2))
		item_cost_text = intermediate_font.render(f"{shop.page_1_item_10_cost}", 1, BLACK)
		screen.blit(item_cost_text, ( BUY_ITEM_NUM_TEN_BAND.right - 5 - item_cost_text.get_width(), BUY_ITEM_NUM_TEN_BAND.centery - item_name_text.get_height()//2))
	'''

	pygame.draw.rect(screen, GRAY, BACK_BUTTON_TOP)
	back_text = font.render("Back", 1, BLACK)
	screen.blit(back_text, ( BACK_BUTTON_TOP.centerx - back_text.get_width()//2, BACK_BUTTON_TOP.centery - back_text.get_height()//2))

	pygame.draw.rect(screen, INTERMEDIATE_GRAY, DESCRIPTION_BAND)
	if item_cost != None:
		item_name_text = font.render(f"{item_name}", 1, BLACK)
		screen.blit(item_name_text, ( DESCRIPTION_BAND.x + 25, DESCRIPTION_BAND.y + 10))
		if stack_number != "Max":
			item_cost_text = intermediate_font.render(f"Cost : {item_cost * stack_number} Gold", 1, BLACK)
			item_number_text = intermediate_font.render(f"Buy : x{stack_number}", 1, BLACK)
		else:
			number_of_buy = inventory.town_gold // item_cost
			item_cost_text = intermediate_font.render(f"Cost : {item_cost * number_of_buy} Gold", 1, BLACK)
			item_number_text = intermediate_font.render(f"Buy : x{number_of_buy}", 1, BLACK)
		screen.blit(item_cost_text, ( DESCRIPTION_BAND.right - 20 - item_cost_text.get_width(), DESCRIPTION_BAND.y + 10))
		screen.blit(item_number_text, ( DESCRIPTION_BAND.right - 20 - item_number_text.get_width(), DESCRIPTION_BAND.y + 25))
		item_description_text = intermediate_font.render(f"{item_description}", 1, BLACK)
		screen.blit(item_description_text, ( DESCRIPTION_BAND.centerx - item_description_text.get_width()//2, DESCRIPTION_BAND.centery))
		item_owned_text = intermediate_font.render(f"Owned : {item_owned}", 1, BLACK)
		screen.blit(item_owned_text, ( DESCRIPTION_BAND.right - 20 - item_owned_text.get_width(), DESCRIPTION_BAND.bottom - 10 - item_owned_text.get_height()))

	for anim in animations:
		if anim["name"] == "cost":
			cost_text = description_font.render(f"- {anim['value']}", 1, RED)
			screen.blit(cost_text, ( WIDTH//2 + gold_available_text.get_width()//2 + 10, BUY_SWITCH_NUMBER_OF_STACKS_BUTTON.centery - gold_available_text.get_height()//2 - anim["current_frame"]/9))
		if anim["name"] == "bought":
			bought_text = description_font.render(f"+ {anim['value']}", 1, GREEN)
			screen.blit(bought_text, ( anim["coordinate_x"], anim["coordinate_y"] - anim["current_frame"]/9))
		anim["current_frame"] += 1
		if anim["current_frame"] == anim["max_frame"]:
			animations.remove(anim)

	pygame.display.update()

def in_buying():
	click = False
	run = True
	stack_number = 1
	page = 1
	temp_buy = {}
	animations = []
	while run:
		clock.tick(60)
		mx, my = pygame.mouse.get_pos()
		item_name = None
		item_cost = None
		item_description = None
		item_owned = None
		
		if BUY_SWITCH_NUMBER_OF_STACKS_BUTTON.collidepoint((mx, my)):
			if click:
				if stack_number == 1:
					stack_number = 10
				elif stack_number == 10:
					stack_number = 100
				elif stack_number == 100:
					stack_number = "Max"
				elif stack_number == "Max":
					stack_number = 1


		if BUY_ITEM_NUM_ONE_BUTTON.collidepoint((mx, my)) or BUY_ITEM_NUM_ONE_BAND.collidepoint((mx,my)):
			item_name,item_cost,item_description,item_owned = buy(page,1)
			if stack_number != "Max":
				if click and inventory.town_gold >= item_cost * stack_number and BUY_ITEM_NUM_ONE_BUTTON.collidepoint((mx, my)):
					price = item_cost * stack_number
					inventory.town_gold -= price
					temp_buy[item_name] = stack_number
					animations.append({"name" : "cost", "value" : price, "current_frame" : 0, "max_frame" : 60})
					animations.append({"name" : "bought", "value" : stack_number, "coordinate_x": (BUY_ITEM_NUM_ONE_BUTTON.centerx), "coordinate_y": (BUY_ITEM_NUM_ONE_BUTTON.centery - 7), "current_frame" : 0, "max_frame" : 60})
			else:
				if click and inventory.town_gold >= item_cost and BUY_ITEM_NUM_ONE_BUTTON.collidepoint((mx, my)):
					number_of_buy = inventory.town_gold // item_cost
					price = item_cost * number_of_buy
					inventory.town_gold -= price
					temp_buy[item_name] = number_of_buy
					animations.append({"name" : "cost", "value" : price, "current_frame" : 0, "max_frame" : 60})
					animations.append({"name" : "bought", "value" : number_of_buy, "coordinate_x": (BUY_ITEM_NUM_ONE_BUTTON.centerx), "coordinate_y": (BUY_ITEM_NUM_ONE_BUTTON.centery - 7), "current_frame" : 0, "max_frame" : 60})

		if BUY_ITEM_NUM_TWO_BUTTON.collidepoint((mx, my)) or BUY_ITEM_NUM_TWO_BAND.collidepoint((mx,my)):
			item_name,item_cost,item_description,item_owned = buy(page,2)
			if stack_number != "Max":
				if click and inventory.town_gold >= item_cost * stack_number and BUY_ITEM_NUM_TWO_BUTTON.collidepoint((mx, my)):
					price = item_cost * stack_number
					inventory.town_gold -= price
					temp_buy[item_name] = stack_number
					animations.append({"name" : "cost", "value" : price, "current_frame" : 0, "max_frame" : 60})
					animations.append({"name" : "bought", "value" : stack_number, "coordinate_x": (BUY_ITEM_NUM_TWO_BUTTON.centerx), "coordinate_y": (BUY_ITEM_NUM_TWO_BUTTON.centery - 7), "current_frame" : 0, "max_frame" : 60})
			else:
				if click and inventory.town_gold >= item_cost and BUY_ITEM_NUM_TWO_BUTTON.collidepoint((mx, my)):
					number_of_buy = inventory.town_gold // item_cost
					price = item_cost * number_of_buy
					inventory.town_gold -= price
					temp_buy[item_name] = number_of_buy
					animations.append({"name" : "cost", "value" : price, "current_frame" : 0, "max_frame" : 60})
					animations.append({"name" : "bought", "value" : number_of_buy, "coordinate_x": (BUY_ITEM_NUM_TWO_BUTTON.centerx), "coordinate_y": (BUY_ITEM_NUM_TWO_BUTTON.centery - 7), "current_frame" : 0, "max_frame" : 60})

		if BUY_ITEM_NUM_THREE_BUTTON.collidepoint((mx, my)) or BUY_ITEM_NUM_THREE_BAND.collidepoint((mx,my)):
			item_name,item_cost,item_description,item_owned = buy(page,3)
			if stack_number != "Max":
				if click and inventory.town_gold >= item_cost * stack_number and BUY_ITEM_NUM_THREE_BUTTON.collidepoint((mx, my)):
					price = item_cost * stack_number
					inventory.town_gold -= price
					temp_buy[item_name] = stack_number
					animations.append({"name" : "cost", "value" : price, "current_frame" : 0, "max_frame" : 60})
					animations.append({"name" : "bought", "value" : stack_number, "coordinate_x": (BUY_ITEM_NUM_THREE_BUTTON.centerx), "coordinate_y": (BUY_ITEM_NUM_THREE_BUTTON.centery - 7), "current_frame" : 0, "max_frame" : 60})
			else:
				if click and inventory.town_gold >= item_cost and BUY_ITEM_NUM_THREE_BUTTON.collidepoint((mx, my)):
					number_of_buy = inventory.town_gold // item_cost
					price = item_cost * number_of_buy
					inventory.town_gold -= price
					temp_buy[item_name] = number_of_buy
					animations.append({"name" : "cost", "value" : price, "current_frame" : 0, "max_frame" : 60})
					animations.append({"name" : "bought", "value" : number_of_buy, "coordinate_x": (BUY_ITEM_NUM_THREE_BUTTON.centerx), "coordinate_y": (BUY_ITEM_NUM_THREE_BUTTON.centery - 7), "current_frame" : 0, "max_frame" : 60})


		if BUY_ITEM_NUM_FOUR_BUTTON.collidepoint((mx, my)) or BUY_ITEM_NUM_FOUR_BAND.collidepoint((mx,my)):
			item_name,item_cost,item_description,item_owned = buy(page,4)
			if stack_number != "Max":
				if click and inventory.town_gold >= item_cost * stack_number and BUY_ITEM_NUM_FOUR_BUTTON.collidepoint((mx, my)):
					price = item_cost * stack_number
					inventory.town_gold -= price
					temp_buy[item_name] = stack_number
					animations.append({"name" : "cost", "value" : price, "current_frame" : 0, "max_frame" : 60})
					animations.append({"name" : "bought", "value" : stack_number, "coordinate_x": (BUY_ITEM_NUM_FOUR_BUTTON.centerx), "coordinate_y": (BUY_ITEM_NUM_FOUR_BUTTON.centery - 7), "current_frame" : 0, "max_frame" : 60})
			else:
				if click and inventory.town_gold >= item_cost and BUY_ITEM_NUM_FOUR_BUTTON.collidepoint((mx, my)):
					number_of_buy = inventory.town_gold // item_cost
					price = item_cost * number_of_buy
					inventory.town_gold -= price
					temp_buy[item_name] = number_of_buy
					animations.append({"name" : "cost", "value" : price, "current_frame" : 0, "max_frame" : 60})
					animations.append({"name" : "bought", "value" : number_of_buy, "coordinate_x": (BUY_ITEM_NUM_FOUR_BUTTON.centerx), "coordinate_y": (BUY_ITEM_NUM_FOUR_BUTTON.centery - 7), "current_frame" : 0, "max_frame" : 60})

		if BUY_ITEM_NUM_FIVE_BUTTON.collidepoint((mx, my)) or BUY_ITEM_NUM_FIVE_BAND.collidepoint((mx,my)):
			item_name,item_cost,item_description,item_owned = buy(page,5)
			if stack_number != "Max":
				if click and inventory.town_gold >= item_cost * stack_number and BUY_ITEM_NUM_FIVE_BUTTON.collidepoint((mx, my)):
					price = item_cost * stack_number
					inventory.town_gold -= price
					temp_buy[item_name] = stack_number
					animations.append({"name" : "cost", "value" : price, "current_frame" : 0, "max_frame" : 60})
					animations.append({"name" : "bought", "value" : stack_number, "coordinate_x": (BUY_ITEM_NUM_FIVE_BUTTON.centerx), "coordinate_y": (BUY_ITEM_NUM_FIVE_BUTTON.centery - 7), "current_frame" : 0, "max_frame" : 60})
			else:
				if click and inventory.town_gold >= item_cost and BUY_ITEM_NUM_FIVE_BUTTON.collidepoint((mx, my)):
					number_of_buy = inventory.town_gold // item_cost
					price = item_cost * number_of_buy
					inventory.town_gold -= price
					temp_buy[item_name] = number_of_buy
					animations.append({"name" : "cost", "value" : price, "current_frame" : 0, "max_frame" : 60})
					animations.append({"name" : "bought", "value" : number_of_buy, "coordinate_x": (BUY_ITEM_NUM_FIVE_BUTTON.centerx), "coordinate_y": (BUY_ITEM_NUM_FIVE_BUTTON.centery - 7), "current_frame" : 0, "max_frame" : 60})

		if BUY_ITEM_NUM_SIX_BUTTON.collidepoint((mx, my)) or BUY_ITEM_NUM_SIX_BAND.collidepoint((mx,my)):
			item_name,item_cost,item_description,item_owned = buy(page,6)
			if stack_number != "Max":
				if click and inventory.town_gold >= item_cost * stack_number and BUY_ITEM_NUM_SIX_BUTTON.collidepoint((mx, my)):
					price = item_cost * stack_number
					inventory.town_gold -= price
					temp_buy[item_name] = stack_number
					animations.append({"name" : "cost", "value" : price, "current_frame" : 0, "max_frame" : 60})
					animations.append({"name" : "bought", "value" : stack_number, "coordinate_x": (BUY_ITEM_NUM_SIX_BUTTON.centerx), "coordinate_y": (BUY_ITEM_NUM_SIX_BUTTON.centery - 7), "current_frame" : 0, "max_frame" : 60})
			else:
				if click and inventory.town_gold >= item_cost and BUY_ITEM_NUM_SIX_BUTTON.collidepoint((mx, my)):
					number_of_buy = inventory.town_gold // item_cost
					price = item_cost * number_of_buy
					inventory.town_gold -= price
					temp_buy[item_name] = number_of_buy
					animations.append({"name" : "cost", "value" : price, "current_frame" : 0, "max_frame" : 60})
					animations.append({"name" : "bought", "value" : number_of_buy, "coordinate_x": (BUY_ITEM_NUM_SIX_BUTTON.centerx), "coordinate_y": (BUY_ITEM_NUM_SIX_BUTTON.centery - 7), "current_frame" : 0, "max_frame" : 60})


		if BACK_BUTTON_TOP.collidepoint((mx, my)):
			if click:
				run = False

		click = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					run = False
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True

		if len(temp_buy) > 0:
			for item in temp_buy:
				if item in inventory.consumable:
					inventory.consumable[item] += temp_buy[item]
				else:
					inventory.consumable[item] = temp_buy[item]
			temp_buy = {}

		in_buying_draw_window(stack_number,page,item_name,item_cost,item_description,item_owned,animations)

def selling_info(item_name):
	if item_name == "Goblin's Soulgem":
		item_cost = 50
		item_description = "A little gem containing the soul of a goblin."
		item_owned = inventory.town_storage[item_name]
	elif item_name == "Hobgoblin's Soulgem":
		item_cost = 200
		item_description = "A little gem containing the soul of a hobgoblin."
		item_owned = inventory.town_storage[item_name]
	elif item_name == "Goblin's ear jewel":
		item_cost = 750
		item_description = "A unique type of jewel that belonged to a goblin."
		item_owned = inventory.town_storage[item_name]

	return item_cost,item_description,item_owned

def selling_image(item_name):
	item_image = TEMPLATE_IMAGE
	if item_name == "Goblin's Soulgem":
		item_image = SOULGEM_IMAGE
	
	return item_image

def in_selling_draw_window(item_name_list,item_number_list,stack_number,page,item_name,item_cost,item_description,item_owned,animations,storage):
	BACKGROUND()
	pygame.draw.rect(screen, GRAY, TOP_BAND)
	context_text = font.render("Selling", 1, BLACK)
	screen.blit(context_text, (TOP_BAND.centerx - context_text.get_width()//2, TOP_BAND.centery - context_text.get_height()//2))

	gold_available_text = font.render(f"{inventory.town_gold} Gold", 1, BLACK)
	screen.blit(gold_available_text, ( WIDTH//2 - gold_available_text.get_width()//2, BUY_SWITCH_NUMBER_OF_STACKS_BUTTON.centery - gold_available_text.get_height()//2))

	pygame.draw.rect(screen, GRAY, BUY_PAGE_LEFT_BUTTON)
	screen.blit(LEFT_ARROW_IMAGE, ( BUY_PAGE_LEFT_BUTTON.x, BUY_PAGE_LEFT_BUTTON.y))
	pygame.draw.rect(screen, GRAY, BUY_PAGE_RIGHT_BUTTON)
	screen.blit(RIGHT_ARROW_IMAGE, ( BUY_PAGE_RIGHT_BUTTON.x, BUY_PAGE_RIGHT_BUTTON.y))

	pygame.draw.rect(screen, GRAY, BUY_SWITCH_STORAGE_CONSUMABLE_BUTTON)
	if storage:
		storage_text = intermediate_font.render("Consumables", 1, BLACK)
	else:
		storage_text = intermediate_font.render("Storage", 1, BLACK)
	screen.blit(storage_text, ( BUY_SWITCH_STORAGE_CONSUMABLE_BUTTON.centerx - storage_text.get_width()//2, BUY_SWITCH_STORAGE_CONSUMABLE_BUTTON.centery - storage_text.get_height()//2))

	pygame.draw.rect(screen, GRAY, BUY_SWITCH_NUMBER_OF_STACKS_BUTTON)
	switch_text = intermediate_font.render(f"{stack_number}", 1, BLACK)
	screen.blit(switch_text, ( BUY_SWITCH_NUMBER_OF_STACKS_BUTTON.centerx - switch_text.get_width()//2, BUY_SWITCH_NUMBER_OF_STACKS_BUTTON.centery - switch_text.get_height()//2))
	
	pygame.draw.rect(screen, GRAY, BACK_BUTTON_TOP)
	back_text = font.render("Back", 1, BLACK)
	screen.blit(back_text, ( BACK_BUTTON_TOP.centerx - back_text.get_width()//2, BACK_BUTTON_TOP.centery - back_text.get_height()//2))

	if len(item_name_list) == 0:
		if storage:
			nothing_text = font.render("Nothing in the storage.", 1, BLACK)
		else:
			nothing_text = font.render("No consumables to sell.", 1, BLACK)
		screen.blit(nothing_text, ( WIDTH//2 - nothing_text.get_width()//2, 280))

	if len(item_name_list) >= 1:
		pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_ONE_BAND)
		pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_ONE_BUTTON)
		screen.blit(SELL_IMAGE, ( BUY_ITEM_NUM_ONE_BUTTON.x + 1, BUY_ITEM_NUM_ONE_BUTTON.y + 1))
		screen.blit(selling_image(item_name_list[0]), ( BUY_ITEM_NUM_ONE_BAND.x + 5, BUY_ITEM_NUM_ONE_BAND.y + 2))
		item_name_text = intermediate_font.render(f"{item_name_list[0]}", 1, BLACK)
		screen.blit(item_name_text, ( BUY_ITEM_NUM_ONE_BAND.x + 30, BUY_ITEM_NUM_ONE_BAND.centery - item_name_text.get_height()//2 + 2))
		item_number_text = intermediate_font.render(f"x{item_number_list[0]}", 1, BLACK)
		screen.blit(item_number_text, ( BUY_ITEM_NUM_ONE_BAND.right - 5 - item_number_text.get_width(), BUY_ITEM_NUM_ONE_BAND.centery - item_name_text.get_height()//2 + 2))

	if len(item_name_list) >= 2:
		pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_TWO_BAND)
		pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_TWO_BUTTON)
		screen.blit(SELL_IMAGE, ( BUY_ITEM_NUM_TWO_BUTTON.x + 1, BUY_ITEM_NUM_TWO_BUTTON.y + 1))
		screen.blit(selling_image(item_name_list[1]), ( BUY_ITEM_NUM_TWO_BAND.x + 5, BUY_ITEM_NUM_TWO_BAND.y + 2))
		item_name_text = intermediate_font.render(f"{item_name_list[1]}", 1, BLACK)
		screen.blit(item_name_text, ( BUY_ITEM_NUM_TWO_BAND.x + 30, BUY_ITEM_NUM_TWO_BAND.centery - item_name_text.get_height()//2 + 2))
		item_number_text = intermediate_font.render(f"x{item_number_list[1]}", 1, BLACK)
		screen.blit(item_number_text, ( BUY_ITEM_NUM_TWO_BAND.right - 5 - item_number_text.get_width(), BUY_ITEM_NUM_TWO_BAND.centery - item_name_text.get_height()//2 + 2))
		
	if len(item_name_list) >= 3:
		pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_THREE_BAND)
		pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_THREE_BUTTON)
		screen.blit(SELL_IMAGE, ( BUY_ITEM_NUM_THREE_BUTTON.x + 1, BUY_ITEM_NUM_THREE_BUTTON.y + 1))
		screen.blit(selling_image(item_name_list[2]), ( BUY_ITEM_NUM_THREE_BAND.x + 5, BUY_ITEM_NUM_THREE_BAND.y + 2))
		item_name_text = intermediate_font.render(f"{item_name_list[2]}", 1, BLACK)
		screen.blit(item_name_text, ( BUY_ITEM_NUM_THREE_BAND.x + 30, BUY_ITEM_NUM_THREE_BAND.centery - item_name_text.get_height()//2 + 2))
		item_number_text = intermediate_font.render(f"x{item_number_list[2]}", 1, BLACK)
		screen.blit(item_number_text, ( BUY_ITEM_NUM_THREE_BAND.right - 5 - item_number_text.get_width(), BUY_ITEM_NUM_THREE_BAND.centery - item_name_text.get_height()//2 + 2))
		
	if len(item_name_list) >= 4:
		pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_FOUR_BAND)
		pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_FOUR_BUTTON)
		screen.blit(SELL_IMAGE, ( BUY_ITEM_NUM_FOUR_BUTTON.x + 1, BUY_ITEM_NUM_FOUR_BUTTON.y + 1))
		screen.blit(selling_image(item_name_list[3]), ( BUY_ITEM_NUM_FOUR_BAND.x + 5, BUY_ITEM_NUM_FOUR_BAND.y + 2))
		item_name_text = intermediate_font.render(f"{item_name_list[3]}", 1, BLACK)
		screen.blit(item_name_text, ( BUY_ITEM_NUM_FOUR_BAND.x + 30, BUY_ITEM_NUM_FOUR_BAND.centery - item_name_text.get_height()//2 + 2))
		item_number_text = intermediate_font.render(f"x{item_number_list[3]}", 1, BLACK)
		screen.blit(item_number_text, ( BUY_ITEM_NUM_FOUR_BAND.right - 5 - item_number_text.get_width(), BUY_ITEM_NUM_FOUR_BAND.centery - item_name_text.get_height()//2 + 2))
		
	if len(item_name_list) >= 5:
		pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_FIVE_BAND)
		pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_FIVE_BUTTON)
		screen.blit(SELL_IMAGE, ( BUY_ITEM_NUM_FIVE_BUTTON.x + 1, BUY_ITEM_NUM_FIVE_BUTTON.y + 1))
		screen.blit(selling_image(item_name_list[4]), ( BUY_ITEM_NUM_FIVE_BAND.x + 5, BUY_ITEM_NUM_FIVE_BAND.y + 2))
		item_name_text = intermediate_font.render(f"{item_name_list[4]}", 1, BLACK)
		screen.blit(item_name_text, ( BUY_ITEM_NUM_FIVE_BAND.x + 30, BUY_ITEM_NUM_FIVE_BAND.centery - item_name_text.get_height()//2 + 2))
		item_number_text = intermediate_font.render(f"x{item_number_list[4]}", 1, BLACK)
		screen.blit(item_number_text, ( BUY_ITEM_NUM_FIVE_BAND.right - 5 - item_number_text.get_width(), BUY_ITEM_NUM_FIVE_BAND.centery - item_name_text.get_height()//2 + 2))
		
	if len(item_name_list) >= 6:
		pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_SIX_BAND)
		pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_SIX_BUTTON)
		screen.blit(SELL_IMAGE, ( BUY_ITEM_NUM_SIX_BUTTON.x + 1, BUY_ITEM_NUM_SIX_BUTTON.y + 1))
		screen.blit(selling_image(item_name_list[5]), ( BUY_ITEM_NUM_SIX_BAND.x + 5, BUY_ITEM_NUM_SIX_BAND.y + 2))
		item_name_text = intermediate_font.render(f"{item_name_list[5]}", 1, BLACK)
		screen.blit(item_name_text, ( BUY_ITEM_NUM_SIX_BAND.x + 30, BUY_ITEM_NUM_SIX_BAND.centery - item_name_text.get_height()//2 + 2))
		item_number_text = intermediate_font.render(f"x{item_number_list[5]}", 1, BLACK)
		screen.blit(item_number_text, ( BUY_ITEM_NUM_SIX_BAND.right - 5 - item_number_text.get_width(), BUY_ITEM_NUM_SIX_BAND.centery - item_name_text.get_height()//2 + 2))
		
	if len(item_name_list) >= 7:
		pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_SEVEN_BAND)
		pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_SEVEN_BUTTON)
		screen.blit(SELL_IMAGE, ( BUY_ITEM_NUM_SEVEN_BUTTON.x + 1, BUY_ITEM_NUM_SEVEN_BUTTON.y + 1))
		screen.blit(selling_image(item_name_list[6]), ( BUY_ITEM_NUM_SEVEN_BAND.x + 5, BUY_ITEM_NUM_SEVEN_BAND.y + 2))
		item_name_text = intermediate_font.render(f"{item_name_list[6]}", 1, BLACK)
		screen.blit(item_name_text, ( BUY_ITEM_NUM_SEVEN_BAND.x + 30, BUY_ITEM_NUM_SEVEN_BAND.centery - item_name_text.get_height()//2 + 2))
		item_number_text = intermediate_font.render(f"x{item_number_list[6]}", 1, BLACK)
		screen.blit(item_number_text, ( BUY_ITEM_NUM_SEVEN_BAND.right - 5 - item_number_text.get_width(), BUY_ITEM_NUM_SEVEN_BAND.centery - item_name_text.get_height()//2 + 2))
		
	if len(item_name_list) >= 8:
		pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_EIGHT_BAND)
		pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_EIGHT_BUTTON)
		screen.blit(SELL_IMAGE, ( BUY_ITEM_NUM_EIGHT_BUTTON.x + 1, BUY_ITEM_NUM_EIGHT_BUTTON.y + 1))
		screen.blit(selling_image(item_name_list[7]), ( BUY_ITEM_NUM_EIGHT_BAND.x + 5, BUY_ITEM_NUM_EIGHT_BAND.y + 2))
		item_name_text = intermediate_font.render(f"{item_name_list[7]}", 1, BLACK)
		screen.blit(item_name_text, ( BUY_ITEM_NUM_EIGHT_BAND.x + 30, BUY_ITEM_NUM_EIGHT_BAND.centery - item_name_text.get_height()//2 + 2))
		item_number_text = intermediate_font.render(f"x{item_number_list[7]}", 1, BLACK)
		screen.blit(item_number_text, ( BUY_ITEM_NUM_EIGHT_BAND.right - 5 - item_number_text.get_width(), BUY_ITEM_NUM_EIGHT_BAND.centery - item_name_text.get_height()//2 + 2))
		
	if len(item_name_list) >= 9:
		pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_NINE_BAND)
		pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_NINE_BUTTON)
		screen.blit(SELL_IMAGE, ( BUY_ITEM_NUM_NINE_BUTTON.x + 1, BUY_ITEM_NUM_NINE_BUTTON.y + 1))
		screen.blit(selling_image(item_name_list[8]), ( BUY_ITEM_NUM_NINE_BAND.x + 5, BUY_ITEM_NUM_NINE_BAND.y + 2))
		item_name_text = intermediate_font.render(f"{item_name_list[8]}", 1, BLACK)
		screen.blit(item_name_text, ( BUY_ITEM_NUM_NINE_BAND.x + 30, BUY_ITEM_NUM_NINE_BAND.centery - item_name_text.get_height()//2 + 2))
		item_number_text = intermediate_font.render(f"x{item_number_list[8]}", 1, BLACK)
		screen.blit(item_number_text, ( BUY_ITEM_NUM_NINE_BAND.right - 5 - item_number_text.get_width(), BUY_ITEM_NUM_NINE_BAND.centery - item_name_text.get_height()//2 + 2))
		
	if len(item_name_list) >= 10:
		pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_TEN_BAND)
		pygame.draw.rect(screen, GRAY, BUY_ITEM_NUM_TEN_BUTTON)
		screen.blit(SELL_IMAGE, ( BUY_ITEM_NUM_TEN_BUTTON.x + 1, BUY_ITEM_NUM_TEN_BUTTON.y + 1))
		screen.blit(selling_image(item_name_list[9]), ( BUY_ITEM_NUM_TEN_BAND.x + 5, BUY_ITEM_NUM_TEN_BAND.y + 2))
		item_name_text = intermediate_font.render(f"{item_name_list[9]}", 1, BLACK)
		screen.blit(item_name_text, ( BUY_ITEM_NUM_TEN_BAND.x + 30, BUY_ITEM_NUM_TEN_BAND.centery - item_name_text.get_height()//2 + 2))
		item_number_text = intermediate_font.render(f"x{item_number_list[9]}", 1, BLACK)
		screen.blit(item_number_text, ( BUY_ITEM_NUM_TEN_BAND.right - 5 - item_number_text.get_width(), BUY_ITEM_NUM_TEN_BAND.centery - item_name_text.get_height()//2 + 2))


	pygame.draw.rect(screen, INTERMEDIATE_GRAY, DESCRIPTION_BAND)
	if item_cost != None:
		item_name_text = font.render(f"{item_name}", 1, BLACK)
		screen.blit(item_name_text, ( DESCRIPTION_BAND.x + 25, DESCRIPTION_BAND.y + 10))
		if stack_number != "Max" and stack_number <= item_owned:
			item_cost_text = intermediate_font.render(f"Profit : {item_cost * stack_number} Gold", 1, BLACK)
			item_number_text = intermediate_font.render(f"Sell : x{stack_number}", 1, BLACK)
		else:
			number_of_sell = item_owned
			item_cost_text = intermediate_font.render(f"Profit : {item_cost * number_of_sell} Gold", 1, BLACK)
			item_number_text = intermediate_font.render(f"Sell : x{number_of_sell}", 1, BLACK)
		screen.blit(item_cost_text, ( DESCRIPTION_BAND.right - 20 - item_cost_text.get_width(), DESCRIPTION_BAND.y + 10))
		screen.blit(item_number_text, ( DESCRIPTION_BAND.right - 20 - item_number_text.get_width(), DESCRIPTION_BAND.y + 25))
		item_description_text = intermediate_font.render(f"{item_description}", 1, BLACK)
		screen.blit(item_description_text, ( DESCRIPTION_BAND.x + 10, DESCRIPTION_BAND.centery))
		item_owned_text = intermediate_font.render(f"Owned : {item_owned}", 1, BLACK)
		screen.blit(item_owned_text, ( DESCRIPTION_BAND.right - 20 - item_owned_text.get_width(), DESCRIPTION_BAND.bottom - 10 - item_owned_text.get_height()))

	for anim in animations:
		if anim["name"] == "benefits":
			benefits_text = description_font.render(f"+ {anim['value']}", 1, GREEN)
			screen.blit(benefits_text, ( WIDTH//2 + gold_available_text.get_width()//2 + 10, BUY_SWITCH_NUMBER_OF_STACKS_BUTTON.centery - gold_available_text.get_height()//2 - anim["current_frame"]/9))
		if anim["name"] == "sold":
			sold_text = description_font.render(f"- {anim['value']}", 1, RED)
			screen.blit(sold_text, ( anim["coordinate_x"], anim["coordinate_y"] - anim["current_frame"]/9))
		anim["current_frame"] += 1
		if anim["current_frame"] == anim["max_frame"]:
			animations.remove(anim)

	pygame.display.update()

def in_selling():
	click = False
	run = True
	stack_number = 1
	page = 0
	max_page = 0
	animations = []
	storage = True
	while run:
		clock.tick(60)
		mx, my = pygame.mouse.get_pos()
		item_name = None
		item_cost = None
		item_description = None
		item_owned = None
		item_name_list = []
		item_number_list = []
		sold_out = []

		if BUY_PAGE_LEFT_BUTTON.collidepoint((mx, my)):
			if click and page > 0:
				page -= 1
		if BUY_PAGE_RIGHT_BUTTON.collidepoint((mx, my)):
			if click and page < max_page:
				page += 1

		if BUY_SWITCH_STORAGE_CONSUMABLE_BUTTON.collidepoint((mx, my)):
			if click:
				if storage:
					storage = False
				else:
					storage = True

		if storage:
			max_page = len(inventory.town_storage)//10
			keys_list = list(inventory.town_storage)
			for key in keys_list[page * 10 : (page + 1) * 10]:
				item_name_list.append(key)
				item_number_list.append(inventory.town_storage[key])
		else:
			max_page = len(inventory.consumable)//10
			keys_list = list(inventory.consumable)
			for key in keys_list[page * 10 : (page + 1) * 10]:
				item_name_list.append(key)
				item_number_list.append(inventory.consumable[key])


		if BUY_SWITCH_NUMBER_OF_STACKS_BUTTON.collidepoint((mx, my)):
			if click:
				if stack_number == 1:
					stack_number = 10
				elif stack_number == 10:
					stack_number = 100
				elif stack_number == 100:
					stack_number = "Max"
				elif stack_number == "Max":
					stack_number = 1

		if (BUY_ITEM_NUM_ONE_BUTTON.collidepoint((mx, my)) or BUY_ITEM_NUM_ONE_BAND.collidepoint((mx,my))) and len(item_name_list) >= 1:
			item_name = item_name_list[0]
			item_cost,item_description,item_owned = selling_info(item_name)	
			if item_owned > 0:
				if stack_number != "Max":
					if click and BUY_ITEM_NUM_ONE_BUTTON.collidepoint((mx, my)):
						if stack_number >= item_owned:
							item_sold = item_owned
						else:
							item_sold = stack_number
						benefits = item_cost * item_sold
						inventory.town_gold += benefits
						inventory.town_storage[item_name] -= item_sold
						animations.append({"name" : "benefits", "value" : benefits, "current_frame" : 0, "max_frame" : 60})
						animations.append({"name" : "sold", "value" : item_sold, "coordinate_x": (BUY_ITEM_NUM_ONE_BUTTON.centerx), "coordinate_y": (BUY_ITEM_NUM_ONE_BUTTON.centery - 7), "current_frame" : 0, "max_frame" : 60})
				else:
					if click and BUY_ITEM_NUM_ONE_BUTTON.collidepoint((mx, my)):
						item_sold = item_owned
						benefits = item_cost * item_sold
						inventory.town_gold += benefits
						inventory.town_storage[item_name] -= item_sold
						animations.append({"name" : "benefits", "value" : benefits, "current_frame" : 0, "max_frame" : 60})
						animations.append({"name" : "sold", "value" : item_sold, "coordinate_x": (BUY_ITEM_NUM_ONE_BUTTON.centerx), "coordinate_y": (BUY_ITEM_NUM_ONE_BUTTON.centery - 7), "current_frame" : 0, "max_frame" : 60})

		if (BUY_ITEM_NUM_TWO_BUTTON.collidepoint((mx, my)) or BUY_ITEM_NUM_TWO_BAND.collidepoint((mx,my))) and len(item_name_list) >= 2:
			item_name = item_name_list[1]
			item_cost,item_description,item_owned = selling_info(item_name)	
			if item_owned > 0:
				if stack_number != "Max":
					if click and BUY_ITEM_NUM_TWO_BUTTON.collidepoint((mx, my)):
						if stack_number >= item_owned:
							item_sold = item_owned
						else:
							item_sold = stack_number
						benefits = item_cost * item_sold
						inventory.town_gold += benefits
						inventory.town_storage[item_name] -= item_sold
						animations.append({"name" : "benefits", "value" : benefits, "current_frame" : 0, "max_frame" : 60})
						animations.append({"name" : "sold", "value" : item_sold, "coordinate_x": (BUY_ITEM_NUM_TWO_BUTTON.centerx), "coordinate_y": (BUY_ITEM_NUM_TWO_BUTTON.centery - 7), "current_frame" : 0, "max_frame" : 60})
				else:
					if click and BUY_ITEM_NUM_TWO_BUTTON.collidepoint((mx, my)):
						item_sold = item_owned
						benefits = item_cost * item_sold
						inventory.town_gold += benefits
						inventory.town_storage[item_name] -= item_sold
						animations.append({"name" : "benefits", "value" : benefits, "current_frame" : 0, "max_frame" : 60})
						animations.append({"name" : "sold", "value" : item_sold, "coordinate_x": (BUY_ITEM_NUM_TWO_BUTTON.centerx), "coordinate_y": (BUY_ITEM_NUM_TWO_BUTTON.centery - 7), "current_frame" : 0, "max_frame" : 60})
						
		if (BUY_ITEM_NUM_THREE_BUTTON.collidepoint((mx, my)) or BUY_ITEM_NUM_THREE_BAND.collidepoint((mx,my))) and len(item_name_list) >= 3:
			item_name = item_name_list[2]
			item_cost,item_description,item_owned = selling_info(item_name)	
			if item_owned > 0:
				if stack_number != "Max":
					if click and BUY_ITEM_NUM_THREE_BUTTON.collidepoint((mx, my)):
						if stack_number >= item_owned:
							item_sold = item_owned
						else:
							item_sold = stack_number
						benefits = item_cost * item_sold
						inventory.town_gold += benefits
						inventory.town_storage[item_name] -= item_sold
						animations.append({"name" : "benefits", "value" : benefits, "current_frame" : 0, "max_frame" : 60})
						animations.append({"name" : "sold", "value" : item_sold, "coordinate_x": (BUY_ITEM_NUM_THREE_BUTTON.centerx), "coordinate_y": (BUY_ITEM_NUM_THREE_BUTTON.centery - 7), "current_frame" : 0, "max_frame" : 60})
				else:
					if click and BUY_ITEM_NUM_THREE_BUTTON.collidepoint((mx, my)):
						item_sold = item_owned
						benefits = item_cost * item_sold
						inventory.town_gold += benefits
						inventory.town_storage[item_name] -= item_sold
						animations.append({"name" : "benefits", "value" : benefits, "current_frame" : 0, "max_frame" : 60})
						animations.append({"name" : "sold", "value" : item_sold, "coordinate_x": (BUY_ITEM_NUM_THREE_BUTTON.centerx), "coordinate_y": (BUY_ITEM_NUM_THREE_BUTTON.centery - 7), "current_frame" : 0, "max_frame" : 60})
						
		if (BUY_ITEM_NUM_FOUR_BUTTON.collidepoint((mx, my)) or BUY_ITEM_NUM_FOUR_BAND.collidepoint((mx,my))) and len(item_name_list) >= 4:
			item_name = item_name_list[3]
			item_cost,item_description,item_owned = selling_info(item_name)	
			if item_owned > 0:
				if stack_number != "Max":
					if click and BUY_ITEM_NUM_FOUR_BUTTON.collidepoint((mx, my)):
						if stack_number >= item_owned:
							item_sold = item_owned
						else:
							item_sold = stack_number
						benefits = item_cost * item_sold
						inventory.town_gold += benefits
						inventory.town_storage[item_name] -= item_sold
						animations.append({"name" : "benefits", "value" : benefits, "current_frame" : 0, "max_frame" : 60})
						animations.append({"name" : "sold", "value" : item_sold, "coordinate_x": (BUY_ITEM_NUM_FOUR_BUTTON.centerx), "coordinate_y": (BUY_ITEM_NUM_FOUR_BUTTON.centery - 7), "current_frame" : 0, "max_frame" : 60})
				else:
					if click and BUY_ITEM_NUM_FOUR_BUTTON.collidepoint((mx, my)):
						item_sold = item_owned
						benefits = item_cost * item_sold
						inventory.town_gold += benefits
						inventory.town_storage[item_name] -= item_sold
						animations.append({"name" : "benefits", "value" : benefits, "current_frame" : 0, "max_frame" : 60})
						animations.append({"name" : "sold", "value" : item_sold, "coordinate_x": (BUY_ITEM_NUM_FOUR_BUTTON.centerx), "coordinate_y": (BUY_ITEM_NUM_FOUR_BUTTON.centery - 7), "current_frame" : 0, "max_frame" : 60})
						
		if (BUY_ITEM_NUM_FIVE_BUTTON.collidepoint((mx, my)) or BUY_ITEM_NUM_FIVE_BAND.collidepoint((mx,my))) and len(item_name_list) >= 5:
			item_name = item_name_list[4]
			item_cost,item_description,item_owned = selling_info(item_name)	
			if item_owned > 0:
				if stack_number != "Max":
					if click and BUY_ITEM_NUM_FIVE_BUTTON.collidepoint((mx, my)):
						if stack_number >= item_owned:
							item_sold = item_owned
						else:
							item_sold = stack_number
						benefits = item_cost * item_sold
						inventory.town_gold += benefits
						inventory.town_storage[item_name] -= item_sold
						animations.append({"name" : "benefits", "value" : benefits, "current_frame" : 0, "max_frame" : 60})
						animations.append({"name" : "sold", "value" : item_sold, "coordinate_x": (BUY_ITEM_NUM_FIVE_BUTTON.centerx), "coordinate_y": (BUY_ITEM_NUM_FIVE_BUTTON.centery - 7), "current_frame" : 0, "max_frame" : 60})
				else:
					if click and BUY_ITEM_NUM_FIVE_BUTTON.collidepoint((mx, my)):
						item_sold = item_owned
						benefits = item_cost * item_sold
						inventory.town_gold += benefits
						inventory.town_storage[item_name] -= item_sold
						animations.append({"name" : "benefits", "value" : benefits, "current_frame" : 0, "max_frame" : 60})
						animations.append({"name" : "sold", "value" : item_sold, "coordinate_x": (BUY_ITEM_NUM_FIVE_BUTTON.centerx), "coordinate_y": (BUY_ITEM_NUM_FIVE_BUTTON.centery - 7), "current_frame" : 0, "max_frame" : 60})
						
		if (BUY_ITEM_NUM_SIX_BUTTON.collidepoint((mx, my)) or BUY_ITEM_NUM_SIX_BAND.collidepoint((mx,my))) and len(item_name_list) >= 6:
			item_name = item_name_list[5]
			item_cost,item_description,item_owned = selling_info(item_name)	
			if item_owned > 0:
				if stack_number != "Max":
					if click and BUY_ITEM_NUM_SIX_BUTTON.collidepoint((mx, my)):
						if stack_number >= item_owned:
							item_sold = item_owned
						else:
							item_sold = stack_number
						benefits = item_cost * item_sold
						inventory.town_gold += benefits
						inventory.town_storage[item_name] -= item_sold
						animations.append({"name" : "benefits", "value" : benefits, "current_frame" : 0, "max_frame" : 60})
						animations.append({"name" : "sold", "value" : item_sold, "coordinate_x": (BUY_ITEM_NUM_SIX_BUTTON.centerx), "coordinate_y": (BUY_ITEM_NUM_SIX_BUTTON.centery - 7), "current_frame" : 0, "max_frame" : 60})
				else:
					if click and BUY_ITEM_NUM_SIX_BUTTON.collidepoint((mx, my)):
						item_sold = item_owned
						benefits = item_cost * item_sold
						inventory.town_gold += benefits
						inventory.town_storage[item_name] -= item_sold
						animations.append({"name" : "benefits", "value" : benefits, "current_frame" : 0, "max_frame" : 60})
						animations.append({"name" : "sold", "value" : item_sold, "coordinate_x": (BUY_ITEM_NUM_SIX_BUTTON.centerx), "coordinate_y": (BUY_ITEM_NUM_SIX_BUTTON.centery - 7), "current_frame" : 0, "max_frame" : 60})
						
		if (BUY_ITEM_NUM_SEVEN_BUTTON.collidepoint((mx, my)) or BUY_ITEM_NUM_SEVEN_BAND.collidepoint((mx,my))) and len(item_name_list) >= 7:
			item_name = item_name_list[6]
			item_cost,item_description,item_owned = selling_info(item_name)	
			if item_owned > 0:
				if stack_number != "Max":
					if click and BUY_ITEM_NUM_SEVEN_BUTTON.collidepoint((mx, my)):
						if stack_number >= item_owned:
							item_sold = item_owned
						else:
							item_sold = stack_number
						benefits = item_cost * item_sold
						inventory.town_gold += benefits
						inventory.town_storage[item_name] -= item_sold
						animations.append({"name" : "benefits", "value" : benefits, "current_frame" : 0, "max_frame" : 60})
						animations.append({"name" : "sold", "value" : item_sold, "coordinate_x": (BUY_ITEM_NUM_SEVEN_BUTTON.centerx), "coordinate_y": (BUY_ITEM_NUM_SEVEN_BUTTON.centery - 7), "current_frame" : 0, "max_frame" : 60})
				else:
					if click and BUY_ITEM_NUM_SEVEN_BUTTON.collidepoint((mx, my)):
						item_sold = item_owned
						benefits = item_cost * item_sold
						inventory.town_gold += benefits
						inventory.town_storage[item_name] -= item_sold
						animations.append({"name" : "benefits", "value" : benefits, "current_frame" : 0, "max_frame" : 60})
						animations.append({"name" : "sold", "value" : item_sold, "coordinate_x": (BUY_ITEM_NUM_SEVEN_BUTTON.centerx), "coordinate_y": (BUY_ITEM_NUM_SEVEN_BUTTON.centery - 7), "current_frame" : 0, "max_frame" : 60})
						
		if (BUY_ITEM_NUM_EIGHT_BUTTON.collidepoint((mx, my)) or BUY_ITEM_NUM_EIGHT_BAND.collidepoint((mx,my))) and len(item_name_list) >= 8:
			item_name = item_name_list[7]
			item_cost,item_description,item_owned = selling_info(item_name)	
			if item_owned > 0:
				if stack_number != "Max":
					if click and BUY_ITEM_NUM_EIGHT_BUTTON.collidepoint((mx, my)):
						if stack_number >= item_owned:
							item_sold = item_owned
						else:
							item_sold = stack_number
						benefits = item_cost * item_sold
						inventory.town_gold += benefits
						inventory.town_storage[item_name] -= item_sold
						animations.append({"name" : "benefits", "value" : benefits, "current_frame" : 0, "max_frame" : 60})
						animations.append({"name" : "sold", "value" : item_sold, "coordinate_x": (BUY_ITEM_NUM_EIGHT_BUTTON.centerx), "coordinate_y": (BUY_ITEM_NUM_EIGHT_BUTTON.centery - 7), "current_frame" : 0, "max_frame" : 60})
				else:
					if click and BUY_ITEM_NUM_EIGHT_BUTTON.collidepoint((mx, my)):
						item_sold = item_owned
						benefits = item_cost * item_sold
						inventory.town_gold += benefits
						inventory.town_storage[item_name] -= item_sold
						animations.append({"name" : "benefits", "value" : benefits, "current_frame" : 0, "max_frame" : 60})
						animations.append({"name" : "sold", "value" : item_sold, "coordinate_x": (BUY_ITEM_NUM_EIGHT_BUTTON.centerx), "coordinate_y": (BUY_ITEM_NUM_EIGHT_BUTTON.centery - 7), "current_frame" : 0, "max_frame" : 60})
						
		if (BUY_ITEM_NUM_NINE_BUTTON.collidepoint((mx, my)) or BUY_ITEM_NUM_NINE_BAND.collidepoint((mx,my))) and len(item_name_list) >= 9:
			item_name = item_name_list[8]
			item_cost,item_description,item_owned = selling_info(item_name)	
			if item_owned > 0:
				if stack_number != "Max":
					if click and BUY_ITEM_NUM_NINE_BUTTON.collidepoint((mx, my)):
						if stack_number >= item_owned:
							item_sold = item_owned
						else:
							item_sold = stack_number
						benefits = item_cost * item_sold
						inventory.town_gold += benefits
						inventory.town_storage[item_name] -= item_sold
						animations.append({"name" : "benefits", "value" : benefits, "current_frame" : 0, "max_frame" : 60})
						animations.append({"name" : "sold", "value" : item_sold, "coordinate_x": (BUY_ITEM_NUM_NINE_BUTTON.centerx), "coordinate_y": (BUY_ITEM_NUM_NINE_BUTTON.centery - 7), "current_frame" : 0, "max_frame" : 60})
				else:
					if click and BUY_ITEM_NUM_NINE_BUTTON.collidepoint((mx, my)):
						item_sold = item_owned
						benefits = item_cost * item_sold
						inventory.town_gold += benefits
						inventory.town_storage[item_name] -= item_sold
						animations.append({"name" : "benefits", "value" : benefits, "current_frame" : 0, "max_frame" : 60})
						animations.append({"name" : "sold", "value" : item_sold, "coordinate_x": (BUY_ITEM_NUM_NINE_BUTTON.centerx), "coordinate_y": (BUY_ITEM_NUM_NINE_BUTTON.centery - 7), "current_frame" : 0, "max_frame" : 60})
						
		if (BUY_ITEM_NUM_TEN_BUTTON.collidepoint((mx, my)) or BUY_ITEM_NUM_TEN_BAND.collidepoint((mx,my))) and len(item_name_list) >= 10:
			item_name = item_name_list[9]
			item_cost,item_description,item_owned = selling_info(item_name)	
			if item_owned > 0:
				if stack_number != "Max":
					if click and BUY_ITEM_NUM_TEN_BUTTON.collidepoint((mx, my)):
						if stack_number >= item_owned:
							item_sold = item_owned
						else:
							item_sold = stack_number
						benefits = item_cost * item_sold
						inventory.town_gold += benefits
						inventory.town_storage[item_name] -= item_sold
						animations.append({"name" : "benefits", "value" : benefits, "current_frame" : 0, "max_frame" : 60})
						animations.append({"name" : "sold", "value" : item_sold, "coordinate_x": (BUY_ITEM_NUM_TEN_BUTTON.centerx), "coordinate_y": (BUY_ITEM_NUM_TEN_BUTTON.centery - 7), "current_frame" : 0, "max_frame" : 60})
				else:
					if click and BUY_ITEM_NUM_TEN_BUTTON.collidepoint((mx, my)):
						item_sold = item_owned
						benefits = item_cost * item_sold
						inventory.town_gold += benefits
						inventory.town_storage[item_name] -= item_sold
						animations.append({"name" : "benefits", "value" : benefits, "current_frame" : 0, "max_frame" : 60})
						animations.append({"name" : "sold", "value" : item_sold, "coordinate_x": (BUY_ITEM_NUM_TEN_BUTTON.centerx), "coordinate_y": (BUY_ITEM_NUM_TEN_BUTTON.centery - 7), "current_frame" : 0, "max_frame" : 60})
					
		for item in inventory.town_storage:
			if inventory.town_storage[item] == 0:
				sold_out.append(item)
		for item in sold_out:
			del inventory.town_storage[item]

		if BACK_BUTTON_TOP.collidepoint((mx, my)):
			if click:
				run = False

		click = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					run = False
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True

		in_selling_draw_window(item_name_list,item_number_list,stack_number,page,item_name,item_cost,item_description,item_owned,animations,storage)

def pre_upgrade_draw_window():
	BACKGROUND()
	pygame.draw.rect(screen, GRAY, TOP_BAND)
	check_party_text = font.render("Blacksmith", 1, BLACK)
	screen.blit(check_party_text, (TOP_BAND.centerx - check_party_text.get_width()//2, TOP_BAND.centery - check_party_text.get_height()//2))

	overall_text = None
	for ally in party.party:
		coordinate_x, coordinate_y = get_coordinate_new(ally,"party")
		overall_text = font.render(f"{ally.name} :", 1, BLACK)
		screen.blit(overall_text, (75, coordinate_y))

		overall_text = font.render(f"Armor type: {ally.armor_type}", 1, BLACK)
		screen.blit(overall_text, (75, coordinate_y + 25))
		overall_text = font.render(f"Weapon type: {ally.weapon_type}", 1, BLACK)
		screen.blit(overall_text, (75, coordinate_y + 50))
	
	if len(party.party) >= 1:
		pygame.draw.rect(screen, GRAY, FIRST_MEMBER_BUTTON)
		screen.blit(UPGRADE_IMAGE, (FIRST_MEMBER_BUTTON.x, FIRST_MEMBER_BUTTON.y))
	if len(party.party) >= 2:
		pygame.draw.rect(screen, GRAY, SECOND_MEMBER_BUTTON)
		screen.blit(UPGRADE_IMAGE, (SECOND_MEMBER_BUTTON.x, SECOND_MEMBER_BUTTON.y))
	if len(party.party) >= 3:
		pygame.draw.rect(screen, GRAY, THIRD_MEMBER_BUTTON)
		screen.blit(UPGRADE_IMAGE, (THIRD_MEMBER_BUTTON.x, THIRD_MEMBER_BUTTON.y))
	if len(party.party) == 4:
		pygame.draw.rect(screen, GRAY, FOURTH_MEMBER_BUTTON)
		screen.blit(UPGRADE_IMAGE, (FOURTH_MEMBER_BUTTON.x, FOURTH_MEMBER_BUTTON.y))

	pygame.draw.rect(screen, GRAY, BACK_BUTTON)
	back_button_text = font.render("Back", 1, BLACK)
	screen.blit(back_button_text, (BACK_BUTTON.centerx - back_button_text.get_width()//2, BACK_BUTTON.centery - back_button_text.get_height()//2))

	pygame.display.update()

def pre_upgrade():
	click = False
	run = True
	while run:
		clock.tick(60)
		mx, my = pygame.mouse.get_pos()
		
		if FIRST_MEMBER_BUTTON.collidepoint((mx, my)):
			if click and len(party.party) >= 1:
				in_upgrade(party.party[0])
		if SECOND_MEMBER_BUTTON.collidepoint((mx, my)):
			if click and len(party.party) >= 2:
				in_upgrade(party.party[1])
		if THIRD_MEMBER_BUTTON.collidepoint((mx, my)):
			if click and len(party.party) >= 3:
				in_upgrade(party.party[2])
		if FOURTH_MEMBER_BUTTON.collidepoint((mx, my)):
			if click and len(party.party) == 4:
				in_upgrade(party.party[3])

		if BACK_BUTTON.collidepoint((mx, my)):
			if click:
				run = False

		click = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					run = False
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True

		pre_upgrade_draw_window()


def in_upgrade_draw_window(ally,upgrade_category,upgrade_name,upgrade_cost,upgrade_description_1,upgrade_description_2,upgrade_description_3):
	BACKGROUND()
	pygame.draw.rect(screen, GRAY, TOP_BAND)
	context_text = font.render("Upgrade", 1, BLACK)
	screen.blit(context_text, (TOP_BAND.centerx - context_text.get_width()//2, TOP_BAND.centery - context_text.get_height()//2))

	name_text = font.render(f"{ally.name}", 1, BLACK)
	screen.blit(name_text, ( WIDTH//2 - name_text.get_width()//2, 100))

	town_gold_text = font.render(f"Gold : {inventory.town_gold}", 1, BLACK)
	screen.blit(town_gold_text, ( 15, 100))

	pygame.draw.rect(screen, GRAY, HELMET_UPGRADE_BUTTON)
	if ally.armor_type == "Warrior":
		if ally.helmet_tier == 1:
			screen.blit(WAR_HELMET_1_IMAGE, (HELMET_UPGRADE_BUTTON.x, HELMET_UPGRADE_BUTTON.y))
		if ally.helmet_tier == 2:
			screen.blit(WAR_HELMET_2_IMAGE, (HELMET_UPGRADE_BUTTON.x, HELMET_UPGRADE_BUTTON.y))
		if ally.helmet_tier == 3:
			screen.blit(WAR_HELMET_3_IMAGE, (HELMET_UPGRADE_BUTTON.x, HELMET_UPGRADE_BUTTON.y))
		if ally.helmet_tier == 4:
			screen.blit(WAR_HELMET_4_IMAGE, (HELMET_UPGRADE_BUTTON.x, HELMET_UPGRADE_BUTTON.y))
		if ally.helmet_tier == 5:
			screen.blit(WAR_HELMET_5_IMAGE, (HELMET_UPGRADE_BUTTON.x, HELMET_UPGRADE_BUTTON.y))
		if ally.helmet_tier == 6:
			screen.blit(WAR_HELMET_6_IMAGE, (HELMET_UPGRADE_BUTTON.x, HELMET_UPGRADE_BUTTON.y))
		if ally.helmet_tier == 7:
			screen.blit(WAR_HELMET_7_IMAGE, (HELMET_UPGRADE_BUTTON.x, HELMET_UPGRADE_BUTTON.y))
	pygame.draw.rect(screen, GRAY, CHEST_UPGRADE_BUTTON)
	if ally.armor_type == "Warrior":
		if ally.chest_tier == 1:
			screen.blit(WAR_CHEST_1_IMAGE, (CHEST_UPGRADE_BUTTON.x, CHEST_UPGRADE_BUTTON.y))
		if ally.chest_tier == 2:
			screen.blit(WAR_CHEST_2_IMAGE, (CHEST_UPGRADE_BUTTON.x, CHEST_UPGRADE_BUTTON.y))
		if ally.chest_tier == 3:
			screen.blit(WAR_CHEST_3_IMAGE, (CHEST_UPGRADE_BUTTON.x, CHEST_UPGRADE_BUTTON.y))
		if ally.chest_tier == 4:
			screen.blit(WAR_CHEST_4_IMAGE, (CHEST_UPGRADE_BUTTON.x, CHEST_UPGRADE_BUTTON.y))
		if ally.chest_tier == 5:
			screen.blit(WAR_CHEST_5_IMAGE, (CHEST_UPGRADE_BUTTON.x, CHEST_UPGRADE_BUTTON.y))
		if ally.chest_tier == 6:
			screen.blit(WAR_CHEST_6_IMAGE, (CHEST_UPGRADE_BUTTON.x, CHEST_UPGRADE_BUTTON.y))
		if ally.chest_tier == 7:
			screen.blit(WAR_CHEST_7_IMAGE, (CHEST_UPGRADE_BUTTON.x, CHEST_UPGRADE_BUTTON.y))
	pygame.draw.rect(screen, GRAY, LEGS_UPGRADE_BUTTON)
	if ally.armor_type == "Warrior":
		if ally.legs_tier == 1:
			screen.blit(WAR_LEGS_1_IMAGE, (LEGS_UPGRADE_BUTTON.x, LEGS_UPGRADE_BUTTON.y))
		if ally.legs_tier == 2:
			screen.blit(WAR_LEGS_2_IMAGE, (LEGS_UPGRADE_BUTTON.x, LEGS_UPGRADE_BUTTON.y))
		if ally.legs_tier == 3:
			screen.blit(WAR_LEGS_3_IMAGE, (LEGS_UPGRADE_BUTTON.x, LEGS_UPGRADE_BUTTON.y))
		if ally.legs_tier == 4:
			screen.blit(WAR_LEGS_4_IMAGE, (LEGS_UPGRADE_BUTTON.x, LEGS_UPGRADE_BUTTON.y))
		if ally.legs_tier == 5:
			screen.blit(WAR_LEGS_5_IMAGE, (LEGS_UPGRADE_BUTTON.x, LEGS_UPGRADE_BUTTON.y))
		if ally.legs_tier == 6:
			screen.blit(WAR_LEGS_6_IMAGE, (LEGS_UPGRADE_BUTTON.x, LEGS_UPGRADE_BUTTON.y))
		if ally.legs_tier == 7:
			screen.blit(WAR_LEGS_7_IMAGE, (LEGS_UPGRADE_BUTTON.x, LEGS_UPGRADE_BUTTON.y))
	pygame.draw.rect(screen, GRAY, FEET_UPGRADE_BUTTON)
	if ally.armor_type == "Warrior":
		if ally.feet_tier == 1:
			screen.blit(WAR_FEET_1_IMAGE, (FEET_UPGRADE_BUTTON.x, FEET_UPGRADE_BUTTON.y))
		if ally.feet_tier == 2:
			screen.blit(WAR_FEET_2_IMAGE, (FEET_UPGRADE_BUTTON.x, FEET_UPGRADE_BUTTON.y))
		if ally.feet_tier == 3:
			screen.blit(WAR_FEET_3_IMAGE, (FEET_UPGRADE_BUTTON.x, FEET_UPGRADE_BUTTON.y))
		if ally.feet_tier == 4:
			screen.blit(WAR_FEET_4_IMAGE, (FEET_UPGRADE_BUTTON.x, FEET_UPGRADE_BUTTON.y))
		if ally.feet_tier == 5:
			screen.blit(WAR_FEET_5_IMAGE, (FEET_UPGRADE_BUTTON.x, FEET_UPGRADE_BUTTON.y))
		if ally.feet_tier == 6:
			screen.blit(WAR_FEET_6_IMAGE, (FEET_UPGRADE_BUTTON.x, FEET_UPGRADE_BUTTON.y))
		if ally.feet_tier == 7:
			screen.blit(WAR_FEET_7_IMAGE, (FEET_UPGRADE_BUTTON.x, FEET_UPGRADE_BUTTON.y))
	pygame.draw.rect(screen, GRAY, GLOVES_UPGRADE_BUTTON)
	if ally.armor_type == "Warrior":
		if ally.gloves_tier == 1:
			screen.blit(WAR_GLOVES_1_IMAGE, (GLOVES_UPGRADE_BUTTON.x, GLOVES_UPGRADE_BUTTON.y))
		if ally.gloves_tier == 2:
			screen.blit(WAR_GLOVES_2_IMAGE, (GLOVES_UPGRADE_BUTTON.x, GLOVES_UPGRADE_BUTTON.y))
		if ally.gloves_tier == 3:
			screen.blit(WAR_GLOVES_3_IMAGE, (GLOVES_UPGRADE_BUTTON.x, GLOVES_UPGRADE_BUTTON.y))
		if ally.gloves_tier == 4:
			screen.blit(WAR_GLOVES_4_IMAGE, (GLOVES_UPGRADE_BUTTON.x, GLOVES_UPGRADE_BUTTON.y))
		if ally.gloves_tier == 5:
			screen.blit(WAR_GLOVES_5_IMAGE, (GLOVES_UPGRADE_BUTTON.x, GLOVES_UPGRADE_BUTTON.y))
		if ally.gloves_tier == 6:
			screen.blit(WAR_GLOVES_6_IMAGE, (GLOVES_UPGRADE_BUTTON.x, GLOVES_UPGRADE_BUTTON.y))
		if ally.gloves_tier == 7:
			screen.blit(WAR_GLOVES_7_IMAGE, (GLOVES_UPGRADE_BUTTON.x, GLOVES_UPGRADE_BUTTON.y))

	if ally.two_handed:
		pygame.draw.rect(screen, GRAY, WEAPON_TWO_HANDED_UPGRADE_BUTTON)
		if ally.weapon == "sword":
			if ally.weapon_tier == 1:
				screen.blit(TH_SWORD_1_IMAGE, (WEAPON_TWO_HANDED_UPGRADE_BUTTON.x, WEAPON_TWO_HANDED_UPGRADE_BUTTON.y))
			if ally.weapon_tier == 2:
				screen.blit(TH_SWORD_2_IMAGE, (WEAPON_TWO_HANDED_UPGRADE_BUTTON.x, WEAPON_TWO_HANDED_UPGRADE_BUTTON.y))
			if ally.weapon_tier == 3:
				screen.blit(TH_SWORD_3_IMAGE, (WEAPON_TWO_HANDED_UPGRADE_BUTTON.x, WEAPON_TWO_HANDED_UPGRADE_BUTTON.y))
			if ally.weapon_tier == 4:
				screen.blit(TH_SWORD_4_IMAGE, (WEAPON_TWO_HANDED_UPGRADE_BUTTON.x, WEAPON_TWO_HANDED_UPGRADE_BUTTON.y))
			if ally.weapon_tier == 5:
				screen.blit(TH_SWORD_5_IMAGE, (WEAPON_TWO_HANDED_UPGRADE_BUTTON.x, WEAPON_TWO_HANDED_UPGRADE_BUTTON.y))
			if ally.weapon_tier == 6:
				screen.blit(TH_SWORD_6_IMAGE, (WEAPON_TWO_HANDED_UPGRADE_BUTTON.x, WEAPON_TWO_HANDED_UPGRADE_BUTTON.y))
			if ally.weapon_tier == 7:
				screen.blit(TH_SWORD_7_IMAGE, (WEAPON_TWO_HANDED_UPGRADE_BUTTON.x, WEAPON_TWO_HANDED_UPGRADE_BUTTON.y))
	else:
		pygame.draw.rect(screen, GRAY, WEAPON_MAIN_HAND_UPGRADE_BUTTON)
		pygame.draw.rect(screen, GRAY, WEAPON_OFF_HAND_UPGRADE_BUTTON)

	pygame.draw.rect(screen, INTERMEDIATE_GRAY, UPGRADE_DESCRIPTION_BAND)
	if upgrade_category:
		upgrade_category_text = intermediate_font.render(f"{upgrade_category}:", 1, BLACK)
		screen.blit(upgrade_category_text, ( 10, UPGRADE_DESCRIPTION_BAND.top + 5))
	if upgrade_name:
		upgrade_name_text = intermediate_font.render(f"{upgrade_name}", 1, BLACK)
		screen.blit(upgrade_name_text, ( UPGRADE_DESCRIPTION_BAND.right - 25 - upgrade_name_text.get_width(), UPGRADE_DESCRIPTION_BAND.top + 5))
	if upgrade_cost:
		upgrade_cost_text = intermediate_font.render(f"Cost : {upgrade_cost} Gold", 1, BLACK)
		screen.blit(upgrade_cost_text, ( UPGRADE_DESCRIPTION_BAND.right - 25 - upgrade_cost_text.get_width(), UPGRADE_DESCRIPTION_BAND.top + 30))
	if upgrade_description_1:
		upgrade_description_1_text = intermediate_font.render(f"{upgrade_description_1}", 1, BLACK)
		screen.blit(upgrade_description_1_text, ( 50, UPGRADE_DESCRIPTION_BAND.y + 30))
	if upgrade_description_2:
		upgrade_description_2_text = intermediate_font.render(f"{upgrade_description_2}", 1, BLACK)
		screen.blit(upgrade_description_2_text, ( 50, UPGRADE_DESCRIPTION_BAND.y + 55))
	if upgrade_description_3:
		upgrade_description_3_text = intermediate_font.render(f"{upgrade_description_3}", 1, BLACK)
		screen.blit(upgrade_description_3_text, ( 50, UPGRADE_DESCRIPTION_BAND.y + 80))

	pygame.draw.rect(screen, GRAY, BACK_BUTTON_BIS_2)
	back_text = font.render("Back", 1, BLACK)
	screen.blit(back_text, ( BACK_BUTTON_BIS_2.centerx - back_text.get_width()//2, BACK_BUTTON_BIS_2.centery - back_text.get_height()//2))

	pygame.display.update()

def in_upgrade(ally):
	click = False
	run = True
	while run:
		clock.tick(60)
		mx, my = pygame.mouse.get_pos()
		upgrade_category = None
		upgrade_name = None
		upgrade_cost = None
		upgrade_description_1 = None
		upgrade_description_2 = None
		upgrade_description_3 = None

		if HELMET_UPGRADE_BUTTON.collidepoint((mx, my)):
			upgrade_category, upgrade_name, upgrade_cost, upgrade_description_1, upgrade_description_2, upgrade_description_3 = equipment_database(ally,"helmet")
			if click and ally.helmet_tier < 7 and inventory.town_gold >= upgrade_cost:
				ally.helmet_tier += 1
				inventory.town_gold -= upgrade_cost
			
		if CHEST_UPGRADE_BUTTON.collidepoint((mx, my)):
			upgrade_category, upgrade_name, upgrade_cost, upgrade_description_1, upgrade_description_2, upgrade_description_3 = equipment_database(ally,"chest")
			if click and ally.chest_tier < 7 and inventory.town_gold >= upgrade_cost:
				ally.chest_tier += 1
				inventory.town_gold -= upgrade_cost
			
		if LEGS_UPGRADE_BUTTON.collidepoint((mx, my)):
			upgrade_category, upgrade_name, upgrade_cost, upgrade_description_1, upgrade_description_2, upgrade_description_3 = equipment_database(ally,"legs")
			if click and ally.legs_tier < 7 and inventory.town_gold >= upgrade_cost:
				ally.legs_tier += 1
				inventory.town_gold -= upgrade_cost
			
		if FEET_UPGRADE_BUTTON.collidepoint((mx, my)):
			upgrade_category, upgrade_name, upgrade_cost, upgrade_description_1, upgrade_description_2, upgrade_description_3 = equipment_database(ally,"feet")
			if click and ally.feet_tier < 7 and inventory.town_gold >= upgrade_cost:
				ally.feet_tier += 1
				inventory.town_gold -= upgrade_cost
				
		if GLOVES_UPGRADE_BUTTON.collidepoint((mx, my)):
			upgrade_category, upgrade_name, upgrade_cost, upgrade_description_1, upgrade_description_2, upgrade_description_3 = equipment_database(ally,"gloves")
			if click and ally.gloves_tier < 7 and inventory.town_gold >= upgrade_cost:
				ally.gloves_tier += 1
				inventory.town_gold -= upgrade_cost
				
		if WEAPON_MAIN_HAND_UPGRADE_BUTTON.collidepoint((mx, my)) and ally.two_handed == False:
			if click:
				print("main hand")
				
		if WEAPON_OFF_HAND_UPGRADE_BUTTON.collidepoint((mx, my)) and ally.two_handed == False:
			if click:
				print("off hand")
				
		if WEAPON_TWO_HANDED_UPGRADE_BUTTON.collidepoint((mx, my)) and ally.two_handed:
			upgrade_category, upgrade_name, upgrade_cost, upgrade_description_1, upgrade_description_2, upgrade_description_3 = equipment_database(ally,"two handed weapon")
			if click and ally.weapon_tier < 7 and inventory.town_gold >= upgrade_cost:
				ally.weapon_tier += 1
				inventory.town_gold -= upgrade_cost
				
		if BACK_BUTTON_BIS_2.collidepoint((mx, my)):
			if click:
				run = False


		click = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					run = False
			if event.type == KEYDOWN:
				if event.key == K_SPACE:
					click = True
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True
		
		in_upgrade_draw_window(ally,upgrade_category,upgrade_name,upgrade_cost,upgrade_description_1,upgrade_description_2,upgrade_description_3)
	if ally.name == "Alex":
		alex_assign_bonus()

#################################
##### Statistics assignment #####

def claim_kill(user,target):
	if user.friendly:
		if target.hp == 0 or target.dead:
			user.enemy_killed += 1
			if target.specie == "goblin":
				user.goblin_killed += 1
			elif target.specie == "hobgoblin":
				user.hobgoblin_killed += 1

def consecutive_turn_survived(user):
	if user.friendly and user.dead == False:
		if user.hp/user.max_hp <= 0.1:
			if user.turn_survived_with_10percent_hp_tracker == 0 or user.turn_survived_with_10percent_hp_tracker == user.turn_count - 1:
				user.turn_survived_with_10percent_hp += 1
				print(user.turn_survived_with_10percent_hp)
				if user.turn_survived_with_10percent_hp >= 3:
					user.survivor = True
					print("survivor")

#############################
##### Titles assignment #####

def award_killer_titles(user):
	if user.enemy_killed >= 10:
		user.killer = True
		if user.enemy_killed >= 100:
			user.slaughterer = True
	if user.goblin_killed >= 10:
		user.goblin_killer = True
		if user.goblin_killed >= 100:
			user.goblin_bane = True
	if user.hobgoblin_killed >= 10:
		user.hobgoblin_killer = True

#######################
##### Bonus Stats #####

def reset_bonus_stats(target):
	target.max_hp = target.base_max_hp
	target.hp -= target.bonus_max_hp
	if target.hp <= 0:
		target.hp = 1
	target.bonus_max_hp = 0
	
	target.max_mp = target.base_max_mp
	target.mp -= target.bonus_max_mp
	if target.mp < 0:
		target.mp = 0
	target.bonus_max_mp = 0
	
	target.dmg = target.base_dmg
	target.bonus_dmg = 0
	target.bonus_dmg_multiplier = 1

	target.armor = target.base_armor
	target.bonus_armor = 0

	target.crit_chance = target.crit_chance_base
	target.crit_chance_bonus = 0

	target.defensive_roll = target.defensive_roll_base
	target.defensive_roll_bonus = 0

	target.crit_defensive_roll = target.crit_defensive_roll_bonus
	target.crit_defensive_roll_bonus = 0

	target.speed = target.speed_base
	target.speed_bonus = 0

	target.riposte = False

	target.passive_skill = []
	target.passive_skill_name = []
	target.learned_skill = []
	target.learned_skill_name = []
	target.skills_description.clear()

def assign_bonus_stats(target):
	target.max_hp = target.base_max_hp + target.bonus_max_hp
	target.hp += target.bonus_max_hp
	if target.hp > target.max_hp:
		target.hp = target.max_hp

	target.max_mp = target.base_max_mp + target.bonus_max_mp
	target.mp += target.bonus_max_mp
	if target.mp > target.max_mp:
		target.mp = target.max_mp

	target.armor = target.base_armor + target.bonus_armor

	target.dmg = (target.base_dmg + target.bonus_dmg) * target.bonus_dmg_multiplier

	target.crit_chance = target.crit_chance_base + target.crit_chance_bonus

	target.defensive_roll_chance = target.defensive_roll_base + target.defensive_roll_bonus

	target.crit_defensive_roll_chance = target.crit_defensive_roll_base + target.crit_defensive_roll_bonus

####################################
##### Mastery Bonus Assignment #####

def alex_assign_bonus():
	reset_bonus_stats(Alex)
	assign_equipment_bonus(Alex)
	if Alex.first_row_middle_passive:
		Alex.passive_skill.append(enraged_regeneration)
		Alex.passive_skill_name.append("Enraged Regeneration")
		Alex.skills_description["Enraged Regeneration"] = {
			"name" : "Enraged Regeneration",
			"category" : "Passive",
			"effect" : "Recover 5% max hp per turn while in combat",
			"description_lines" : 2,
			"description_1" : "Alex's battle rage sustains him",
			"description_2" : "keeping him in the fight. "
		}

	if Alex.second_row_left_passive:
		Alex.bonus_dmg += int(50 + 50 * (0.3 * (Alex.level - 1)))
	if Alex.second_row_middle_passive:
		Alex.bonus_armor += int(10 + 10 * (0.3 * (Alex.level - 1)))
	if Alex.second_row_right_passive:
		Alex.bonus_max_hp += int(200 + 200 * (0.3 * (Alex.level - 1)))

	if Alex.third_row_left_passive:
		Alex.learned_skill.append(can_multistrike)
		Alex.learned_skill_name.append("Multistrike")
		Alex.skills_description["Multistrike"] = {
			"name" : "Multistrike",
			"category" : "Active",
			"cost" : "5 mp",
			"effect" : "Deals 100% DMG to every enemy",
			"description_lines" : 2,
			"description_1" : "Alex quickly dash through the battlefield",
			"description_2" : "and strike every enemy. (can crit)",
			"cooldown" : "5 turns"
		}
	if Alex.third_row_middle_passive:
		Alex.riposte = True
		Alex.passive_skill_name.append("Riposte")
		Alex.skills_description["Riposte"] = {
			"name" : "Riposte",
			"category" : "Passive",
			"effect" : "Deals DMG depending on riposte strength stat",
			"description_lines" : 3,
			"description_1" : "On a succesfull critical defensive roll,",
			"description_2" : "perform a riposte instead of a dodge ",
			"description_3" : "dealing damage on the attacking enemy. (Cannot crit)"
		}
	if Alex.third_row_right_passive:
		Alex.defensive_roll_bonus += int(20 + 2 * (Alex.level - 1))

	if Alex.fourth_row_left_passive:
		Alex.crit_chance_bonus += int(30 + 3 * (Alex.level - 1))
	if Alex.fourth_row_middle_passive:
		Alex.learned_skill.append(can_warcry)
		Alex.learned_skill_name.append("Warcry")
		Alex.skills_description["Warcry"] = {
			"name" : "Warcry",
			"category" : "Active",
			"cost" : "100 Rage",
			"effect" : "Multiply user's damage 3x for 5 turns.",
			"description_lines" : 2,
			"description_1" : "Alex unleash a rage filled warcry",
			"description_2" : "dramatically increasing his physical damage",
			"description_3" : "for the next 5 turns.",
			"cooldown" : "10 turns"
		}
	if Alex.fourth_row_right_passive:
		Alex.crit_defensive_roll_bonus += int(10 + 1 * (Alex.level - 1))

	if Alex.fifth_row_left_passive:
		pass
	if Alex.fifth_row_middle_passive:
		pass
	if Alex.fifth_row_right_passive:
		pass


	assign_bonus_stats(Alex)


######################################
##### Equipment Bonus Assignment #####

def assign_equipment_bonus(ally):
	#weapons#
	if ally.two_handed:
		if ally.weapon == "sword":
			if ally.weapon_tier == 1:
				ally.bonus_dmg_multiplier = 1.1
				ally.bonus_dmg += 10
				ally.crit_defensive_roll_bonus += 2
			elif ally.weapon_tier == 2:
				ally.bonus_dmg_multiplier = 1.2
				ally.bonus_dmg += 25
				ally.crit_defensive_roll_bonus += 4
			elif ally.weapon_tier == 3:
				ally.bonus_dmg_multiplier = 1.3
				ally.bonus_dmg += 70
				ally.crit_defensive_roll_bonus += 6
			elif ally.weapon_tier == 4:
				ally.bonus_dmg_multiplier = 1.4
				ally.bonus_dmg += 200
				ally.crit_defensive_roll_bonus += 8
			elif ally.weapon_tier == 5:
				ally.bonus_dmg_multiplier = 1.5
				ally.bonus_dmg += 500
				ally.crit_defensive_roll_bonus += 10
			elif ally.weapon_tier == 6:
				ally.bonus_dmg_multiplier = 1.7
				ally.bonus_dmg += 1300
				ally.crit_defensive_roll_bonus += 12
			elif ally.weapon_tier == 7:
				ally.bonus_dmg_multiplier = 2
				ally.bonus_dmg += 3000
				ally.crit_defensive_roll_bonus += 15
		if ally.weapon == "spear":
			pass
	else:
		if ally.weapon == "sword":
			pass
		if ally.weapon == "shield":
			pass

	#armor#
	#warrior type#
	if ally.armor_type == "Warrior":
		if ally.helmet_tier == 1:
			ally.bonus_armor += 2
			ally.bonus_max_mp += 5
		if ally.helmet_tier == 2:
			ally.bonus_armor += 5
			ally.bonus_max_mp += 10
		if ally.helmet_tier == 3:
			ally.bonus_armor += 15
			ally.bonus_max_mp += 20
		if ally.helmet_tier == 4:
			ally.bonus_armor += 25
			ally.bonus_max_mp += 40
		if ally.helmet_tier == 5:
			ally.bonus_armor += 40
			ally.bonus_max_mp += 100
		if ally.helmet_tier == 6:
			ally.bonus_armor += 70
			ally.bonus_max_mp += 250
		if ally.helmet_tier == 7:
			ally.bonus_armor += 100
			ally.bonus_max_mp += 500

		if ally.chest_tier == 1:
			ally.bonus_armor += 5
			ally.bonus_max_hp += 25
		if ally.chest_tier == 2:
			ally.bonus_armor += 15
			ally.bonus_max_hp += 75
		if ally.chest_tier == 3:
			ally.bonus_armor += 40
			ally.bonus_max_hp += 200
		if ally.chest_tier == 4:
			ally.bonus_armor += 75
			ally.bonus_max_hp += 400
		if ally.chest_tier == 5:
			ally.bonus_armor += 125
			ally.bonus_max_hp += 700
		if ally.chest_tier == 6:
			ally.bonus_armor += 200
			ally.bonus_max_hp += 1200
		if ally.chest_tier == 7:
			ally.bonus_armor += 300
			ally.bonus_max_hp += 2000

		if ally.legs_tier == 1:
			ally.bonus_armor += 4
			ally.defensive_roll_bonus += 2
		if ally.legs_tier == 2:
			ally.bonus_armor += 12
			ally.defensive_roll_bonus += 5
		if ally.legs_tier == 3:
			ally.bonus_armor += 35
			ally.defensive_roll_bonus += 10
		if ally.legs_tier == 4:
			ally.bonus_armor += 65
			ally.defensive_roll_bonus += 15
		if ally.legs_tier == 5:
			ally.bonus_armor += 110
			ally.defensive_roll_bonus += 20
		if ally.legs_tier == 6:
			ally.bonus_armor += 170
			ally.defensive_roll_bonus += 25
		if ally.legs_tier == 7:
			ally.bonus_armor += 250
			ally.defensive_roll_bonus += 30

		if ally.feet_tier == 1:
			ally.armor += 1
			ally.speed += 3
		if ally.feet_tier == 2:
			ally.armor += 5
			ally.speed += 10
		if ally.feet_tier == 3:
			ally.armor += 10
			ally.speed += 25
		if ally.feet_tier == 4:
			ally.armor += 20
			ally.speed += 50
		if ally.feet_tier == 5:
			ally.armor += 30
			ally.speed += 90
		if ally.feet_tier == 6:
			ally.armor += 40
			ally.speed += 150
		if ally.feet_tier == 7:
			ally.armor += 50
			ally.speed += 225

		if ally.gloves_tier == 1:
			ally.armor += 1
			ally.crit_chance_bonus += 2
		if ally.gloves_tier == 2:
			ally.armor += 5
			ally.crit_chance_bonus += 5
		if ally.gloves_tier == 3:
			ally.armor += 10
			ally.crit_chance_bonus += 10
		if ally.gloves_tier == 4:
			ally.armor += 20
			ally.crit_chance_bonus += 17
		if ally.gloves_tier == 5:
			ally.armor += 30
			ally.crit_chance_bonus += 25
		if ally.gloves_tier == 6:
			ally.armor += 40
			ally.crit_chance_bonus += 32
		if ally.gloves_tier == 7:
			ally.armor += 50
			ally.crit_chance_bonus += 40

	elif armor_type == "Archer":
		pass


######################
###### Fighting ######
######################

#########################
###### Fight Class ######

class fighting_base():
	turn_count = 0
	battle_order = []
	victory = False
	defeat = False

	playing = None
	target = []

	ally_1 = None
	ally_2 = None
	ally_3 = None
	ally_4 = None

	enemy_1 = None
	enemy_2 = None
	enemy_3 = None
	enemy_4 = None

	animations = []

	battle_order_done = False
	effects_tick_done = False
	effect_tick_proc = False
	effect_tick_list = []
	effects_end_done = False
	effect_end_proc = False

	goddess_power = 0
	goddess_turn = False


##############################################
##### Universal Battle Related Functions #####

def check_for_death():
	party.party_alive = []
	party.party_dead = []
	party.number_of_ally_alive = 0
	enemy_party.enemy_alive = []
	enemy_party.enemy_dead = []

	for ally in party.party:
		if ally.hp <= 0 or ally.dead:
			ally.dead = True
			party.party_dead.append(ally)
		else:
			party.party_alive.append(ally)
			party.number_of_ally_alive += 1
	
	for enemy in enemy_party.enemy_list:
		if enemy.hp <= 0 or enemy.dead:
			enemy.dead = True
			enemy.killed_by = enemy.last_attacked_by
			enemy_party.enemy_dead.append(enemy)
		else:
			enemy_party.enemy_alive.append(enemy)


def get_coordinate_new(target,type):
	coordinate_x, coordinate_y = None, None
	if type == "dmg":
		if target.friendly:
			if target == fighting.ally_1:
				coordinate_x = FIRST_EMPLACEMENT_ALLY_HP_BACKGROUND.right + 3
				coordinate_y = FIRST_EMPLACEMENT_ALLY_HP_BACKGROUND.top
			elif target == fighting.ally_2:
				coordinate_x = SECOND_EMPLACEMENT_ALLY_HP_BACKGROUND.right + 3
				coordinate_y = SECOND_EMPLACEMENT_ALLY_HP_BACKGROUND.top
			elif target == fighting.ally_3:
				coordinate_x = THIRD_EMPLACEMENT_ALLY_HP_BACKGROUND.right + 3
				coordinate_y = THIRD_EMPLACEMENT_ALLY_HP_BACKGROUND.top
			elif target == fighting.ally_4:
				coordinate_x = FOURTH_EMPLACEMENT_ALLY_HP_BACKGROUND.right + 3
				coordinate_y = FOURTH_EMPLACEMENT_ALLY_HP_BACKGROUND.top
		else:
			if target == fighting.enemy_1:
				coordinate_x = FIRST_EMPLACEMENT_ENY_HP_BACKGROUND.left - 3
				coordinate_y = FIRST_EMPLACEMENT_ENY_HP_BACKGROUND.top
			if target == fighting.enemy_2:
				coordinate_x = SECOND_EMPLACEMENT_ENY_HP_BACKGROUND.left - 3
				coordinate_y = SECOND_EMPLACEMENT_ENY_HP_BACKGROUND.top
			if target == fighting.enemy_3:
				coordinate_x = THIRD_EMPLACEMENT_ENY_HP_BACKGROUND.left - 3
				coordinate_y = THIRD_EMPLACEMENT_ENY_HP_BACKGROUND.top
			if target == fighting.enemy_4:
				coordinate_x = FOURTH_EMPLACEMENT_ENY_HP_BACKGROUND.left - 3
				coordinate_y = FOURTH_EMPLACEMENT_ENY_HP_BACKGROUND.top
				
	if type == "heal":
		if target.friendly:
			if target == fighting.ally_1:
				coordinate_x = FIRST_EMPLACEMENT_ALLY_HP_BACKGROUND.right + 3
				coordinate_y = FIRST_EMPLACEMENT_ALLY_HP_BACKGROUND.top
			elif target == fighting.ally_2:
				coordinate_x = SECOND_EMPLACEMENT_ALLY_HP_BACKGROUND.right + 3
				coordinate_y = SECOND_EMPLACEMENT_ALLY_HP_BACKGROUND.top
			elif target == fighting.ally_3:
				coordinate_x = THIRD_EMPLACEMENT_ALLY_HP_BACKGROUND.right + 3
				coordinate_y = THIRD_EMPLACEMENT_ALLY_HP_BACKGROUND.top
			elif target == fighting.ally_4:
				coordinate_x = FOURTH_EMPLACEMENT_ALLY_HP_BACKGROUND.right + 3
				coordinate_y = FOURTH_EMPLACEMENT_ALLY_HP_BACKGROUND.top
		else:
			if target == fighting.enemy_1:
				coordinate_x = FIRST_EMPLACEMENT_ENY_HP_BACKGROUND.left - 3
				coordinate_y = FIRST_EMPLACEMENT_ENY_HP_BACKGROUND.top
			if target == fighting.enemy_2:
				coordinate_x = SECOND_EMPLACEMENT_ENY_HP_BACKGROUND.left - 3
				coordinate_y = SECOND_EMPLACEMENT_ENY_HP_BACKGROUND.top
			if target == fighting.enemy_3:
				coordinate_x = THIRD_EMPLACEMENT_ENY_HP_BACKGROUND.left - 3
				coordinate_y = THIRD_EMPLACEMENT_ENY_HP_BACKGROUND.top
			if target == fighting.enemy_4:
				coordinate_x = FOURTH_EMPLACEMENT_ENY_HP_BACKGROUND.left - 3
				coordinate_y = FOURTH_EMPLACEMENT_ENY_HP_BACKGROUND.top

	if type == "attacker":
		if target.friendly:
			if target == fighting.ally_1:
				coordinate_x = FIRST_EMPLACEMENT_ALLY.right - 15
				coordinate_y = FIRST_EMPLACEMENT_ALLY.top - 15
			elif target == fighting.ally_2:
				coordinate_x = SECOND_EMPLACEMENT_ALLY.right - 15
				coordinate_y = SECOND_EMPLACEMENT_ALLY.top - 15
			elif target == fighting.ally_3:
				coordinate_x = THIRD_EMPLACEMENT_ALLY.right - 15
				coordinate_y = THIRD_EMPLACEMENT_ALLY.top - 15
			elif target == fighting.ally_4:
				coordinate_x = FOURTH_EMPLACEMENT_ALLY.right - 15
				coordinate_y = FOURTH_EMPLACEMENT_ALLY.top - 15
		else:
			if target == fighting.enemy_1:
				coordinate_x = FIRST_EMPLACEMENT_ENY.left - 15
				coordinate_y = FIRST_EMPLACEMENT_ENY.top - 15
			if target == fighting.enemy_2:
				coordinate_x = SECOND_EMPLACEMENT_ENY.left - 15
				coordinate_y = SECOND_EMPLACEMENT_ENY.top - 15
			if target == fighting.enemy_3:
				coordinate_x = THIRD_EMPLACEMENT_ENY.left - 15
				coordinate_y = THIRD_EMPLACEMENT_ENY.top - 15
			if target == fighting.enemy_4:
				coordinate_x = FOURTH_EMPLACEMENT_ENY.left - 15
				coordinate_y = FOURTH_EMPLACEMENT_ENY.top - 15
				
	if type == "defender":
		if target.friendly:
			if target == fighting.ally_1:
				coordinate_x = FIRST_EMPLACEMENT_ALLY.right - 15
				coordinate_y = FIRST_EMPLACEMENT_ALLY.top - 15
			elif target == fighting.ally_2:
				coordinate_x = SECOND_EMPLACEMENT_ALLY.right - 15
				coordinate_y = SECOND_EMPLACEMENT_ALLY.top - 15
			elif target == fighting.ally_3:
				coordinate_x = THIRD_EMPLACEMENT_ALLY.right - 15
				coordinate_y = THIRD_EMPLACEMENT_ALLY.top - 15
			elif target == fighting.ally_4:
				coordinate_x = FOURTH_EMPLACEMENT_ALLY.right - 15
				coordinate_y = FOURTH_EMPLACEMENT_ALLY.top - 15
		else:
			if target == fighting.enemy_1:
				coordinate_x = FIRST_EMPLACEMENT_ENY.left - 15
				coordinate_y = FIRST_EMPLACEMENT_ENY.top - 15
			if target == fighting.enemy_2:
				coordinate_x = SECOND_EMPLACEMENT_ENY.left - 15
				coordinate_y = SECOND_EMPLACEMENT_ENY.top - 15
			if target == fighting.enemy_3:
				coordinate_x = THIRD_EMPLACEMENT_ENY.left - 15
				coordinate_y = THIRD_EMPLACEMENT_ENY.top - 15
			if target == fighting.enemy_4:
				coordinate_x = FOURTH_EMPLACEMENT_ENY.left - 15
				coordinate_y = FOURTH_EMPLACEMENT_ENY.top - 15
				
	if type == "death":
		if target.friendly:
			if target == fighting.ally_1:
				coordinate_x = FIRST_EMPLACEMENT_ALLY.centerx
				coordinate_y = FIRST_EMPLACEMENT_ALLY.bottom
			elif target == fighting.ally_2:
				coordinate_x = SECOND_EMPLACEMENT_ALLY.centerx
				coordinate_y = SECOND_EMPLACEMENT_ALLY.bottom
			elif target == fighting.ally_3:
				coordinate_x = THIRD_EMPLACEMENT_ALLY.centerx
				coordinate_y = THIRD_EMPLACEMENT_ALLY.bottom
			elif target == fighting.ally_4:
				coordinate_x = FOURTH_EMPLACEMENT_ALLY.centerx
				coordinate_y = FOURTH_EMPLACEMENT_ALLY.bottom
		else:
			if target == fighting.enemy_1:
				coordinate_x = FIRST_EMPLACEMENT_ENY.centerx
				coordinate_y = FIRST_EMPLACEMENT_ENY.bottom
			if target == fighting.enemy_2:
				coordinate_x = SECOND_EMPLACEMENT_ENY.centerx
				coordinate_y = SECOND_EMPLACEMENT_ENY.bottom
			if target == fighting.enemy_3:
				coordinate_x = THIRD_EMPLACEMENT_ENY.centerx
				coordinate_y = THIRD_EMPLACEMENT_ENY.bottom
			if target == fighting.enemy_4:
				coordinate_x = FOURTH_EMPLACEMENT_ENY.centerx
				coordinate_y = FOURTH_EMPLACEMENT_ENY.bottom
				
	if type == "skill icon":
		if target.friendly:
			if target == fighting.ally_1:
				coordinate_x = FIRST_EMPLACEMENT_ALLY_HP_BACKGROUND.centerx
				coordinate_y = FIRST_EMPLACEMENT_ALLY_HP_BACKGROUND.centery
			elif target == fighting.ally_2:
				coordinate_x = SECOND_EMPLACEMENT_ALLY_HP_BACKGROUND.centerx
				coordinate_y = SECOND_EMPLACEMENT_ALLY_HP_BACKGROUND.centery
			elif target == fighting.ally_3:
				coordinate_x = THIRD_EMPLACEMENT_ALLY_HP_BACKGROUND.centerx
				coordinate_y = THIRD_EMPLACEMENT_ALLY_HP_BACKGROUND.centery
			elif target == fighting.ally_4:
				coordinate_x = FOURTH_EMPLACEMENT_ALLY_HP_BACKGROUND.centerx
				coordinate_y = FOURTH_EMPLACEMENT_ALLY_HP_BACKGROUND.centery
		else:
			if target == fighting.enemy_1:
				coordinate_x = FIRST_EMPLACEMENT_ENY_HP_BACKGROUND.centerx
				coordinate_y = FIRST_EMPLACEMENT_ENY_HP_BACKGROUND.centery
			if target == fighting.enemy_2:
				coordinate_x = SECOND_EMPLACEMENT_ENY_HP_BACKGROUND.centerx
				coordinate_y = SECOND_EMPLACEMENT_ENY_HP_BACKGROUND.centery
			if target == fighting.enemy_3:
				coordinate_x = THIRD_EMPLACEMENT_ENY_HP_BACKGROUND.centerx
				coordinate_y = THIRD_EMPLACEMENT_ENY_HP_BACKGROUND.centery
			if target == fighting.enemy_4:
				coordinate_x = FOURTH_EMPLACEMENT_ENY_HP_BACKGROUND.centerx
				coordinate_y = FOURTH_EMPLACEMENT_ENY_HP_BACKGROUND.centery

	if type == "party":
		if party.party.index(target) + 1 == 1:
			coordinate_x = FIRST_EMPLACEMENT_ALLY.centerx
			coordinate_y = FIRST_EMPLACEMENT_ALLY.centery + 20
		elif party.party.index(target) + 1 == 2:
			coordinate_x = SECOND_EMPLACEMENT_ALLY.centerx
			coordinate_y = SECOND_EMPLACEMENT_ALLY.centery + 20
		elif party.party.index(target) + 1 == 3:
			coordinate_x = THIRD_EMPLACEMENT_ALLY.centerx
			coordinate_y = THIRD_EMPLACEMENT_ALLY.centery + 20
		elif party.party.index(target) + 1 == 4:
			coordinate_x = FOURTH_EMPLACEMENT_ALLY.centerx
			coordinate_y = FOURTH_EMPLACEMENT_ALLY.centery + 20

	return coordinate_x, coordinate_y

#################################
##### Pre Battle Operations #####

def pre_battle():
	fighting.victory = False
	fighting.defeat = False

	enemy_party.number_of_enemy = rand.randint(1,4)
	enemy_party.number_of_enemy_alive = enemy_party.number_of_enemy

	enemy_party.enemy_list = []
	for i in range(enemy_party.number_of_enemy):
		chosen_enemy = rand.choice(dungeon.floor_monsterpedia)
		enemy_party.enemy_list.append(chosen_enemy(i+1))
	
	check_for_death()

	fighting.enemy_1 = enemy_party.enemy_alive[0]
	if enemy_party.number_of_enemy >= 2:
		fighting.enemy_2 = enemy_party.enemy_alive[1]
	if enemy_party.number_of_enemy >= 3:
		fighting.enemy_3 = enemy_party.enemy_alive[2]
	if enemy_party.number_of_enemy >= 4:
		fighting.enemy_4 = enemy_party.enemy_alive[3]

	fighting.ally_1 = party.party_alive[0]
	if party.number_of_ally_alive >= 2:
		fighting.ally_2 = party.party_alive[1]
	if party.number_of_ally_alive >= 3:
		fighting.ally_3 = party.party_alive[2]
	if party.number_of_ally_alive >=4:
		fighting.ally_4 = party.party_alive[3]

	all_combattant_list = party.party_alive + enemy_party.enemy_alive
	number_of_combattant = len(all_combattant_list)
	while number_of_combattant != 0:
		temp_selected = all_combattant_list[0]
		for each in all_combattant_list:
			if each.speed > temp_selected.speed:
				temp_selected = each
		fighting.battle_order.append(temp_selected)
		all_combattant_list.remove(temp_selected)
		number_of_combattant = len(all_combattant_list)

def in_pre_battle_draw_window():
	BACKGROUND()
	pygame.draw.rect(screen, GRAY, TOP_BAND)
	context_text = font.render("Pre-Battle", 1, BLACK)
	screen.blit(context_text, (TOP_BAND.centerx - context_text.get_width()//2, TOP_BAND.centery - context_text.get_height()//2))

	prepare_to_fight_text = font.render("Prepare for battle !", 1, BLACK)
	screen.blit(prepare_to_fight_text, (WIDTH//2 - prepare_to_fight_text.get_width()//2, 100))
	enemy_composition_text = intermediate_font.render("Enemy Party Composition :", 1, BLACK)
	screen.blit(enemy_composition_text, (30, 130))
	
	pygame.draw.rect(screen, INTERMEDIATE_GRAY, PRE_BATTLE_BOTTOM_BAND)
	pygame.draw.rect(screen, GRAY, PRE_BATTLE_FIGHT_BUTTON)
	explore_text = intermediate_font.render("Fight", 1, BLACK)
	screen.blit(explore_text, (PRE_BATTLE_FIGHT_BUTTON.centerx - explore_text.get_width()//2, PRE_BATTLE_FIGHT_BUTTON.centery - explore_text.get_height()//2))
	pygame.draw.rect(screen, GRAY, PRE_BATTLE_FLEE_BUTTON)
	farm_text = intermediate_font.render("Flee", 1, BLACK)
	screen.blit(farm_text, (PRE_BATTLE_FLEE_BUTTON.centerx - farm_text.get_width()//2, PRE_BATTLE_FLEE_BUTTON.centery - farm_text.get_height()//2))
	pygame.draw.rect(screen, GRAY, PRE_BATTLE_AMBUSH_BUTTON)
	sneak_text = intermediate_font.render("Ambush", 1, BLACK)
	screen.blit(sneak_text, (PRE_BATTLE_AMBUSH_BUTTON.centerx - sneak_text.get_width()//2, PRE_BATTLE_AMBUSH_BUTTON.centery - sneak_text.get_height()//2))
	pygame.draw.rect(screen, GRAY, PRE_BATTLE_AVOID_BUTTON)
	return_text = intermediate_font.render("Avoid", 1, BLACK)
	screen.blit(return_text, (PRE_BATTLE_AVOID_BUTTON.centerx - return_text.get_width()//2, PRE_BATTLE_AVOID_BUTTON.centery - return_text.get_height()//2))

	already_done = []
	offset = 0
	for type in dungeon.floor_monsterpedia:
		temp = type.specie
		count = 0
		if temp in already_done:
			pass
		else:
			already_done.append(temp)
			for enemy in enemy_party.enemy_list:
				if temp == enemy.specie:
					count += 1
			if count == 1:
				eny_announcer_text = font.render(f"{count} {type.specie}", 1, BLACK)
				screen.blit(eny_announcer_text, (30, 150 + offset))
				offset += 20
			elif count > 1:
				eny_announcer_text = font.render(f"{count} {type.specie}s", 1, BLACK)
				screen.blit(eny_announcer_text, (30, 150 + offset))
				offset += 20
	pygame.display.update()

def in_pre_battle():
	pre_battle()
	click = False
	run = True
	while run:
		clock.tick(60)
		mx, my = pygame.mouse.get_pos()

		if PRE_BATTLE_FIGHT_BUTTON.collidepoint((mx, my)):
			if click:
				run = False
		if PRE_BATTLE_FLEE_BUTTON.collidepoint((mx, my)):
			if click:
				pass
		if PRE_BATTLE_AMBUSH_BUTTON.collidepoint((mx, my)):
			if click:
				pass
		if PRE_BATTLE_AVOID_BUTTON.collidepoint((mx, my)):
			if click:
				pass

		click = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				dungeon.run = False
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_SPACE:
					run = False
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True
		
		in_pre_battle_draw_window()

###################
###### Fight ######

#################################
##### One Turn Operations #####

def generate_skill_description(name,description):
	skill_description_animation = {"name" : name, "type" : "skill description", "description" : description, "max_frame" : 90, "current_frame" : 0, "buffer_frame" : 30}
	fighting.animations.append(skill_description_animation)
	
def generate_skill_icon(icon):
	skill_icon_animation = {"type" : "skill icon", "icon" : icon, "user" : fighting.playing, "max_frame" : 75, "current_frame" : 0, "buffer_frame" : 30}
	fighting.animations.append(skill_icon_animation)

def generate_dmg_animation(target,value):
	dmg_animation = {"type" : "dmg", "value" : value, "user" : fighting.playing, "target" : target, "max_frame" : 90, "current_frame" : 0, "buffer_frame" : 30}
	fighting.animations.append(dmg_animation)

def generate_crit_dmg_animation(target,value):
	crit_dmg_animation = {"type" : "crit dmg", "value" : value, "user" : fighting.playing, "target" : target, "max_frame" : 90, "current_frame" : 0, "buffer_frame" : 30}
	fighting.animations.append(crit_dmg_animation)

def generate_riposte_animation(target,value):
	riposte_animation = {"type" : "dmg", "value" : value, "user" : target, "target" : fighting.playing, "max_frame" : 90, "current_frame" : 0, "buffer_frame" : 30}
	fighting.animations.append(riposte_animation)

def generate_dodge_animation(target,value):
	dodge_animation = {"type" : "dodge", "value" : value, "user" : fighting.playing, "target" : target, "max_frame" : 90, "current_frame" : 0, "buffer_frame" : 30}
	fighting.animations.append(dodge_animation)
	
def generate_parry_animation(target,value):
	parry_animation = {"type" : "dmg", "value" : value, "user" : fighting.playing, "target" : target, "max_frame" : 90, "current_frame" : 0, "buffer_frame" : 30}
	fighting.animations.append(parry_animation)

def generate_heal_animation(target,value):
	heal_animation = {"type" : "heal", "value" : value, "target" : target, "max_frame" : 90, "current_frame" : 0, "buffer_frame" : 30}
	fighting.animations.append(heal_animation)

def generate_death_animation(target):
	death_animation = {"type" : "death", "target" : target, "max_frame" : 90, "current_frame" : 0}
	fighting.animations.append(death_animation)

def generic_effects_draw_window():
	wait = False
	for animation in fighting.animations:
		if animation["type"] == "wait":
			animation["current_frame"] += 1
			if animation["max_frame"] == animation["current_frame"]:
				fighting.animations.remove(animation)
			wait = True

	if wait == False:
		for animation in fighting.animations:
			if animation["type"] == "skill description":
				name_text = font.render(animation["name"], 1, BLACK)
				screen.blit(name_text, ( SKILL_BAND.centerx - name_text.get_width()//2, SKILL_BAND.y + 5))
				skill_text = font.render(animation["description"], 1, BLACK)
				screen.blit(skill_text, ( 10, SKILL_BAND.centery))
				
			if animation["type"] == "skill icon":
				coordinate_x, coordinate_y = get_coordinate_new(animation["user"],"skill icon")
				icon = animation["icon"]
				if animation["current_frame"] <= 5:
					icon = pygame.transform.scale(icon,( 50//5 * animation["current_frame"], 50//5 * animation["current_frame"]))
				elif animation["max_frame"] - animation["current_frame"] <= 5:
					icon = pygame.transform.scale(icon,( 50//5 * (-(animation["current_frame"] - animation["max_frame"])), 50//5 * (-(animation["current_frame"] - animation["max_frame"]))))
				if animation["user"].friendly:
					screen.blit(icon, (coordinate_x - animation["icon"].get_width()//2, coordinate_y - animation["icon"].get_height()//2))
				else:
					screen.blit(icon, (coordinate_x - animation["icon"].get_width()//2, coordinate_y - animation["icon"].get_height()//2))

			if animation["type"] == "dmg":
				coordinate_x, coordinate_y = get_coordinate_new(animation["target"],"dmg")
				dmg_text = intermediate_font.render(f"- {animation['value']}", 1, RED)
				if animation["target"].friendly:
					screen.blit(dmg_text, (coordinate_x, coordinate_y - animation["current_frame"]/6))
				else:
					screen.blit(dmg_text, (coordinate_x - dmg_text.get_width(), coordinate_y - animation["current_frame"]/6))
				
			if animation["type"] == "crit dmg":
				coordinate_x, coordinate_y = get_coordinate_new(animation["target"],"dmg")
				crit_dmg_text = font.render(f"- {animation['value']}", 1, FIRE)
				if animation["target"].friendly:
					screen.blit(crit_dmg_text, (coordinate_x, coordinate_y - animation["current_frame"]/6))
				else:
					screen.blit(crit_dmg_text, (coordinate_x - crit_dmg_text.get_width(), coordinate_y - animation["current_frame"]/6))
			
			if animation["type"] == "heal":
				coordinate_x, coordinate_y = get_coordinate_new(animation["target"],"heal")
				heal_text = intermediate_font.render(f"- {animation['value']}", 1, GREEN)
				if animation["target"].friendly:
					screen.blit(heal_text, (coordinate_x, coordinate_y - animation["current_frame"]/6))
				else:
					screen.blit(heal_text, (coordinate_x - heal_text.get_width(), coordinate_y - animation["current_frame"]/6))
				
			if animation["type"] == "dodge":
				coordinate_x, coordinate_y = get_coordinate_new(animation["target"],"dmg")
				dmg_text = intermediate_font.render(f"- {animation['value']}", 1, METAL)
				if animation["target"].friendly:
					screen.blit(dmg_text, (coordinate_x, coordinate_y - animation["current_frame"]/6))
				else:
					screen.blit(dmg_text, (coordinate_x - dmg_text.get_width(), coordinate_y - animation["current_frame"]/6))

			if animation["type"] == "attacker":
				coordinate_x, coordinate_y = get_coordinate_new(animation["target"],"attacker")
				screen.blit(ATTACKER_IMAGE, (coordinate_x, coordinate_y))

			if animation["type"] == "defender":
				coordinate_x, coordinate_y = get_coordinate_new(animation["target"],"defender")
				screen.blit(DEFENDER_IMAGE, (coordinate_x, coordinate_y))
				
			if animation["type"] == "death":
				coordinate_x, coordinate_y = get_coordinate_new(animation["target"],"death")
				screen.blit(DEATH_IMAGE, (coordinate_x - DEATH_IMAGE.get_width()//2, coordinate_y - DEATH_IMAGE.get_height()))
				if animation["current_frame"] == 0:			
					death_sfx.play()
					death_sfx.set_volume(0.5)
			
			animation["current_frame"] += 1
			if animation["max_frame"] == animation["current_frame"]:
				fighting.animations.remove(animation)

def attacker_animation(playing):
	attacker_animation = {"type" : "attacker", "target" : playing, "max_frame" : 90, "current_frame" : 0}
	fighting.animations.append(attacker_animation)

def defender_animation(target):
	defender_animation = {"type" : "defender", "target" : target, "max_frame" : 90, "current_frame" : 0}
	fighting.animations.append(defender_animation)

def one_turn_fight_phase_one():
	if fighting.battle_order_done == False:
		fighting.target = []
		if fighting.goddess_power == 100:
			fighting.goddess_turn = True
			fighting.goddess_power = 0
			fighting.playing = "goddess"
			fighting.effects_tick_done = True
			fighting.effects_end_done = True
		else:			
			fighting.goddess_power += 50
			if fighting.goddess_power > 100:
				fighting.goddess_power = 100
			playing = fighting.battle_order[0]
			fighting.battle_order.remove(playing)
			fighting.battle_order.append(playing)
			playing.turn_count += 1
			if playing.friendly:
				playing.global_turn_count += 1

			for fighter in fighting.battle_order:
				if fighter.turn_count > fighting.turn_count:
					fighting.turn_count += 1
			fighting.playing = playing
		fighting.battle_order_done = True

	if fighting.effects_tick_done == False:
		effects_tick(fighting.playing)
		if fighting.effect_tick_proc == False:
			fighting.effects_tick_done = True
			fighting.effect_tick_list = []

	if fighting.effects_end_done == False and fighting.effects_tick_done:
		effects_end(fighting.playing)
		if fighting.effect_end_proc == False:
			fighting.effects_end_done = True

	if fighting.animations != []:
		attacker_animation(fighting.playing)

	if fighting.effects_end_done and fighting.effects_tick_done:
		fighting.battle_order_done = False
		fighting.effects_tick_done = False
		fighting.effects_end_done = False
		return True
	else:
		return False

def one_turn_fight_phase_two():
	attacker_animation(fighting.playing)

	#check available skills
	skill_list_reset()
	skill_checker()
	#choose if skill or attack
	if fighting.playing.friendly:
		fighting.playing.behaviour()
	else:
		fighting.playing.casting_skill = attack
	fighting.playing.casting_skill()


def one_turn_fight_phase_three():
	temp_ally_dead = []
	for ally in party.party_alive:
		if ally.dead or ally.hp <= 0:
			ally.dead = True
			generate_death_animation(ally)
			clear_all_effects(ally)
			fighting.battle_order.remove(ally)
			temp_ally_dead.append(ally)

	for ally in temp_ally_dead:
		party.party_alive.remove(ally)
		party.party_dead.append(ally)
		party.number_of_ally_alive -= 1

	if party.number_of_ally_alive == 0 or party.party_alive == []:
		fighting.defeat = True


	temp_enemy_dead = []
	for enemy in enemy_party.enemy_alive:
		if enemy.dead or enemy.hp <= 0:
			enemy.dead = True
			generate_death_animation(enemy)
			clear_all_effects(enemy)
			fighting.battle_order.remove(enemy)
			temp_enemy_dead.append(enemy)

	for enemy in temp_enemy_dead:
		enemy_party.enemy_alive.remove(enemy)
		enemy_party.enemy_dead.append(enemy)
		enemy_party.number_of_enemy_alive -= 1

	if enemy_party.number_of_enemy_alive == 0 or enemy_party.enemy_alive == []:
		fighting.victory = True

	

#################################
##### In Battle Operations #####

def before_first_turn():
	for enemy in enemy_party.enemy_alive:
		apply_passive_effects(enemy)
	for ally in party.party:
		ally.turn_count = 0
	fighting.turn_count = 0
	time_before_first_attack = {"type" : "wait", "max_frame" : 90, "current_frame" : 0}
	fighting.animations.append(time_before_first_attack)
	play_battle_music()

def in_fight_draw_window():
	BACKGROUND()

	turn_count_text = intermediate_font.render(f"Turn : {fighting.turn_count}", 1, BLACK)
	screen.blit(turn_count_text, ( 3, 3))

	pygame.draw.rect(screen, GRAY, IN_BATTLE_BAND)
	in_battle_text = intermediate_font.render("In Battle...", 1, BLACK)
	screen.blit(in_battle_text, (IN_BATTLE_BAND.centerx - in_battle_text.get_width()//2, IN_BATTLE_BAND.centery - in_battle_text.get_height()//2))
	pygame.draw.rect(screen, GRAY, SKILL_BAND)
	pygame.draw.rect(screen, BLACK, SKILL_TOP_LINE)

	pygame.draw.rect(screen, BLACK, FIRST_EMPLACEMENT_ALLY_LINING)
	pygame.draw.rect(screen, GRAY, FIRST_EMPLACEMENT_ALLY)
	if fighting.ally_1 != None:
		pygame.draw.rect(screen, GRAY, FIRST_EMPLACEMENT_ALLY_NAME_BACKGROUND)
		name_ally1_text = intermediate_font.render(fighting.ally_1.name, 1, BLACK)
		screen.blit(name_ally1_text, (FIRST_EMPLACEMENT_ALLY_NAME_BACKGROUND.x, FIRST_EMPLACEMENT_ALLY_NAME_BACKGROUND.y))
		if fighting.ally_1.dead == False:
			pygame.draw.rect(screen, BLACK, FIRST_EMPLACEMENT_ALLY_HP_BACKGROUND)
			pygame.draw.rect(screen, RED, (20, 55, (int(fighting.ally_1.hp/fighting.ally_1.max_hp * 140)), 15))
			hp_ally1_text = description_font.render(f"{fighting.ally_1.hp}/{fighting.ally_1.max_hp}", 1, WHITE)
			screen.blit(hp_ally1_text, (FIRST_EMPLACEMENT_ALLY_HP_BACKGROUND.centerx - hp_ally1_text.get_width()//2, FIRST_EMPLACEMENT_ALLY_HP_BACKGROUND.centery - hp_ally1_text.get_height()//2))
			pygame.draw.rect(screen, BLACK, FIRST_EMPLACEMENT_ALLY_MP_BACKGROUND)
			pygame.draw.rect(screen, BLUE, (20, 75, (int(fighting.ally_1.mp/fighting.ally_1.max_mp * 140)), 15))
			mp_ally1_text = description_font.render(f"{fighting.ally_1.mp}/{fighting.ally_1.max_mp}", 1, WHITE)
			screen.blit(mp_ally1_text, (FIRST_EMPLACEMENT_ALLY_MP_BACKGROUND.centerx - mp_ally1_text.get_width()//2, FIRST_EMPLACEMENT_ALLY_MP_BACKGROUND.centery - mp_ally1_text.get_height()//2))
			if fighting.ally_1.special_ressource == "rage":
				pygame.draw.rect(screen, METAL, FIRST_EMPLACEMENT_ALLY_SPECIAL_BACKGROUND)
				if fighting.ally_1.rage >= 20:
					pygame.draw.rect(screen, FIRE, FIRST_EMPLACEMENT_ALLY_RAGE_1)
				if fighting.ally_1.rage >= 40:
					pygame.draw.rect(screen, FIRE, FIRST_EMPLACEMENT_ALLY_RAGE_2)
				if fighting.ally_1.rage >= 60:
					pygame.draw.rect(screen, FIRE, FIRST_EMPLACEMENT_ALLY_RAGE_3)
				if fighting.ally_1.rage >= 80:
					pygame.draw.rect(screen, FIRE, FIRST_EMPLACEMENT_ALLY_RAGE_4)
				if fighting.ally_1.rage == 100:
					pygame.draw.rect(screen, FIRE, FIRST_EMPLACEMENT_ALLY_RAGE_5)
				rage_text = description_font.render(f"{fighting.ally_1.rage}/100", 1, WHITE)
				screen.blit(rage_text, (FIRST_EMPLACEMENT_ALLY_SPECIAL_BACKGROUND.centerx - rage_text.get_width()//2, FIRST_EMPLACEMENT_ALLY_SPECIAL_BACKGROUND.centery - rage_text.get_height()//2))

			effects_offset = 0
			for effect in fighting.ally_1.effects:
				icon = effect["icon"]
				icon = pygame.transform.scale(icon, ( 20, 20))
				screen.blit(icon, (FIRST_EMPLACEMENT_ALLY.left + 5 + effects_offset, FIRST_EMPLACEMENT_ALLY.bottom - 10))
				if  effect["end"] - fighting.ally_1.global_turn_count == 1:
					text_color = METAL
				else:
					text_color = WHITE
				dmg_up_text = description_font.render(f"{effect['power']}", 1, text_color)
				screen.blit(dmg_up_text, (FIRST_EMPLACEMENT_ALLY.left + 15 + effects_offset - dmg_up_text.get_width()//2, FIRST_EMPLACEMENT_ALLY.bottom - 7))
				effects_offset += 30

		else:
			dead_text = big_font.render("Dead", 1, BLACK)
			screen.blit(dead_text, (FIRST_EMPLACEMENT_ALLY.centerx - dead_text.get_width()//2, FIRST_EMPLACEMENT_ALLY.centery - dead_text.get_height()//2 + 10))

	pygame.draw.rect(screen, BLACK, SECOND_EMPLACEMENT_ALLY_LINING)
	pygame.draw.rect(screen, GRAY, SECOND_EMPLACEMENT_ALLY)
	if fighting.ally_2 != None:
		pygame.draw.rect(screen, GRAY, SECOND_EMPLACEMENT_ALLY_NAME_BACKGROUND)
		name_ally2_text = intermediate_font.render(fighting.ally_2.name, 1, BLACK)
		screen.blit(name_ally2_text, (SECOND_EMPLACEMENT_ALLY_NAME_BACKGROUND.x, SECOND_EMPLACEMENT_ALLY_NAME_BACKGROUND.y))
		if fighting.ally_2.dead == False:
			pygame.draw.rect(screen, BLACK, SECOND_EMPLACEMENT_ALLY_HP_BACKGROUND)
			pygame.draw.rect(screen, RED, (20, 165, (int(fighting.ally_2.hp/fighting.ally_2.max_hp * 140)), 15))
			hp_ally2_text = description_font.render(f"{fighting.ally_2.hp}/{fighting.ally_2.max_hp}", 1, WHITE)
			screen.blit(hp_ally2_text, (SECOND_EMPLACEMENT_ALLY_HP_BACKGROUND.centerx - hp_ally2_text.get_width()//2, SECOND_EMPLACEMENT_ALLY_HP_BACKGROUND.centery - hp_ally2_text.get_height()//2))
			pygame.draw.rect(screen, BLACK, SECOND_EMPLACEMENT_ALLY_MP_BACKGROUND)
			pygame.draw.rect(screen, BLUE, (20, 185, (int(fighting.ally_2.mp/fighting.ally_2.max_mp * 140)), 15))
			mp_ally2_text = description_font.render(f"{fighting.ally_2.mp}/{fighting.ally_2.max_mp}", 1, WHITE)
			screen.blit(mp_ally2_text, (SECOND_EMPLACEMENT_ALLY_MP_BACKGROUND.centerx - mp_ally2_text.get_width()//2, SECOND_EMPLACEMENT_ALLY_MP_BACKGROUND.centery - mp_ally2_text.get_height()//2))
		else:
			dead_text = big_font.render("Dead", 1, BLACK)
			screen.blit(dead_text, (SECOND_EMPLACEMENT_ALLY.centerx - dead_text.get_width()//2, SECOND_EMPLACEMENT_ALLY.centery - dead_text.get_height()//2 + 10))

	pygame.draw.rect(screen, BLACK, THIRD_EMPLACEMENT_ALLY_LINING)
	pygame.draw.rect(screen, GRAY, THIRD_EMPLACEMENT_ALLY)
	if fighting.ally_3 != None:
		pygame.draw.rect(screen, GRAY, THIRD_EMPLACEMENT_ALLY_NAME_BACKGROUND)
		name_ally3_text = intermediate_font.render(fighting.ally_3.name, 1, BLACK)
		screen.blit(name_ally3_text, (THIRD_EMPLACEMENT_ALLY_NAME_BACKGROUND.x, THIRD_EMPLACEMENT_ALLY_NAME_BACKGROUND.y))
		if fighting.ally_3.dead == False:
			pygame.draw.rect(screen, BLACK, THIRD_EMPLACEMENT_ALLY_HP_BACKGROUND)
			pygame.draw.rect(screen, RED, (20, 275, (int(fighting.ally_3.hp/fighting.ally_3.max_hp * 140)), 15))
			hp_ally3_text = description_font.render(f"{fighting.ally_3.hp}/{fighting.ally_3.max_hp}", 1, WHITE)
			screen.blit(hp_ally3_text, (THIRD_EMPLACEMENT_ALLY_HP_BACKGROUND.centerx - hp_ally3_text.get_width()//2, THIRD_EMPLACEMENT_ALLY_HP_BACKGROUND.centery - hp_ally3_text.get_height()//2))
			pygame.draw.rect(screen, BLACK, THIRD_EMPLACEMENT_ALLY_MP_BACKGROUND)
			pygame.draw.rect(screen, BLUE, (20, 295, (int(fighting.ally_3.mp/fighting.ally_3.max_mp * 140)), 15))
			mp_ally3_text = description_font.render(f"{fighting.ally_3.mp}/{fighting.ally_3.max_mp}", 1, WHITE)
			screen.blit(mp_ally3_text, (THIRD_EMPLACEMENT_ALLY_MP_BACKGROUND.centerx - mp_ally3_text.get_width()//2, THIRD_EMPLACEMENT_ALLY_MP_BACKGROUND.centery - mp_ally3_text.get_height()//2))
		else:
			dead_text = big_font.render("Dead", 1, BLACK)
			screen.blit(dead_text, (THIRD_EMPLACEMENT_ALLY.centerx - dead_text.get_width()//2, THIRD_EMPLACEMENT_ALLY.centery - dead_text.get_height()//2 + 10))

	pygame.draw.rect(screen, BLACK, FOURTH_EMPLACEMENT_ALLY_LINING)
	pygame.draw.rect(screen, GRAY, FOURTH_EMPLACEMENT_ALLY)
	if fighting.ally_4 != None:
		pygame.draw.rect(screen, GRAY, FOURTH_EMPLACEMENT_ALLY_NAME_BACKGROUND)
		name_ally4_text = intermediate_font.render(fighting.ally_4.name, 1, BLACK)
		screen.blit(name_ally4_text, (FOURTH_EMPLACEMENT_ALLY_NAME_BACKGROUND.x, FOURTH_EMPLACEMENT_ALLY_NAME_BACKGROUND.y))
		if fighting.ally_4.dead == False:
			pygame.draw.rect(screen, BLACK, FOURTH_EMPLACEMENT_ALLY_HP_BACKGROUND)
			pygame.draw.rect(screen, RED, (20, 385, (int(fighting.ally_4.hp/fighting.ally_4.max_hp * 140)), 15))
			hp_ally4_text = description_font.render(f"{fighting.ally_4.hp}/{fighting.ally_4.max_hp}", 1, WHITE)
			screen.blit(hp_ally4_text, (FOURTH_EMPLACEMENT_ALLY_HP_BACKGROUND.centerx - hp_ally4_text.get_width()//2, FOURTH_EMPLACEMENT_ALLY_HP_BACKGROUND.centery - hp_ally4_text.get_height()//2))
			pygame.draw.rect(screen, BLACK, FOURTH_EMPLACEMENT_ALLY_MP_BACKGROUND)
			pygame.draw.rect(screen, BLUE, (20, 405, (int(fighting.ally_4.mp/fighting.ally_4.max_mp * 140)), 15))
			mp_ally4_text = description_font.render(f"{fighting.ally_4.mp}/{fighting.ally_4.max_mp}", 1, WHITE)
			screen.blit(mp_ally4_text, (FOURTH_EMPLACEMENT_ALLY_MP_BACKGROUND.centerx - mp_ally4_text.get_width()//2, FOURTH_EMPLACEMENT_ALLY_MP_BACKGROUND.centery - mp_ally4_text.get_height()//2))
		else:
			dead_text = big_font.render("Dead", 1, BLACK)
			screen.blit(dead_text, (FOURTH_EMPLACEMENT_ALLY.centerx - dead_text.get_width()//2, FOURTH_EMPLACEMENT_ALLY.centery - dead_text.get_height()//2 + 10))


	pygame.draw.rect(screen, BLACK, FIRST_EMPLACEMENT_ENY_LINING)
	pygame.draw.rect(screen, GRAY, FIRST_EMPLACEMENT_ENY)
	if fighting.enemy_1 != None:
		pygame.draw.rect(screen, GRAY, FIRST_EMPLACEMENT_ENY_NAME_BACKGROUND)
		name_eny1_text = intermediate_font.render(fighting.enemy_1.name, 1, BLACK)
		screen.blit(name_eny1_text, (FIRST_EMPLACEMENT_ENY_NAME_BACKGROUND.x, FIRST_EMPLACEMENT_ENY_NAME_BACKGROUND.y))
		if fighting.enemy_1.dead == False:
			pygame.draw.rect(screen, BLACK, FIRST_EMPLACEMENT_ENY_HP_BACKGROUND)
			pygame.draw.rect(screen, RED, (340, 55, (int(fighting.enemy_1.hp/fighting.enemy_1.max_hp * 140)), 15))
			hp_eny1_text = description_font.render(f"{fighting.enemy_1.hp}/{fighting.enemy_1.max_hp}", 1, WHITE)
			screen.blit(hp_eny1_text, (FIRST_EMPLACEMENT_ENY_HP_BACKGROUND.centerx - hp_eny1_text.get_width()//2, FIRST_EMPLACEMENT_ENY_HP_BACKGROUND.centery - hp_eny1_text.get_height()//2))
			pygame.draw.rect(screen, BLACK, FIRST_EMPLACEMENT_ENY_MP_BACKGROUND)
			pygame.draw.rect(screen, BLUE, (340, 75, (int(fighting.enemy_1.mp/fighting.enemy_1.max_mp * 140)), 15))
			mp_eny1_text = description_font.render(f"{fighting.enemy_1.mp}/{fighting.enemy_1.max_mp}", 1, WHITE)
			screen.blit(mp_eny1_text, (FIRST_EMPLACEMENT_ENY_MP_BACKGROUND.centerx - mp_eny1_text.get_width()//2, FIRST_EMPLACEMENT_ENY_MP_BACKGROUND.centery - mp_eny1_text.get_height()//2))
		else:
			dead_text = big_font.render("Dead", 1, BLACK)
			screen.blit(dead_text, (FIRST_EMPLACEMENT_ENY.centerx - dead_text.get_width()//2, FIRST_EMPLACEMENT_ENY.centery - dead_text.get_height()//2 + 10))

	pygame.draw.rect(screen, BLACK, SECOND_EMPLACEMENT_ENY_LINING)
	pygame.draw.rect(screen, GRAY, SECOND_EMPLACEMENT_ENY)
	if fighting.enemy_2 != None:
		pygame.draw.rect(screen, GRAY, SECOND_EMPLACEMENT_ENY_NAME_BACKGROUND)
		name_eny2_text = intermediate_font.render(fighting.enemy_2.name, 1, BLACK)
		screen.blit(name_eny2_text, (SECOND_EMPLACEMENT_ENY_NAME_BACKGROUND.x, SECOND_EMPLACEMENT_ENY_NAME_BACKGROUND.y))
		if fighting.enemy_2.dead == False:
			pygame.draw.rect(screen, BLACK, SECOND_EMPLACEMENT_ENY_HP_BACKGROUND)
			pygame.draw.rect(screen, RED, (340, 165, (int(fighting.enemy_2.hp/fighting.enemy_2.max_hp * 140)), 15))
			hp_eny2_text = description_font.render(f"{fighting.enemy_2.hp}/{fighting.enemy_2.max_hp}", 1, WHITE)
			screen.blit(hp_eny2_text, (SECOND_EMPLACEMENT_ENY_HP_BACKGROUND.centerx - hp_eny2_text.get_width()//2, SECOND_EMPLACEMENT_ENY_HP_BACKGROUND.centery - hp_eny2_text.get_height()//2))
			pygame.draw.rect(screen, BLACK, SECOND_EMPLACEMENT_ENY_MP_BACKGROUND)
			pygame.draw.rect(screen, BLUE, (340, 185, (int(fighting.enemy_2.mp/fighting.enemy_2.max_mp * 140)), 15))
			mp_eny2_text = description_font.render(f"{fighting.enemy_2.mp}/{fighting.enemy_2.max_mp}", 1, WHITE)
			screen.blit(mp_eny2_text, (SECOND_EMPLACEMENT_ENY_MP_BACKGROUND.centerx - mp_eny2_text.get_width()//2, SECOND_EMPLACEMENT_ENY_MP_BACKGROUND.centery - mp_eny2_text.get_height()//2))
		else:
			dead_text = big_font.render("Dead", 1, BLACK)
			screen.blit(dead_text, (SECOND_EMPLACEMENT_ENY.centerx - dead_text.get_width()//2, SECOND_EMPLACEMENT_ENY.centery - dead_text.get_height()//2 + 10))

	pygame.draw.rect(screen, BLACK, THIRD_EMPLACEMENT_ENY_LINING)
	pygame.draw.rect(screen, GRAY, THIRD_EMPLACEMENT_ENY)
	if fighting.enemy_3 != None:
		pygame.draw.rect(screen, GRAY, THIRD_EMPLACEMENT_ENY_NAME_BACKGROUND)
		name_eny3_text = intermediate_font.render(fighting.enemy_3.name, 1, BLACK)
		screen.blit(name_eny3_text, (THIRD_EMPLACEMENT_ENY_NAME_BACKGROUND.x, THIRD_EMPLACEMENT_ENY_NAME_BACKGROUND.y))
		if fighting.enemy_3.dead == False:
			pygame.draw.rect(screen, BLACK, THIRD_EMPLACEMENT_ENY_HP_BACKGROUND)
			pygame.draw.rect(screen, RED, (340, 275, (int(fighting.enemy_3.hp/fighting.enemy_3.max_hp * 140)), 15))
			hp_eny3_text = description_font.render(f"{fighting.enemy_3.hp}/{fighting.enemy_3.max_hp}", 1, WHITE)
			screen.blit(hp_eny3_text, (THIRD_EMPLACEMENT_ENY_HP_BACKGROUND.centerx - hp_eny3_text.get_width()//2, THIRD_EMPLACEMENT_ENY_HP_BACKGROUND.centery - hp_eny3_text.get_height()//2))
			pygame.draw.rect(screen, BLACK, THIRD_EMPLACEMENT_ENY_MP_BACKGROUND)
			pygame.draw.rect(screen, BLUE, (340, 295, (int(fighting.enemy_3.mp/fighting.enemy_3.max_mp * 140)), 15))
			mp_eny3_text = description_font.render(f"{fighting.enemy_3.mp}/{fighting.enemy_3.max_mp}", 1, WHITE)
			screen.blit(mp_eny3_text, (THIRD_EMPLACEMENT_ENY_MP_BACKGROUND.centerx - mp_eny3_text.get_width()//2, THIRD_EMPLACEMENT_ENY_MP_BACKGROUND.centery - mp_eny3_text.get_height()//2))
		else:
			dead_text = big_font.render("Dead", 1, BLACK)
			screen.blit(dead_text, (THIRD_EMPLACEMENT_ENY.centerx - dead_text.get_width()//2, THIRD_EMPLACEMENT_ENY.centery - dead_text.get_height()//2 + 10))

	pygame.draw.rect(screen, BLACK, FOURTH_EMPLACEMENT_ENY_LINING)
	pygame.draw.rect(screen, GRAY, FOURTH_EMPLACEMENT_ENY)
	if fighting.enemy_4 != None:
		pygame.draw.rect(screen, GRAY, FOURTH_EMPLACEMENT_ENY_NAME_BACKGROUND)
		name_eny4_text = intermediate_font.render(fighting.enemy_4.name, 1, BLACK)
		screen.blit(name_eny4_text, (FOURTH_EMPLACEMENT_ENY_NAME_BACKGROUND.x, FOURTH_EMPLACEMENT_ENY_NAME_BACKGROUND.y))
		if fighting.enemy_4.dead == False:
			pygame.draw.rect(screen, BLACK, FOURTH_EMPLACEMENT_ENY_HP_BACKGROUND)
			pygame.draw.rect(screen, RED, (340, 385, (int(fighting.enemy_4.hp/fighting.enemy_4.max_hp * 140)), 15))
			hp_eny4_text = description_font.render(f"{fighting.enemy_4.hp}/{fighting.enemy_4.max_hp}", 1, WHITE)
			screen.blit(hp_eny4_text, (FOURTH_EMPLACEMENT_ENY_HP_BACKGROUND.centerx - hp_eny4_text.get_width()//2, FOURTH_EMPLACEMENT_ENY_HP_BACKGROUND.centery - hp_eny4_text.get_height()//2))
			pygame.draw.rect(screen, BLACK, FOURTH_EMPLACEMENT_ENY_MP_BACKGROUND)
			pygame.draw.rect(screen, BLUE, (340, 405, (int(fighting.enemy_4.mp/fighting.enemy_4.max_mp * 140)), 15))
			mp_eny4_text = description_font.render(f"{fighting.enemy_4.mp}/{fighting.enemy_4.max_mp}", 1, WHITE)
			screen.blit(mp_eny4_text, (FOURTH_EMPLACEMENT_ENY_MP_BACKGROUND.centerx - mp_eny4_text.get_width()//2, FOURTH_EMPLACEMENT_ENY_MP_BACKGROUND.centery - mp_eny4_text.get_height()//2))
		else:
			dead_text = big_font.render("Dead", 1, BLACK)
			screen.blit(dead_text, (FOURTH_EMPLACEMENT_ENY.centerx - dead_text.get_width()//2, FOURTH_EMPLACEMENT_ENY.centery - dead_text.get_height()//2 + 10))

	generic_effects_draw_window()

	pygame.display.update()

def in_fight():
	click = False
	run = True
	in_pre_battle()
	before_first_turn()
	phase_one_done = False
	phase_two_done = False
	while run:
		clock.tick(60)
		mx, my = pygame.mouse.get_pos()

		if click:
			fighting.animations = []


		if (fighting.animations == [] or click) and (fighting.victory or fighting.defeat):
			if fighting.defeat:
				dungeon.defeated = True
			run = False

		else:
			if (click or fighting.animations == []) and phase_one_done == False and fighting.playing != "goddess":
				phase_one_done = one_turn_fight_phase_one()
				if fighting.playing == "goddess":
					phase_one_done = False
				
			elif (click or fighting.animations == []) and phase_one_done and phase_two_done == False:
				one_turn_fight_phase_two()
				phase_two_done = True
				
			elif (click or fighting.animations == []) and phase_one_done and phase_two_done:
				one_turn_fight_phase_three()
				phase_one_done = False
				phase_two_done = False

		

		click = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_SPACE:
					click = True
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True
		
		in_fight_draw_window()
	
	in_post_battle()


############################################################

def rage_check(user):
	if user.name == "Alex":
		if user.rage > 100:
			user.rage = 100

def is_critical(user):
	roll = rand.randint(0,100)
	if roll <= user.crit_chance:
		return True
	else:
		return False

	#consecutive_turn_survived(user)

def player_reaction(user,crit):
	roll = rand.randint(0,100)
	if crit == True and user.friendly == True and roll >= 70:
		react = rand.choice(user.phrase_crit)
		print(f"{user.name}: {react}")
		print("")

def effects_end(user):
	fighting.effect_end_proc = False
	for effect in user.effects:
		if fighting.effect_end_proc == False:
			if effect["end"] <= user.global_turn_count:
				if effect["scope"] == "self":
					if effect["type"] == "buff":
						if effect["sub_type"] == "dmg":
							user.dmg -= effect["power"]
							generate_skill_description(effect["name"],f"The effect of {effect['name']} on {user.name} wears off.")
				user.effects.remove(effect)
				fighting.effect_end_proc = True

def effects_tick(user):
	fighting.effect_tick_proc = False
	for effect in user.effects:
		if fighting.effect_tick_proc == False:
			if effect["ticks"] and (effect not in fighting.effect_tick_list):
				if effect["scope"] == "self":
					if effect["type"] == "regen":
						if effect["sub_type"] == "hp":
							user.hp += effect["power"]
							generate_heal_animation(user,effect["power"])
							generate_skill_description(effect["name"],effect["description"])
							regen_sfx.play()
							regen_sfx.set_volume(0.25)
							if user.hp > user.max_hp:
								user.hp = user.max_hp
							fighting.effect_tick_proc = True
							fighting.effect_tick_list.append(effect)

def clear_all_effects(user):
	user.effects = []

def defensive_roll(target):
	roll = rand.randint(0,100)
	if target.defensive_roll_chance >= roll:
		roll2 = rand.randint(0,100)
		if target.crit_defensive_roll_chance >= roll2:
			return 0
		else:
			return 0.2
	else:
		return 1

##############################

def no_hp_under(target):
	if target.hp < 0:
		target.hp = 0
		target.dead = True

##############################

def apply_passive_effects(user):
	if len(user.passive_skill) > 0:
		for skill in user.passive_skill:
			skill(user)

##############################
##### Stats-tracking #####

def specie_counter():
    for enemy in enemy_party.enemy_dead:
        for each in statistics.kill_count:
            if enemy.specie == each["name"]:
                each["count"] += 1


#def goblin_slayer_award()

##########################
######  Post Battle  #####

def post_battle_draw_window():
	BACKGROUND()
	pygame.draw.rect(screen, GRAY, TOP_BAND)
	post_battle_text = font.render("Post Battle", 1, BLACK)
	screen.blit(post_battle_text, (TOP_BAND.centerx - post_battle_text.get_width()//2, TOP_BAND.centery - post_battle_text.get_height()//2))

	if fighting.victory:
		fight_result_text = big_font.render("Victory !", 1, BLACK)
	else:
		fight_result_text = big_font.render("Defeat !", 1, BLACK)
	screen.blit(fight_result_text, (WIDTH//2 - fight_result_text.get_width()//2, 75))

	xp_gained_text = font.render(f"Every party member gained {inventory.xp_per_ally} xp", 1, BLACK)
	screen.blit(xp_gained_text, (WIDTH//2 - xp_gained_text.get_width()//2, 150 - xp_gained_text.get_height()//2))
	mastery_gained_text = font.render(f"Every party member gained {inventory.mastery_per_ally} mastery points", 1, BLACK)
	screen.blit(mastery_gained_text, (WIDTH//2 - mastery_gained_text.get_width()//2, 180 - mastery_gained_text.get_height()//2))
	if len(party.party_alive) > 0:
		gold_gained_text = font.render(f"They've scavenged {inventory.battle_gold} Gold", 1, BLACK)
		screen.blit(gold_gained_text, (WIDTH//2 - gold_gained_text.get_width()//2, 210 - gold_gained_text.get_height()//2))
		loot_text = font.render("The party found :", 1, BLACK)
		screen.blit(loot_text, (WIDTH//2 - loot_text.get_width()//2, 270 - loot_text.get_height()//2))
		offset = 0
		if len(inventory.battle_loot) == 0:
			loot_gained_text = font.render("Nothing", 1, BLACK)
			screen.blit(loot_gained_text, (WIDTH//2 - loot_gained_text.get_width()//2, 300 + offset - loot_gained_text.get_height()//2))
			pygame.display.update()
		else:
			for loot in inventory.battle_loot:
				loot_storage_text = font.render(f"{loot} x{inventory.battle_loot[loot]}", 1, BLACK)
				screen.blit(loot_storage_text, (WIDTH//2 - loot_storage_text.get_width()//2, 300 + offset - loot_storage_text.get_height()//2))
				offset += 30
			pygame.display.update()
	else:
		pygame.display.update()

def post_battle():
	inventory.battle_gold = 0
	inventory.battle_loot = {}
	total_xp = 0
	total_gold = 0
	total_mastery = 0
	total_loot = []

#specie_counter()
	
	for enemy in enemy_party.enemy_dead:
		total_xp += enemy.xp
		total_gold += enemy.gold
		total_mastery += enemy.mastery_xp
		total_loot.append(enemy.soul)
		for loot in enemy.loot_table:
			dice_roll = rand.random()
			if dice_roll <= 0.10:
				total_loot.append(loot)

	if len(party.party_alive) > 0:
		play_victory_music()
		battle_loot = inventory.battle_loot
		if len(total_loot) > 0:
			total_loot.sort()
			set_total_loot = set(total_loot)
			for item in set_total_loot:
				count = 0
				for current_item in total_loot:
					if item == current_item:
						count += 1
				if item in battle_loot:
					battle_loot[item] += count
				else:
					battle_loot[item] = count
			inventory.battle_loot = battle_loot
			
			battle_loot = inventory.battle_loot
			if len(battle_loot) > 0:
				for loot in battle_loot:
					if loot in inventory.dungeon_loot:
						inventory.dungeon_loot[loot] += battle_loot[loot]
					else:
						inventory.dungeon_loot[loot] = battle_loot[loot]

					

		inventory.battle_gold = total_gold
		inventory.dungeon_gold += inventory.battle_gold

	else:
		play_defeat_music()
		inventory.battle_gold = 0
		inventory.dungeon_gold = 0
		inventory.dungeon_loot = {}

	for ally in party.party:
		xp_per_ally = total_xp // (len(party.party))
		ally.xp += xp_per_ally
		mastery_per_ally = total_mastery // len(party.party)
		ally.mastery += mastery_per_ally

	inventory.xp_per_ally = xp_per_ally
	inventory.mastery_per_ally = mastery_per_ally

	enemy_party.enemy_list = []
	enemy_party.enemy_alive = []
	enemy_party.enemy_dead = []
	enemy_party.number_of_enemy = 0
	enemy_party.number_of_enemy_alive = 0
	fighting.battle_order = []
	fighting.enemy_1 = None
	fighting.enemy_2 = None
	fighting.enemy_3 = None
	fighting.enemy_4 = None

def in_post_battle():
	click = False
	run = True
	post_battle()
	while run:
		clock.tick(60)
		mx, my = pygame.mouse.get_pos()

		if click:
			run = False

		click = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					run = False
				if event.key == K_SPACE:
					run = False
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True
		post_battle_draw_window()


########################
########Inventory#######

def inventory_sorting():
	inventory.town_gold += inventory.dungeon_gold
	statistics.gold_earned += inventory.dungeon_gold
	dungeon_loot = inventory.dungeon_loot
	if len(dungeon_loot) > 0:
		for loot in dungeon_loot:
			if loot in inventory.town_storage:
				inventory.town_storage[loot] += dungeon_loot[loot]
			else:
				inventory.town_storage[loot] = dungeon_loot[loot]
	inventory.dungeon_loot = {}
	inventory.dungeon_gold = 0

def empty_storage(inventory):
	count = 0
	for items in inventory.storage:
		count += 1
	return count

##############################
##############################
##############################
##############################
##############################

class goddess_base:
	soul_power = 0
	heal = True

################################
######## Manage Goddess ########

def manage_goddess_draw_window():
	BACKGROUND()
	pygame.draw.rect(screen, GRAY, TOP_BAND)
	band_text = font.render("Goddess", 1, BLACK)
	screen.blit(band_text, ( TOP_BAND.centerx - band_text.get_width()//2, TOP_BAND.centery - band_text.get_height()//2))

	pygame.draw.rect(screen, GRAY, GODDESS_LEVEL_UP_BUTTON)
	goddess_level_up_text = intermediate_font.render("Offering", 1, BLACK)
	screen.blit(goddess_level_up_text, (GODDESS_LEVEL_UP_BUTTON.centerx - goddess_level_up_text.get_width()//2, GODDESS_LEVEL_UP_BUTTON.centery - goddess_level_up_text.get_height()//2))
	pygame.draw.rect(screen, GRAY, GODDESS_SKILL_BUTTON)
	goddess_skill_text = intermediate_font.render("Divine Skills", 1, BLACK)
	screen.blit(goddess_skill_text, (GODDESS_SKILL_BUTTON.centerx - goddess_skill_text.get_width()//2, GODDESS_SKILL_BUTTON.centery - goddess_skill_text.get_height()//2))
	pygame.draw.rect(screen, GRAY, GODDESS_BLESSING_BUTTON)
	goddess_blessing_text = intermediate_font.render("Blessing", 1, BLACK)
	screen.blit(goddess_blessing_text, (GODDESS_BLESSING_BUTTON.centerx - goddess_blessing_text.get_width()//2, GODDESS_BLESSING_BUTTON.centery - goddess_blessing_text.get_height()//2))


	pygame.draw.rect(screen, GRAY, BACK_BUTTON)
	back_text = intermediate_font.render("Back", 1, BLACK)
	screen.blit(back_text, (BACK_BUTTON.centerx - back_text.get_width()//2, BACK_BUTTON.centery - back_text.get_height()//2))

	pygame.display.update()

def manage_goddess():
	run = True
	click = False
	while run:
		clock.tick(60)
		mx, my = pygame.mouse.get_pos()

		if GODDESS_LEVEL_UP_BUTTON.collidepoint((mx, my)):
			if click:
				goddess_level_up()

		if GODDESS_SKILL_BUTTON.collidepoint((mx, my)):
			if click:
				goddess_active_skill()

		if GODDESS_BLESSING_BUTTON.collidepoint((mx, my)):
			if click:
				goddess_blessing()

		if BACK_BUTTON.collidepoint((mx, my)):
			if click:
				run = False

		click = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					run = False
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True

		manage_goddess_draw_window()


def calculate_offering_amount():
	offering = 0
	for item in inventory.town_storage:
		if item == "Goblin's Soulgem":
			offering += 1 * inventory.town_storage[item]
		if item == "Hobgoblin's Soulgem":
			offering += 3 * inventory.town_storage[item]
	return offering
	
def offer_souls():
	offering = 0
	temp_list = []
	for item in inventory.town_storage:
		if item == "Goblin's Soulgem":
			offering += 1 * inventory.town_storage[item]
			temp_list.append(item)
		if item == "Hobgoblin's Soulgem":
			offering += 3 * inventory.town_storage[item]
			temp_list.append(item)
	for item in temp_list:
		del inventory.town_storage[item]
	
	goddess.soul_power += offering

def goddess_level_up_draw_window():
	BACKGROUND()
	pygame.draw.rect(screen, GRAY, TOP_BAND)
	band_text = font.render("Offering", 1, BLACK)
	screen.blit(band_text, ( TOP_BAND.centerx - band_text.get_width()//2, TOP_BAND.centery - band_text.get_height()//2))

	offering_text = intermediate_font.render("Offer Souls", 1, BLACK)
	screen.blit(offering_text, (OFFERING_CONVERT_SOUL_BUTTON.centerx - offering_text.get_width()//2, OFFERING_CONVERT_SOUL_BUTTON.y - offering_text.get_height() - 5))
	pygame.draw.rect(screen, GRAY, OFFERING_CONVERT_SOUL_BUTTON)
	offering_amount_text = intermediate_font.render(f"{calculate_offering_amount()}", 1, BLACK)
	screen.blit(offering_amount_text, (OFFERING_CONVERT_SOUL_BUTTON.centerx - offering_amount_text.get_width()//2, OFFERING_CONVERT_SOUL_BUTTON.centery - offering_amount_text.get_height()//2))

	soul_power_text = intermediate_font.render(f"{goddess.soul_power} SP", 1, BLACK)
	screen.blit(soul_power_text, (TOP_BAND.x + 30, OFFERING_CONVERT_SOUL_BUTTON.y - soul_power_text.get_height() - 5))

	pygame.draw.rect(screen, GRAY, OFFERING_FIRST_BUTTON)

	pygame.draw.rect(screen, GRAY, BACK_BUTTON)
	back_text = intermediate_font.render("Back", 1, BLACK)
	screen.blit(back_text, (BACK_BUTTON.centerx - back_text.get_width()//2, BACK_BUTTON.centery - back_text.get_height()//2))

	pygame.display.update()

def goddess_level_up():
	run = True
	click = False
	while run:
		clock.tick(60)
		mx, my = pygame.mouse.get_pos()

		if OFFERING_CONVERT_SOUL_BUTTON.collidepoint((mx, my)):
			if click:
				offer_souls()

		if BACK_BUTTON.collidepoint((mx, my)):
			if click:
				run = False


		click = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					run = False
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True

		goddess_level_up_draw_window()


def goddess_active_skill():
	pass

def goddess_blessing():
	pass

#############################
######## Manage Team ########

def manage_team_draw_window(ally_index):
	BACKGROUND()
	pygame.draw.rect(screen, GRAY, TOP_BAND)
	title_text = font.render("Manage Team", 1, BLACK)
	screen.blit(title_text, (TOP_BAND.centerx - title_text.get_width()//2, TOP_BAND.centery - title_text.get_height()//2))
	
	pygame.draw.rect(screen, GRAY, ALLY_BAND)
	title_text = font.render("Ally", 1, BLACK)
	screen.blit(title_text, (ALLY_BAND.centerx - title_text.get_width()//2, ALLY_BAND.centery - title_text.get_height()//2))
	
	pygame.draw.rect(screen, GRAY, PARTY_BAND)
	title_text = font.render("Party", 1, BLACK)
	screen.blit(title_text, (PARTY_BAND.centerx - title_text.get_width()//2, PARTY_BAND.centery - title_text.get_height()//2))

	pygame.draw.rect(screen, GRAY, (50, 160 + 25 * ally_index, 100, 20))

	offset = 0
	for ally in party.available_ally:
		overall_text = font.render(f"{ally.name}", 1, BLACK)
		screen.blit(overall_text, (50, 160 + offset))
		offset += 25

	offset = 0
	for ally in party.party:
		overall_text = font.render(f"{ally.name}", 1, BLACK)
		screen.blit(overall_text, (350, 160 + offset))
		offset += 25

	pygame.draw.rect(screen, LIGHT_GRAY, ARROW_UP_BUTTON)
	screen.blit(ARROW_UP_IMAGE, (ARROW_UP_BUTTON.x, ARROW_UP_BUTTON.y))
	
	pygame.draw.rect(screen, LIGHT_GRAY, ARROW_DOWN_BUTTON)
	screen.blit(ARROW_DOWN_IMAGE, (ARROW_DOWN_BUTTON.x, ARROW_DOWN_BUTTON.y))
	
	pygame.draw.rect(screen, GRAY, ADD_BUTTON)
	add_button_text = font.render("Add", 1, BLACK)
	screen.blit(add_button_text, (ADD_BUTTON.centerx - add_button_text.get_width()//2, ADD_BUTTON.centery - add_button_text.get_height()//2))
	
	pygame.draw.rect(screen, GRAY, REMOVE_BUTTON)
	remove_button_text = font.render("Remove", 1, BLACK)
	screen.blit(remove_button_text, (REMOVE_BUTTON.centerx - remove_button_text.get_width()//2, REMOVE_BUTTON.centery - remove_button_text.get_height()//2))

	pygame.draw.rect(screen, GRAY, BACK_BUTTON)
	back_button_text = font.render("Back", 1, BLACK)
	screen.blit(back_button_text, (BACK_BUTTON.centerx - back_button_text.get_width()//2, BACK_BUTTON.centery - back_button_text.get_height()//2))

	if len(party.party) == 0:
		need_more_member_text = small_font.render("You need atleast one member in your party !", 1, RED)
		screen.blit(need_more_member_text, (WIDTH//2 - need_more_member_text.get_width()//2, BACK_BUTTON.centery - need_more_member_text.get_height()//2 - 50))

	pygame.display.update()

def manage_team():
	click = False
	run = True
	ally_index = 0
	number_of_ally = len(party.available_ally) - 1
	while run:
		clock.tick(60)
		mx, my = pygame.mouse.get_pos()

		if ARROW_UP_BUTTON.collidepoint((mx, my)):
			if click:
				if ally_index - 1 >= 0:
					ally_index -= 1
		if ARROW_DOWN_BUTTON.collidepoint((mx, my)):
			if click:
				if ally_index + 1 <= number_of_ally:
					ally_index += 1
		if ADD_BUTTON.collidepoint((mx, my)):
			if click:
				if (party.available_ally[ally_index] in party.party) == False and len(party.party) <= 4:
					party.party.append(party.available_ally[ally_index])
		if REMOVE_BUTTON.collidepoint((mx, my)):
			if click:
				if (party.available_ally[ally_index] in party.party) == True:
					del party.party[party.party.index(party.available_ally[ally_index])]
		if BACK_BUTTON.collidepoint((mx, my)):
			if click:
				if len(party.party) == 0:
					pass
				else:
					party.number_of_ally = len(party.party)
					break

		click = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					run = False
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True
		manage_team_draw_window(ally_index)
	

#############################
##### Lvl up  fonctions #####

def check_level_up(user):
	x = user.level
	xp_check = x * x * 300 + int(math.exp(x))
	if user.xp >= xp_check:
		return True
	else:
		return False

def stats_up(user):
	user.max_hp = int(user.max_hp * 1.3)
	user.dmg = int(user.dmg * 1.3)
	user.magic_dmg = int(user.magic_dmg * 1.3)
	user.max_mp = int(user.max_mp * 1.3)
	user.speed = int(user.speed * 1.3)

def recover():
	for member in party.party:
		member.hp = member.max_hp
		member.mp = member.max_mp
		member.dead = False
		if member.special_ressource == "rage":
			member.rage = 0


#############################
####### Rest / Lvl Up #######

def home_rest_lvl_up_draw_window():
	BACKGROUND()
	pygame.draw.rect(screen, GRAY, TOP_BAND)
	title_text = font.render("Status Update", 1, BLACK)
	screen.blit(title_text, (TOP_BAND.centerx - title_text.get_width()//2, TOP_BAND.centery - title_text.get_height()//2))

	offset = 0
	for ally in party.party:
		lvl_up = check_level_up(ally)
		count = 0
		starting_level = ally.level
		while lvl_up:
			count += 1
			ally.level += 1
			stats_up(ally)
			lvl_up = check_level_up(ally)
		if count > 0:
			final_level = starting_level + count
			level_up_text = font.render(f"{ally.name} level {starting_level} -> {final_level} !", 1, BLACK)
			screen.blit(level_up_text, (100, 150 + offset))
			offset += 50
	
	pygame.display.update()

def home_rest_no_lvl_up_draw_window():
	BACKGROUND()
	pygame.draw.rect(screen, GRAY, TOP_BAND)
	title_text = font.render("Status Update", 1, BLACK)
	screen.blit(title_text, (TOP_BAND.centerx - title_text.get_width()//2, TOP_BAND.centery - title_text.get_height()//2))

	level_up_fail_text = font.render(f"No one in your party leveled up", 1, BLACK)
	screen.blit(level_up_fail_text, (WIDTH//2 - level_up_fail_text.get_width()//2, 300 - level_up_fail_text.get_height()//2))

	pygame.display.update()

def home_rest_xp_check_draw_window():
	BACKGROUND()
	pygame.draw.rect(screen, GRAY, TOP_BAND)
	title_text = font.render("Status Update", 1, BLACK)
	screen.blit(title_text, (TOP_BAND.centerx - title_text.get_width()//2, TOP_BAND.centery - title_text.get_height()//2))

	updating_status_text = font.render(f"Updating status...", 1, BLACK)
	screen.blit(updating_status_text, (WIDTH//2 - updating_status_text.get_width()//2, 300 - updating_status_text.get_height()//2))

	pygame.display.update()

def home_rest_xp_check():
	home_rest_xp_check_draw_window()
	status_update_sfx.play()
	status_update_sfx.set_volume(0.25)
	pygame.time.delay(3000)
	status_update_sfx.stop()
	is_lvl_up = False
	for ally in party.party:
		award_killer_titles(ally)
		lvl_up = check_level_up(ally)
		if lvl_up:
			is_lvl_up = True
	if is_lvl_up:
		home_rest_lvl_up_draw_window()
	else:
		home_rest_no_lvl_up_draw_window()
	wait()

def home_rest_draw_window():
	BACKGROUND()
	pygame.draw.rect(screen, GRAY, TOP_BAND)
	rest_text = font.render("Resting", 1, BLACK)
	screen.blit(rest_text, (TOP_BAND.centerx - rest_text.get_width()//2, TOP_BAND.centery - rest_text.get_height()//2))
	
	recover_text = font.render(f"Your party have recovered !", 1, BLACK)
	screen.blit(recover_text, (WIDTH//2 - recover_text.get_width()//2, 100 - recover_text.get_height()//2))

	lvl_up_text = font.render(f"Do you wish to update your status ?", 1, BLACK)
	screen.blit(lvl_up_text, (WIDTH//2 - lvl_up_text.get_width()//2, 300 - lvl_up_text.get_height()//2))

	pygame.draw.rect(screen, GRAY, YES_LVL_UP_BUTTON)
	yes_text = font.render("Yes", 1, BLACK)
	screen.blit(yes_text, (YES_LVL_UP_BUTTON.centerx - yes_text.get_width()//2, YES_LVL_UP_BUTTON.centery - yes_text.get_height()//2))

	pygame.draw.rect(screen, GRAY, NO_LVL_UP_BUTTON)
	no_text = font.render("No", 1, BLACK)
	screen.blit(no_text, (NO_LVL_UP_BUTTON.centerx - no_text.get_width()//2, NO_LVL_UP_BUTTON.centery - no_text.get_height()//2))

	pygame.display.update()

def home_rest():
	recover()
	rest_regen_sfx.play()
	rest_regen_sfx.set_volume(0.25)
	click = False
	run = True
	while run:
		clock.tick(60)
		mx, my = pygame.mouse.get_pos()

		if YES_LVL_UP_BUTTON.collidepoint((mx, my)):
			if click:
				home_rest_xp_check()
				recover()
				break
		if NO_LVL_UP_BUTTON.collidepoint((mx, my)):
			if click:
				break

		click = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					run = False
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True
		home_rest_draw_window()

############################
##### Check Individual #####

def check_character_sheet_draw_window(ally,column,page):
	BACKGROUND()
	#pygame.draw.rect(screen, GRAY, UPPER_LEFT_ARROW_BUTTON)
	screen.blit(LEFT_ARROW_IMAGE, (UPPER_LEFT_ARROW_BUTTON.x, UPPER_LEFT_ARROW_BUTTON.y))
	#pygame.draw.rect(screen, GRAY, UPPER_RIGHT_ARROW_BUTTON)
	screen.blit(RIGHT_ARROW_IMAGE, (UPPER_RIGHT_ARROW_BUTTON.x, UPPER_RIGHT_ARROW_BUTTON.y))
	name_text = font.render(ally.name, 1, BLACK)
	screen.blit(name_text, (WIDTH//2 - name_text.get_width()//2, 15 - name_text.get_height()//2))

	pygame.draw.rect(screen, GRAY, STATS_COLUMN_BUTTON)
	stats_column_text = font.render("Stats", 1, BLACK)
	screen.blit(stats_column_text, (STATS_COLUMN_BUTTON.centerx - stats_column_text.get_width()//2, STATS_COLUMN_BUTTON.centery - stats_column_text.get_height()//2))
	pygame.draw.rect(screen, GRAY, SKILL_COLUMN_BUTTON)
	skill_column_text = font.render("Skills", 1, BLACK)
	screen.blit(skill_column_text, (SKILL_COLUMN_BUTTON.centerx - skill_column_text.get_width()//2, SKILL_COLUMN_BUTTON.centery - skill_column_text.get_height()//2))
	pygame.draw.rect(screen, GRAY, TITLE_COLUMN_BUTTON)
	title_column_text = font.render("Titles", 1, BLACK)
	screen.blit(title_column_text, (TITLE_COLUMN_BUTTON.centerx - title_column_text.get_width()//2, TITLE_COLUMN_BUTTON.centery - title_column_text.get_height()//2))
	pygame.draw.rect(screen, GRAY, RECORDS_COLUMN_BUTTON)
	records_column_text = font.render("Records", 1, BLACK)
	screen.blit(records_column_text, (RECORDS_COLUMN_BUTTON.centerx - records_column_text.get_width()//2, RECORDS_COLUMN_BUTTON.centery - records_column_text.get_height()//2))
	pygame.draw.rect(screen, BLACK, FIRST_COLUMN_SEPARATOR)
	pygame.draw.rect(screen, BLACK, SECOND_COLUMN_SEPARATOR)
	pygame.draw.rect(screen, BLACK, THIRD_COLUMN_SEPARATOR)

	#columns
	if column == "stats":
		if dungeon.run:
			effects_max_page = len(ally.effects) + 1
			if page > effects_max_page:
				page = effects_max_page
		else:
			page = 1

		if page == 1:
			name_text = intermediate_font.render(f"Name : {ally.name}", 1, BLACK)
			screen.blit(name_text, ( 15, 80))
			level_text = intermediate_font.render(f"Level : {ally.level}", 1, BLACK)
			screen.blit(level_text, ( 15, 100))
			x = ally.level
			xp_check = x * x * 300 + int(math.exp(x))
			xp_text = intermediate_font.render(f"Xp : {ally.xp}/{xp_check}", 1, BLACK)
			screen.blit(xp_text, ( 15, 120))
			mastery_text = intermediate_font.render(f"Mastery : {ally.mastery} points", 1, BLACK)
			screen.blit(mastery_text, ( 15, 140))
			hp_text = intermediate_font.render(f"Hp : {ally.hp}/{ally.max_hp}", 1, BLACK)
			screen.blit(hp_text, ( 15, 160))
			mp_text = intermediate_font.render(f"Mp : {ally.mp}/{ally.max_mp}", 1, BLACK)
			screen.blit(mp_text, ( 15, 180))
			if ally.special_ressource == "rage":
				rage_text = intermediate_font.render(f"Rage : {ally.rage}/100", 1, BLACK)
				screen.blit(rage_text, ( 325, 180))
			armor_text = intermediate_font.render(f"Armor : {ally.armor}", 1, BLACK)
			screen.blit(armor_text, ( 15, 200))
			dmg_text = intermediate_font.render(f"Dmg : {ally.dmg}", 1, BLACK)
			screen.blit(dmg_text, ( 15, 220))
			magic_dmg_text = intermediate_font.render(f"Magic dmg : {ally.magic_dmg}", 1, BLACK)
			screen.blit(magic_dmg_text, ( 15, 240))
			critical_chance_text = intermediate_font.render(f"Critical chance : {ally.crit_chance}", 1, BLACK)
			screen.blit(critical_chance_text, ( 15, 260))
			defensive_roll_chance_text = intermediate_font.render(f"Defensive roll chance : {ally.defensive_roll_chance}", 1, BLACK)
			screen.blit(defensive_roll_chance_text, ( 15, 280))
			critical_defensive_roll_text = intermediate_font.render(f"Critical defensive roll chance : {ally.crit_defensive_roll_chance}", 1, BLACK)
			screen.blit(critical_defensive_roll_text, ( 15, 300))
			if ally.riposte:
				riposte_dmg_text = intermediate_font.render(f"Riposte dmg multiplier : {ally.riposte_strength}x", 1, BLACK)
				screen.blit(riposte_dmg_text, ( 15, 320))
			speed_text = intermediate_font.render(f"Speed : {ally.speed}", 1, BLACK)
			screen.blit(speed_text, ( 15, 340))
			active_skill_text = intermediate_font.render(f"Active skills : {ally.learned_skill_name}", 1, BLACK)
			screen.blit(active_skill_text, ( 15, 360))
			passive_skill_text = intermediate_font.render(f"Passives : {ally.passive_skill_name}", 1, BLACK)
			screen.blit(passive_skill_text, ( 15, 380))
			if dungeon.run:
				effects_base_text = intermediate_font.render("Current Effects :", 1, BLACK)
				screen.blit(effects_base_text, ( 15, 420))
				effects_offset = 0
				for effect in ally.effects:
					effects_text = intermediate_font.render(f"- {effect['name']}", 1, BLACK)
					screen.blit(effects_text, ( 15 + effects_base_text.get_width() + 10, 420 + effects_offset))
					effects_offset += 20

		elif page > 1:
			effect = ally.effects[page - 2]
			name_text = intermediate_font.render(f"Effect name : {effect['name']}", 1, BLACK)
			screen.blit(name_text, ( 15, 100))
			screen.blit(effect["icon"], ( 400, 100))
			type_text = intermediate_font.render(f"Type : {effect['type']}", 1, BLACK)
			screen.blit(type_text, ( 15, 130))
			sub_type_text = intermediate_font.render(f"Subtype : {effect['sub_type']}", 1, BLACK)
			screen.blit(sub_type_text, ( 15, 160))
			if (effect['end'] - ally.global_turn_count) >= 1000:
				duration_text = intermediate_font.render(f"Remaining duration : Permanent", 1, BLACK)
			else:
				duration_text = intermediate_font.render(f"Remaining duration : {effect['end'] - ally.global_turn_count}", 1, BLACK)
			screen.blit(duration_text, ( 15, 190))
			power_text = intermediate_font.render(f"Power : {effect['power']}", 1, BLACK)
			screen.blit(power_text, ( 15, 220))
			


	if column == "skill":
		all_skills = ally.learned_skill_name + ally.passive_skill_name
		max_page = len(all_skills)
		if max_page > 0:
			if page > max_page:
				page = max_page
			viewed_skill = all_skills[page - 1]
			number_of_description_lines = ally.skills_description[viewed_skill]["description_lines"]
			name_text = intermediate_font.render("Skill Name :", 1, BLACK)
			screen.blit(name_text, ( 15, 80))
			skill_name_text = intermediate_font.render(ally.skills_description[viewed_skill]["name"], 1, BLACK)
			screen.blit(skill_name_text, ( 15, 100))
			category_text = intermediate_font.render("Category :", 1, BLACK)
			screen.blit(category_text, ( 15, 150))
			skill_category_text = intermediate_font.render(ally.skills_description[viewed_skill]["category"], 1, BLACK)
			screen.blit(skill_category_text, ( 15, 170))
			if "cost" in ally.skills_description[viewed_skill]:
				cost_text = intermediate_font.render("Cost :", 1, BLACK)
				screen.blit(cost_text, (300, 150))
				skill_cost_text = intermediate_font.render(ally.skills_description[viewed_skill]["cost"], 1, BLACK)
				screen.blit(skill_cost_text, (300, 170))
			effect_text = intermediate_font.render("Effect :", 1, BLACK)
			screen.blit(effect_text, ( 15, 220))
			skill_effect_text = intermediate_font.render(ally.skills_description[viewed_skill]["effect"], 1, BLACK)
			screen.blit(skill_effect_text, ( 15, 240))
			if "cooldown" in ally.skills_description[viewed_skill]:
				cooldown_text = intermediate_font.render("Cooldown :", 1, BLACK)
				screen.blit(cooldown_text, ( 15, 290))
				skill_cooldown_text = intermediate_font.render(ally.skills_description[viewed_skill]["cooldown"], 1, BLACK)
				screen.blit(skill_cooldown_text, ( 15, 310))
				description_text = intermediate_font.render("Description :", 1, BLACK)
				screen.blit(description_text, ( 15, 360))
				skill_description_text_1 = intermediate_font.render(ally.skills_description[viewed_skill]["description_1"], 1, BLACK)
				screen.blit(skill_description_text_1, ( 15, 380))
				if number_of_description_lines > 1:
					skill_description_text_2 = intermediate_font.render(ally.skills_description[viewed_skill]["description_2"], 1, BLACK)
					screen.blit(skill_description_text_2, ( 15, 400))
				if number_of_description_lines > 2:
					skill_description_text_3 = intermediate_font.render(ally.skills_description[viewed_skill]["description_3"], 1, BLACK)
					screen.blit(skill_description_text_3, ( 15, 420))
				if number_of_description_lines > 3:
					skill_description_text_4 = intermediate_font.render(ally.skills_description[viewed_skill]["description_4"], 1, BLACK)
					screen.blit(skill_description_text_4, ( 15, 440))
			else:
				description_text = intermediate_font.render("Description :", 1, BLACK)
				screen.blit(description_text, ( 15, 290))
				skill_description_text_1 = intermediate_font.render(ally.skills_description[viewed_skill]["description_1"], 1, BLACK)
				screen.blit(skill_description_text_1, ( 15, 310))
				if number_of_description_lines > 1:
					skill_description_text_2 = intermediate_font.render(ally.skills_description[viewed_skill]["description_2"], 1, BLACK)
					screen.blit(skill_description_text_2, ( 15, 330))
				if number_of_description_lines > 2:
					skill_description_text_3 = intermediate_font.render(ally.skills_description[viewed_skill]["description_3"], 1, BLACK)
					screen.blit(skill_description_text_3, ( 15, 350))
				if number_of_description_lines > 3:
					skill_description_text_4 = intermediate_font.render(ally.skills_description[viewed_skill]["description_4"], 1, BLACK)
					screen.blit(skill_description_text_4, ( 15, 370))
		else:
			no_skill_text = font.render("No skill or passive acquired.", 1, BLACK)
			screen.blit(no_skill_text, ( WIDTH//2 - no_skill_text.get_width()//2, HEIGHT//2 - no_skill_text.get_height()//2))

	if column == "title":
		offset = 80
		if ally.killer:
			killer_title_text = intermediate_font.render(f"Killer", 1, BLACK)
			screen.blit(killer_title_text, ( 15, offset))
			killer_effect_text = intermediate_font.render(f"{ally.killer_effect}", 1, BLACK)
			screen.blit(killer_effect_text, ( 250, offset))
			offset += 20
		if ally.slaughterer:
			slaughterer_title_text = intermediate_font.render(f"Slaughterer", 1, BLACK)
			screen.blit(slaughterer_title_text, ( 15, offset))
			slaughterer_effect_text = intermediate_font.render(f"{ally.slaughterer_effect}", 1, BLACK)
			screen.blit(slaughterer_effect_text, ( 250, offset))
			offset += 20
		if ally.goblin_killer:
			goblin_killer_title_text = intermediate_font.render(f"Goblin Killer", 1, BLACK)
			screen.blit(goblin_killer_title_text, ( 15, offset))
			offset += 20
		if ally.hobgoblin_killer:
			hobgoblin_killer_title_text = intermediate_font.render(f"Hobgoblin Killer", 1, BLACK)
			screen.blit(hobgoblin_killer_title_text, ( 15, offset))
			offset += 20
		if ally.survivor:
			survivor_title_text = intermediate_font.render(f"Survivor", 1, BLACK)
			screen.blit(survivor_title_text, ( 15, offset))
			offset += 20
		if offset == 80:
			no_title_text = font.render("No title acquired.", 1, BLACK)
			screen.blit(no_title_text, ( WIDTH//2 - no_title_text.get_width()//2, HEIGHT//2 - no_title_text.get_height()//2))

	if column == "records":
		enemy_killed_text = intermediate_font.render(f"Number of enemies killed : {ally.enemy_killed}", 1, BLACK)
		screen.blit(enemy_killed_text, ( 15, 80))
		goblin_killed_text = intermediate_font.render(f"Goblin killed : {ally.goblin_killed}", 1, BLACK)
		screen.blit( goblin_killed_text, ( 15, 100))
		hobgoblin_killed_text = intermediate_font.render(f"Hobgoblin killed : {ally.hobgoblin_killed}", 1, BLACK)
		screen.blit( hobgoblin_killed_text, ( 15, 120))

	pygame.draw.rect(screen, GRAY, LOWER_LEFT_ARROW_BUTTON)
	screen.blit(LEFT_ARROW_IMAGE, (LOWER_LEFT_ARROW_BUTTON.x, LOWER_LEFT_ARROW_BUTTON.y))
	pygame.draw.rect(screen, GRAY, LOWER_RIGHT_ARROW_BUTTON)
	screen.blit(RIGHT_ARROW_IMAGE, (LOWER_RIGHT_ARROW_BUTTON.x, LOWER_RIGHT_ARROW_BUTTON.y))
	pygame.draw.rect(screen, GRAY, BACK_BUTTON_MIDDLE)
	back_button_text = font.render("BACK", 1, BLACK)
	screen.blit(back_button_text, (BACK_BUTTON_MIDDLE.centerx - back_button_text.get_width()//2, BACK_BUTTON_MIDDLE.centery - back_button_text.get_height()//2))

	pygame.display.update()

def check_character_sheet(ally,party_index):
	click = False
	run = True
	column = "stats"
	page = 1
	while run:
		clock.tick(60)
		mx, my = pygame.mouse.get_pos()

		if UPPER_LEFT_ARROW_BUTTON.collidepoint((mx, my)):
			if click:
				if party_index > 0:
					party_index -= 1
					ally = party.party[party_index]
		if UPPER_RIGHT_ARROW_BUTTON.collidepoint((mx, my)):
			if click:
				if party_index < 3 and len(party.party) > party_index + 1:
					party_index += 1
					ally = party.party[party_index]
		if STATS_COLUMN_BUTTON.collidepoint((mx, my)):
			if click:
				column = "stats"
				page = 1
		if SKILL_COLUMN_BUTTON.collidepoint((mx, my)):
			if click:
				column = "skill"
				page = 1
		if TITLE_COLUMN_BUTTON.collidepoint((mx, my)):
			if click:
				column = "title"
				page = 1
		if RECORDS_COLUMN_BUTTON.collidepoint((mx, my)):
			if click:
				column = "records"
				page = 1
		if LOWER_LEFT_ARROW_BUTTON.collidepoint((mx, my)):
			if click:
				if page > 1:
					page -= 1
		if LOWER_RIGHT_ARROW_BUTTON.collidepoint((mx, my)):
			if click:
				page += 1

		if BACK_BUTTON_MIDDLE.collidepoint((mx, my)):
			if click:
				run = False
				break

		click = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					run = False
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True

		check_character_sheet_draw_window(ally,column,page)

#############################
######## Check Party ########

def check_party_draw_window():
	BACKGROUND()
	pygame.draw.rect(screen, GRAY, TOP_BAND)
	check_party_text = font.render("Party", 1, BLACK)
	screen.blit(check_party_text, (TOP_BAND.centerx - check_party_text.get_width()//2, TOP_BAND.centery - check_party_text.get_height()//2))

	overall_text = None
	for ally in party.party:
		x = ally.level
		xp_check = x * x * 300 + int(math.exp(x))
		coordinate_x, coordinate_y = get_coordinate_new(ally,"party")
		overall_text = font.render(f"{ally.name} :", 1, BLACK)
		screen.blit(overall_text, (75, coordinate_y))

		overall_text = font.render(f"lvl: {ally.level}", 1, BLACK)
		screen.blit(overall_text, (75, coordinate_y + 25))
		overall_text = font.render(f"{ally.hp}/{ally.max_hp} hp", 1, BLACK)
		screen.blit(overall_text, (75, coordinate_y + 50))

		overall_text = font.render(f"{ally.xp}/{xp_check} xp", 1, BLACK)
		screen.blit(overall_text, (200, coordinate_y + 25))
		overall_text = font.render(f"{ally.mp}/{ally.max_mp} mp", 1, BLACK)
		screen.blit(overall_text, (200, coordinate_y + 50))
	
	if len(party.party) >= 1:
		pygame.draw.rect(screen, GRAY, FIRST_MEMBER_BUTTON)
		screen.blit(EYE_IMAGE, (FIRST_MEMBER_BUTTON.x, FIRST_MEMBER_BUTTON.y))
	if len(party.party) >= 2:
		pygame.draw.rect(screen, GRAY, SECOND_MEMBER_BUTTON)
		screen.blit(EYE_IMAGE, (SECOND_MEMBER_BUTTON.x, SECOND_MEMBER_BUTTON.y))
	if len(party.party) >= 3:
		pygame.draw.rect(screen, GRAY, THIRD_MEMBER_BUTTON)
		screen.blit(EYE_IMAGE, (THIRD_MEMBER_BUTTON.x, THIRD_MEMBER_BUTTON.y))
	if len(party.party) == 4:
		pygame.draw.rect(screen, GRAY, FOURTH_MEMBER_BUTTON)
		screen.blit(EYE_IMAGE, (FOURTH_MEMBER_BUTTON.x, FOURTH_MEMBER_BUTTON.y))

	pygame.draw.rect(screen, GRAY, BACK_BUTTON)
	back_button_text = font.render("Back", 1, BLACK)
	screen.blit(back_button_text, (BACK_BUTTON.centerx - back_button_text.get_width()//2, BACK_BUTTON.centery - back_button_text.get_height()//2))

	pygame.display.update()

def check_party():
	click = False
	run = True
	while run:
		clock.tick(60)
		mx, my = pygame.mouse.get_pos()

		if FIRST_MEMBER_BUTTON.collidepoint((mx, my)):
			if click and len(party.party) >= 1:
				check_character_sheet(party.party[0],0)
		if SECOND_MEMBER_BUTTON.collidepoint((mx, my)):
			if click and len(party.party) >= 2:
				check_character_sheet(party.party[1],1)
		if THIRD_MEMBER_BUTTON.collidepoint((mx, my)):
			if click and len(party.party) >= 3:
				check_character_sheet(party.party[2],2)
		if FOURTH_MEMBER_BUTTON.collidepoint((mx, my)):
			if click and len(party.party) == 4:
				check_character_sheet(party.party[3],3)
		if BACK_BUTTON.collidepoint((mx, my)):
			if click:
				run = False

		click = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					run = False
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True

		check_party_draw_window()

##############################
####### Check  Storage #######

def check_storage_draw_window():
	BACKGROUND()
	pygame.draw.rect(screen, GRAY, TOP_BAND)
	storage_text = font.render("Storage", 1, BLACK)
	screen.blit(storage_text, (TOP_BAND.centerx - storage_text.get_width()//2, TOP_BAND.centery - storage_text.get_height()//2))

	offset = 100
	storage_gold_text = font.render(f"You have {inventory.town_gold} Gold", 1, BLACK)
	screen.blit(storage_gold_text, (WIDTH//2 - storage_gold_text.get_width()//2, HEIGHT//5 - storage_gold_text.get_height()//2))
	
	item_text = font.render("In Storage :", 1, BLACK)
	screen.blit(item_text, (WIDTH//2 - item_text.get_width()//2, HEIGHT//5 + 50 - item_text.get_height()//2))
	for item in inventory.town_storage:
		item_storage_text = font.render(f"{item} x{inventory.town_storage[item]}", 1, BLACK)
		screen.blit(item_storage_text, (WIDTH//2 - item_storage_text.get_width()//2, HEIGHT//5 + offset - item_storage_text.get_height()//2))
		offset += 30

	pygame.draw.rect(screen, GRAY, BACK_BUTTON)
	back_button_text = font.render("Back", 1, BLACK)
	screen.blit(back_button_text, (BACK_BUTTON.centerx - back_button_text.get_width()//2, BACK_BUTTON.centery - back_button_text.get_height()//2))
	
	pygame.display.update()

def check_storage():
	click = False
	run = True
	while run:
		clock.tick(60)
		mx, my = pygame.mouse.get_pos()

		if BACK_BUTTON.collidepoint((mx, my)):
			if click:
				break

		click = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					run = False
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True

		check_storage_draw_window()


#############################

def all_dead():
	count = 0
	for ally in party.party:
		if ally.dead == False:
			count += 1
	if count != 0:
		return False
	else:
		return True

###########################
###### Dungeon Class ######

class dungeon_base():
	run = False
	defeated = False

	fight = False
	current_floor = 1
	current_room = 0
	max_room = 0
	room_exploration_progress = 0
	floor_completed = False
	room_till_next_floor = 20
	room_to_return = 0
	is_the_way_to_the_next_floor_known = False
	min_room_till_next_floor = 20
	floor_aggro_level = 25
	floor_monsterpedia = None
	returning = False

	floor_1_room_explored = 0
	floor_1_max_room = 100
	floor_1_completed = False
	floor_1_next_floor_found = False
	floor_1_min_room_till_next_floor = 20
	floor_1_aggro_level = 25
	
	floor_2_room_explored = 0
	floor_2_max_room = 100
	floor_2_completed = False
	floor_2_next_floor_found = False
	floor_2_min_room_till_next_floor = 25
	floor_2_aggro_level = 35

	floor_3_room_explored = 0
	floor_3_max_room = 150
	floor_3_completed = False
	floor_3_next_floor_found = False
	floor_3_min_room_till_next_floor = 25
	floor_3_aggro_level = 50


	environment_text = None
	entering_text = "You've entered the dungeon..."
	fight_text_list = ["'Enemies incoming !'", "'To arms !'", "'Get ready for battle !'"]
	intimidation_text_list = ["No enemy dares to approach you.", "'They're afraid, good.'", "'You sense enemies nearby but none attacks.'"]
	sneak_text_list = ["You advance silently.", "You advance in the shadows.", "You press forward not getting noticed."]
	end_fight_text_list = ["You survived this fight", "'Well done !'", "'Another victory.'"]

###########################
###### Go To Dungeon ######

def set_floor_variable():
	dungeon.current_room = 0
	dungeon.room_to_return = 0

	if dungeon.current_floor == 1:
		dungeon.room_till_next_floor = dungeon.floor_1_min_room_till_next_floor
		dungeon.max_room = dungeon.floor_1_max_room
		dungeon.room_exploration_progress = dungeon.floor_1_room_explored
		dungeon.floor_completed = dungeon.floor_1_completed
		dungeon.is_the_way_to_the_next_floor_known = dungeon.floor_1_next_floor_found
		dungeon.min_room_till_next_floor = dungeon.floor_1_min_room_till_next_floor
		dungeon.floor_aggro_level = dungeon.floor_1_aggro_level
		dungeon.floor_monsterpedia = monsterpedia.floor_1
		if dungeon.returning:
			dungeon.room_to_return = dungeon.floor_1_min_room_till_next_floor
			dungeon.room_till_next_floor = 0
			dungeon.current_room = dungeon.floor_1_min_room_till_next_floor

	if dungeon.current_floor == 2:
		dungeon.room_exploration_progress = dungeon.floor_2_room_explored
		dungeon.max_room = dungeon.floor_2_max_room
		dungeon.floor_completed = dungeon.floor_2_completed
		dungeon.is_the_way_to_the_next_floor_known = dungeon.floor_2_next_floor_found
		dungeon.room_till_next_floor = dungeon.floor_2_min_room_till_next_floor
		dungeon.min_room_till_next_floor = dungeon.floor_2_min_room_till_next_floor
		dungeon.floor_aggro_level = dungeon.floor_2_aggro_level
		dungeon.floor_monsterpedia = monsterpedia.floor_2
		if dungeon.returning:
			dungeon.room_to_return = dungeon.floor_2_min_room_till_next_floor
			dungeon.room_till_next_floor = 0
			dungeon.current_room = dungeon.floor_2_min_room_till_next_floor
		
	if dungeon.current_floor == 3:
		dungeon.room_exploration_progress = dungeon.floor_3_room_explored
		dungeon.max_room = dungeon.floor_3_max_room
		dungeon.floor_completed = dungeon.floor_3_completed
		dungeon.is_the_way_to_the_next_floor_known = dungeon.floor_3_next_floor_found
		dungeon.room_till_next_floor = dungeon.floor_3_min_room_till_next_floor
		dungeon.min_room_till_next_floor = dungeon.floor_3_min_room_till_next_floor
		dungeon.floor_aggro_level = dungeon.floor_3_aggro_level
		dungeon.floor_monsterpedia = monsterpedia.floor_3
		if dungeon.returning:
			dungeon.room_to_return = dungeon.floor_3_min_room_till_next_floor
			dungeon.room_till_next_floor = 0
			dungeon.current_room = dungeon.floor_3_min_room_till_next_floor

def save_current_floor_variable():
	if dungeon.current_floor == 1:
		dungeon.floor_1_room_explored = dungeon.room_exploration_progress
		dungeon.floor_1_completed = dungeon.floor_completed
		dungeon.floor_1_next_floor_found = dungeon.is_the_way_to_the_next_floor_known

	if dungeon.current_floor == 2:
		dungeon.floor_2_room_explored = dungeon.room_exploration_progress
		dungeon.floor_2_completed = dungeon.floor_completed
		dungeon.floor_2_next_floor_found = dungeon.is_the_way_to_the_next_floor_known
		
	if dungeon.current_floor == 3:
		dungeon.floor_3_room_explored = dungeon.room_exploration_progress
		dungeon.floor_3_completed = dungeon.floor_completed
		dungeon.floor_3_next_floor_found = dungeon.is_the_way_to_the_next_floor_known

def found_next_floor():
    if dungeon.floor_completed:
        dungeon.is_the_way_to_the_next_floor_known = True

    if dungeon.is_the_way_to_the_next_floor_known == False and dungeon.floor_completed == False:
        if dungeon.current_room >= dungeon.room_till_next_floor:
            roll = rand.randint(0,100)
            if roll <= int(dungeon.room_exploration_progress/dungeon.max_room * 100):
                dungeon.is_the_way_to_the_next_floor_known = True
                dungeon.room_till_next_floor = 0

    if dungeon.is_the_way_to_the_next_floor_known:
        if dungeon.current_floor == 1:
            dungeon.floor_1_next_floor_found = True

def is_intimidation_or_sneak_highest():
	intimidation_level = 0
	for ally in party.party_alive:
		intimidation_level += ally.intimidation
	avg_sneak = 0
	for ally in party.party_alive:
		avg_sneak += ally.sneak
	avg_sneak = int(avg_sneak/len(party.party_alive))
	if intimidation_level >= avg_sneak:
		return intimidation_level, "intimidation"
	else:
		return avg_sneak, "sneak"

def dungeon_decide_event(activity):
	aggro_level = dungeon.floor_aggro_level
	if activity == "explore":
		allied_roll, roll_type = is_intimidation_or_sneak_highest()
		aggro_level = int(aggro_level * 1.5)
		roll = rand.randint(allied_roll,aggro_level)
		if roll <= aggro_level * 0.7:
			dungeon.fight = True
			set_environment_text("fight")
		else:
			set_environment_text(roll_type)

	if activity == "next floor":
		if dungeon.is_the_way_to_the_next_floor_known == True:
			allied_roll, roll_type = is_intimidation_or_sneak_highest()
			roll = rand.randint(allied_roll,aggro_level)
			if roll <= aggro_level * 0.7:
				dungeon.fight = True
				set_environment_text("fight")
			else:
				set_environment_text(roll_type)
		else:
			dungeon.environment_text = "You do not know the way to the next floor."

	if activity == "farm":
		dungeon.fight = True
		set_environment_text("fight")
	
	if activity == "return":
		allied_roll, roll_type = is_intimidation_or_sneak_highest()
		aggro_level = int(aggro_level * 0.75)
		roll = rand.randint(allied_roll,aggro_level)
		if roll <= aggro_level * 0.7:
			dungeon.fight = True
			set_environment_text("fight")
		else:
			set_environment_text(roll_type)

def dungeon_room_explore():
	dungeon.current_room += 1
	dungeon.room_to_return += 1

	if dungeon.is_the_way_to_the_next_floor_known:
		dungeon.room_till_next_floor += 1
		if dungeon.room_till_next_floor > dungeon.max_room - dungeon.min_room_till_next_floor:
			dungeon.room_till_next_floor = dungeon.max_room - dungeon.min_room_till_next_floor
    
	if dungeon.room_to_return > dungeon.max_room - dungeon.min_room_till_next_floor:
		dungeon.room_to_return = dungeon.max_room - dungeon.min_room_till_next_floor
    
	if dungeon.current_room > dungeon.room_exploration_progress:
		dungeon.room_exploration_progress = dungeon.current_room
    
	if dungeon.room_exploration_progress == dungeon.max_room:
		dungeon.floor_completed = True

def set_environment_text(activity):
	text_snapshot = dungeon.environment_text
	if activity == "fight":
		dungeon.environment_text = rand.choice(dungeon.fight_text_list)
	if activity == "intimidation":
		dungeon.environment_text = rand.choice(dungeon.intimidation_text_list)
	if activity == "sneak":
		dungeon.environment_text = rand.choice(dungeon.sneak_text_list)
	if activity == "fight end":
		dungeon.environment_text = rand.choice(dungeon.end_fight_text_list)

	if dungeon.environment_text == text_snapshot:
		set_environment_text(activity)

def dungeon_explore():
	dungeon_room_explore()
	dungeon_decide_event("explore")
	found_next_floor()

def dungeon_next_floor():
	dungeon_decide_event("next floor")
	if dungeon.room_till_next_floor == 0:
		dungeon.current_floor += 1
		dungeon.environment_text = f"You've advanced into floor {dungeon.current_floor}."
		set_floor_variable()
	else:
		dungeon.room_till_next_floor -= 1

def dungeon_return():
	dungeon.room_to_return -= 1
	dungeon.room_till_next_floor += 1
	if dungeon.room_to_return <= 0:
		if dungeon.current_floor == 1:
			inventory_sorting()
			for ally in party.party:
				clear_all_effects(ally)
			dungeon.run = False
			play_town_music()
			for ally in party.party:
				if ally.special_ressource == "rage":
					ally.rage = 0
		else:
			dungeon.current_floor -= 1
			dungeon.returning = True
			dungeon.environment_text = f"You've returned into floor {dungeon.current_floor}."
			set_floor_variable()
			dungeon.returning = False
	else:
		dungeon_decide_event("return")

def in_dungeon_draw_window():
	BACKGROUND()
	pygame.draw.rect(screen, GRAY, TOP_BAND)
	context_text = font.render("Dungeon", 1, BLACK)
	screen.blit(context_text, ( TOP_BAND.centerx - context_text.get_width()//2, TOP_BAND.centery - context_text.get_height()//2))
	current_floor_text = intermediate_font.render(f"Floor {dungeon.current_floor}", 1, BLACK)
	screen.blit(current_floor_text, ( 5, 80))
	screen.blit(DUNGEON_RETURN_IMAGE, ( 5, 100))
	room_to_return_text = intermediate_font.render(f"{dungeon.room_to_return}", 1, BLACK)
	screen.blit(room_to_return_text, ( 5 + DUNGEON_RETURN_IMAGE.get_width(), 100))

	if dungeon.floor_completed:
		explored_floor_text = intermediate_font.render("Completed !", 1, BLACK)
	else:
		if dungeon.room_exploration_progress != 0:
			exploration_progress = int(dungeon.room_exploration_progress/dungeon.max_room * 100)
		else:
			exploration_progress = 0
		explored_floor_text = intermediate_font.render(f"{exploration_progress}%", 1, BLACK)
	screen.blit(explored_floor_text, (495 - explored_floor_text.get_width(), 80))

	if dungeon.is_the_way_to_the_next_floor_known:
		room_till_next_floor_text = intermediate_font.render(f"{dungeon.room_till_next_floor} room", 1, BLACK)
		screen.blit(room_till_next_floor_text, (495 - room_till_next_floor_text.get_width() - DUNGEON_NEXT_FLOOR_TRUE_IMAGE.get_width(), 100))
		screen.blit(DUNGEON_NEXT_FLOOR_TRUE_IMAGE, (495 - DUNGEON_NEXT_FLOOR_TRUE_IMAGE.get_width(), 100))
	else:
		screen.blit(DUNGEON_NEXT_FLOOR_FALSE_IMAGE, (495 - DUNGEON_NEXT_FLOOR_FALSE_IMAGE.get_width(), 100))

	environment_text = font.render(dungeon.environment_text, 1, BLACK)
	screen.blit(environment_text, (30, 295))

	pygame.draw.rect(screen, GRAY, DUNGEON_CHECK_PARTY_BUTTON)
	screen.blit(CHECK_PARTY_IMAGE, ( DUNGEON_CHECK_PARTY_BUTTON.x, DUNGEON_CHECK_PARTY_BUTTON.y))
	pygame.draw.rect(screen, GRAY, DUNGEON_USE_CONSUMABLES_BUTTON)
	screen.blit(DUNGEON_CONSUMABLE_IMAGE, ( DUNGEON_USE_CONSUMABLES_BUTTON.x, DUNGEON_USE_CONSUMABLES_BUTTON.y))
	pygame.draw.rect(screen, GRAY, DUNGEON_CHECK_LOOT_BUTTON)
	screen.blit(CHECK_LOOT_IMAGE, ( DUNGEON_CHECK_LOOT_BUTTON.x, DUNGEON_CHECK_LOOT_BUTTON.y))

	pygame.draw.rect(screen, INTERMEDIATE_GRAY, DUNGEON_BOTTOM_BAND)
	pygame.draw.rect(screen, GRAY, DUNGEON_EXPLORE_BUTTON)
	explore_text = intermediate_font.render("Explore", 1, BLACK)
	screen.blit(explore_text, (DUNGEON_EXPLORE_BUTTON.centerx - explore_text.get_width()//2, DUNGEON_EXPLORE_BUTTON.centery - explore_text.get_height()//2))
	pygame.draw.rect(screen, GRAY, DUNGEON_FARM_BUTTON)
	farm_text = intermediate_font.render("Farm", 1, BLACK)
	screen.blit(farm_text, (DUNGEON_FARM_BUTTON.centerx - farm_text.get_width()//2, DUNGEON_FARM_BUTTON.centery - farm_text.get_height()//2))
	pygame.draw.rect(screen, GRAY, DUNGEON_NEXT_FLOOR_BUTTON)
	sneak_text = intermediate_font.render("Next Floor", 1, BLACK)
	screen.blit(sneak_text, (DUNGEON_NEXT_FLOOR_BUTTON.centerx - sneak_text.get_width()//2, DUNGEON_NEXT_FLOOR_BUTTON.centery - sneak_text.get_height()//2))
	pygame.draw.rect(screen, GRAY, DUNGEON_RETURN_BUTTON)
	return_text = intermediate_font.render("Return", 1, BLACK)
	screen.blit(return_text, (DUNGEON_RETURN_BUTTON.centerx - return_text.get_width()//2, DUNGEON_RETURN_BUTTON.centery - return_text.get_height()//2))

	pygame.display.update()

def in_dungeon():
	click = False
	dungeon.run = True
	dungeon.fight = False
	
	play_dungeon_music()
	dungeon.environment_text = dungeon.entering_text
	set_floor_variable()
	for ally in party.party_alive:
		apply_passive_effects(ally)
		if ally.special_ressource == "rage":
			ally.rage = 0
	
	while dungeon.run:
		clock.tick(60)
		mx, my = pygame.mouse.get_pos()

		if click:
			save_current_floor_variable()

		if DUNGEON_CHECK_PARTY_BUTTON.collidepoint((mx, my)):
			if click:
				check_party()
		if DUNGEON_USE_CONSUMABLES_BUTTON.collidepoint((mx, my)):
			if click:
				dungeon_choose_consumable()
		if DUNGEON_CHECK_LOOT_BUTTON.collidepoint((mx, my)):
			if click:
				dungeon_check_loot()

		if DUNGEON_EXPLORE_BUTTON.collidepoint((mx, my)):
			if click and dungeon.fight == False:
				dungeon_explore()
		if DUNGEON_FARM_BUTTON.collidepoint((mx, my)):
			if click and dungeon.fight == False:
				dungeon_decide_event("farm")
		if DUNGEON_NEXT_FLOOR_BUTTON.collidepoint((mx, my)):
			if click and dungeon.fight == False:
				dungeon_next_floor()
		if DUNGEON_RETURN_BUTTON.collidepoint((mx, my)):
			if click and dungeon.fight == False:
				dungeon_return()

		click = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				dungeon.run = False
				pygame.quit()
				sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True

		if dungeon.fight and click:
			in_fight()
			dungeon.fight = False
			if dungeon.defeated:
				dungeon.defeated = False
				dungeon.run = False
				play_town_music()
			else:
				set_environment_text("fight end")
				play_dungeon_music()
		
		in_dungeon_draw_window()

def consumable_effect(ally,item_name,item_emplacement):
	if item_name == "Small Health Potion":
		ally.hp += 50
		if ally.hp > ally.max_hp:
			ally.hp = ally.max_hp
		del inventory.dungeon_consumable[item_emplacement]
		animation = {"color" : RED, "value" : "+50 HP", "current_frame" : 0, "max_frame" : 60}
		return animation

	if item_name == "Medium Health Potion":
		ally.hp += 250
		if ally.hp > ally.max_hp:
			ally.hp = ally.max_hp
		del inventory.dungeon_consumable[item_emplacement]
		animation = {"color" : RED, "value" : "+250 HP", "current_frame" : 0, "max_frame" : 60}
		return animation

	if item_name == "Large Health Potion":
		ally.hp += 1000
		if ally.hp > ally.max_hp:
			ally.hp = ally.max_hp
		del inventory.dungeon_consumable[item_emplacement]
		animation = {"color" : RED, "value" : "+1000 HP", "current_frame" : 0, "max_frame" : 60}
		return animation

	if item_name == "Small Mana Potion":
		ally.mp += 10
		if ally.mp > ally.max_mp:
			ally.mp = ally.max_mp
		del inventory.dungeon_consumable[item_emplacement]
		animation = {"color" : BLUE, "value" : "+10 MP", "current_frame" : 0, "max_frame" : 60}
		return animation

	if item_name == "Medium Mana Potion":
		ally.mp += 50
		if ally.mp > ally.max_mp:
			ally.mp = ally.max_mp
		del inventory.dungeon_consumable[item_emplacement]
		animation = {"color" : BLUE, "value" : "+50 MP", "current_frame" : 0, "max_frame" : 60}
		return animation

	if item_name == "Large Mana Potion":
		ally.mp += 200
		if ally.mp > ally.max_mp:
			ally.mp = ally.max_mp
		del inventory.dungeon_consumable[item_emplacement]
		animation = {"color" : BLUE, "value" : "+200 MP", "current_frame" : 0, "max_frame" : 60}
		return animation


def consumable_info(item_name):
	item_description = None
	if item_name == "Small Health Potion":
		item_description = "Restore 50 HP to the user."
	if item_name == "Medium Health Potion":
		item_description = "Restore 250 HP to the user."
	if item_name == "Large Health Potion":
		item_description = "Restore 1000 HP to the user."
	if item_name == "Small Mana Potion":
		item_description = "Restore 10 MP to the user."
	if item_name == "Medium Mana Potion":
		item_description = "Restore 50 MP to the user."
	if item_name == "Large Mana Potion":
		item_description = "Restore 200 MP to the user."

	return item_description

def consumable_icon(emplacement):
	icon = None
	if emplacement == 1:
		if inventory.dungeon_consumable[1] == "Small Health Potion":
			icon = SMALL_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[1] == "Medium Health Potion":
			icon = MEDIUM_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[1] == "Large Health Potion":
			icon = LARGE_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[1] == "Small Mana Potion":
			icon = SMALL_MANA_POTION_IMAGE
		if inventory.dungeon_consumable[1] == "Medium Mana Potion":
			icon = MEDIUM_MANA_POTION_IMAGE
		if inventory.dungeon_consumable[1] == "Large Mana Potion":
			icon = LARGE_MANA_POTION_IMAGE
			
	if emplacement == 2:
		if inventory.dungeon_consumable[2] == "Small Health Potion":
			icon = SMALL_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[2] == "Medium Health Potion":
			icon = MEDIUM_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[2] == "Large Health Potion":
			icon = LARGE_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[2] == "Small Mana Potion":
			icon = SMALL_MANA_POTION_IMAGE
		if inventory.dungeon_consumable[2] == "Medium Mana Potion":
			icon = MEDIUM_MANA_POTION_IMAGE
		if inventory.dungeon_consumable[2] == "Large Mana Potion":
			icon = LARGE_MANA_POTION_IMAGE
			
	if emplacement == 3:
		if inventory.dungeon_consumable[3] == "Small Health Potion":
			icon = SMALL_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[3] == "Medium Health Potion":
			icon = MEDIUM_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[3] == "Large Health Potion":
			icon = LARGE_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[3] == "Small Mana Potion":
			icon = SMALL_MANA_POTION_IMAGE
		if inventory.dungeon_consumable[3] == "Medium Mana Potion":
			icon = MEDIUM_MANA_POTION_IMAGE
		if inventory.dungeon_consumable[3] == "Large Mana Potion":
			icon = LARGE_MANA_POTION_IMAGE
			
	if emplacement == 4:
		if inventory.dungeon_consumable[4] == "Small Health Potion":
			icon = SMALL_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[4] == "Medium Health Potion":
			icon = MEDIUM_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[4] == "Large Health Potion":
			icon = LARGE_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[4] == "Small Mana Potion":
			icon = SMALL_MANA_POTION_IMAGE
		if inventory.dungeon_consumable[4] == "Medium Mana Potion":
			icon = MEDIUM_MANA_POTION_IMAGE
		if inventory.dungeon_consumable[4] == "Large Mana Potion":
			icon = LARGE_MANA_POTION_IMAGE
			
	if emplacement == 5:
		if inventory.dungeon_consumable[5] == "Small Health Potion":
			icon = SMALL_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[5] == "Medium Health Potion":
			icon = MEDIUM_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[5] == "Large Health Potion":
			icon = LARGE_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[5] == "Small Mana Potion":
			icon = SMALL_MANA_POTION_IMAGE
		if inventory.dungeon_consumable[5] == "Medium Mana Potion":
			icon = MEDIUM_MANA_POTION_IMAGE
		if inventory.dungeon_consumable[5] == "Large Mana Potion":
			icon = LARGE_MANA_POTION_IMAGE
			
	if emplacement == 6:
		if inventory.dungeon_consumable[6] == "Small Health Potion":
			icon = SMALL_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[6] == "Medium Health Potion":
			icon = MEDIUM_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[6] == "Large Health Potion":
			icon = LARGE_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[6] == "Small Mana Potion":
			icon = SMALL_MANA_POTION_IMAGE
		if inventory.dungeon_consumable[6] == "Medium Mana Potion":
			icon = MEDIUM_MANA_POTION_IMAGE
		if inventory.dungeon_consumable[6] == "Large Mana Potion":
			icon = LARGE_MANA_POTION_IMAGE
			
	if emplacement == 7:
		if inventory.dungeon_consumable[7] == "Small Health Potion":
			icon = SMALL_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[7] == "Medium Health Potion":
			icon = MEDIUM_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[7] == "Large Health Potion":
			icon = LARGE_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[7] == "Small Mana Potion":
			icon = SMALL_MANA_POTION_IMAGE
		if inventory.dungeon_consumable[7] == "Medium Mana Potion":
			icon = MEDIUM_MANA_POTION_IMAGE
		if inventory.dungeon_consumable[7] == "Large Mana Potion":
			icon = LARGE_MANA_POTION_IMAGE
			
	if emplacement == 8:
		if inventory.dungeon_consumable[8] == "Small Health Potion":
			icon = SMALL_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[8] == "Medium Health Potion":
			icon = MEDIUM_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[8] == "Large Health Potion":
			icon = LARGE_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[8] == "Small Mana Potion":
			icon = SMALL_MANA_POTION_IMAGE
		if inventory.dungeon_consumable[8] == "Medium Mana Potion":
			icon = MEDIUM_MANA_POTION_IMAGE
		if inventory.dungeon_consumable[8] == "Large Mana Potion":
			icon = LARGE_MANA_POTION_IMAGE
			
	if emplacement == 9:
		if inventory.dungeon_consumable[9] == "Small Health Potion":
			icon = SMALL_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[9] == "Medium Health Potion":
			icon = MEDIUM_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[9] == "Large Health Potion":
			icon = LARGE_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[9] == "Small Mana Potion":
			icon = SMALL_MANA_POTION_IMAGE
		if inventory.dungeon_consumable[9] == "Medium Mana Potion":
			icon = MEDIUM_MANA_POTION_IMAGE
		if inventory.dungeon_consumable[9] == "Large Mana Potion":
			icon = LARGE_MANA_POTION_IMAGE
			
	if emplacement == 10:
		if inventory.dungeon_consumable[10] == "Small Health Potion":
			icon = SMALL_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[10] == "Medium Health Potion":
			icon = MEDIUM_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[10] == "Large Health Potion":
			icon = LARGE_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[10] == "Small Mana Potion":
			icon = SMALL_MANA_POTION_IMAGE
		if inventory.dungeon_consumable[10] == "Medium Mana Potion":
			icon = MEDIUM_MANA_POTION_IMAGE
		if inventory.dungeon_consumable[10] == "Large Mana Potion":
			icon = LARGE_MANA_POTION_IMAGE
			
	if emplacement == 11:
		if inventory.dungeon_consumable[11] == "Small Health Potion":
			icon = SMALL_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[11] == "Medium Health Potion":
			icon = MEDIUM_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[11] == "Large Health Potion":
			icon = LARGE_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[11] == "Small Mana Potion":
			icon = SMALL_MANA_POTION_IMAGE
		if inventory.dungeon_consumable[11] == "Medium Mana Potion":
			icon = MEDIUM_MANA_POTION_IMAGE
		if inventory.dungeon_consumable[11] == "Large Mana Potion":
			icon = LARGE_MANA_POTION_IMAGE
			
	if emplacement == 12:
		if inventory.dungeon_consumable[12] == "Small Health Potion":
			icon = SMALL_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[12] == "Medium Health Potion":
			icon = MEDIUM_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[12] == "Large Health Potion":
			icon = LARGE_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[12] == "Small Mana Potion":
			icon = SMALL_MANA_POTION_IMAGE
		if inventory.dungeon_consumable[12] == "Medium Mana Potion":
			icon = MEDIUM_MANA_POTION_IMAGE
		if inventory.dungeon_consumable[12] == "Large Mana Potion":
			icon = LARGE_MANA_POTION_IMAGE
			
	if emplacement == 13:
		if inventory.dungeon_consumable[13] == "Small Health Potion":
			icon = SMALL_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[13] == "Medium Health Potion":
			icon = MEDIUM_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[13] == "Large Health Potion":
			icon = LARGE_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[13] == "Small Mana Potion":
			icon = SMALL_MANA_POTION_IMAGE
		if inventory.dungeon_consumable[13] == "Medium Mana Potion":
			icon = MEDIUM_MANA_POTION_IMAGE
		if inventory.dungeon_consumable[13] == "Large Mana Potion":
			icon = LARGE_MANA_POTION_IMAGE
			
	if emplacement == 14:
		if inventory.dungeon_consumable[14] == "Small Health Potion":
			icon = SMALL_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[14] == "Medium Health Potion":
			icon = MEDIUM_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[14] == "Large Health Potion":
			icon = LARGE_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[14] == "Small Mana Potion":
			icon = SMALL_MANA_POTION_IMAGE
		if inventory.dungeon_consumable[14] == "Medium Mana Potion":
			icon = MEDIUM_MANA_POTION_IMAGE
		if inventory.dungeon_consumable[14] == "Large Mana Potion":
			icon = LARGE_MANA_POTION_IMAGE
			
	if emplacement == 15:
		if inventory.dungeon_consumable[15] == "Small Health Potion":
			icon = SMALL_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[15] == "Medium Health Potion":
			icon = MEDIUM_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[15] == "Large Health Potion":
			icon = LARGE_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[15] == "Small Mana Potion":
			icon = SMALL_MANA_POTION_IMAGE
		if inventory.dungeon_consumable[15] == "Medium Mana Potion":
			icon = MEDIUM_MANA_POTION_IMAGE
		if inventory.dungeon_consumable[15] == "Large Mana Potion":
			icon = LARGE_MANA_POTION_IMAGE
			
	if emplacement == 16:
		if inventory.dungeon_consumable[16] == "Small Health Potion":
			icon = SMALL_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[16] == "Medium Health Potion":
			icon = MEDIUM_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[16] == "Large Health Potion":
			icon = LARGE_HEALTH_POTION_IMAGE
		if inventory.dungeon_consumable[16] == "Small Mana Potion":
			icon = SMALL_MANA_POTION_IMAGE
		if inventory.dungeon_consumable[16] == "Medium Mana Potion":
			icon = MEDIUM_MANA_POTION_IMAGE
		if inventory.dungeon_consumable[16] == "Large Mana Potion":
			icon = LARGE_MANA_POTION_IMAGE

	return icon

def dungeon_choose_consumable_draw_window(item_name,item_description):
	BACKGROUND()
	pygame.draw.rect(screen, GRAY, TOP_BAND)
	context_text = font.render("Select Consumable", 1, BLACK)
	screen.blit(context_text, ( TOP_BAND.centerx - context_text.get_width()//2, TOP_BAND.centery - context_text.get_height()//2))

	if inventory.max_consumable >= 1:
		pygame.draw.rect(screen, GRAY, CONSUMABLE_EMPLACEMENT_ONE)
		if 1 in inventory.dungeon_consumable:
			icon = consumable_icon(1)
			screen.blit(icon, (CONSUMABLE_EMPLACEMENT_ONE.x, CONSUMABLE_EMPLACEMENT_ONE.y + 1))
		
	if inventory.max_consumable >= 2:
		pygame.draw.rect(screen, GRAY, CONSUMABLE_EMPLACEMENT_TWO)
		if 2 in inventory.dungeon_consumable:
			icon = consumable_icon(2)
			screen.blit(icon, (CONSUMABLE_EMPLACEMENT_TWO.x, CONSUMABLE_EMPLACEMENT_TWO.y + 1))
		
	if inventory.max_consumable >= 3:
		pygame.draw.rect(screen, GRAY, CONSUMABLE_EMPLACEMENT_THREE)
		if 3 in inventory.dungeon_consumable:
			icon = consumable_icon(3)
			screen.blit(icon, (CONSUMABLE_EMPLACEMENT_THREE.x, CONSUMABLE_EMPLACEMENT_THREE.y + 1))
		
	if inventory.max_consumable >= 4:
		pygame.draw.rect(screen, GRAY, CONSUMABLE_EMPLACEMENT_FOUR)
		if 4 in inventory.dungeon_consumable:
			icon = consumable_icon(4)
			screen.blit(icon, (CONSUMABLE_EMPLACEMENT_FOUR.x, CONSUMABLE_EMPLACEMENT_FOUR.y + 1))
		
	if inventory.max_consumable >= 5:
		pygame.draw.rect(screen, GRAY, CONSUMABLE_EMPLACEMENT_FIVE)
		if 5 in inventory.dungeon_consumable:
			icon = consumable_icon(5)
			screen.blit(icon, (CONSUMABLE_EMPLACEMENT_FIVE.x, CONSUMABLE_EMPLACEMENT_FIVE.y + 1))
		
	if inventory.max_consumable >= 6:
		pygame.draw.rect(screen, GRAY, CONSUMABLE_EMPLACEMENT_SIX)
		if 6 in inventory.dungeon_consumable:
			icon = consumable_icon(6)
			screen.blit(icon, (CONSUMABLE_EMPLACEMENT_SIX.x, CONSUMABLE_EMPLACEMENT_SIX.y + 1))
		
	if inventory.max_consumable >= 7:
		pygame.draw.rect(screen, GRAY, CONSUMABLE_EMPLACEMENT_SEVEN)
		if 7 in inventory.dungeon_consumable:
			icon = consumable_icon(7)
			screen.blit(icon, (CONSUMABLE_EMPLACEMENT_SEVEN.x, CONSUMABLE_EMPLACEMENT_SEVEN.y + 1))
		
	if inventory.max_consumable >= 8:
		pygame.draw.rect(screen, GRAY, CONSUMABLE_EMPLACEMENT_EIGHT)
		if 8 in inventory.dungeon_consumable:
			icon = consumable_icon(8)
			screen.blit(icon, (CONSUMABLE_EMPLACEMENT_EIGHT.x, CONSUMABLE_EMPLACEMENT_EIGHT.y + 1))
		
	if inventory.max_consumable >= 9:
		pygame.draw.rect(screen, GRAY, CONSUMABLE_EMPLACEMENT_NINE)
		if 9 in inventory.dungeon_consumable:
			icon = consumable_icon(9)
			screen.blit(icon, (CONSUMABLE_EMPLACEMENT_NINE.x, CONSUMABLE_EMPLACEMENT_NINE.y + 1))
		
	if inventory.max_consumable >= 10:
		pygame.draw.rect(screen, GRAY, CONSUMABLE_EMPLACEMENT_TEN)
		if 10 in inventory.dungeon_consumable:
			icon = consumable_icon(10)
			screen.blit(icon, (CONSUMABLE_EMPLACEMENT_TEN.x, CONSUMABLE_EMPLACEMENT_TEN.y + 1))
		
	if inventory.max_consumable >= 11:
		pygame.draw.rect(screen, GRAY, CONSUMABLE_EMPLACEMENT_ELEVEN)
		if 11 in inventory.dungeon_consumable:
			icon = consumable_icon(11)
			screen.blit(icon, (CONSUMABLE_EMPLACEMENT_ELEVEN.x, CONSUMABLE_EMPLACEMENT_ELEVEN.y + 1))
		
	if inventory.max_consumable >= 12:
		pygame.draw.rect(screen, GRAY, CONSUMABLE_EMPLACEMENT_TWELVE)
		if 12 in inventory.dungeon_consumable:
			icon = consumable_icon(12)
			screen.blit(icon, (CONSUMABLE_EMPLACEMENT_TWELVE.x, CONSUMABLE_EMPLACEMENT_TWELVE.y + 1))
		
	if inventory.max_consumable >= 13:
		pygame.draw.rect(screen, GRAY, CONSUMABLE_EMPLACEMENT_THIRTEEN)
		if 13 in inventory.dungeon_consumable:
			icon = consumable_icon(13)
			screen.blit(icon, (CONSUMABLE_EMPLACEMENT_THIRTEEN.x, CONSUMABLE_EMPLACEMENT_THIRTEEN.y + 1))
		
	if inventory.max_consumable >= 14:
		pygame.draw.rect(screen, GRAY, CONSUMABLE_EMPLACEMENT_FOURTEEN)
		if 14 in inventory.dungeon_consumable:
			icon = consumable_icon(14)
			screen.blit(icon, (CONSUMABLE_EMPLACEMENT_FOURTEEN.x, CONSUMABLE_EMPLACEMENT_FOURTEEN.y + 1))
		
	if inventory.max_consumable >= 15:
		pygame.draw.rect(screen, GRAY, CONSUMABLE_EMPLACEMENT_FIFTEEN)
		if 15 in inventory.dungeon_consumable:
			icon = consumable_icon(15)
			screen.blit(icon, (CONSUMABLE_EMPLACEMENT_FIFTEEN.x, CONSUMABLE_EMPLACEMENT_FIFTEEN.y + 1))
		
	if inventory.max_consumable >= 16:
		pygame.draw.rect(screen, GRAY, CONSUMABLE_EMPLACEMENT_SIXTEEN)
		if 16 in inventory.dungeon_consumable:
			icon = consumable_icon(16)
			screen.blit(icon, (CONSUMABLE_EMPLACEMENT_SIXTEEN.x, CONSUMABLE_EMPLACEMENT_SIXTEEN.y + 1))

	pygame.draw.rect(screen, GRAY, BACK_BUTTON_BIS)
	back_button_text = intermediate_font.render("Back", 1, BLACK)
	screen.blit(back_button_text, ( BACK_BUTTON_BIS.centerx - back_button_text.get_width()//2, BACK_BUTTON_BIS.centery - back_button_text.get_height()//2))

	pygame.draw.rect(screen, INTERMEDIATE_GRAY, DESCRIPTION_BAND)
	if item_name != None:
		item_name_text = font.render(f"{item_name}", 1, BLACK)
		screen.blit(item_name_text, (DESCRIPTION_BAND.centerx - item_name_text.get_width()//2, DESCRIPTION_BAND.y + 5))
		item_description_text = intermediate_font.render(f"{item_description}", 1, BLACK)
		screen.blit(item_description_text, (DESCRIPTION_BAND.centerx - item_description_text.get_width()//2, DESCRIPTION_BAND.centery))

	pygame.display.update()

def dungeon_choose_consumable():
	click = False
	run = True
	while run:
		clock.tick(60)
		mx, my = pygame.mouse.get_pos()
		item_name = None
		item_description = None

		if CONSUMABLE_EMPLACEMENT_ONE.collidepoint((mx, my)) and 1 in inventory.dungeon_consumable:
			item_name = inventory.dungeon_consumable[1]
			item_description = consumable_info(inventory.dungeon_consumable[1])
			if click:
				dungeon_use_consumable(1,item_name)

		if CONSUMABLE_EMPLACEMENT_TWO.collidepoint((mx, my)) and 2 in inventory.dungeon_consumable:
			item_name = inventory.dungeon_consumable[2]
			item_description = consumable_info(inventory.dungeon_consumable[2])
			if click:
				dungeon_use_consumable(2,item_name)

		if CONSUMABLE_EMPLACEMENT_THREE.collidepoint((mx, my)) and 3 in inventory.dungeon_consumable:
			item_name = inventory.dungeon_consumable[3]
			item_description = consumable_info(inventory.dungeon_consumable[3])
			if click:
				dungeon_use_consumable(3,item_name)

		if CONSUMABLE_EMPLACEMENT_FOUR.collidepoint((mx, my)) and 4 in inventory.dungeon_consumable:
			item_name = inventory.dungeon_consumable[4]
			item_description = consumable_info(inventory.dungeon_consumable[4])
			if click:
				dungeon_use_consumable(4,item_name)

		if CONSUMABLE_EMPLACEMENT_FIVE.collidepoint((mx, my)) and 5 in inventory.dungeon_consumable:
			item_name = inventory.dungeon_consumable[5]
			item_description = consumable_info(inventory.dungeon_consumable[5])
			if click:
				dungeon_use_consumable(5,item_name)

		if CONSUMABLE_EMPLACEMENT_SIX.collidepoint((mx, my)) and 6 in inventory.dungeon_consumable:
			item_name = inventory.dungeon_consumable[6]
			item_description = consumable_info(inventory.dungeon_consumable[6])
			if click:
				dungeon_use_consumable(6,item_name)

		if CONSUMABLE_EMPLACEMENT_SEVEN.collidepoint((mx, my)) and 7 in inventory.dungeon_consumable:
			item_name = inventory.dungeon_consumable[7]
			item_description = consumable_info(inventory.dungeon_consumable[7])
			if click:
				dungeon_use_consumable(7,item_name)

		if CONSUMABLE_EMPLACEMENT_EIGHT.collidepoint((mx, my)) and 8 in inventory.dungeon_consumable:
			item_name = inventory.dungeon_consumable[8]
			item_description = consumable_info(inventory.dungeon_consumable[8])
			if click:
				dungeon_use_consumable(8,item_name)

		if CONSUMABLE_EMPLACEMENT_NINE.collidepoint((mx, my)) and 9 in inventory.dungeon_consumable:
			item_name = inventory.dungeon_consumable[9]
			item_description = consumable_info(inventory.dungeon_consumable[9])
			if click:
				dungeon_use_consumable(9,item_name)

		if CONSUMABLE_EMPLACEMENT_TEN.collidepoint((mx, my)) and 10 in inventory.dungeon_consumable:
			item_name = inventory.dungeon_consumable[10]
			item_description = consumable_info(inventory.dungeon_consumable[10])
			if click:
				dungeon_use_consumable(10,item_name)

		if CONSUMABLE_EMPLACEMENT_ELEVEN.collidepoint((mx, my)) and 11 in inventory.dungeon_consumable:
			item_name = inventory.dungeon_consumable[11]
			item_description = consumable_info(inventory.dungeon_consumable[11])
			if click:
				dungeon_use_consumable(11,item_name)

		if CONSUMABLE_EMPLACEMENT_TWELVE.collidepoint((mx, my)) and 12 in inventory.dungeon_consumable:
			item_name = inventory.dungeon_consumable[12]
			item_description = consumable_info(inventory.dungeon_consumable[12])
			if click:
				dungeon_use_consumable(12,item_name)

		if CONSUMABLE_EMPLACEMENT_THIRTEEN.collidepoint((mx, my)) and 13 in inventory.dungeon_consumable:
			item_name = inventory.dungeon_consumable[13]
			item_description = consumable_info(inventory.dungeon_consumable[13])
			if click:
				dungeon_use_consumable(13,item_name)

		if CONSUMABLE_EMPLACEMENT_FOURTEEN.collidepoint((mx, my)) and 14 in inventory.dungeon_consumable:
			item_name = inventory.dungeon_consumable[14]
			item_description = consumable_info(inventory.dungeon_consumable[14])
			if click:
				dungeon_use_consumable(14,item_name)

		if CONSUMABLE_EMPLACEMENT_FIFTEEN.collidepoint((mx, my)) and 15 in inventory.dungeon_consumable:
			item_name = inventory.dungeon_consumable[15]
			item_description = consumable_info(inventory.dungeon_consumable[15])
			if click:
				dungeon_use_consumable(15,item_name)

		if CONSUMABLE_EMPLACEMENT_SIXTEEN.collidepoint((mx, my)) and 16 in inventory.dungeon_consumable:
			item_name = inventory.dungeon_consumable[16]
			item_description = consumable_info(inventory.dungeon_consumable[16])
			if click:
				dungeon_use_consumable(16,item_name)

		if BACK_BUTTON_BIS.collidepoint((mx, my)):
			if click:
				run = False

		click = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				dungeon.run = False
				pygame.quit()
				sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True
		dungeon_choose_consumable_draw_window(item_name,item_description)

def dungeon_use_consumable_draw_window(item_name,animations):
	BACKGROUND()
	pygame.draw.rect(screen, GRAY, TOP_BAND)
	context_text = font.render("Select Party Member", 1, BLACK)
	screen.blit(context_text, ( TOP_BAND.centerx - context_text.get_width()//2, TOP_BAND.centery - context_text.get_height()//2))
	
	#item icon

	if len(party.party) >= 1:
		pygame.draw.rect(screen, INTERMEDIATE_GRAY, FIRST_PARTY_MEMBER_BUTTON)
		name_text = intermediate_font.render(f"{party.party[0].name}", 1, BLACK)
		screen.blit(name_text, (FIRST_PARTY_MEMBER_BUTTON.x + 10, FIRST_PARTY_MEMBER_BUTTON.y + 10))
		hp_text = intermediate_font.render(f"{party.party[0].hp}/{party.party[0].max_hp} HP", 1, BLACK)
		screen.blit(hp_text, ( FIRST_PARTY_MEMBER_BUTTON.x + 10, FIRST_PARTY_MEMBER_BUTTON.y + 25))
		mp_text = intermediate_font.render(f"{party.party[0].mp}/{party.party[0].max_mp} MP", 1, BLACK)
		screen.blit(mp_text, ( FIRST_PARTY_MEMBER_BUTTON.x + 10, FIRST_PARTY_MEMBER_BUTTON.y + 40))
	if len(party.party) >= 2:
		pygame.draw.rect(screen, INTERMEDIATE_GRAY, SECOND_PARTY_MEMBER_BUTTON)
		name_text = intermediate_font.render(f"{party.party[1].name}", 1, BLACK)
		screen.blit(name_text, (SECOND_PARTY_MEMBER_BUTTON.x + 10, SECOND_PARTY_MEMBER_BUTTON.y + 10))
		hp_text = intermediate_font.render(f"{party.party[1].hp}/{party.party[1].max_hp} HP", 1, BLACK)
		screen.blit(hp_text, ( SECOND_PARTY_MEMBER_BUTTON.x + 10, SECOND_PARTY_MEMBER_BUTTON.y + 25))
		mp_text = intermediate_font.render(f"{party.party[1].mp}/{party.party[1].max_mp} MP", 1, BLACK)
		screen.blit(mp_text, ( SECOND_PARTY_MEMBER_BUTTON.x + 10, SECOND_PARTY_MEMBER_BUTTON.y + 40))
	if len(party.party) >= 3:
		pygame.draw.rect(screen, INTERMEDIATE_GRAY, THIRD_PARTY_MEMBER_BUTTON)
		name_text = intermediate_font.render(f"{party.party[2].name}", 1, BLACK)
		screen.blit(name_text, (THIRD_PARTY_MEMBER_BUTTON.x + 10, THIRD_PARTY_MEMBER_BUTTON.y + 10))
		hp_text = intermediate_font.render(f"{party.party[2].hp}/{party.party[2].max_hp} HP", 1, BLACK)
		screen.blit(hp_text, ( THIRD_PARTY_MEMBER_BUTTON.x + 10, THIRD_PARTY_MEMBER_BUTTON.y + 25))
		mp_text = intermediate_font.render(f"{party.party[2].mp}/{party.party[2].max_mp} MP", 1, BLACK)
		screen.blit(mp_text, ( THIRD_PARTY_MEMBER_BUTTON.x + 10, THIRD_PARTY_MEMBER_BUTTON.y + 40))
	if len(party.party) == 4:
		pygame.draw.rect(screen, INTERMEDIATE_GRAY, FOURTH_PARTY_MEMBER_BUTTON)
		name_text = intermediate_font.render(f"{party.party[3].name}", 1, BLACK)
		screen.blit(name_text, (FOURTH_PARTY_MEMBER_BUTTON.x + 10, FOURTH_PARTY_MEMBER_BUTTON.y + 10))
		hp_text = intermediate_font.render(f"{party.party[3].hp}/{party.party[3].max_hp} HP", 1, BLACK)
		screen.blit(hp_text, ( FOURTH_PARTY_MEMBER_BUTTON.x + 10, FOURTH_PARTY_MEMBER_BUTTON.y + 25))
		mp_text = intermediate_font.render(f"{party.party[3].mp}/{party.party[3].max_mp} MP", 1, BLACK)
		screen.blit(mp_text, ( FOURTH_PARTY_MEMBER_BUTTON.x + 10, FOURTH_PARTY_MEMBER_BUTTON.y + 40))

	pygame.draw.rect(screen, GRAY, BACK_BUTTON)
	back_button_text = intermediate_font.render("Back", 1, BLACK)
	screen.blit(back_button_text, ( BACK_BUTTON.centerx - back_button_text.get_width()//2, BACK_BUTTON.centery - back_button_text.get_height()//2))

	for anim in animations:
		fx_text = intermediate_font.render(f"{anim['value']}", 1, anim["color"])
		screen.blit(fx_text, (anim["target"].x + 125, anim["target"].y + 25 - anim["current_frame"]/9))
		anim["current_frame"] += 1
		if anim["current_frame"] == anim["max_frame"]:
			animations.remove(anim)

	pygame.display.update()

def dungeon_use_consumable(item_emplacement,item_name):
	click = False
	run = True
	used = False
	animations = []
	while run:
		clock.tick(60)
		mx, my = pygame.mouse.get_pos()

		if click and used:
			run = False

		if FIRST_PARTY_MEMBER_BUTTON.collidepoint((mx, my)) and used == False:
			if click:
				anim = consumable_effect(party.party[0],item_name,item_emplacement)
				anim["target"] = FIRST_PARTY_MEMBER_BUTTON
				animations.append(anim)
				consumable_sfx.play()
				consumable_sfx.set_volume(0.15)
				used = True
		if SECOND_PARTY_MEMBER_BUTTON.collidepoint((mx, my)) and used == False and len(party.party) >= 2:
			if click:
				anim = consumable_effect(party.party[1],item_name,item_emplacement)
				anim["target"] = SECOND_PARTY_MEMBER_BUTTON
				animations.append(anim)
				consumable_sfx.play()
				consumable_sfx.set_volume(0.15)
				used = True
		if THIRD_PARTY_MEMBER_BUTTON.collidepoint((mx, my)) and used == False and len(party.party) >= 3:
			if click:
				anim = consumable_effect(party.party[2],item_name,item_emplacement)
				anim["target"] = THIRD_PARTY_MEMBER_BUTTON
				animations.append(anim)
				consumable_sfx.play()
				consumable_sfx.set_volume(0.15)
				used = True
		if FOURTH_PARTY_MEMBER_BUTTON.collidepoint((mx, my)) and used == False and len(party.party) >= 4:
			if click:
				anim = consumable_effect(party.party[3],item_name,item_emplacement)
				anim["target"] = FOURTH_PARTY_MEMBER_BUTTON
				animations.append(anim)
				consumable_sfx.play()
				consumable_sfx.set_volume(0.15)
				used = True

		if BACK_BUTTON.collidepoint((mx,my)):
			if click:
				run = False

		click = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				dungeon.run = False
				pygame.quit()
				sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True
		dungeon_use_consumable_draw_window(item_name,animations)

def dungeon_check_loot_draw_window(item_name_list,item_number_list):
	BACKGROUND()
	pygame.draw.rect(screen, GRAY, TOP_BAND)
	context_text = font.render("Loot", 1, BLACK)
	screen.blit(context_text, ( TOP_BAND.centerx - context_text.get_width()//2, TOP_BAND.centery - context_text.get_height()//2))
	
	pygame.draw.rect(screen, GRAY, LOOT_PAGE_LEFT_BUTTON)
	screen.blit(LEFT_ARROW_IMAGE, ( LOOT_PAGE_LEFT_BUTTON.x, LOOT_PAGE_LEFT_BUTTON.y))
	pygame.draw.rect(screen, GRAY, LOOT_PAGE_RIGHT_BUTTON)
	screen.blit(RIGHT_ARROW_IMAGE, ( LOOT_PAGE_RIGHT_BUTTON.x, LOOT_PAGE_RIGHT_BUTTON.y))

	if len(item_name_list) == 0:
		nothing_text = font.render("Empty.", 1, BLACK)
		screen.blit(nothing_text, ( WIDTH//2 - nothing_text.get_width()//2, 280))

	if len(item_name_list) >= 1:
		pygame.draw.rect(screen, GRAY, LOOT_ITEM_NUM_ONE_BAND)
		screen.blit(selling_image(item_name_list[0]), ( LOOT_ITEM_NUM_ONE_BAND.x + 5, LOOT_ITEM_NUM_ONE_BAND.y + 2))
		item_name_text = intermediate_font.render(f"{item_name_list[0]}", 1, BLACK)
		screen.blit(item_name_text, ( LOOT_ITEM_NUM_ONE_BAND.x + 30, LOOT_ITEM_NUM_ONE_BAND.centery - item_name_text.get_height()//2 + 2))
		item_number_text = intermediate_font.render(f"x{item_number_list[0]}", 1, BLACK)
		screen.blit(item_number_text, ( LOOT_ITEM_NUM_ONE_BAND.right - 5 - item_number_text.get_width(), LOOT_ITEM_NUM_ONE_BAND.centery - item_name_text.get_height()//2 + 2))

	if len(item_name_list) >= 2:
		pygame.draw.rect(screen, GRAY, LOOT_ITEM_NUM_TWO_BAND)
		screen.blit(selling_image(item_name_list[1]), ( LOOT_ITEM_NUM_TWO_BAND.x + 5, LOOT_ITEM_NUM_TWO_BAND.y + 2))
		item_name_text = intermediate_font.render(f"{item_name_list[1]}", 1, BLACK)
		screen.blit(item_name_text, ( LOOT_ITEM_NUM_TWO_BAND.x + 30, LOOT_ITEM_NUM_TWO_BAND.centery - item_name_text.get_height()//2 + 2))
		item_number_text = intermediate_font.render(f"x{item_number_list[1]}", 1, BLACK)
		screen.blit(item_number_text, ( LOOT_ITEM_NUM_TWO_BAND.right - 5 - item_number_text.get_width(), LOOT_ITEM_NUM_TWO_BAND.centery - item_name_text.get_height()//2 + 2))
		
	if len(item_name_list) >= 3:
		pygame.draw.rect(screen, GRAY, LOOT_ITEM_NUM_THREE_BAND)
		screen.blit(selling_image(item_name_list[2]), ( LOOT_ITEM_NUM_THREE_BAND.x + 5, LOOT_ITEM_NUM_THREE_BAND.y + 2))
		item_name_text = intermediate_font.render(f"{item_name_list[2]}", 1, BLACK)
		screen.blit(item_name_text, ( LOOT_ITEM_NUM_THREE_BAND.x + 30, LOOT_ITEM_NUM_THREE_BAND.centery - item_name_text.get_height()//2 + 2))
		item_number_text = intermediate_font.render(f"x{item_number_list[2]}", 1, BLACK)
		screen.blit(item_number_text, ( LOOT_ITEM_NUM_THREE_BAND.right - 5 - item_number_text.get_width(), LOOT_ITEM_NUM_THREE_BAND.centery - item_name_text.get_height()//2 + 2))
		
	if len(item_name_list) >= 4:
		pygame.draw.rect(screen, GRAY, LOOT_ITEM_NUM_FOUR_BAND)
		screen.blit(selling_image(item_name_list[3]), ( LOOT_ITEM_NUM_FOUR_BAND.x + 5, LOOT_ITEM_NUM_FOUR_BAND.y + 2))
		item_name_text = intermediate_font.render(f"{item_name_list[3]}", 1, BLACK)
		screen.blit(item_name_text, ( LOOT_ITEM_NUM_FOUR_BAND.x + 30, LOOT_ITEM_NUM_FOUR_BAND.centery - item_name_text.get_height()//2 + 2))
		item_number_text = intermediate_font.render(f"x{item_number_list[3]}", 1, BLACK)
		screen.blit(item_number_text, ( LOOT_ITEM_NUM_FOUR_BAND.right - 5 - item_number_text.get_width(), LOOT_ITEM_NUM_FOUR_BAND.centery - item_name_text.get_height()//2 + 2))
		
	if len(item_name_list) >= 5:
		pygame.draw.rect(screen, GRAY, LOOT_ITEM_NUM_FIVE_BAND)
		screen.blit(selling_image(item_name_list[4]), ( LOOT_ITEM_NUM_FIVE_BAND.x + 5, LOOT_ITEM_NUM_FIVE_BAND.y + 2))
		item_name_text = intermediate_font.render(f"{item_name_list[4]}", 1, BLACK)
		screen.blit(item_name_text, ( LOOT_ITEM_NUM_FIVE_BAND.x + 30, LOOT_ITEM_NUM_FIVE_BAND.centery - item_name_text.get_height()//2 + 2))
		item_number_text = intermediate_font.render(f"x{item_number_list[4]}", 1, BLACK)
		screen.blit(item_number_text, ( LOOT_ITEM_NUM_FIVE_BAND.right - 5 - item_number_text.get_width(), LOOT_ITEM_NUM_FIVE_BAND.centery - item_name_text.get_height()//2 + 2))
		
	if len(item_name_list) >= 6:
		pygame.draw.rect(screen, GRAY, LOOT_ITEM_NUM_SIX_BAND)
		screen.blit(selling_image(item_name_list[5]), ( LOOT_ITEM_NUM_SIX_BAND.x + 5, LOOT_ITEM_NUM_SIX_BAND.y + 2))
		item_name_text = intermediate_font.render(f"{item_name_list[5]}", 1, BLACK)
		screen.blit(item_name_text, ( LOOT_ITEM_NUM_SIX_BAND.x + 30, LOOT_ITEM_NUM_SIX_BAND.centery - item_name_text.get_height()//2 + 2))
		item_number_text = intermediate_font.render(f"x{item_number_list[5]}", 1, BLACK)
		screen.blit(item_number_text, ( LOOT_ITEM_NUM_SIX_BAND.right - 5 - item_number_text.get_width(), LOOT_ITEM_NUM_SIX_BAND.centery - item_name_text.get_height()//2 + 2))
		
	if len(item_name_list) >= 7:
		pygame.draw.rect(screen, GRAY, LOOT_ITEM_NUM_SEVEN_BAND)
		screen.blit(selling_image(item_name_list[6]), ( LOOT_ITEM_NUM_SEVEN_BAND.x + 5, LOOT_ITEM_NUM_SEVEN_BAND.y + 2))
		item_name_text = intermediate_font.render(f"{item_name_list[6]}", 1, BLACK)
		screen.blit(item_name_text, ( LOOT_ITEM_NUM_SEVEN_BAND.x + 30, LOOT_ITEM_NUM_SEVEN_BAND.centery - item_name_text.get_height()//2 + 2))
		item_number_text = intermediate_font.render(f"x{item_number_list[6]}", 1, BLACK)
		screen.blit(item_number_text, ( LOOT_ITEM_NUM_SEVEN_BAND.right - 5 - item_number_text.get_width(), LOOT_ITEM_NUM_SEVEN_BAND.centery - item_name_text.get_height()//2 + 2))
		
	if len(item_name_list) >= 8:
		pygame.draw.rect(screen, GRAY, LOOT_ITEM_NUM_EIGHT_BAND)
		screen.blit(selling_image(item_name_list[7]), ( LOOT_ITEM_NUM_EIGHT_BAND.x + 5, LOOT_ITEM_NUM_EIGHT_BAND.y + 2))
		item_name_text = intermediate_font.render(f"{item_name_list[7]}", 1, BLACK)
		screen.blit(item_name_text, ( LOOT_ITEM_NUM_EIGHT_BAND.x + 30, LOOT_ITEM_NUM_EIGHT_BAND.centery - item_name_text.get_height()//2 + 2))
		item_number_text = intermediate_font.render(f"x{item_number_list[7]}", 1, BLACK)
		screen.blit(item_number_text, ( LOOT_ITEM_NUM_EIGHT_BAND.right - 5 - item_number_text.get_width(), LOOT_ITEM_NUM_EIGHT_BAND.centery - item_name_text.get_height()//2 + 2))
		
	if len(item_name_list) >= 9:
		pygame.draw.rect(screen, GRAY, LOOT_ITEM_NUM_NINE_BAND)
		screen.blit(selling_image(item_name_list[8]), ( LOOT_ITEM_NUM_NINE_BAND.x + 5, LOOT_ITEM_NUM_NINE_BAND.y + 2))
		item_name_text = intermediate_font.render(f"{item_name_list[8]}", 1, BLACK)
		screen.blit(item_name_text, ( LOOT_ITEM_NUM_NINE_BAND.x + 30, LOOT_ITEM_NUM_NINE_BAND.centery - item_name_text.get_height()//2 + 2))
		item_number_text = intermediate_font.render(f"x{item_number_list[8]}", 1, BLACK)
		screen.blit(item_number_text, ( LOOT_ITEM_NUM_NINE_BAND.right - 5 - item_number_text.get_width(), LOOT_ITEM_NUM_NINE_BAND.centery - item_name_text.get_height()//2 + 2))
		
	if len(item_name_list) >= 10:
		pygame.draw.rect(screen, GRAY, LOOT_ITEM_NUM_TEN_BAND)
		screen.blit(selling_image(item_name_list[9]), ( LOOT_ITEM_NUM_TEN_BAND.x + 5, LOOT_ITEM_NUM_TEN_BAND.y + 2))
		item_name_text = intermediate_font.render(f"{item_name_list[9]}", 1, BLACK)
		screen.blit(item_name_text, ( LOOT_ITEM_NUM_TEN_BAND.x + 30, LOOT_ITEM_NUM_TEN_BAND.centery - item_name_text.get_height()//2 + 2))
		item_number_text = intermediate_font.render(f"x{item_number_list[9]}", 1, BLACK)
		screen.blit(item_number_text, ( LOOT_ITEM_NUM_TEN_BAND.right - 5 - item_number_text.get_width(), LOOT_ITEM_NUM_TEN_BAND.centery - item_name_text.get_height()//2 + 2))

	pygame.draw.rect(screen, GRAY, BACK_BUTTON)
	back_button_text = intermediate_font.render("Back", 1, BLACK)
	screen.blit(back_button_text, ( BACK_BUTTON.centerx - back_button_text.get_width()//2, BACK_BUTTON.centery - back_button_text.get_height()//2))

	pygame.display.update()

def dungeon_check_loot():
	click = False
	run = True
	page = 0
	max_page = 0
	while run:
		clock.tick(60)
		mx, my = pygame.mouse.get_pos()
		item_name_list = []
		item_number_list = []

		if LOOT_PAGE_LEFT_BUTTON.collidepoint((mx, my)):
			if click and page > 0:
				page -= 1
		if LOOT_PAGE_RIGHT_BUTTON.collidepoint((mx, my)):
			if click and page < max_page:
				page += 1
				
		max_page = len(inventory.dungeon_loot)//10
		keys_list = list(inventory.dungeon_loot)
		for key in keys_list[page * 10 : (page + 1) * 10]:
			item_name_list.append(key)
			item_number_list.append(inventory.dungeon_loot[key])

		if BACK_BUTTON.collidepoint((mx,my)):
			if click:
				run = False

		click = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				dungeon.run = False
				pygame.quit()
				sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True

		dungeon_check_loot_draw_window(item_name_list,item_number_list)

##############################
###### SAVING / LOADING ######

def format_hero_data(hero):
    hero_data = { "name" : hero.name , "level" : hero.level , "xp" : hero.xp , "max_hp" : hero.max_hp , "hp" : hero.hp , "max_mp" : hero.max_mp , "mp" : hero.mp }
    return hero_data

def format_save_data(party,inventory):
	inventory_data = { "name" : "inventory" , "gold" : inventory.storage_gold , "storage" : inventory.storage }
	party_data = { "name" : "party" , "party" : party }
	data = [inventory_data,party_data]
	for hero in party:
		data.append(format_hero_data(hero))
	return data

def saving(data):
    with open("save.txt", "wb") as f:
        pickle.dump(data, f)
    print("")
    print("Game saved !")

def complete_save():
	data = format_save_data(party,inventory)
	saving(data)

def loading():
    with open("save.txt", "rb") as f:
        return pickle.load(f)

def load_depacking(data):
	for item in data:
		if item["name"] == "inventory":
			inventory.storage_gold = item["gold"]
			inventory.storage = item["storage"]
		elif item["name"] == "Alex":
			Alex.level = item["level"]
			Alex.xp = item["xp"]
			Alex.max_hp = item["max_hp"]
			Alex.hp = item["hp"]
			Alex.max_mp = item["max_mp"]
			Alex.mp = item["mp"]
		elif item["name"] == "Emeline":
			Emeline.level = item["level"]
			Emeline.xp = item["xp"]
			Emeline.max_hp = item["max_hp"]
			Emeline.hp = item["hp"]
			Emeline.max_mp = item["max_mp"]
			Emeline.mp = item["mp"]
		elif item["name"] == "Azazel":
			Azazel.level = item["level"]
			Azazel.xp = item["xp"]
			Azazel.max_hp = item["max_hp"]
			Azazel.hp = item["hp"]
			Azazel.max_mp = item["max_mp"]
			Azazel.mp = item["mp"]
		elif item["name"] == "Ezekiel":
			Ezekiel.level = item["level"]
			Ezekiel.xp = item["xp"]
			Ezekiel.max_hp = item["max_hp"]
			Ezekiel.hp = item["hp"]
			Ezekiel.max_mp = item["max_mp"]
			Ezekiel.mp = item["mp"]
		elif item["name"] == "party":
			party = item["party"]
	print("Data loaded !")
	print("")

def complete_load():
	data = loading()
	load_depacking(data)

#######################
######## Wait #########

def wait():
	pygame.event.clear()
	waiting = True
	while True:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				waiting = False
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					waiting = False
		if waiting == False:
			break

def timed_wait():
	pygame.event.clear()
	wait_end_time = pygame.time.get_ticks() + 3000
	waiting = True
	while True:
		clock.tick(60)
		current_time = pygame.time.get_ticks()
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key == K_SPACE:
					waiting = False
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					waiting = False
		if current_time >= wait_end_time:
			break
		if waiting == False:
			break

###########################

def get_coordinate(target):
	coordinate_x, coordinate_y = None, None
	if target.friendly == True:
		if target.emplacement == 1:
			coordinate_x, coordinate_y = FIRST_EMPLACEMENT_ALLY
		elif target.emplacement == 2:
			coordinate_x, coordinate_y = SECOND_EMPLACEMENT_ALLY
		elif target.emplacement == 3:
			coordinate_x, coordinate_y = THIRD_EMPLACEMENT_ALLY
		elif target.emplacement == 4:
			coordinate_x, coordinate_y = FOURTH_EMPLACEMENT_ALLY
	elif target.friendly == False:
		if target.emplacement == 1:
			coordinate_x, coordinate_y = FIRST_EMPLACEMENT_ENY
		elif target.emplacement == 2:
			coordinate_x, coordinate_y = SECOND_EMPLACEMENT_ENY
		elif target.emplacement == 3:
			coordinate_x, coordinate_y = THIRD_EMPLACEMENT_ENY
		elif target.emplacement == 4:
			coordinate_x, coordinate_y = FOURTH_EMPLACEMENT_ENY
	return coordinate_x, coordinate_y

def user_target_overview_screen_draw(user,target):
	offset = 1
	if user.friendly:
		offset = -1
	coordinate_x, coordinate_y = get_coordinate(user)
	screen.blit(CROSSEDSWORDS_IMAGE, (coordinate_x - 20 * (offset), coordinate_y - 30))
	coordinate_x, coordinate_y = get_coordinate(target)
	screen.blit(SHIELD_IMAGE, (coordinate_x + 20 * (offset), coordinate_y - 30))

def parry_screen_draw(target):
	offset = -1
	if target.friendly:
		offset = 1
	coordinate_x, coordinate_y = get_coordinate(target)
	screen.blit(SHIELD_DEFLECT_IMAGE, (coordinate_x + 160 * offset, coordinate_y - 30))
	pygame.display.update()

def parry_screen_draw_multiple(target,offset_y):
	offset = -1
	if target.friendly:
		offset = 1
	coordinate_x, coordinate_y = get_coordinate(target)
	screen.blit(SHIELD_DEFLECT_IMAGE, (coordinate_x + 160 * offset, coordinate_y - 30 - offset_y))
	pygame.display.update()

def dodge_screen_draw(target):
	offset = -1
	if target.friendly:
		offset = 1
	coordinate_x, coordinate_y = get_coordinate(target)
	screen.blit(DODGE_IMAGE, (coordinate_x + 160 * offset, coordinate_y - 30))
	pygame.display.update()

def dodge_screen_draw_multiple(target,offset_y):
	offset = -1
	if target.friendly:
		offset = 1
	coordinate_x, coordinate_y = get_coordinate(target)
	screen.blit(DODGE_IMAGE, (coordinate_x + 160 * offset, coordinate_y - 30 - offset_y))
	pygame.display.update()

def riposte_screen_draw(target):
	offset = -1
	if target.friendly:
		offset = 1
	coordinate_x, coordinate_y = get_coordinate(target)
	screen.blit(RIPOSTE_IMAGE, (coordinate_x + 160 * offset, coordinate_y - 30))
	pygame.display.update()

def ability_announcer_screen_draw(ability_string):
	pygame.draw.rect(screen, VERY_LIGHT_GRAY, ABILITY_BAND)
	ability_text = font.render( ability_string, 1, BLACK)
	screen.blit(ability_text, (ABILITY_BAND.centerx - ability_text.get_width()//2, ABILITY_BAND.centery - ability_text.get_height()//2))
	pygame.display.update()

def death_announcer_screen_draw(target):
	pygame.draw.rect(screen, VERY_LIGHT_GRAY, ABILITY_BAND)
	death_string = (f"{target.name} died !")
	death_text = font.render( death_string, 1, BLACK)
	screen.blit(death_text, (ABILITY_BAND.centerx - death_text.get_width()//2, ABILITY_BAND.centery - death_text.get_height()//2))
	offset = 1
	if target.friendly:
		offset = -1
	coordinate_x, coordinate_y = get_coordinate(target)
	screen.blit(SKULL_IMAGE, (coordinate_x + 10 * (offset), coordinate_y - 30))
	pygame.display.update()
	timed_wait()

def dmg_announcer_screen_draw(target,final_dmg,crit_multiplier):
	if crit_multiplier != 1:
		dmg_text = font.render(f"-{final_dmg}", 1, YELLOW)
	else:
		dmg_text = font.render(f"-{final_dmg}", 1, RED)
	coordinate = get_coordinate(target)
	screen.blit(dmg_text, coordinate)
	pygame.display.update()
	timed_wait()

def dmg_announcer_screen_draw_multiple(target_list,dmg_list,crit_multiplier_list,def_roll_list):
	target_done = []
	dmg_instance_count = 0
	for target in target_list:
		if crit_multiplier_list[dmg_instance_count] != 1:
			dmg_text = font.render(f"-{dmg_list[dmg_instance_count]}", 1, YELLOW)
		else:
			dmg_text = font.render(f"-{dmg_list[dmg_instance_count]}", 1, RED)
		coordinate_x, coordinate_y = get_coordinate(target)
		offset = 20 * target_done.count(target)
		coordinate_y -= offset
		screen.blit(dmg_text, (coordinate_x, coordinate_y))
		if def_roll_list[dmg_instance_count] == 0:
			dodge_screen_draw_multiple(target,offset)
		elif def_roll_list[dmg_instance_count] == 0.2:
			parry_screen_draw_multiple(target,offset)
		dmg_instance_count += 1
		target_done.append(target)
		pygame.display.update()
		timed_wait()

def heal_announcer_screen_draw(target, final_healing):
	heal_text = font.render(f"+{final_healing}", 1, GREEN)
	coordinate = get_coordinate(target)
	screen.blit(heal_text, coordinate)
	pygame.display.update()

def victory_screen_draw_window():
	BACKGROUND()
	victory_text = big_font.render("Victory !", 1, BLACK)
	screen.blit(victory_text, (WIDTH//2 - victory_text.get_width()//2, HEIGHT//5 - victory_text.get_height()//2))
	pygame.display.update()

def defeat_screen_draw_window():
	BACKGROUND()
	defeat_text = big_font.render("Defeat !", 1, BLACK)
	screen.blit(defeat_text, (WIDTH//2 - defeat_text.get_width()//2, HEIGHT//5 - defeat_text.get_height()//2))
	pygame.display.update()

###################

def rest_before_dungeon_draw_window():
	BACKGROUND()
	pygame.draw.rect(screen, GRAY, TOP_BAND)
	top_band_text = font.render("Dungeon", 1, BLACK)
	screen.blit(top_band_text, (TOP_BAND.centerx - top_band_text.get_width()//2, TOP_BAND.centery - top_band_text.get_height()//2))

	need_rest_text = font.render("You need to rest before going to the dungeon", 1, BLACK)
	screen.blit(need_rest_text, (WIDTH//2 - need_rest_text.get_width()//2, HEIGHT//2 - need_rest_text.get_height()//2))

	pygame.draw.rect(screen, GRAY, BACK_BUTTON_MIDDLE)
	back_button_text = font.render("Back", 1, BLACK)
	screen.blit(back_button_text, (BACK_BUTTON_MIDDLE.centerx - back_button_text.get_width()//2, BACK_BUTTON_MIDDLE.centery - back_button_text.get_height()//2))

	pygame.display.update()

def rest_before_dungeon():
	click = False
	run = True
	while run:
		clock.tick(60)
		mx, my = pygame.mouse.get_pos()

		if BACK_BUTTON_MIDDLE.collidepoint((mx, my)):
			if click:
				run = False

		click = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					run = False
			if event.type == KEYDOWN:
				if event.key == K_SPACE:
					run = False
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True

		rest_before_dungeon_draw_window()



###################
### Home Screen ###

def home_screen_draw_window():
	BACKGROUND()
	pygame.draw.rect(screen, GRAY, TOP_BAND)
	home_text = font.render("Home", 1, BLACK)
	screen.blit(home_text, (TOP_BAND.centerx - home_text.get_width()//2, TOP_BAND.centery - home_text.get_height()//2))

	pygame.draw.rect(screen, GRAY, CHECK_PARTY_BUTTON)
	check_party_text = font.render("Party", 1, BLACK)
	screen.blit(check_party_text, (CHECK_PARTY_BUTTON.centerx - check_party_text.get_width()//2, CHECK_PARTY_BUTTON.centery - check_party_text.get_height()//2))
	
	pygame.draw.rect(screen, GRAY, CHECK_INVENTORY_BUTTON)
	check_inventory_text = font.render("Inventory", 1, BLACK)
	screen.blit(check_inventory_text, (CHECK_INVENTORY_BUTTON.centerx - check_inventory_text.get_width()//2, CHECK_INVENTORY_BUTTON.centery - check_inventory_text.get_height()//2))
	
	pygame.draw.rect(screen, GRAY, REST_BUTTON)
	rest_text = font.render("Rest", 1, BLACK)
	screen.blit(rest_text, (REST_BUTTON.centerx - rest_text.get_width()//2, REST_BUTTON.centery - rest_text.get_height()//2))
	
	pygame.draw.rect(screen, GRAY, MANAGE_TEAM_BUTTON)
	manage_team_text = font.render("Manage Team", 1, BLACK)
	screen.blit(manage_team_text, (MANAGE_TEAM_BUTTON.centerx - manage_team_text.get_width()//2, MANAGE_TEAM_BUTTON.centery - manage_team_text.get_height()//2))
	
	pygame.draw.rect(screen, GRAY, GODDESS_BUTTON)
	goddess_button_text = font.render("Goddess", 1, BLACK)
	screen.blit(goddess_button_text, (GODDESS_BUTTON.centerx - goddess_button_text.get_width()//2, GODDESS_BUTTON.centery - goddess_button_text.get_height()//2))

	pygame.draw.rect(screen, GRAY, BACK_BUTTON)
	back_button_text = font.render("Back", 1, BLACK)
	screen.blit(back_button_text, (BACK_BUTTON.centerx - back_button_text.get_width()//2, BACK_BUTTON.centery - back_button_text.get_height()//2))

	pygame.display.update()

def home_screen():
	click = False
	run = True
	while run:
		clock.tick(60)
		mx, my = pygame.mouse.get_pos()

		if CHECK_PARTY_BUTTON.collidepoint((mx, my)):
			if click:
				check_party()
		if CHECK_INVENTORY_BUTTON.collidepoint((mx, my)):
			if click:
				check_storage()
		if REST_BUTTON.collidepoint((mx, my)):
			if click:
				home_rest()
		if MANAGE_TEAM_BUTTON.collidepoint((mx, my)):
			if click:
				manage_team()
		if GODDESS_BUTTON.collidepoint((mx, my)):
			if click:
				manage_goddess()
			
		if BACK_BUTTON.collidepoint((mx, my)):
			if click:
				break

		click = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					run = False
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True

		home_screen_draw_window()

###################
# TRAINING GROUND #

def training_draw_window(ally,passive_description,passive_cost,passive_name):
	BACKGROUND()
	pygame.draw.rect(screen, GRAY, TOP_LEFT_BAND)
	name_text = font.render(f"{ally.name}", 1, BLACK)
	screen.blit(name_text, (TOP_LEFT_BAND.centerx - name_text.get_width()//2, TOP_LEFT_BAND.centery - name_text.get_height()//2))

	pygame.draw.rect(screen, GRAY, TOP_RIGHT_BAND)
	mastery_text = small_font.render(f"Mastery : {ally.mastery}", 1, BLACK)
	screen.blit(mastery_text, (TOP_RIGHT_BAND.centerx - mastery_text.get_width()//2, TOP_RIGHT_BAND.centery - mastery_text.get_height()//2))

	if ally.first_row_middle_passive:
		pygame.draw.rect(screen, GRAY, FIRST_ROW_MIDDLE_ABILITY_BUTTON)
		screen.blit(ally.first_row_middle_passive_icon, (FIRST_ROW_MIDDLE_ABILITY_BUTTON.x, FIRST_ROW_MIDDLE_ABILITY_BUTTON.y))
	else:
		pygame.draw.rect(screen, GRAY, FIRST_ROW_MIDDLE_ABILITY_BUTTON)
		screen.blit(ally.first_row_middle_passive_icon_gray, (FIRST_ROW_MIDDLE_ABILITY_BUTTON.x, FIRST_ROW_MIDDLE_ABILITY_BUTTON.y))
	

	if ally.second_row_left_passive:
		pygame.draw.rect(screen, RED, SECOND_ROW_LEFT_ABILITY_BUTTON)
		screen.blit(ally.second_row_left_passive_icon, (SECOND_ROW_LEFT_ABILITY_BUTTON.x, SECOND_ROW_LEFT_ABILITY_BUTTON.y))
	else:
		pygame.draw.rect(screen, GRAY, SECOND_ROW_LEFT_ABILITY_BUTTON)
		screen.blit(ally.second_row_left_passive_icon_gray, (SECOND_ROW_LEFT_ABILITY_BUTTON.x, SECOND_ROW_LEFT_ABILITY_BUTTON.y))

	if ally.second_row_middle_passive:
		pygame.draw.rect(screen, RED, SECOND_ROW_MIDDLE_ABILITY_BUTTON)
		screen.blit(ally.second_row_middle_passive_icon, (SECOND_ROW_MIDDLE_ABILITY_BUTTON.x, SECOND_ROW_MIDDLE_ABILITY_BUTTON.y))
	else:
		pygame.draw.rect(screen, GRAY, SECOND_ROW_MIDDLE_ABILITY_BUTTON)
		screen.blit(ally.second_row_middle_passive_icon_gray, (SECOND_ROW_MIDDLE_ABILITY_BUTTON.x, SECOND_ROW_MIDDLE_ABILITY_BUTTON.y))

	if ally.second_row_right_passive:
		pygame.draw.rect(screen, RED, SECOND_ROW_RIGHT_ABILITY_BUTTON)
		screen.blit(ally.second_row_right_passive_icon, (SECOND_ROW_RIGHT_ABILITY_BUTTON.x, SECOND_ROW_RIGHT_ABILITY_BUTTON.y))
	else:
		pygame.draw.rect(screen, GRAY, SECOND_ROW_RIGHT_ABILITY_BUTTON)
		screen.blit(ally.second_row_right_passive_icon_gray, (SECOND_ROW_RIGHT_ABILITY_BUTTON.x, SECOND_ROW_RIGHT_ABILITY_BUTTON.y))


	if ally.third_row_left_passive:
		pygame.draw.rect(screen, RED, THIRD_ROW_LEFT_ABILITY_BUTTON)
		screen.blit(ally.third_row_left_passive_icon, (THIRD_ROW_LEFT_ABILITY_BUTTON.x, THIRD_ROW_LEFT_ABILITY_BUTTON.y))
	else:
		pygame.draw.rect(screen, GRAY, THIRD_ROW_LEFT_ABILITY_BUTTON)
		screen.blit(ally.third_row_left_passive_icon_gray, (THIRD_ROW_LEFT_ABILITY_BUTTON.x, THIRD_ROW_LEFT_ABILITY_BUTTON.y))
	
	if ally.third_row_middle_passive:
		pygame.draw.rect(screen, RED, THIRD_ROW_MIDDLE_ABILITY_BUTTON)
		screen.blit(ally.third_row_middle_passive_icon, (THIRD_ROW_MIDDLE_ABILITY_BUTTON.x, THIRD_ROW_MIDDLE_ABILITY_BUTTON.y))
	else:
		pygame.draw.rect(screen, GRAY, THIRD_ROW_MIDDLE_ABILITY_BUTTON)
		screen.blit(ally.third_row_middle_passive_icon_gray, (THIRD_ROW_MIDDLE_ABILITY_BUTTON.x, THIRD_ROW_MIDDLE_ABILITY_BUTTON.y))

	if ally.third_row_right_passive:
		pygame.draw.rect(screen, RED, THIRD_ROW_RIGHT_ABILITY_BUTTON)
		screen.blit(ally.third_row_right_passive_icon, (THIRD_ROW_RIGHT_ABILITY_BUTTON.x, THIRD_ROW_RIGHT_ABILITY_BUTTON.y))
	else:
		pygame.draw.rect(screen, GRAY, THIRD_ROW_RIGHT_ABILITY_BUTTON)
		screen.blit(ally.third_row_right_passive_icon_gray, (THIRD_ROW_RIGHT_ABILITY_BUTTON.x, THIRD_ROW_RIGHT_ABILITY_BUTTON.y))


	if ally.fourth_row_left_passive:
		pygame.draw.rect(screen, RED, FOURTH_ROW_LEFT_ABILITY_BUTTON)
		screen.blit(ally.fourth_row_left_passive_icon, (FOURTH_ROW_LEFT_ABILITY_BUTTON.x, FOURTH_ROW_LEFT_ABILITY_BUTTON.y))
	else:
		pygame.draw.rect(screen, GRAY, FOURTH_ROW_LEFT_ABILITY_BUTTON)
		screen.blit(ally.fourth_row_left_passive_icon_gray, (FOURTH_ROW_LEFT_ABILITY_BUTTON.x, FOURTH_ROW_LEFT_ABILITY_BUTTON.y))

	if ally.fourth_row_middle_passive:
		pygame.draw.rect(screen, RED, FOURTH_ROW_MIDDLE_ABILITY_BUTTON)
		screen.blit(ally.fourth_row_middle_passive_icon, (FOURTH_ROW_MIDDLE_ABILITY_BUTTON.x, FOURTH_ROW_MIDDLE_ABILITY_BUTTON.y))
	else:
		pygame.draw.rect(screen, GRAY, FOURTH_ROW_MIDDLE_ABILITY_BUTTON)
		screen.blit(ally.fourth_row_middle_passive_icon_gray, (FOURTH_ROW_MIDDLE_ABILITY_BUTTON.x, FOURTH_ROW_MIDDLE_ABILITY_BUTTON.y))

	if ally.fourth_row_right_passive:
		pygame.draw.rect(screen, RED, FOURTH_ROW_RIGHT_ABILITY_BUTTON)
		screen.blit(ally.fourth_row_right_passive_icon, (FOURTH_ROW_RIGHT_ABILITY_BUTTON.x, FOURTH_ROW_RIGHT_ABILITY_BUTTON.y))
	else:
		pygame.draw.rect(screen, GRAY, FOURTH_ROW_RIGHT_ABILITY_BUTTON)
		screen.blit(ally.fourth_row_right_passive_icon_gray, (FOURTH_ROW_RIGHT_ABILITY_BUTTON.x, FOURTH_ROW_RIGHT_ABILITY_BUTTON.y))


	if ally.fifth_row_left_passive:
		pygame.draw.rect(screen, RED, FIFTH_ROW_LEFT_ABILITY_BUTTON)
	else:
		pygame.draw.rect(screen, GRAY, FIFTH_ROW_LEFT_ABILITY_BUTTON)

	if ally.fifth_row_middle_passive:
		pygame.draw.rect(screen, RED, FIFTH_ROW_MIDDLE_ABILITY_BUTTON)
	else:
		pygame.draw.rect(screen, GRAY, FIFTH_ROW_MIDDLE_ABILITY_BUTTON)
	
	if ally.fifth_row_right_passive:
		pygame.draw.rect(screen, RED, FIFTH_ROW_RIGHT_ABILITY_BUTTON)
	else:
		pygame.draw.rect(screen, GRAY, FIFTH_ROW_RIGHT_ABILITY_BUTTON)


	if ally.sixth_row_left_passive:
		pygame.draw.rect(screen, RED, SIXTH_ROW_LEFT_ABILITY_BUTTON)
	else:
		pygame.draw.rect(screen, GRAY, SIXTH_ROW_LEFT_ABILITY_BUTTON)
	
	if ally.sixth_row_middle_passive:
		pygame.draw.rect(screen, RED, SIXTH_ROW_MIDDLE_ABILITY_BUTTON)
	else:
		pygame.draw.rect(screen, GRAY, SIXTH_ROW_MIDDLE_ABILITY_BUTTON)
	
	if ally.sixth_row_right_passive:
		pygame.draw.rect(screen, RED, SIXTH_ROW_RIGHT_ABILITY_BUTTON)
	else:
		pygame.draw.rect(screen, GRAY, SIXTH_ROW_RIGHT_ABILITY_BUTTON)


	pygame.draw.rect(screen, GRAY, BACK_BUTTON_BIS)
	back_button_text = font.render("Back", 1, BLACK)
	screen.blit(back_button_text, (BACK_BUTTON_BIS.centerx - back_button_text.get_width()//2, BACK_BUTTON_BIS.centery - back_button_text.get_height()//2))

	pygame.draw.rect(screen, INTERMEDIATE_GRAY, DESCRIPTION_BAND)
	passive_description_text = intermediate_font.render(passive_description, 1,BLACK)
	screen.blit(passive_description_text, (DESCRIPTION_BAND.x + 10, DESCRIPTION_BAND.centery - passive_description_text.get_height()//2))
	if passive_cost:
		passive_cost_text = intermediate_font.render(f"cost: {passive_cost}", 1, BLACK)
		screen.blit(passive_cost_text, (DESCRIPTION_BAND.right - 10 - passive_cost_text.get_width(), DESCRIPTION_BAND.y + 5))
	if passive_name:
		passive_name_text = intermediate_font.render(f"{passive_name}:", 1, BLACK)
		screen.blit(passive_name_text, (DESCRIPTION_BAND.x + 5, DESCRIPTION_BAND.y + 5))

	pygame.display.update()

def training(ally):
	click = False
	run = True
	while run:
		clock.tick(60)
		mx, my = pygame.mouse.get_pos()
		passive_description = None
		passive_cost = None
		passive_name = None

		if FIRST_ROW_MIDDLE_ABILITY_BUTTON.collidepoint((mx, my)):
			passive_description = ally.first_row_middle_passive_description
			passive_cost = "100"
			passive_name = ally.first_row_middle_passive_name
			if click and ally.mastery >= 100 and ally.first_row_middle_passive == False:
				ally.first_row_middle_passive = True
				ally.mastery -= 100

		if SECOND_ROW_LEFT_ABILITY_BUTTON.collidepoint((mx, my)):
			passive_description = ally.second_row_left_passive_description
			passive_cost = "300"
			passive_name = ally.second_row_left_passive_name
			if click and ally.mastery >= 300 and ally.second_row_left_passive == False and ally.first_row_middle_passive:
				ally.second_row_left_passive = True
				ally.mastery -= 300
		if SECOND_ROW_MIDDLE_ABILITY_BUTTON.collidepoint((mx, my)):
			passive_description = ally.second_row_middle_passive_description
			passive_cost = "300"
			passive_name = ally.second_row_middle_passive_name
			if click and ally.mastery >= 300 and ally.second_row_middle_passive == False and ally.first_row_middle_passive:
				ally.second_row_middle_passive = True
				ally.mastery -= 300
		if SECOND_ROW_RIGHT_ABILITY_BUTTON.collidepoint((mx, my)):
			passive_description = ally.second_row_right_passive_description
			passive_cost = "300"
			passive_name = ally.second_row_right_passive_name
			if click and ally.mastery >= 300 and ally.second_row_right_passive == False and ally.first_row_middle_passive:
				ally.second_row_right_passive = True
				ally.mastery -= 300

		if THIRD_ROW_LEFT_ABILITY_BUTTON.collidepoint((mx, my)):
			passive_description = ally.third_row_left_passive_description
			passive_cost = "1000"
			passive_name = ally.third_row_left_passive_name
			if click and ally.mastery >= 1000 and ally.third_row_left_passive == False and ally.second_row_left_passive:
				ally.third_row_left_passive = True
				ally.mastery -= 1000
		if THIRD_ROW_MIDDLE_ABILITY_BUTTON.collidepoint((mx, my)):
			passive_description = ally.third_row_middle_passive_description
			passive_cost = "1000"
			passive_name = ally.third_row_middle_passive_name
			if click and ally.mastery >= 1000 and ally.third_row_middle_passive == False and ally.second_row_middle_passive:
				ally.third_row_middle_passive = True
				ally.mastery -= 1000
		if THIRD_ROW_RIGHT_ABILITY_BUTTON.collidepoint((mx, my)):
			passive_description = ally.third_row_right_passive_description
			passive_cost = "1000"
			passive_name = ally.third_row_right_passive_name
			if click and ally.mastery >= 1000 and ally.third_row_right_passive == False and ally.second_row_right_passive:
				ally.third_row_right_passive = True
				ally.mastery -= 1000
				
		if FOURTH_ROW_LEFT_ABILITY_BUTTON.collidepoint((mx, my)):
			passive_description = ally.fourth_row_left_passive_description
			passive_cost = "2500"
			passive_name = ally.fourth_row_left_passive_name
			if click and ally.mastery >= 2500 and ally.fourth_row_left_passive == False and ally.third_row_left_passive:
				ally.fourth_row_left_passive = True
				ally.mastery -= 2500
		if FOURTH_ROW_MIDDLE_ABILITY_BUTTON.collidepoint((mx, my)):
			passive_description = ally.fourth_row_middle_passive_description
			passive_cost = "2500"
			passive_name = ally.fourth_row_middle_passive_name
			if click and ally.mastery >= 2500 and ally.fourth_row_middle_passive == False and ally.third_row_middle_passive:
				ally.fourth_row_middle_passive = True
				ally.mastery -= 2500
		if FOURTH_ROW_RIGHT_ABILITY_BUTTON.collidepoint((mx, my)):
			passive_description = ally.fourth_row_right_passive_description
			passive_cost = "2500"
			passive_name = ally.fourth_row_right_passive_name
			if click and Alex.mastery >= 2500 and ally.fourth_row_right_passive == False and ally.third_row_right_passive:
				ally.fourth_row_right_passive = True
				ally.mastery -= 2500
				
		if FIFTH_ROW_LEFT_ABILITY_BUTTON.collidepoint((mx, my)):
			passive_cost = "10000"
			if click and ally.mastery >= 10000 and ally.fifth_row_left_passive == False and ally.fourth_row_left_passive:
				ally.fifth_row_left_passive = True
				ally.mastery -= 10000
		if FIFTH_ROW_MIDDLE_ABILITY_BUTTON.collidepoint((mx, my)):
			passive_cost = "10000"
			if click and ally.mastery >= 10000 and ally.fifth_row_middle_passive == False and ally.fourth_row_middle_passive:
				ally.fifth_row_middle_passive = True
				ally.mastery -= 10000
		if FIFTH_ROW_RIGHT_ABILITY_BUTTON.collidepoint((mx, my)):
			passive_cost = "10000"
			if click and ally.mastery >= 10000 and ally.fifth_row_right_passive == False and ally.fourth_row_right_passive:
				ally.fifth_row_right_passive = True
				ally.mastery -= 10000

		if SIXTH_ROW_LEFT_ABILITY_BUTTON.collidepoint((mx, my)):
			passive_cost = "50000"
			if click and ally.mastery >= 50000 and ally.sixth_row_left_passive == False and ally.fifth_row_left_passive:
				ally.sixth_row_left_passive = True
				ally.mastery -= 50000
		if SIXTH_ROW_MIDDLE_ABILITY_BUTTON.collidepoint((mx, my)):
			passive_cost = "50000"
			if click and ally.mastery >= 50000 and ally.sixth_row_middle_passive == False and ally.fifth_row_middle_passive:
				ally.sixth_row_middle_passive = True
				ally.mastery -= 50000
		if SIXTH_ROW_RIGHT_ABILITY_BUTTON.collidepoint((mx, my)):
			passive_cost = "50000"
			if click and ally.mastery >= 50000 and ally.sixth_row_right_passive == False and ally.fifth_row_right_passive:
				ally.sixth_row_right_passive = True
				ally.mastery -= 50000

		if BACK_BUTTON_BIS.collidepoint((mx, my)):
			if click:
				run = False
				break

		click = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					run = False
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True

		training_draw_window(ally,passive_description,passive_cost,passive_name)
	if ally.name == "Alex":
		alex_assign_bonus()

###################
# TRAINING GROUND #

def training_ground_main_draw_window():
	BACKGROUND()
	pygame.draw.rect(screen, GRAY, TOP_BAND)
	check_party_text = font.render("Training Ground", 1, BLACK)
	screen.blit(check_party_text, (TOP_BAND.centerx - check_party_text.get_width()//2, TOP_BAND.centery - check_party_text.get_height()//2))

	overall_text = None
	for ally in party.party:
		coordinate_x, coordinate_y = get_coordinate_new(ally,"party")
		overall_text = font.render(f"{ally.name} :", 1, BLACK)
		screen.blit(overall_text, (75, coordinate_y))

		overall_text = font.render(f"Mastery: {ally.mastery}", 1, BLACK)
		screen.blit(overall_text, (75, coordinate_y + 25))
	
	if len(party.party) >= 1:
		pygame.draw.rect(screen, GRAY, FIRST_MEMBER_BUTTON)
		screen.blit(TRAINING_IMAGE, (FIRST_MEMBER_BUTTON.x, FIRST_MEMBER_BUTTON.y))
	if len(party.party) >= 2:
		pygame.draw.rect(screen, GRAY, SECOND_MEMBER_BUTTON)
		screen.blit(TRAINING_IMAGE, (SECOND_MEMBER_BUTTON.x, SECOND_MEMBER_BUTTON.y))
	if len(party.party) >= 3:
		pygame.draw.rect(screen, GRAY, THIRD_MEMBER_BUTTON)
		screen.blit(TRAINING_IMAGE, (THIRD_MEMBER_BUTTON.x, THIRD_MEMBER_BUTTON.y))
	if len(party.party) == 4:
		pygame.draw.rect(screen, GRAY, FOURTH_MEMBER_BUTTON)
		screen.blit(TRAINING_IMAGE, (FOURTH_MEMBER_BUTTON.x, FOURTH_MEMBER_BUTTON.y))

	pygame.draw.rect(screen, GRAY, BACK_BUTTON)
	back_button_text = font.render("Back", 1, BLACK)
	screen.blit(back_button_text, (BACK_BUTTON.centerx - back_button_text.get_width()//2, BACK_BUTTON.centery - back_button_text.get_height()//2))

	pygame.display.update()

def training_ground_main():
	click = False
	run = True
	while run:
		clock.tick(60)
		mx, my = pygame.mouse.get_pos()
		
		if FIRST_MEMBER_BUTTON.collidepoint((mx, my)):
			if click and len(party.party) >= 1:
				training(party.party[0])
		if SECOND_MEMBER_BUTTON.collidepoint((mx, my)):
			if click and len(party.party) >= 2:
				training(party.party[1])
		if THIRD_MEMBER_BUTTON.collidepoint((mx, my)):
			if click and len(party.party) >= 3:
				training(party.party[2])
		if FOURTH_MEMBER_BUTTON.collidepoint((mx, my)):
			if click and len(party.party) == 4:
				training(party.party[3])
		if BACK_BUTTON.collidepoint((mx, my)):
			if click:
				run = False

		click = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					run = False
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True

		training_ground_main_draw_window()

###################
#### Town ####

def town_draw_window():
	BACKGROUND()
	pygame.draw.rect(screen, GRAY, TOP_BAND)
	main_menu_text = font.render("Town", 1, BLACK)
	screen.blit(main_menu_text, (TOP_BAND.centerx - main_menu_text.get_width()//2, TOP_BAND.centery - main_menu_text.get_height()//2))

	pygame.draw.rect(screen, GRAY, FIGHT_BUTTON)
	fight_text = font.render("Fight", 1, BLACK)
	screen.blit(fight_text, (FIGHT_BUTTON.centerx - fight_text.get_width()//2, FIGHT_BUTTON.centery - fight_text.get_height()//2))

	pygame.draw.rect(screen, GRAY, SHOP_BUTTON)
	shop_text = font.render("Shop", 1, BLACK)
	screen.blit(shop_text, (SHOP_BUTTON.centerx - shop_text.get_width()//2, SHOP_BUTTON.centery - shop_text.get_height()//2))
	
	pygame.draw.rect(screen, GRAY, GO_HOME_BUTTON)
	go_home_text = font.render("Home", 1, BLACK)
	screen.blit(go_home_text, (GO_HOME_BUTTON.centerx - go_home_text.get_width()//2, GO_HOME_BUTTON.centery - go_home_text.get_height()//2))

	pygame.draw.rect(screen, GRAY, TRAINING_GROUND_BUTTON)
	training_ground_text = intermediate_font.render("Training Ground", 1, BLACK)
	screen.blit(training_ground_text, (TRAINING_GROUND_BUTTON.centerx - training_ground_text.get_width()//2, TRAINING_GROUND_BUTTON.centery - training_ground_text.get_height()//2))

	pygame.draw.rect(screen, GRAY, SAVE_BUTTON)
	save_text = font.render("Save", 1, BLACK)
	screen.blit(save_text, (SAVE_BUTTON.centerx - save_text.get_width()//2, SAVE_BUTTON.centery - save_text.get_height()//2))

	pygame.display.update()

def town():
	click = False
	run = True
	play_town_music()
	while run:
		clock.tick(60)
		mx, my = pygame.mouse.get_pos()

		if FIGHT_BUTTON.collidepoint((mx, my)):
			if click:
				check_for_death()
				if len(party.party_alive) != 0:
					in_dungeon()
				else:
					rest_before_dungeon()
		if SHOP_BUTTON.collidepoint((mx, my)):
			if click:
				in_shop()
		if GO_HOME_BUTTON.collidepoint((mx, my)):
			if click:
				home_screen()
		if TRAINING_GROUND_BUTTON.collidepoint((mx, my)):
			if click:
				training_ground_main()
		if SAVE_BUTTON.collidepoint((mx, my)):
			if click:
				complete_save()

		click = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True

		town_draw_window()

###################
### Game  Start ###

def game_start_draw_window():
	BACKGROUND()
	pygame.draw.rect(screen, GRAY, GAME_NAME_BAND)
	game_title_text = big_font.render("First Light", 1, BLACK)
	screen.blit(game_title_text, (GAME_NAME_BAND.centerx - game_title_text.get_width()//2, GAME_NAME_BAND.centery - game_title_text.get_height()//2))

	pygame.draw.rect(screen, GRAY, NEW_GAME_BUTTON)
	new_game_text = font.render("New Game", 1, BLACK)
	screen.blit(new_game_text, (NEW_GAME_BUTTON.centerx - new_game_text.get_width()//2, NEW_GAME_BUTTON.centery - new_game_text.get_height()//2))

	pygame.draw.rect(screen, GRAY, LOAD_GAME_BUTTON)
	load_game_text = font.render("Load Game", 1, BLACK)
	screen.blit(load_game_text, ( LOAD_GAME_BUTTON.centerx - load_game_text.get_width()//2, LOAD_GAME_BUTTON.centery - load_game_text.get_height()//2))

	pygame.draw.rect(screen, GRAY, CREDITS_BUTTON)
	credits_text = font.render("Credits", 1, BLACK)
	screen.blit(credits_text, (CREDITS_BUTTON.centerx - credits_text.get_width()//2, CREDITS_BUTTON.centery - credits_text.get_height()//2))

	pygame.display.update()

def game_start():
	click = False
	run = True
	while run:
		clock.tick(60)
		mx, my = pygame.mouse.get_pos()
		if NEW_GAME_BUTTON.collidepoint((mx, my)):
			if click:
				town()
		if LOAD_GAME_BUTTON.collidepoint((mx, my)):
			if click:
				complete_load()
				town()
		if CREDITS_BUTTON.collidepoint((mx, my)):
			if click:
				pass

		click = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True

		game_start_draw_window()

##################
#####Start-Up#####

Alex = Alex_stats()
goddess = goddess_base()
Emeline = Emeline_stats()
Azazel = Azazel_stats()
Ezekiel = Ezekiel_stats()
#available_ally = [Alex,Emeline,Azazel,Ezekiel]
#party = [Alex]
clock = pygame.time.Clock()
inventory = party_inventory()
#party_dead = []
monsterpedia = monsterpedia_base()
statistics = statistics_base()
achievement = achievement_base()
dungeon = dungeon_base()
fighting = fighting_base()
party = party_base()
shop = shop_database()

party.party.append(Alex)
party.number_of_ally = 1
party.number_of_ally_alive = 1
party.party_alive.append(Alex)
party.available_ally.append(Alex)
party.available_ally.append(Emeline)
party.available_ally.append(Azazel)
party.available_ally.append(Ezekiel)

enemy_party = enemy_party_base()

Alex.mastery = 1000000
#Alex.rage = 100
inventory.town_gold += 900000

#inventory.dungeon_loot = {"something" : 3, "else" : 1, "yes" : 5, "no" : 4, "why" : 11, "though" : 89, "the" : 105, "fuck" : 99, "is" : 54, "that" : 74, "shit" : 85200, "bruh" : 754}
inventory.town_storage = {"Goblin's Soulgem" : 5}

game_start()
#in_dungeon()
#in_fight()