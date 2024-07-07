print("GAME STARTED ########################################################################################################################################")
import pygame
import math
import copy
import random
from sys import exit
from rendering_3d_functions_module import clbrt,unclbrt,magnify,project,point_in_plane,point_in_rect,point_inside,calculate_circle_points,rotate_point,dist,geo_cent,dist3d,avg_depth,angle_between_points,bulk_magnify
from other_functions_module import mod,get_alpha,get_key
import asyncio
async def main():

    screenx=1550
    screeny=810
    pygame.init()
    pygame.mixer.init()
    screen=pygame.display.set_mode((screenx,screeny))
    clock=pygame.time.Clock()
    # initialization
    particles=50
    particle_size=50
    particle_images=[]
    particle_rects=[]
    line_ends=[]
    particle_velocities=[]
    resultant_velocity=1
    menu_activated=False
    clock_woosh_path="assets\woosh.mp3"
    anti_clock_woosh_path="assets\shoow.mp3"
    instructions_path="assets\instructions.png"
    menu_image_path="assets\menu.png"
    menu_icon_image_path="assets\menu_icon.png"
    on_switch_path="assets\on_switch.png"
    off_switch_path="assets\off_switch.png"
    small_off_switch_path="assets\small_off_switch.png"
    small_on_switch_path="assets\small_on_switch.png"
    minus_button_path="assets\minus_button.png"
    plus_button_path="assets\plus_button.png"
    shuffle_path="assets\shuffle.png"
    solve_path="assets\solve.png"
    icon_path="assets\solve.ico"
    woosh = pygame.mixer.Sound(clock_woosh_path)
    shoow = pygame.mixer.Sound(anti_clock_woosh_path)
    menu=pygame.image.load(menu_image_path).convert_alpha()
    menu_icon=pygame.image.load(menu_icon_image_path).convert_alpha()
    menu_icon_rect=menu_icon.get_rect(topleft=(10,5))
    menu_rect=menu.get_rect(topright=(0,0))
    icon_image = pygame.image.load(icon_path)  
    icon_size = (50, 50) 
    icon = pygame.transform.scale(icon_image, icon_size)
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Rubick's Cube by Aadi")
    class switch:
        def __init__(self,on,rect):
            self.on=on
            self.onimage=pygame.image.load(on_switch_path).convert_alpha()
            self.offimage=pygame.image.load(off_switch_path).convert_alpha()
            self.rect=rect
            if self.on:
                self.image=self.onimage
            else:
                self.image=self.offimage
        def display(self):
            screen.blit(self.image,self.rect)
        def detect(self):
            if point_in_plane(mouse_pos,self.rect.topleft,self.rect.bottomright):
                for event in pygame.event.get():
                    if event.type==pygame.MOUSEBUTTONDOWN and event.key==1:
                        self.on=not(self.on)
                        break
        def update(self):
            if self.on:
                self.image=self.onimage
            else:
                self.image=self.offimage
    for i in range(particles):
        particle_images.append(pygame.image.load("assets\star.png"))
        particle_rects.append(particle_images[i].get_rect(center=(0,0)))
        line_ends.append([0,0])
    particle_velocities=calculate_circle_points(50,particles)
    solved=True
    xrecord=0
    yrecord=0
    s=100 #side length of cube
    spr=15 #seperation between the boxes
    senstivity=5 #mouse sensitivity
    speed=9 #speed of turning , speed must be factor of 90
    sr=300 #screen depth
    cm=[0,0,1000] #camera position
    shaders=True
    brightness=750 #brightness
    contrast=2 #contast of shaders
    screen_color=(0,0,0)
    line_color=(0,0,0)
    highlight=100
    magnification=1.3
    center_mode=True
    keyboard_mode=False
    solve_=False
    mix=False
    mixnumber=20
    record_of_moves=[]
    #1 for transparent 
    #2 for opaque 
    #3 for black
    tob=3
    side_mode=not center_mode
    selection_mode=center_mode
    if tob==1:
        show_infaces=False
        curtain=False
    elif tob==2:
        show_infaces=True
        curtain=False
    else:
        thickness=0
        show_infaces=True
        curtain=True
    win = False
    cube_shuffled=False
    maxl=s*1.5 + spr
    offset=spr+s
    x,y,z=0,1,2
    center=[0,0,0]
    Cntr=[0,0,0]
    vertices3d=[]
    center2d=screenx/2,screeny/2
    #cube
    for i1 in [0,-1,1]:
        for j1 in [0,-1,1]:
            for k1 in [0,-1,1]:
                for i in [1,-1]:
                    for j in [1,-1]:
                        for k in [1,-1]:
                            vertices3d.append([(s/2*i)+(offset*i1),(s/2*j)+(offset*j1),(s/2*k)+(offset*k1)])
    font_size = 20
    font = pygame.font.Font(None, font_size)
    button1pressed=False
    true_points={}
    x_turn=y_turn=0
    # classes
    class point:
        def __init__(self,name,coords2d,coords3d):
            self.coords2d=coords2d
            self.coords3d=coords3d
            self.name=name
    for i in range(len(vertices3d)):
        true_points[chr(97+(i%8))+str(int(i//8))]=point(chr(97+(i%8)),project(vertices3d[i]),vertices3d[i])
    true_points["anchor0"],anchor0=point("anchor0",None,[0,0,(s*1.5)+spr]),point("anchor0",None,[0,0,(s*1.5)+spr])
    true_points["anchor1"],anchor1=point("anchor1",None,[0,(s*1.5)+spr,0]),point("anchor1",None,[0,(s*1.5)+spr,0])
    def find_correction():
        xycorrection=angle_between_points(  [dist([0,0],true_points["anchor0"].coords3d[:2]),0]  ,  true_points["anchor0"].coords3d[:2] )
        #finding correction for xy ad xz for anchor0
        i=true_points["anchor0"].coords3d[:]
        i=rotate_point(i,0,1,xycorrection)
        if round(i[1])==0.0:
            pass
        else:
            xycorrection=-xycorrection
            i=true_points["anchor0"].coords3d[:]
            i=rotate_point(i,0,1,xycorrection)
        anchor0temp=i[:]
        xzcorrection=angle_between_points([anchor0temp[0],anchor0temp[2]],[anchor0.coords3d[0],anchor0.coords3d[2]])
        i=anchor0temp[:]
        i=rotate_point(i,0,2,xzcorrection)
        if round(i[0])==0.0:
            pass
        else:
            xzcorrection=-xzcorrection
            i=anchor0temp[:]
            i=rotate_point(i,0,2,xzcorrection)
        anchor0temp=i[:]
        #applying correction to anchor1
        i=true_points["anchor1"].coords3d[:]
        i=rotate_point(i,0,1,xycorrection)
        i=rotate_point(i,0,2,xzcorrection)
        anchor1temp=i[:]
        finalxycorrection=angle_between_points(anchor1temp[:2],anchor1.coords3d[:2])
        i=anchor1temp[:]
        i=rotate_point(i,0,1,finalxycorrection)
        if round(i[0])==round(anchor1.coords3d[0]) and round(i[1])==round(anchor1.coords3d[1]) and round(i[2])==round(anchor1.coords3d[2]):
            pass
        else:
            finalxycorrection=-finalxycorrection
            i=anchor1temp[:]
            i=rotate_point(i,0,1,finalxycorrection)
        return[xycorrection,xzcorrection,finalxycorrection]
    presolved=True
    fireworks=False
    planes=[]
    for i in range(len(vertices3d)//8):
        for j in ["abdc","eacg","fegh","bfhd","feab","hdcg"]:
            str1=""
            for k in j:
                str1+=k+str(i)+" "
            str1.strip()
            planes.append(str1)
    # #Yellow acge- blue front
    yellowf=[ [17 , 11 , 14] , [8 ,  2 ,  5] , [26 , 20 , 23] ]
    # #Blue - bdca
    bluef=[[26 , 20 , 23],[24 , 18 , 21],[25 , 19 , 22]]
    # #Red- cdhg
    redf=[[23 , 5 , 14],[21 , 3 , 12],[22 , 4 , 13]]
    # #green eghf
    greenf=[[14 , 11 , 17],[12 ,  9 , 15],[13 , 10 , 16]]
    # #pink - baef
    pinkf=[[24 , 25 , 26],[7 , 6 , 8],[16 , 15 , 17]]
    # #white fhdb- yellow down , red front
    whitef=[[16 , 7 , 25],[10 , 1 , 19],[13 , 4 , 22]]
    visible={"eacg":yellowf,"hdcg":redf,"abdc":bluef,"fegh":greenf,"feab":pinkf,"bfhd":whitef}
    out_faces=[]
    for k,v in visible.items():
        for i in v:
            for j in i:
                str1=""
                for k1 in k:
                    str1+=k1+str(j)+" "
                str1.strip()
                out_faces.append(str1)

    boxes={}
    for i in range(27):
        corners=[]
        for j in "abcdefgh":
            corners.append(true_points[j+str(i)].coords3d)
        boxes[i]=(corners)
    box_centers={}
    for k,v in boxes.items():
        box_centers[k]=geo_cent(v)
    color_set=[[0, 0, 255], [255, 255, 0], [0, 255, 0], [255, 255, 255], [255, 0, 255], [255, 0, 0]]
    colors={}
    count=0
    for  i in planes:
        colors[i]=color_set[count%6]
        count+=1
    def turn_face(face_name,degrees):
        nonlocal true_points
        corrections=find_correction()
        for k in true_points:
            true_points[k].coords3d=rotate_point(true_points[k].coords3d,0,1,corrections[0])
            true_points[k].coords3d=rotate_point(true_points[k].coords3d,0,2,corrections[1])
            true_points[k].coords3d=rotate_point(true_points[k].coords3d,0,1,corrections[2])
        pointkey=face_turn_dict[face_name]
        turning_points=[]
        for i in pointkey:
            axis=-1
            for j in true_points[i].coords3d:
                axis+=1
                if round(j,5) in [(s/2)+spr,-(s/2)-spr,(s*1.5)+spr,-(s*1.5)-spr]:
                    for k,v in true_points.items():
                        if round(v.coords3d[axis],5)==round(j,5):
                            turning_points.append(k)
        for k in turning_points:
            if k in "anchor1anchor0":
                pass
            else:
                i=true_points[k].coords3d
                if face_name in "redpink":
                    i=rotate_point(i,0,2,degrees)
                
                elif face_name in "bluegreen":
                    i=rotate_point(i,1,2,degrees)
                else:
                    i=rotate_point(i,1,0,degrees)
                true_points[k].coords3d=i
        for k in true_points:
            true_points[k].coords3d=rotate_point(true_points[k].coords3d,0,1,-corrections[2])
            true_points[k].coords3d=rotate_point(true_points[k].coords3d,0,2,-corrections[1])
            true_points[k].coords3d=rotate_point(true_points[k].coords3d,0,1,-corrections[0])
    face_turn_dict={"yellow":["a2","b2"],"blue":["a18","e18"],"white":["a1","b1"],"green":["a9","e9"],"red":["c3","a3"],"pink":["a6","c6"]}
    face_to_color={"eacg":"yellow","hdcg":"red","abdc":"blue","fegh":"green","feab":"pink","bfhd":"white"}
    color_to_face={"yellow":"e2 a2 c2 g2 ","blue":"a18 b18 d18 c18","white":"b1 f1 h1 d1","green":"f9 e9 g9 h9","red":"h3 d3 c3 g3","pink":"f6 e6 a6 b6"}
    id_dict={(s*1.5 + spr, 2): "yellow",(s*1.5 + spr, 0): "blue",(-(s*1.5 + spr), 1): "red",(-(s*1.5 + spr), 2): "white",(-(s*1.5 + spr), 0): "green",(s*1.5 + spr, 1): "pink"}
    celebrating=False
    celeb_count=0
    center_faces=" e2 a2 c2 g2 h3 d3 c3 g3 b1 f1 h1 d1 f6 e6 a6 b6 a18 b18 d18 c18 f9 e9 g9 h9 "
    tick=0
    mouse_pos=[0,0]
    selected_color=None
    selected_plane=None
    turning=False
    x_dif=y_dif=0
    anti= False
    color_val_dict={114:"red",121:"yellow",98:"blue",103:"green",112:"pink",119:"white"}
    checkpoints=copy.deepcopy(true_points)
    undo=False
    undo_count=0
    redo=False
    for k,v in true_points.items():
        true_points[k].coords3d=rotate_point(true_points[k].coords3d,0,2,45)
        true_points[k].coords3d=rotate_point(true_points[k].coords3d,2,1,45)
    mute=True
    inverted_mouse=False
    menu_moving=False
    reset_cube=False
    reset_settings=False
    resetting=False
    menuxvelocity=0
    speed_list=[1,3,5,6,9,10,15,30,45]
    speed_len=len(speed_list)
    inverted_mouse_switch_on=pygame.image.load(on_switch_path).convert_alpha()
    center_mode_switch_on=pygame.image.load(on_switch_path).convert_alpha()
    side_mode_switch_on=pygame.image.load(on_switch_path).convert_alpha()
    keyboard_mode_switch_on=pygame.image.load(on_switch_path).convert_alpha()
    shaders_switch_on=pygame.image.load(small_on_switch_path).convert_alpha()
    hollow_switch_on=pygame.image.load(small_on_switch_path).convert_alpha()
    solid_switch_on=pygame.image.load(small_on_switch_path).convert_alpha()
    black_switch_on=pygame.image.load(small_on_switch_path).convert_alpha()
    senstivity_plus=pygame.image.load(plus_button_path).convert_alpha()
    senstivity_minus=pygame.image.load(minus_button_path).convert_alpha()
    senstivity_plus_rect=senstivity_plus.get_rect(center=(255,125))
    senstivity_minus_rect=senstivity_minus.get_rect(center=(275,125))
    brightness_plus=pygame.image.load(plus_button_path).convert_alpha()
    brightness_minus=pygame.image.load(minus_button_path).convert_alpha()
    brightness_plus_rect=senstivity_plus.get_rect(center=(255,360))
    brightness_minus_rect=senstivity_minus.get_rect(center=(275,360))
    contrast_plus=pygame.image.load(plus_button_path).convert_alpha()
    contrast_minus=pygame.image.load(minus_button_path).convert_alpha()
    contrast_plus_rect=senstivity_plus.get_rect(center=(255,385))
    contrast_minus_rect=senstivity_minus.get_rect(center=(275,385))
    mute_switch_on=pygame.image.load(on_switch_path).convert_alpha()
    mute_switch_off=pygame.image.load(off_switch_path).convert_alpha()
    mute_switch_rect=mute_switch_on.get_rect(center=(265,530))
    magnification_plus=pygame.image.load(plus_button_path).convert_alpha()
    magnification_minus=pygame.image.load(minus_button_path).convert_alpha()
    magnification_plus_rect=senstivity_plus.get_rect(center=(255,570))
    magnification_minus_rect=senstivity_minus.get_rect(center=(275,570))
    speed_plus=pygame.image.load(plus_button_path).convert_alpha()
    speed_minus=pygame.image.load(minus_button_path).convert_alpha()
    speed_plus_rect=senstivity_plus.get_rect(center=(255,615))
    speed_minus_rect=senstivity_minus.get_rect(center=(275,615))
    spr_plus=pygame.image.load(plus_button_path).convert_alpha()
    spr_minus=pygame.image.load(minus_button_path).convert_alpha()
    spr_plus_rect=senstivity_plus.get_rect(center=(255,715))
    spr_minus_rect=senstivity_minus.get_rect(center=(275,715))
    s_plus=pygame.image.load(plus_button_path).convert_alpha()
    s_minus=pygame.image.load(minus_button_path).convert_alpha()
    s_plus_rect=senstivity_plus.get_rect(center=(255,760))
    s_minus_rect=senstivity_minus.get_rect(center=(275,760))
    inverted_mouse_switch_off=pygame.image.load(off_switch_path).convert_alpha()
    center_mode_switch_off=pygame.image.load(off_switch_path).convert_alpha()
    side_mode_switch_off=pygame.image.load(off_switch_path).convert_alpha()
    keyboard_mode_switch_off=pygame.image.load(off_switch_path).convert_alpha()
    shaders_switch_off=pygame.image.load(small_off_switch_path).convert_alpha()
    hollow_switch_off=pygame.image.load(small_off_switch_path).convert_alpha()
    solid_switch_off=pygame.image.load(small_off_switch_path).convert_alpha()
    black_switch_off=pygame.image.load(small_off_switch_path).convert_alpha()
    inverted_mouse_switch_rect=inverted_mouse_switch_off.get_rect(center=(265,85))
    center_mode_switch_rect=center_mode_switch_off.get_rect(center=(265,170))
    side_mode_switch_rect=center_mode_switch_off.get_rect(center=(265,215))
    keyboard_mode_switch_rect=center_mode_switch_off.get_rect(center=(265,260))
    shaders_switch_rect=shaders_switch_off.get_rect(center=(265,340))
    hollow_switch_rect=hollow_switch_off.get_rect(center=(265,440))
    solid_switch_rect=solid_switch_off.get_rect(center=(265,463))
    black_switch_rect=black_switch_off.get_rect(center=(265,486))
    solve_button=pygame.image.load(solve_path).convert_alpha()
    shuffle_button=pygame.image.load(shuffle_path).convert_alpha()
    solve_rect=solve_button.get_rect(bottomright=(1550,800))
    shuffle_rect=shuffle_button.get_rect(bottomright=solve_rect.bottomleft)
    shuffle_rect.centerx-=50
    solve_rect.centerx-=20
    speed_index=6
    while True:
        screen.fill((255,0,0))
        mouse_pos1=list(pygame.mouse.get_pos())
        mouse_pos1[0]-=20
        if reset_cube:
            reset_cube=False
            screenx=1550
            screeny=810
            particles=50
            particle_size=50
            particle_images=[]
            particle_rects=[]
            line_ends=[]
            particle_velocities=[]
            resultant_velocity=1
            for i in range(particles):
                particle_images.append(pygame.image.load("assets\star.png"))
                particle_rects.append(particle_images[i].get_rect(center=(0,0)))
                line_ends.append([0,0])
            particle_velocities=calculate_circle_points(50,particles)
            solved=True
            xrecord=0
            yrecord=0
            thickness=1 #thickness of border of cube
            senstivity=5 #mouse sensitivity
            speed=15 #speed of turning , speed must be factor of 90
            sr=200 #screen depth
            cm=[0,0,1000] #camera position
            shaders=True
            brightness=750 #brightness
            contrast=2 #contast of shaders
            screen_color=(0,0,0)
            line_color=(0,0,0)
            highlight=100
            magnification=1.3
            center_mode=True
            keyboard_mode=False
            solve_=False
            mix=False
            mixnumber=20
            record_of_moves=[]
            #1 for transparent 
            #2 for opaque 
            #3 for black
            tob=3
            side_mode=not center_mode
            selection_mode=center_mode
            if tob==1:
                show_infaces=False
                curtain=False
            elif tob==2:
                show_infaces=True
                curtain=False
            else:
                thickness=0
                show_infaces=True
                curtain=True
            win = False
            cube_shuffled=False
            maxl=s*1.5 + spr
            offset=spr+s
            x,y,z=0,1,2
            center=[0,0,0]
            Cntr=[0,0,0]
            vertices3d=[]
            center2d=screenx/2,screeny/2
            #cube
            for i1 in [0,-1,1]:
                for j1 in [0,-1,1]:
                    for k1 in [0,-1,1]:
                        for i in [1,-1]:
                            for j in [1,-1]:
                                for k in [1,-1]:
                                    vertices3d.append([(s/2*i)+(offset*i1),(s/2*j)+(offset*j1),(s/2*k)+(offset*k1)])
            button1pressed=False
            true_points={}
            x_turn=y_turn=0
            for i in range(len(vertices3d)):
                true_points[chr(97+(i%8))+str(int(i//8))]=point(chr(97+(i%8)),project(vertices3d[i]),vertices3d[i])
            true_points["anchor0"],anchor0=point("anchor0",None,[0,0,(s*1.5)+spr]),point("anchor0",None,[0,0,(s*1.5)+spr])
            true_points["anchor1"],anchor1=point("anchor1",None,[0,(s*1.5)+spr,0]),point("anchor1",None,[0,(s*1.5)+spr,0])
            presolved=True
            fireworks=False
            planes=[]
            for i in range(len(vertices3d)//8):
                for j in ["abdc","eacg","fegh","bfhd","feab","hdcg"]:
                    str1=""
                    for k in j:
                        str1+=k+str(i)+" "
                    str1.strip()
                    planes.append(str1)
            # #Yellow acge- blue front
            yellowf=[ [17 , 11 , 14] , [8 ,  2 ,  5] , [26 , 20 , 23] ]
            # #Blue - bdca
            bluef=[[26 , 20 , 23],[24 , 18 , 21],[25 , 19 , 22]]
            # #Red- cdhg
            redf=[[23 , 5 , 14],[21 , 3 , 12],[22 , 4 , 13]]
            # #green eghf
            greenf=[[14 , 11 , 17],[12 ,  9 , 15],[13 , 10 , 16]]
            # #pink - baef
            pinkf=[[24 , 25 , 26],[7 , 6 , 8],[16 , 15 , 17]]
            # #white fhdb- yellow down , red front
            whitef=[[16 , 7 , 25],[10 , 1 , 19],[13 , 4 , 22]]
            visible={"eacg":yellowf,"hdcg":redf,"abdc":bluef,"fegh":greenf,"feab":pinkf,"bfhd":whitef}
            out_faces=[]
            for k,v in visible.items():
                for i in v:
                    for j in i:
                        str1=""
                        for k1 in k:
                            str1+=k1+str(j)+" "
                        str1.strip()
                        out_faces.append(str1)
            boxes={}
            for i in range(27):
                corners=[]
                for j in "abcdefgh":
                    corners.append(true_points[j+str(i)].coords3d)
                boxes[i]=(corners)
            box_centers={}
            for k,v in boxes.items():
                box_centers[k]=geo_cent(v)
            color_set=[[0, 0, 255], [255, 255, 0], [0, 255, 0], [255, 255, 255], [255, 0, 255], [255, 0, 0]]
            colors={}
            count=0
            for  i in planes:
                colors[i]=color_set[count%6]
                count+=1
            face_turn_dict={"yellow":["a2","b2"],"blue":["a18","e18"],"white":["a1","b1"],"green":["a9","e9"],"red":["c3","a3"],"pink":["a6","c6"]}
            face_to_color={"eacg":"yellow","hdcg":"red","abdc":"blue","fegh":"green","feab":"pink","bfhd":"white"}
            color_to_face={"yellow":"e2 a2 c2 g2 ","blue":"a18 b18 d18 c18","white":"b1 f1 h1 d1","green":"f9 e9 g9 h9","red":"h3 d3 c3 g3","pink":"f6 e6 a6 b6"}
            id_dict={(s*1.5 + spr, 2): "yellow",(s*1.5 + spr, 0): "blue",(-(s*1.5 + spr), 1): "red",(-(s*1.5 + spr), 2): "white",(-(s*1.5 + spr), 0): "green",(s*1.5 + spr, 1): "pink"}
            celebrating=False
            celeb_count=0
            center_faces=" e2 a2 c2 g2 h3 d3 c3 g3 b1 f1 h1 d1 f6 e6 a6 b6 a18 b18 d18 c18 f9 e9 g9 h9 "
            tick=0
            mouse_pos=[0,0]
            selected_color=None
            selected_plane=None
            turning=False
            x_dif=y_dif=0
            anti= False
            color_val_dict={114:"red",121:"yellow",98:"blue",103:"green",112:"pink",119:"white"}
            checkpoints=copy.deepcopy(true_points)
            undo=False
            undo_count=0
            redo=False
            for k,v in true_points.items():        
                true_points[k].coords3d=rotate_point(true_points[k].coords3d,0,2,45)
                true_points[k].coords3d=rotate_point(true_points[k].coords3d,2,1,45)
        if celebrating:
            for i in range(particles):
                pygame.draw.line(screen,(255,255,0),clbrt(particle_rects[i].center),clbrt(line_ends[i]),5)
                pygame.draw.line(screen,(255,255,255),clbrt(particle_rects[i].center),clbrt(line_ends[i]),3)
                screen.blit(particle_images[i],clbrt(list(particle_rects[i].topleft)))
                particle_rects[i].centerx+=particle_velocities[i][0]
                particle_rects[i].centery+=particle_velocities[i][1]
                if dist(particle_rects[i].center,line_ends[i])>200:
                    line_ends[i][0]+=particle_velocities[i][0]
                    line_ends[i][1]+=particle_velocities[i][1]
            for i in range(particles):
                if abs(particle_rects[i].centerx)>screenx/2+200.0 or abs(particle_rects[i].centery)>screeny/2+200.0:
                    pass
                else:
                    break
            else:
                celeb_count+=1
                if celeb_count>1:
                    celebrating=False
                    celeb_count=0
                for i in range(particles):
                    particle_rects[i].center=(0,0)
                    line_ends[i]=[0,0]
        true_mouse_pos=magnify(list(pygame.mouse.get_pos()),True,1/magnification)
        tick+=1
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit()
            if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                if point_in_rect(pygame.mouse.get_pos(),shuffle_rect) and not solve_ and not turning and not mix:
                        mix=True
                        cube_shuffeled=True
                        mixnumber=25
                if point_in_rect(pygame.mouse.get_pos(),solve_rect) and len(record_of_moves)>0 and not solve_ and not turning and not mix:
                    solve_=True
                    solvelen=len(record_of_moves)
                    endlen=len(record_of_moves)+1
                    while solvelen != endlen:
                        solvelen=len(record_of_moves)
                        removal=[]
                        if len(record_of_moves)>1:
                            for i in range(len(record_of_moves)-1):
                                if i in removal:
                                    continue
                                if record_of_moves[i][0]==record_of_moves[i+1][0] and record_of_moves[i][1]==-record_of_moves[i+1][1]:
                                    removal.append(i)
                                    removal.append(i+1)
                            new_record=[]
                            for i in range(len(record_of_moves)):
                                if i not in removal:
                                    new_record.append(record_of_moves[i])
                            record_of_moves=new_record[:]
                        if len(record_of_moves)>2:
                            addition=[]
                            removal=[]
                            for i in range(len(record_of_moves)-2):
                                if i in removal:
                                    continue
                                if record_of_moves[i]==record_of_moves[i+1]==record_of_moves[i+2]:
                                    removal.append(i)
                                    removal.append(i+1)
                                    removal.append(i+2)
                                    addition.append(i)
                                new_record=[]
                            for i in range(len(record_of_moves)):
                                if i not in removal:
                                    new_record.append(record_of_moves[i])
                                elif i in addition:
                                    new_record.append([record_of_moves[i][0],-record_of_moves[i][1]])
                            record_of_moves=new_record[:]
                        endlen=len(record_of_moves)
            if event.type==pygame.MOUSEBUTTONDOWN:
                if (not menu_moving) and menu_activated and event.button==1 and not turning and not solve_ and not mix:
                    if point_in_rect(mouse_pos1,inverted_mouse_switch_rect):
                        inverted_mouse=not(inverted_mouse)
                    if point_in_rect(mouse_pos1,side_mode_switch_rect) or point_in_rect(mouse_pos1,center_mode_switch_rect) :
                        side_mode=not(side_mode)
                        center_mode=not(center_mode)
                    if point_in_rect(mouse_pos1,keyboard_mode_switch_rect):
                        keyboard_mode=not(keyboard_mode)
                    if point_in_rect(mouse_pos1,shaders_switch_rect):
                        shaders=not(shaders)
                    if point_in_rect(mouse_pos1,hollow_switch_rect):
                        tob=1
                    if point_in_rect(mouse_pos1,black_switch_rect):
                        tob=3
                    if point_in_rect(mouse_pos1,solid_switch_rect):
                        tob=2
                    if point_in_rect(mouse_pos1,senstivity_plus_rect):
                        senstivity/=2**0.5
                    if point_in_rect(mouse_pos1,senstivity_minus_rect):
                        senstivity*=2**0.5
                    if point_in_rect(mouse_pos1,mute_switch_rect):
                        mute=not(mute)
                    if tob==1:
                        show_infaces=False
                        curtain=False
                    elif tob==2:
                        show_infaces=True
                        curtain=False
                    else:
                        thickness=0
                        show_infaces=True
                        curtain=True
                    if point_in_rect(mouse_pos1,brightness_plus_rect):
                        brightness+=25
                    if point_in_rect(mouse_pos1,brightness_minus_rect):
                        brightness-=50
                    if point_in_rect(mouse_pos1,contrast_plus_rect):
                        contrast+=0.2
                    if point_in_rect(mouse_pos1,contrast_minus_rect):
                        contrast-=0.2
                    if point_in_rect(mouse_pos1,magnification_plus_rect):
                        magnification*=2**0.5
                    if point_in_rect(mouse_pos1,magnification_minus_rect):
                        magnification/=2**0.5
                    if point_in_rect(mouse_pos1,speed_plus_rect):
                        speed_index+=1
                    if point_in_rect(mouse_pos1,speed_minus_rect):
                        speed_index-=1
                    if speed_index>=speed_len:
                        speed_index=speed_len-1
                    if speed_index<0:
                        speed_index=0
                    speed=speed_list[speed_index]
                    if point_in_rect(mouse_pos1,spr_plus_rect):
                        spr+=10
                        reset_cube=True
                        break
                    if point_in_rect(mouse_pos1,spr_minus_rect):
                        spr-=10
                        reset_cube=True
                        break
                    if point_in_rect(mouse_pos1,s_plus_rect):
                        s+=10
                        reset_cube=True
                        break
                    if point_in_rect(mouse_pos1,s_minus_rect):
                        s-=10
                        reset_cube=True
                        break
                if (not menu_activated) and event.button==1 and point_in_plane(mouse_pos1,menu_icon_rect.topleft,menu_icon_rect.bottomright):
                    menuxvelocity=20
                    menu_activated=True
                    menu_moving=True
                if menu_activated and event.button==1 and dist(mouse_pos1,(371,27))<30:
                    menuxvelocity=-20
                    menu_activated=False
                    menu_moving=True
                if event.button==1 and highest_plane!=None and highest_plane in center_faces and not turning and selection_mode:
                    color_turn = face_to_color[get_alpha(highest_plane)]
                    turning=True
                    turn=0
                    anti=False
                    if anti :
                        dirxn=-1
                    else:
                        dirxn=1
                    if color_turn in "pinkyellowgreen":
                        dirxn=-dirxn
                    if not mute:
                        woosh.play()
                    record_of_moves.append([color_turn,dirxn])
                elif event.button==1 and highest_plane!=None and not turning and side_mode:
                    corrections=find_correction()
                    i=highest_plane
                    i=(i.strip()).split(" ")
                    coords1=[]
                    for j in i:
                        k=j
                        true_points[k].coords3d=rotate_point(true_points[k].coords3d,0,1,corrections[0])
                        true_points[k].coords3d=rotate_point(true_points[k].coords3d,0,2,corrections[1])
                        true_points[k].coords3d=rotate_point(true_points[k].coords3d,0,1,corrections[2])
                        coords1.append(true_points[j].coords3d)
                        true_points[k].coords3d=rotate_point(true_points[k].coords3d,0,1,-corrections[2])
                        true_points[k].coords3d=rotate_point(true_points[k].coords3d,0,2,-corrections[1])
                        true_points[k].coords3d=rotate_point(true_points[k].coords3d,0,1,-corrections[0])
                    for k in range(3):
                        if round(coords1[0][k],5)==round(coords1[1][k],5)==round(coords1[2][k],5)==round(coords1[3][k],5):
                            extension=coords1[0][k]
                            face_axis=k
                            break
                    faceid=(round(extension,5),face_axis)
                    color_turn=id_dict[faceid]
                    turning=True
                    if not mute:
                        if dirxn==-1:
                            woosh.play()
                        else:
                            shoow.play()
                    turn=0
                    face=color_to_face[color_turn]
                    avg1=0
                    for i in (face.strip()).split(" "):
                        avg1+=true_points[i].coords2d[0]
                    avg1=avg1/4
                    if true_mouse_pos[0]>avg1:
                        anti=False
                    else:
                        anti=True
                    if anti :
                        dirxn=-1
                    else:
                        dirxn=1
                    if color_turn in "pinkyellowgreen":
                        dirxn=-dirxn
                    dirxn=-dirxn
                    record_of_moves.append([color_turn,dirxn])
                elif event.button==1:
                    button1pressed=True
                if event.button==3 and not turning and selection_mode and highest_plane!=None and highest_plane in center_faces:
                    color_turn = face_to_color[get_alpha(highest_plane)]
                    turning=True
                    if not mute:
                        shoow.play()
                    turn=0
                    anti=True
                    if anti :
                        dirxn=-1
                    else:
                        dirxn=1
                    if color_turn in "pinkyellowgreen":
                        dirxn=-dirxn
                    record_of_moves.append([color_turn,dirxn])
            if event.type==pygame.MOUSEBUTTONUP:
                if event.button==1:
                    button1pressed=False
            if event.type==pygame.KEYDOWN and keyboard_mode:
                if event.key in [1073742048,1073742049,1073742050]:
                    anti=True
                if event.key in color_val_dict.keys() and not turning:
                    color_turn = color_val_dict[event.key]
                    turning=True
                    turn=0
                    if not mute:
                        if anti:
                            shoow.play()
                        else:
                            woosh.play()
                    if anti :
                        dirxn=-1
                    else:
                        dirxn=1
                    if color_turn in "pinkyellowgreen":
                        dirxn=-dirxn
                    record_of_moves.append([color_turn,dirxn])
            if event.type==pygame.KEYUP:
                if event.key in [1073742048,1073742049,1073742050]:
                    anti=False
        if resetting:
            resetting=False
            continue
        if not selection_mode:
            selected_color=None
            selected_plane=None
        if button1pressed and not turning:
            x_dif=(mouse_pos[0]-true_mouse_pos[0])/senstivity
            y_dif=(mouse_pos[1]-true_mouse_pos[1])/senstivity
            if inverted_mouse:
                x_dif=-x_dif
                y_dif=-y_dif
            xrecord+=x_dif
            yrecord+=y_dif
        else:
            x_dif=y_dif=0
        for k,v in true_points.items():
            ymove=mod(y_dif,360)
            xmove=mod(x_dif,360)
            i=v.coords3d
            i=rotate_point(i,1,2,ymove)
            i=rotate_point(i,0,2,xmove)
            true_points[k].coords3d=i
        mouse_pos=true_mouse_pos
        for k,v in true_points.items():
            true_points[k].coords2d=clbrt(project(true_points[k].coords3d))
        depths={}
        for i in planes:
            depths[i]=avg_depth(i,true_points)
        blit_face_depths=(sorted(depths.values()))
        blitting_faces=[]
        mouse_in_planes=[]
        for i in planes:
            i2=i
            verticesin=[]
            for j in (i2.strip()).split(" "):
                j.strip()
                verticesin.append(true_points[j].coords2d)
            if point_inside(true_mouse_pos,verticesin):
                mouse_in_planes.append(i)
        highest_plane=None
        if len(mouse_in_planes)>0:
            highest_plane=mouse_in_planes[0]
            for i in mouse_in_planes:
                if avg_depth(i,true_points)<avg_depth(highest_plane,true_points):
                    highest_plane=i
        if highest_plane not in out_faces:
            highest_plane=None
        for i in blit_face_depths:
            blitting_faces+=get_key(i,depths)
        blitting_faces=reversed(blitting_faces)
        for i in blitting_faces:
            if show_infaces or i in out_faces:
                i2=i
                depth=avg_depth(i,true_points)
                polyvertices=[]
                i=i.strip()
                for k in i.split(" "):
                    polyvertices.append(true_points[k].coords2d)
                color=copy.deepcopy(colors[i+" "])
                for j in range(len(color)):
                    if shaders:
                        color[j]-=int((depth-brightness)/contrast)
                        if color[j]>255:
                            color[j]=255
                        if color[j]<0:
                            color[j]=0
                if i2 not in out_faces and curtain:
                    pygame.draw.polygon(screen, [0,0,0], bulk_magnify(polyvertices,True,magnification), 0)
                else:
                    if i2 == highest_plane : 
                        for i in range(len(color)):
                            color[i]+=highlight
                            if color[i]>255:
                                color[i]=255
                    pygame.draw.polygon(screen, color, bulk_magnify(polyvertices,True,magnification), 0)
                i2=polyvertices[0]
        if solve_ and not turning and not mix:
            color_turn = record_of_moves[solvelen-1][0]
            turning=True
            if not mute:
                if dirxn==-1:
                    woosh.play()
                else:
                    shoow.play()
            turn=0
            dirxn = (record_of_moves[solvelen-1][1]) * (-1)
            solvelen-=1
            if solvelen-1==-1:
                solve_=False
        if not solve_ and not turning and mix:
            color_turn = random.sample(["red","blue","green","yellow","pink","white"],6)[0]
            turning=True
            turn=0
            dirxn = random.sample([1,-1],2)[0]
            if not mute:
                if dirxn==-1:
                    woosh.play()
                else:
                    shoow.play()
            mixnumber-=1
            record_of_moves.append([color_turn,dirxn])
            if mixnumber==0:
                mix=False
        if turning and turning !=90:
            turn+=speed
            turn_face(color_turn,speed*dirxn)
            if turn ==90:
                turning=False
        corr=find_correction()
        breaker = False
        for i in range(27):
            if i not in [2,3,1,6,18,9]:
                for j in "abcdefgh":
                    temp_point=copy.deepcopy(true_points[j+str(i)].coords3d)
                    temp_point=rotate_point(temp_point,0,1,corr[0])
                    temp_point=rotate_point(temp_point,0,2,corr[1])
                    temp_point=rotate_point(temp_point,0,1,corr[2])
                    for k in range(3):
                        if round(checkpoints[j+str(i)].coords3d[k],4)==round(temp_point[k],4):
                            pass
                        else:
                            breaker=True
                            solved=False
                            break
                    if breaker:
                        break
                if breaker:
                    break
        else:
            solved=True
        if solved and len(record_of_moves)>10:
            celebrating = True
        if solved:
            record_of_moves=[]
        if menu_moving:
            menu_rect.centerx+=menuxvelocity
        if menu_moving and (menu_rect.right<0 or menu_rect.left>0):
            menu_moving=False
        if menu_rect.right<menu_icon_rect.right:
            screen.blit(menu_icon,menu_icon_rect)
        screen.blit(menu,menu_rect)

        if inverted_mouse:
            menu.blit(inverted_mouse_switch_on,inverted_mouse_switch_rect)
        else:
            menu.blit(inverted_mouse_switch_off,inverted_mouse_switch_rect)
        if center_mode:
            side_mode=False
            menu.blit(center_mode_switch_on,center_mode_switch_rect)
            menu.blit(side_mode_switch_off,side_mode_switch_rect)
        else:
            side_mode=True
            menu.blit(center_mode_switch_off,center_mode_switch_rect)
            menu.blit(side_mode_switch_on,side_mode_switch_rect)
        if keyboard_mode:
            menu.blit(keyboard_mode_switch_on,keyboard_mode_switch_rect)
        else:
            menu.blit(keyboard_mode_switch_off,keyboard_mode_switch_rect)
        if shaders:
            menu.blit(shaders_switch_on,shaders_switch_rect)
        else:
            menu.blit(shaders_switch_off,shaders_switch_rect)
        if tob==1:
            menu.blit(black_switch_off,black_switch_rect)
            menu.blit(solid_switch_off,solid_switch_rect)
            menu.blit(hollow_switch_on,hollow_switch_rect)
        if tob==2:
            menu.blit(black_switch_off,black_switch_rect)
            menu.blit(solid_switch_on,solid_switch_rect)
            menu.blit(hollow_switch_off,hollow_switch_rect)
        if tob==3:
            menu.blit(black_switch_on,black_switch_rect)
            menu.blit(solid_switch_off,solid_switch_rect)
            menu.blit(hollow_switch_off,hollow_switch_rect)
        menu.blit(senstivity_plus,senstivity_plus_rect)
        menu.blit(senstivity_minus,senstivity_minus_rect)
        menu.blit(brightness_plus,brightness_plus_rect)
        menu.blit(brightness_minus,brightness_minus_rect)
        menu.blit(contrast_plus,contrast_plus_rect)
        menu.blit(contrast_minus,contrast_minus_rect)
        menu.blit(magnification_plus,magnification_plus_rect)
        menu.blit(magnification_minus,magnification_minus_rect)
        menu.blit(speed_plus,speed_plus_rect)
        menu.blit(speed_minus,speed_minus_rect)
        menu.blit(spr_plus,spr_plus_rect)
        menu.blit(spr_minus,spr_minus_rect)
        menu.blit(s_plus,s_plus_rect)
        menu.blit(s_minus,s_minus_rect)
        screen.blit(shuffle_button,shuffle_rect)
        screen.blit(solve_button,solve_rect)
        if not mute:
            menu.blit(mute_switch_on,mute_switch_rect)
        else:
            menu.blit(mute_switch_off,mute_switch_rect)
        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)
asyncio.run(main())