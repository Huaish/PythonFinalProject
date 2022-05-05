import pygame
import random

colors = {"white" : (255, 255, 255), "black" : (0, 0, 0), "red" : (255, 0, 0), "green" : (0, 255, 0), "blue heavy" : ( 0, 0, 255 ), 
          "blue light" : (125, 185, 222), "gray" : (189, 192, 186), "purple light" : (180, 129, 187), "purple heavy" : (102, 50, 124)}
screen_width = 1250
screen_height = 750
font_size = 25
dialog_x = 1070
dialog_y = 310
pygame.font.init()
pygame.display.init()
font = pygame.font.Font("Font/setofont.ttf", font_size)
role = {}
file = open('Text/story01/管家.txt', 'r',encoding='utf8')
outputtxt = file.readline()[:-1].split(':')[1]
time = pygame.time.get_ticks()
room = [0, 0, 0, 0, 0, 1]
room_table = ['三女兒', '二哥', '大哥', '律師', '富豪', '管家']
hint_table = {1 : '二哥', 2 : '大哥', 3 : '三女兒', 4 : '律師', 5 : '管家'}
hint_answer = ''
player_name = ''

class Screen():
    global screen_width, screen_height
    def __init__(self, title, width = screen_width, height = screen_height, fill = colors["white"]):
        self.title = title
        self.width = width
        self.height = height
        self.fill = fill
        self.current = False
    
    # Current: recent status of the screen
    def setCurrent(self, _current):
        pygame.display.set_caption(self.title)
        self.current = _current
        self.screen = pygame.display.set_mode((self.width, self.height))
    
    def getCurrent(self):
        return self.current
    
    def screenUpdate(self):
        if(self.current):
            self.screen.fill(self.fill)
            
    def returnScreen(self):
        return self.screen

screen = Screen("Screen1")

class Button():
    def __init__(self, x, y, width, height, focus_background_color = colors['red'], 
                 background_color = colors['red'], font = font, font_size = 2, font_color = colors['red'] ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.focus_background_color = focus_background_color
        self.background_color = background_color
        self.font_size = font_size
        self.font_color = font_color
        self.current = False
        self.buttonf = font
    
    def showText(self, text, transparent = False):
        if not transparent:
            if self.current:
                pygame.draw.rect(screen.returnScreen(), self.focus_background_color, (self.x, self.y, self.width, self.height) )
            else:
                pygame.draw.rect(screen.returnScreen(), self.background_color, (self.x, self.y, self.width, self.height) )

        textsurface = self.buttonf.render(text, True, self.font_color)
        screen.returnScreen().blit(textsurface, ((self.x + (self.width/2) - (self.font_size)*(len(text)/2), 
                                                  (self.y + (self.height/2) - (self.font_size/2) - 4) )))

    def showButton(self, img = '', txt = '', txt_x = 0, txt_y = 0, txt_width = 0, txt_height = 0):
        if img:
            img = pygame.image.load(img).convert_alpha()
            img = pygame.transform.scale(img, (self.width, self.height))
            screen.returnScreen().blit(img, (self.x, self.y))
        if txt:
            textsurface = self.buttonf.render(txt, True, colors['black'])
            screen.returnScreen().blit(textsurface, ((txt_x + (txt_width/2) - (font_size)*(len(txt)/2), 
                                                      (txt_y + (txt_height/2) - (font_size/2) - 4) )))

    def showDialogBox(self, text, is_narrator):
        img = pygame.image.load('Image/Dialog_Box.png').convert_alpha()
        img = pygame.transform.scale(img, (screen_width, 300))
        if(self.current):
            screen.returnScreen().blit(img, (0, screen_height - 325))
        
        textsurface = self.buttonf.render(text, True, self.font_color)
        if is_narrator:
            screen.returnScreen().blit(textsurface, ((619 - (self.font_size)*(len(text)/2), (self.y + (self.height/2) - 25 - (self.font_size/2) - 4) )))
        else:
            screen.returnScreen().blit(textsurface, ((719 - (self.font_size)*(len(text)/2), (self.y + (self.height/2) - 25 - (self.font_size/2) - 4) )))
        
    
    def setCurrent(self, current):
        self.current = current

    def getCurrent(self):
        return self.current

    def focusCheck(self, mousepos, mouseclick):
        if( mousepos[0] >= self.x and mousepos[0] <= self.x + self.width and 
           mousepos[1] >= self.y and mousepos[1] <= self.y + self.height ):
            self.current = True
            return mouseclick[0]
        else:
            self.current = False
            return False
    
class Item(Button):
    def __init__(self, _name, _x, _y, item_coordinate = [], _visible = True ):
        self.name = _name
        self.img_real = pygame.image.load("Image/real_character/" + _name + '.png' ).convert_alpha()
        self.img_real = pygame.transform.scale( self.img_real, (138, 184))
        self.img_pixel = pygame.image.load("Image/pixel_character/" + _name + '.png' ).convert_alpha()
        self.img_pixel = pygame.transform.scale( self.img_pixel, (60, 80))
        self.item = []
        itr = 0
        for i in item_coordinate:
            tmp = Button( i[0], i[1], 60, 80, colors["white"], colors["blue heavy"], font, font_size, colors["black"] )
            self.item.append( ['Image/Scene/Scene2/' + _name + '房間物品/item0' + str(itr) + '.png', 
                               i[0], i[1], tmp, 'roomItem/' + _name + '/item0' + str(itr) + '.txt' ] )
            itr += 1
            
        self.x = _x
        self.y = _y
        self.width = 60
        self.height = 80
        self.visible = _visible

    def get_image_big(self):
        return self.img_real

    def get_image_small(self):
        return self.img_pixel

    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def set_x(self, _x):
        self.x = _x
    def set_y(self, _y):
        self.y = _y
    def showRole(self, width, height):
        if not self.visible:
            return
        img = pygame.image.load("Image/pixel_character/" + self.name + '.png' ).convert_alpha()
        img = pygame.transform.scale( self.img_pixel, (width, height))
        self.width = width
        self.height = height
        screen.returnScreen().blit( img, (self.x, self.y))

    def show_room_item(self):
        for i in self.item:
            img = pygame.image.load( i[0] ).convert_alpha()
            img = pygame.transform.scale( img, (60, 80))
            screen.returnScreen().blit( img, (i[1], i[2]))

    def Murmur(self):
        if not self.name == '管家':
            return
        global file
        murmur = Button(self.x - 30, self.y - 20, 50, 10, colors['white'], colors['white'], font, font_size // 2, colors['black'])
        temp_time = pygame.time.get_ticks()
        global time, outputtxt
        if temp_time - time > 1500:
            time = temp_time
            outputtxt = file.readline()[:-1]
            if not outputtxt:
                file.seek(0)
                outputtxt = file.readline()[:-1]
            outputtxt = outputtxt.split(':')[1]
        murmur.showText(outputtxt, True)
            
def Dialog(txt_file, scene):
    dialogBox = Button(0, screen_height - 200, screen_width, 200, colors['gray'], colors['gray'], font, font_size, colors['black'])
    dialogBox.setCurrent(True)
    name = Button(28, 541, 72, 35, colors['gray'], colors['gray'], font, font_size, colors['black'])
    file = open( 'Text/' + txt_file, "r",encoding='utf8')
    global player_name
    inputtxt = file.readline()[:-1].split(':')
    if 'XXX' in inputtxt[1]:
        inputtxt[1] = inputtxt[1].replace("XXX", player_name)
    is_narrator = False
    if inputtxt[0] == '旁白':
        is_narrator = True
    
    while True:
        for event in pygame.event.get():
            screen.screenUpdate()
            screen.returnScreen().blit(scene, (0, 0))
            keys = pygame.key.get_pressed()

            if screen.getCurrent():
                if dialogBox.getCurrent():
                    dialogBox.showDialogBox( inputtxt[1], is_narrator )
                    
                    if inputtxt[0] == '旁白':
                        img = ''
                    else:
                        if inputtxt[0] == '玩家':
                            print( txt_file )
                        img = role[inputtxt[0]].get_image_big()

                    if img:
                        screen.returnScreen().blit(img, (100, 517))
                        name.showText(inputtxt[0], False)
                    if event.type == pygame.KEYDOWN and keys[pygame.K_SPACE]: 
                        inputtxt = file.readline()[:-1]
                        if not inputtxt:
                            file.close()
                            return
                        inputtxt = inputtxt.split(':')
                        if 'XXX' in inputtxt[1]:
                            inputtxt[1] = inputtxt[1].replace("XXX", player_name)
                        if inputtxt[0] == '旁白':
                            is_narrator = True
                        else:
                            is_narrator = False
                                          
        pygame.display.update()

def Scene00():
    scene = pygame.image.load('Image/Scene/宅邸(調色).jpg').convert_alpha()
    scene = pygame.transform.scale(scene, (screen_width, screen_height))
    # startButton = Button(550, 400, 150, 50, colors["blue light"], colors["purple light"], font, font_size, colors["black"] )
    # aboutButton = Button(550, 500, 150, 50, colors["blue light"], colors["purple light"], font, font_size, colors["black"] )
    # quitButton = Button(550, 600, 150, 50, colors["blue light"], colors["purple light"], font, font_size, colors["black"] )
    startButton = Button(500, 400, 259, 75, colors["red"], colors["red"], font, font_size, colors["red"] )
    aboutButton = Button(500, 500, 259, 75, colors["red"], colors["red"], font, font_size, colors["red"] )
    quitButton = Button(500, 600, 259, 75, colors["red"], colors["red"], font, font_size, colors["red"] )
    # sButton_text = Button(510, 409, 240, 70, colors["black"], colors["black"], font, font_size, colors["black"] )
    # aButton_text = Button(510, 509, 240, 70, colors["black"], colors["black"], font, font_size, colors["black"] )
    # qButton_text = Button(510, 609, 240, 70, colors["black"], colors["black"], font, font_size, colors["black"] )
    startButton.setCurrent(True)
    aboutButton.setCurrent(True)
    quitButton.setCurrent(True)

    while True:
        for event in pygame.event.get():
            screen.returnScreen().blit(scene, (0, 0))
            
            startButton.showButton( 'Image/Button_Img00.png', '開始', 510, 409, 240, 70 )
            aboutButton.showButton( 'Image/Button_Img00.png', '關於', 510, 509, 240, 70 )
            quitButton.showButton( 'Image/Button_Img00.png', '退出', 510, 609, 240, 70 )
            
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = [False, False, False]
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = pygame.mouse.get_pressed()
                
            return_start = startButton.focusCheck(mouse_pos, mouse_click)
            # sButton_text.showButton( '開始', True )
            if ( not return_start ) and startButton.getCurrent():
                indicate_start = Button(500, 400, 259, 75, colors["gray"], colors["gray"], font, font_size, colors["black"] )
                indicate_start.showButton( 'Image/Button_Img01.png', '開始', 510, 409, 240, 70 )
            elif return_start:
                return 'start'
            
            return_about = aboutButton.focusCheck(mouse_pos, mouse_click)
            # aButton_text.showButton( '關於', True )
            if ( not return_about ) and aboutButton.getCurrent():
                indicate_about = Button(500, 500, 259, 75, colors["gray"], colors["gray"], font, font_size, colors["black"] )
                indicate_about.showButton( 'Image/Button_Img01.png', '關於', 510, 509, 240, 70 )
            elif return_about:
                return 'about'
            
            return_quit = quitButton.focusCheck(mouse_pos, mouse_click)
            # qButton_text.showButton( '退出', True )
            if ( not return_quit ) and quitButton.getCurrent():
                indicate_quit = Button(500, 600, 259, 75, colors["gray"], colors["gray"], font, font_size, colors["black"] )
                indicate_quit.showButton( 'Image/Button_Img01.png', '退出', 510, 609, 240, 70 )
            elif return_quit:
                return 'quit'
            
            pygame.display.update()

def Scene0():
    for i in range(0,17):
        scene = pygame.image.load('Image/Scene/Scene0/0-' + str(i) + '.jpg').convert_alpha()
        scene = pygame.transform.scale(scene, (screen_width, screen_height))
        Dialog( 'story00/00-' + str(i) + '.txt', scene )

def Scene_about():
    scene_about = pygame.image.load('Image/Scene/About/about.jpeg').convert_alpha()
    scene_about = pygame.transform.scale(scene_about, (screen_width, screen_height))
    cursor = pygame.image.load('Image/Keyboard/cursor.PNG').convert_alpha()
    cursor = pygame.transform.scale(cursor, (80, 100))
    space = pygame.image.load('Image/Keyboard/space.PNG').convert_alpha()
    space = pygame.transform.scale(space, (270, 45))
    returnButton = Button(1100, 700, 150, 50, colors["blue light"], colors["purple light"], font, font_size, colors["black"] )
    cursortxt_1 = Button(700, 210, 150, 50, colors["blue light"], colors["purple light"], font, font_size, colors["black"] )
    cursortxt_2 = Button(600, 260, 150, 50, colors["blue light"], colors["purple light"], font, font_size, colors["black"] )
    spacetxt = Button(650, 400, 150, 50, colors["blue light"], colors["purple light"], font, font_size, colors["black"] )
    text_cursor_1 = '游標：用來點擊場景裡景里的角色、物件(例如：門、房間裡的器具等)，'
    text_cursor_2 = '以及按鈕(例如：右下角的「返回」鍵)。'
    text_space = '空白鍵：在遊戲裡遇到對話框時，按一下可以切換到下一個對話框。'
    Dialog( 'about/introduction.txt', scene_about)
    
    while True:
        for event in pygame.event.get():
            screen.returnScreen().blit(scene_about, (0, 0))
            screen.returnScreen().blit(cursor, (150, 200))
            screen.returnScreen().blit(space, (50, 400))
            cursortxt_1.showButton( text_cursor_1, True)
            cursortxt_2.showButton( text_cursor_2, True)
            spacetxt.showButton( text_space, True)
            
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = [False, False, False]
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = pygame.mouse.get_pressed()        
            returnm = returnButton.focusCheck(mouse_pos, mouse_click)
            returnButton.showButton( '返回' )
            if returnm:
                return
            pygame.display.update()

def Scene1():
    scene = pygame.image.load('Image/Scene/宅邸內側.jpg').convert_alpha()
    scene = pygame.transform.scale(scene, (screen_width, screen_height))
    returnButton = Button(1100, 700, 150, 50, colors["blue light"], colors["purple light"], font, font_size, colors["black"] )
    
    while True:
        for event in pygame.event.get():
            screen.returnScreen().blit(scene, (0, 0)) 
            width, height = 60, 80
            for i in role:
                role[i].Murmur()
                role[i].showRole( width, height)
                width += 9
                height += 12
                
                mouse_pos = pygame.mouse.get_pos()
                mouse_click = [False, False, False]
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_click = pygame.mouse.get_pressed()

                if role[i].focusCheck(mouse_pos, mouse_click):
                    Dialog( 'story01/'+ str(i) + '.txt', scene )
            
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = [False, False, False]
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = pygame.mouse.get_pressed()        
            returnm = returnButton.focusCheck(mouse_pos, mouse_click)
            returnButton.showText( '離開大廳' )
            if returnm:
                return
            pygame.display.update()

def Scene1_5():
    for i in range(0,6):
        scene = pygame.image.load('Image/Scene/Scene1.5/1.5-' + str(i) + '.png').convert_alpha()
        scene = pygame.transform.scale(scene, (screen_width, screen_height))
        Dialog( 'story01.5/01.5-' + str(i) + '.txt', scene )
   
def Scene2():

    role['律師'].set_x(120)
    role['律師'].set_y(300)
    role['二哥'].set_x(250)
    role['二哥'].set_y(300)
    role['三女兒'].set_x(850)
    role['三女兒'].set_y(300)
    role['大哥'].set_x(900)
    role['大哥'].set_y(300)


    scene = pygame.image.load('Image/Scene/Scene2/走廊.png' ).convert_alpha()
    scene = pygame.transform.scale(scene, (screen_width, screen_height))

    Dialog( 'story02/story02-0.txt', scene )
    Room( '承包商' )
    
    door = []
    global room_table
    for i in range(6):
        temp = Button(200 * i + 50, 200, 150, 350, colors["red"], colors["red"], font, font_size, colors["red"] )
        temp.setCurrent(True)
        door.append(temp)

    findKey = False
    global room    
    while True:
        for event in pygame.event.get():
            screen.returnScreen().blit(scene, (0, 0))
            for i in range(0, len(door)) :
                door[i].showButton( 'Image/Scene/Scene2/門.png' )
                
                mouse_pos = pygame.mouse.get_pos()
                mouse_click = [False, False, False]
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_click = pygame.mouse.get_pressed()
                    
                checker = door[i].focusCheck(mouse_pos, mouse_click)

                if ( not checker ) and door[i].getCurrent():
                    indicate_box = Button(mouse_pos[0], mouse_pos[1] - 20, 50, 20, colors["gray"], 
                                          colors["gray"], font, font_size, colors["black"] )
                    indicate_box.showText( room_table[i] + '的房間', True )
                
                elif checker:
                    if room[i] == 1:
                        Dialog( 'story02/empty.txt', scene)
                    elif room_table[i] == '二哥' and not findKey:
                        Dialog( 'story02/02-1(Lock).txt', scene)
                    else:
                        room[i] = 1
                        if room_table[i] == '富豪':
                            return
                        if room_table[i] == '大哥':
                            findKey = True
                        
                        
                        Room( room_table[i] )
                        pygame.display.update()
                
            pygame.display.update()

def Room(name):
    scene = pygame.image.load('Image/Scene/door_open/' + name + '.jpg').convert_alpha()
    scene = pygame.transform.scale(scene, (screen_width, screen_height))
    returnButton = Button(1100, 700, 150, 50, colors["blue light"], colors["purple light"], font, font_size, colors["black"] )

    while True:
        for event in pygame.event.get():
            screen.returnScreen().blit(scene, (0, 0))
            role[name].show_room_item()
            role[name].showRole(300, 400)

            mouse_pos = pygame.mouse.get_pos()
            mouse_click = [False, False, False]
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = pygame.mouse.get_pressed()

            for i in role[name].item:
                if i[3].focusCheck(mouse_pos, mouse_click):
                    Dialog( i[4], scene )
            
            if role[name].focusCheck(mouse_pos, mouse_click):
                Dialog( 'story02/' + name + '.txt', scene)
            
            returnm = returnButton.focusCheck(mouse_pos, mouse_click)
            returnButton.showText( '離開房間' )
            if returnm:
                return
            pygame.display.update()
    
def Scene3():
    scene = pygame.image.load('Image/Scene/富豪房間.jpg').convert_alpha()
    scene = pygame.transform.scale(scene, (screen_width, screen_height))

    picture = []
    hash_table = ['富豪的肖像畫', '富豪跟遺孀的合照', '富豪與兒子們合照']
    for i in range(3):
        temp = Button( 300 * i + 185, screen_height / 2 - 50, 280, 210, colors["red"], colors["red"], font, font_size, colors["red"] )
        temp.setCurrent(True)
        picture.append(temp)

    while True:
        for event in pygame.event.get():
            screen.returnScreen().blit(scene, (0, 0))
            for i in range(0, len(picture)) :
                picture[i].showButton( 'Image/Scene/Scene3/' + hash_table[i] + '(回憶).png' )
                mouse_pos = pygame.mouse.get_pos()
                mouse_click = [False, False, False]
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_click = pygame.mouse.get_pressed()
                    
                checker = picture[i].focusCheck(mouse_pos, mouse_click)

                if ( not checker ) and picture[i].getCurrent():
                    indicate_box = Button(mouse_pos[0], mouse_pos[1] - 20, 50, 20, colors["gray"], 
                                          colors["gray"], font, font_size, colors["black"] )
                    indicate_box.showButton( hash_table[i], True )
                
                elif checker:
                    scene2 = pygame.image.load('Image/Scene/Scene3/picture0' + str(i)+ '.png' ).convert_alpha()
                    scene2 = pygame.transform.scale(scene2, (screen_width, screen_height))
                    Dialog( 'story03/' + hash_table[i] + '.txt' , scene2 )
                    if not hash_table[i] == '富豪的肖像畫':
                        if hash_table[i] == '富豪跟遺孀的合照':
                            room[room_table.index('三女兒')] = 1
                        else:
                            room[room_table.index('大哥')] = 1
                            room[room_table.index('二哥')] = 1
                        return
        pygame.display.update()

def Scene3_5():
    scene = pygame.image.load('Image/Scene/宅邸內側.jpg').convert_alpha()
    scene = pygame.transform.scale(scene, (screen_width, screen_height))
    empty_dialog_box = pygame.image.load('Image/Dialog_Box.png').convert_alpha()
    empty_dialog_box = pygame.transform.scale(empty_dialog_box, (screen_width, 300))
    choose_yes = Button(375, screen_height - 180, 150, 75, colors['red'], colors['red'], font, font_size, colors['black'])
    choose_no = Button(875, screen_height - 180, 150, 75, colors['red'], colors['red'], font, font_size, colors['black'])
    Dialog('story03.5/03.5-0.txt', scene)

    while True:
        for event in pygame.event.get():
            screen.returnScreen().blit(scene, (0, 0))
            screen.returnScreen().blit(empty_dialog_box, (0, screen_height - 325))
            choose_yes.showButton('是', True)
            choose_no.showButton('否', True)
            
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = [False, False, False]
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = pygame.mouse.get_pressed()
                
            if choose_no.focusCheck(mouse_pos, mouse_click):
                return False
            
            elif choose_yes.focusCheck(mouse_pos, mouse_click):
                if random.random() <= 0.25:
                    Dialog('story03.5/03.5-kill.txt', scene)
                    return True
                
                room[room_table.index('律師')] = 1
                Dialog('story03.5/03.5-normal.txt', scene)
                return False
            
            pygame.display.update()

def Scene4():
    scene = pygame.image.load('Image/Scene/宅邸內側.jpg').convert_alpha()
    scene = pygame.transform.scale(scene, (screen_width, screen_height))
    Dialog('story04/story04-0.txt', scene)
    global hint_table, hint_answer
    hint = random.randint(1, 5)
    while not room[room_table.index(hint_table[hint])]:
        hint = random.randint(1, 5)
    hint_answer = hint_table[hint]
    Dialog('story04/story04-' + str(hint) + '.txt', scene)
    Dialog('story04/story04-end.txt', scene)

def Scene5():
    scene = pygame.image.load('Image/Scene/宅邸內側.jpg').convert_alpha()
    scene = pygame.transform.scale(scene, (screen_width, screen_height))
    Dialog('story05/story05-0.txt', scene)
    while True:
        for event in pygame.event.get():
            screen.returnScreen().blit(scene, (0, 0))
            width, height = 60, 80
            for i in role:
                role[i].showRole(width, height)
                width += 9
                height += 12
                
                mouse_pos = pygame.mouse.get_pos()
                mouse_click = [False, False, False]
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_click = pygame.mouse.get_pressed()

                if role[i].focusCheck(mouse_pos, mouse_click):
                    global hint_answer
                    if str(i) == hint_answer:
                        Dialog( 'story05/story05-'+ str(i) + '.txt', scene )
                        Dialog('story05/story05-correct_end.txt', scene)
                        return
                    else:
                        Dialog('story05/story05-wrong_end.txt', scene)
                        return

            pygame.display.update()

def Scene_end():
    scene = pygame.image.load('Image/Scene/宅邸內側.jpg').convert_alpha()
    scene = pygame.transform.scale(scene, (screen_width, screen_height))
    screen.returnScreen().blit(scene, (0, 0))
    Dialog('game_over.txt', scene)

def Reinitialize():
    global file, outputtxt, time, room, hint_answer, player_name
    file.seek(0)
    outputtxt = file.readline()[:-1].split(':')[1]
    time = pygame.time.get_ticks()
    room = [0, 0, 0, 0, 0, 1]
    hint_answer = ''
    player_name = ''

def Input_name():
    scene = pygame.image.load('Image/Scene/宅邸(調色).jpg').convert_alpha()
    scene = pygame.transform.scale(scene, (screen_width, screen_height))
    clock = pygame.time.Clock()
    instruction_txt = Button(555, 560, 200, 32, colors["gray"], colors["gray"], font, font_size, colors["black"] )
    input_box = pygame.Rect(555, 600, 140, 32)
    color_inactive = colors['black']
    color_active = colors['blue heavy']
    color = color_inactive
    active = False
    done = False
    while not done:
        for event in pygame.event.get():
            screen.returnScreen().blit(scene, (0, 0))
            instruction_txt.showText('請輸入您的名字：', False)
            pygame.draw.rect(screen.returnScreen(), colors['white'], ( 555, 600, 200, 32 ) )
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                global player_name
                if active:
                    if event.key == pygame.K_RETURN:
                        return
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode

        txt_surface = font.render(player_name, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.returnScreen().blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen.returnScreen(), color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    pygame.mixer.music.load('Music/background_music.mp3')
    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.play(-1)

    # screen1 = Screen("Screen1")
    # screen2 = Screen("Screen2")
    screen.setCurrent(True)
    done = False

    role['管家'] = Item( "管家", 460, 480 )
    role['律師'] = Item( "律師", 725, 490, [[650, 470], [1020, 440]] )
    role['二哥'] = Item( "二哥", 390, 560, [[200, 600], [650, 470], [1065, 470], [600, 600]] )
    role['富豪'] = Item( "富豪", 580, 600 )
    role['三女兒'] = Item( "三女兒", 850, 570, [[770, 280], [350, 470]] )
    role['再嫁遺孀'] = Item( "再嫁遺孀", 735, 590, [[770, 280], [350, 470]] )
    role['大哥'] = Item( "大哥", 250, 590, [[60, 400], [300, 600], [625, 375]] )
    role['承包商'] = Item( "承包商", 0, 0, [[200,600],[600,600]], False )
    role['酒保'] = Item( "酒保", 0, 0, [], False )
    role['偵探'] = Item( "偵探", 0, 0, [], False )
    role['大嫂'] = Item( "大嫂", 0, 0, [], False )

    while not done:
        for event in pygame.event.get():
            if( event.type == pygame.QUIT ):
                done = True
            
            # screen1.screenUpdate()
            # screen2.screenUpdate()
            screen.screenUpdate()
            mouse_pos = pygame.mouse.get_pos()
            keys = pygame.key.get_pressed()

            mouse_click = [False, False, False]
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = pygame.mouse.get_pressed()

            if screen.getCurrent():
                screen2Button = Scene00()

                if screen2Button == 'start':
                    Input_name()
                    Scene0()
                    # screen2.setCurrent(True)
                    # screen1.setCurrent(False)
                    Scene1()
                    Scene1_5()
                    Scene2()
                    role['律師'].set_x(725)
                    role['律師'].set_y(490)
                    role['二哥'].set_x(390)
                    role['二哥'].set_y(560)
                    role['三女兒'].set_x(850)
                    role['三女兒'].set_y(570)
                    role['大哥'].set_x( 250 )
                    role['大哥'].set_y( 590 )
                    Scene3()
                    checker = Scene3_5()
                        
                    if not checker:
                        Scene4()
                        Scene5()
                        
                    Scene_end()
                    done = False
                    
                    # screen1.setCurrent(True)
                    # screen2.setCurrent(False)
                    
                    Reinitialize()
                
                elif screen2Button == 'about':
                    Scene_about()
                
                elif screen2Button == 'quit':
                    pygame.quit()
                    exit()

        pygame.display.update()

    pygame.quit()