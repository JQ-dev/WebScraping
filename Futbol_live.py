
from vpython import *
from random import *
import string
import numpy as np
import time 
import pandas as pd
import matplotlib.pyplot as plt

# canvas
def new_screen():
    scene = canvas(title='Soccer Match',width=1200, height=600,
                   center = vector(60,40,0), background = vector(0.37,0.5,0.22),
                   resizable = True)
    
    hor_lines = [[0,0,120],[19.85,0,16.5],[19.85,103.5,120],[30.85,0,5.5],[30.85,114.5,120],
                 [49.85,0,5.5],[49.85,114.5,120],[60.15,0,16.5],[60.15,103.5,120],[80,0,120]]
    ver_lines = [[0,0,80],[5.5,30.85,49.85],[16.5,19.85,60.15],[60,0,80],
                 [103.5,19.85,60.15],[114.5,30.85,49.85],[120,0,80]]
    
    for hor in hor_lines:
        static = hor[0]
        p1 = hor[1]
        p2 = hor[2]
        hl = curve(vector(p1,static,0), vector(p2,static,0))
    
    for ver in ver_lines:
        static = ver[0]
        p1 = ver[1]
        p2 = ver[2]
        hl = curve(vector(static,p1,0), vector(static,p2,0))
    
    cr = shapes.circle(pos=[60,40],radius=9.15, np=360)
    for point in cr:
        vect = vector(point[0],point[1],0)
        hl = points(pos=vect, radius=2)
    
    p1 = points(pos=[vector(60,40,0)], radius=3)
    p1 = points(pos=[vector(11,40,0)], radius=3)
    p1 = points(pos=[vector(109,40,0)], radius=3)
    
    ar = shapes.arc(pos=[109,40],radius=9.15, angle1=(pi+0.9258), angle2=(pi-0.9258), np=360)
    for point in ar:
        vect = vector(point[0],point[1],0)
        hl = points(pos=vect, radius=2, color = color.white)
    
    ar = shapes.arc(pos=[11,40],radius=9.15, angle1=(0.9258), angle2=(-0.9258), np=360)
    for point in ar:
        vect = vector(point[0],point[1],0)
        hl = points(pos=vect, radius=2, color = color.white)
    
    del hor_lines, ver_lines, ar, p1, p2 , cr, static, point, hor , ver


full_game = pd.read_csv('full_game.csv',sep=',', header='infer', encoding= "utf-8")

ball_move = pd.read_csv('ball_move.csv',sep=',', header='infer', encoding= "utf-8")

player_dict = full_game['player/id'].drop_duplicates()
.to_dict()



move = full_game.loc[5,:]


def ball_receipt(player_dict,full_row):
    
    if move['ball_receipt/outcome/name'] == 'Incomplete':
        
    
    
    
    return player_id, points


def player_pass (player_dict,full_row,points):
    




########################################################################################################

ball_move = pd.read_csv('ball_move.csv',sep=',', header='infer', encoding= "utf-8")

new_screen()


time.sleep( 5  )

points_pass = 2
#points_pass_press = 1



period = 2
#colors    
pass_color = [vector(0 ,0.5 ,1),vector(1 ,0.5 ,0)]  
carry_color = [vector(0 ,0 ,1),vector(1 ,0 ,0)]   
press_color = [vector(0 ,0 ,1),vector(1 ,0 ,0)]    
    
#def play_half(period):
half = ball_move.loc [ ball_move.loc[:,'period'] == period , : ]

timing = label(text='0.00',box=False, pos= vector(115,85,0), color = color.black)

ball = sphere(  pos=vector(60,40,1),  radius=1, trail_color = vector(0.57,0.7,0.42),
              make_trail=True, trail_type = 'points' , trail_radius = 0.1  , 
              retain=6, texture = textures.wood_old)



speed_time = 4

player_score = {}
previuos_move = ''

for index in half.index[:]:

    i = -1

    i += 1   
    
    index = half.index[i]
    
    team = 1 if half.loc[index,'team/name'] == 'England' else 0
    loc1i = half.loc[index,'location/0']
    loc2i = half.loc[index,'location/1']
    loc1f = half.loc[index,'end_location/0']
    loc2f = half.loc[index,'end_location/1']
    pos_ini = vector(loc1i,loc2i,0)
    pos_fin = vector(loc1f,loc2f,0)

    #wait =  half.loc[index,'secs'] - half.loc[index-1,'secs']
    #timing.text = half.loc[index,'game_time']    
    
    if half.loc[index,'type/name'] == 'Pass':
        player1 = cylinder(pos=pos_ini, axis=vector(0,0,2), radius=0.5 )
        player1.color = pass_color[team] 
        
        player2 = cylinder(pos=pos_fin, axis=vector(0,0,2), radius=0.5 )
        player2.color = press_color[team]         
        
        ball.pos = vector(pos_ini)
        ball.trail_color = pass_color[team]
        pase = curve(pos_ini, pos_fin , color = pass_color[team], radius = 0.2)
        
        time.sleep( half.loc[index,'duration']/speed_time  )        
        try:
            rec.visible = False
        except:
            pass
        player1.visible = False
        player2.visible = False
        pase.visible = False
        
        playerO = half.loc[index,'player']
        #playerD = half.loc[index,'player']
        player_id = half.loc[index,'player/id']
        player_score[player_id] += points_pass
#        previuos_move = 'pass'
#        previous_player = player_id
        print(playerO,'try a pass to')
        
        
        
        
    if half.loc[index,'type/name'] == 'Ball Receipt*':
        player1.pos = vector(pos_ini)
        ball.pos = vector(pos_ini)
        if half.loc[index,'pass/outcome/name'] == 'Incomplete':
            rec = cylinder(pos=pos_ini, axis=vector(0,0,0.5), radius=1 )
            rec.color = press_color[team] 
            
            time.sleep( half.loc[index,'duration']/speed_time  ) 
            rec.visible = False   
        time.sleep( half.loc[index,'duration']/speed_time  )         
        player1.visible = False
         
    
    
    if half.loc[index,'type/name'] == 'Carry':

        player1.pos = vector(pos_ini)
        ball.pos = vector(pos_ini)
        carry = curve(pos_ini, pos_fin , color = carry_color[team], radius = 0.2)
        ball.pos = vector(pos_fin)
        player1.pos = vector(pos_fin)
    
        time.sleep( half.loc[index,'duration']/speed_time  )         
        player1.visible = False
        carry.visible = False    
    
    
    if half.loc[index,'type/name'] == 'Pressure':
        press = cylinder(pos=pos_ini, axis=vector(0,0,2), radius=2 )
        press.color = press_color[team] 
 
        time.sleep( half.loc[index,'duration']/speed_time  )             
        press.visible = False    
        
        if previuos_move == 'pass':
            player_score[player_id] += points_pass_press
    
    
    if half.loc[index,'type/name'] == 'Shot':
       shot = curve(pos_ini, pos_fin, color=color.green) 
       shoot_player = half.loc[index,'player']
       shooter = label(text=shoot_player,  box=False, pos= pos_ini, 
                       color = color.black, heigth = 8)

       time.sleep(2) 
       shooter.visible = False
       
    if half.loc[index,'type/name'] == 'Goal Keeper':
       result = half.loc[index,'goalkeeper/type/name']
       gkeeper = cylinder(pos=pos_ini, axis=vector(0,0,3), radius=3 )
       gkeeper.color = press_color[team]
       outcome = label(text=result,  box=False, pos= pos_ini, 
                       color = color.black, heigth = 8)
       time.sleep(1) 
       gkeeper.visible = False
       outcome.visible = False
               
       
    print(half.loc[index,'type/name'])


#player1.visible = False
#player2.visible = False
#press.visible = False
#carry.visible = False
#ball.visible = False
#pase.visible = False

#ball.trail_color = vector(0.37,0.5,0.22)
#ball.pos = vector(60,40,1)
#time.sleep(0.5)
#ball.pos = vector(60,39,1)
#time.sleep(0.5)
#ball.pos = vector(60,40,1)
#time.sleep(0.5)
#ball.pos = vector(61,40,1)
#time.sleep(0.5)
#ball.pos = vector(60,40,1)


########################################################################################################

def passes():
    
    p = curve(vector(shot_pos[0],shot_pos[1],0), vector(loc1,loc2,0),color=color.yellow)


########################################################################################################
    
    
    
time.sleep(5)

new_screen()
play_half(1)

time.sleep(5)

new_screen()
play_half(2)


      



