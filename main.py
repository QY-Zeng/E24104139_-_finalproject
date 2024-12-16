import pygame
import random
from setting import *
from game import *
from home import * 
import sys


pygame.init()
pygame.font.init()        
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("遊戲")


clock = pygame.time.Clock()


# 初始化混音器 (mixer)
pygame.mixer.init()

# 載入背景音樂
pygame.mixer.music.load("Sound/background1.mp3")  
pygame.mixer.music.set_volume(0.5)  # 設定音量 (0.0 ~ 1.0)
pygame.mixer.music.play(-1)  # -1 表示無限循環播放







running = True
level = 1

def draw_text(surface, text, size, color, bold, x, y):
    font = pygame.font.Font("Font/BoutiqueBitmap9x9_Bold_1.9.ttf", size=size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surface.blit(text_surface, text_rect) 


def calculate_star_points(center, radius, inner_radius, num_points=5):   # by AI
    points = []
    angle = math.pi / 2  # 開始角度
    step = math.pi / num_points  # 角度步長

    for i in range(num_points * 2):
        if i % 2 == 0:
            r = radius  # 外圍點
        else:
            r = inner_radius  # 內部點

        x = center[0] + r * math.cos(angle)
        y = center[1] - r * math.sin(angle)  # 注意 Pygame 的 y 軸向下

        points.append((x, y))
        angle += step

    return points




home = Home()
home.game_start()


for game in home.game_group.sprites():
    if game.level == 1:
        game.play = True

while True:
    home.display_home()
    home.run = True

    
    for event in pygame.event.get():                
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:

            mouse_position = pygame.mouse.get_pos()   # 拿到滑鼠的點擊位置
            can_play = home.get_user_input(mouse_position[0],mouse_position[1])   # can_play[0] -> 滑鼠點擊位置是哪一關卡 can_play[1] -> 這一個關卡是否能玩

            if can_play[1] == True :   # can_play[1]  : true of false
                level = can_play[0] # which level
            

                for game in home.game_group.sprites():
                    if game.level == level : 
                        game.reset_game()
                        while home.run == True : # 當點擊home上面的關卡時  

                            # 遊戲關卡的頁面
                            screen.fill(BLACK)
                            pygame.draw.rect(screen, YELLOW,  (200, 30,620, 650), 0, 10)  # 背景
                            draw_text(screen,f"Level  {level}",40,BLACK, False ,SCREEN_WIDTH/2,40)
                            draw_text(screen,f"The Task:",40,BLACK, False ,SCREEN_WIDTH/2,230)   # 顯示每關關卡目標!!


                            pygame.draw.rect (screen,WHITE , (250,290,530,200),0,20)  # task的白色方框



                            for i in range(len(game.object)):
                                if(game.object[i][0] == "point"):  #通關目標達到特定分數
                                    
                                    game.draw_text(screen,f"{game.object[i][0]}:{game.object[i][1]}",24,BLACK, False ,300,320 + 60*i+50)

                                else: # 消除特定物品 
                                    
                                    
                                    ima = pygame.image.load(game.object[i][0])
                                    ima = pygame.transform.scale(ima, (TILE_SIZE, TILE_SIZE))
                                    screen.blit(ima, (300,320+60*i))
                                    game.draw_text(screen,f"* {game.object[i][1]}",24,BLACK, False ,370,320+60*i+20)


                        
                            pygame.draw.rect(screen, BLUE,  (250, 530,250, 100), 0, 10)  # home按鍵
                            pygame.draw.rect(screen, GREEN,  (530, 530,250, 100), 0, 10) # play按鍵
                        
                        
                            draw_text(screen,f"Home",40,BLACK, False ,375,560)   # home按鍵
                            draw_text(screen,f"Play",40,BLACK, False ,655,560)   # play按鍵
                            
                                
                        
                        
                            # 計算五角星頂點
                            center1 = (430, 150)  # 星星的中心點
                            center2 = (510, 150)  # 星星的中心點
                            center3 = (590, 150)  # 星星的中心點
                            outer_radius = 30   # 外圍半徑
                            inner_radius = 15    # 內部半徑
                            star_points1 = calculate_star_points(center1, outer_radius, inner_radius)
                            star_points2 = calculate_star_points(center2, outer_radius, inner_radius)
                            star_points3 = calculate_star_points(center3, outer_radius, inner_radius)
                        
                        
                            
                            if game.count_star == 0  :  
                                # 繪製星星
                                pygame.draw.polygon(screen, GRAY, star_points1)
                                pygame.draw.polygon(screen, GRAY, star_points2)
                                pygame.draw.polygon(screen, GRAY, star_points3)
                            if game.count_star == 1  :  
                                # 繪製星星
                                pygame.draw.polygon(screen, RED, star_points1)
                                pygame.draw.polygon(screen, GRAY, star_points2)
                                pygame.draw.polygon(screen, GRAY, star_points3)
                            if game.count_star == 2  :  
                                # 繪製星星
                                pygame.draw.polygon(screen, RED, star_points1)
                                pygame.draw.polygon(screen, RED, star_points2)
                                pygame.draw.polygon(screen, GRAY, star_points3)
                            if game.count_star == 3  :  
                                # 繪製星星
                                pygame.draw.polygon(screen, RED, star_points1)
                                pygame.draw.polygon(screen, RED, star_points2)
                                pygame.draw.polygon(screen, RED, star_points3)








                            pygame.display.flip()
                        
                        
                        
                        
                        
                            
                            for event in pygame.event.get():                
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                elif event.type == pygame.MOUSEBUTTONDOWN:   # 要加上判斷按 home鍵跟 play鍵 
                                    
                                   
                                    pos = pygame.mouse.get_pos()
                                    if pos[0] >=250 and pos[0]<=500 and pos[1]>=530 and pos[1]<=630 : # 點擊home鍵   
                                        home.run = False
                                    elif pos[0] >=530 and pos[0]<=780 and pos[1]>=530 and pos[1]<=630 : # 點擊Play鍵 




                                        time = pygame.time.get_ticks() 
                                        delay_time = 1000
                                    
                                        
                                        load = pygame.image.load(LOADING)
                                        load = pygame.transform.scale(load,(SCREEN_WIDTH,SCREEN_HEIGHT))
                                        
                                        
                                        
                                        while True:
                                            now = pygame.time.get_ticks()
                                            screen.blit(load, (0, 0))  # 顯示載入圖片
                                            pygame.display.update()  # 更新畫面
                            
                                            # 事件處理
                                            for event in pygame.event.get():
                                                if event.type == pygame.QUIT:
                                                    pygame.quit()
                                                    sys.exit()
                            
                                            # 檢查是否超過延遲時間
                                            if now - time > delay_time:
                                                game.run_game()
                                                break
                                                
                                        
                                        clock.tick(FPS)
                                        
                                    
                                
                                
                                        


                                if game.run == False and game.win == True:   # 此關遊戲贏了
                                    level = level + 1 

                                    for g in home.game_group.sprites():
                                        if g.level == game.level +1 :
                                            g.play = True  # 下一關可以玩了   

                                    


                                    
                                    
                                while game.run == False and game.win == False:   # 此關遊戲沒有成功通關  
                                    
                                    screen.fill(BLACK)
                                    pygame.draw.rect(screen, YELLOW,  (200, 30,620, 650), 0, 10)  # 
                                    draw_text(screen,f"Level  {game.level}",40,BLACK, False ,SCREEN_WIDTH/2,40)
                                    draw_text(screen,f"You Fail!!",40,BLACK, False ,SCREEN_WIDTH/2,230)
                            
                                    pygame.draw.rect(screen, BLUE,  (250, 530,530, 100), 0, 10)  
                                    
                            
                            
                                    draw_text(screen,f"Retry",40,BLACK, False ,515,560)
                                    
                                    
                                    # 計算五角星頂點
                                    center1 = (430, 150)  # 星星的中心點
                                    center2 = (510, 150)  # 星星的中心點
                                    center3 = (590, 150)  # 星星的中心點
                                    outer_radius = 30   # 外圍半徑
                                    inner_radius = 15    # 內部半徑
                                    star_points1 = calculate_star_points(center1, outer_radius, inner_radius)
                                    star_points2 = calculate_star_points(center2, outer_radius, inner_radius)
                                    star_points3 = calculate_star_points(center3, outer_radius, inner_radius)
                            
                            
                                    pygame.draw.polygon(screen, GRAY, star_points1)
                                    pygame.draw.polygon(screen, GRAY, star_points2)
                                    pygame.draw.polygon(screen, GRAY, star_points3)
                                        
                                    
                                    pygame.display.flip()  # 更新畫面，顯示黑屏和文字
                                    for event in pygame.event.get():                
                                        if event.type == pygame.QUIT:
                                            pygame.quit()
                                            sys.exit()
                                        elif event.type == pygame.MOUSEBUTTONDOWN:
                                            mouse_pos = pygame.mouse.get_pos()
                            
                                            if mouse_pos[0] >= 250 and mouse_pos[0] <= 780 and mouse_pos[1] >= 530 and mouse_pos[1] <= 630: # retry 
                                                level  = level
                                                game.run = True
                                                game.win = False
                                                game.reset_game()

                                                break   
                                            

                                while game.run == False and game.win == True:   # 成功通關
                                    screen.fill(BLACK)
                                    pygame.draw.rect(screen, YELLOW,  (200, 30,620, 650), 0, 10)  # 
                                    draw_text(screen,f"Level  {game.level}",40,BLACK, False ,SCREEN_WIDTH/2,40)
                                    draw_text(screen,f"You Win!!",40,BLACK, False ,SCREEN_WIDTH/2,230)
                            
                                    pygame.draw.rect(screen, BLUE,  (250, 530,250, 100), 0, 10)  
                                    pygame.draw.rect(screen, GREEN,  (530, 530,250, 100), 0, 10)
                            
                            
                                    draw_text(screen,f"Retry",40,BLACK, False ,375,560)
                                    draw_text(screen,f"Continue",40,BLACK, False ,655,560)
                                    
                            
                                    
                            
                                    # 計算五角星頂點
                                    center1 = (430, 150)  # 星星的中心點
                                    center2 = (510, 150)  # 星星的中心點
                                    center3 = (590, 150)  # 星星的中心點
                                    outer_radius = 30   # 外圍半徑
                                    inner_radius = 15    # 內部半徑
                                    star_points1 = calculate_star_points(center1, outer_radius, inner_radius)
                                    star_points2 = calculate_star_points(center2, outer_radius, inner_radius)
                                    star_points3 = calculate_star_points(center3, outer_radius, inner_radius)
                            
                            
                                    
                                    if game.count_star == 3  :  
                                        # 繪製星星
                                        pygame.draw.polygon(screen, RED, star_points1)
                                        pygame.draw.polygon(screen, RED, star_points2)
                                        pygame.draw.polygon(screen, RED, star_points3) 
                                    elif game.count_star == 2  :
                                        # 繪製星星
                                        pygame.draw.polygon(screen, RED, star_points1)
                                        pygame.draw.polygon(screen, RED, star_points2)
                                        pygame.draw.polygon(screen, GRAY, star_points3)   
                                    elif game.count_star == 1  :
                                        # 繪製星星
                                        pygame.draw.polygon(screen, RED, star_points1)
                                        pygame.draw.polygon(screen, GRAY, star_points2)
                                        pygame.draw.polygon(screen, GRAY, star_points3)
                                        
                                    # draw_text(screen,f"按下滑鼠繼續下一關",24,WHITE, False ,SCREEN_WIDTH/2,SCREEN_HEIGHT/2+20)
                                    pygame.display.flip()  # 更新畫面，顯示黑屏和文字
                                    for event in pygame.event.get():                
                                        if event.type == pygame.QUIT:
                                            pygame.quit()
                                            sys.exit()
                                        elif event.type == pygame.MOUSEBUTTONDOWN:
                                            mouse_pos = pygame.mouse.get_pos()
                            
                                            if mouse_pos[0] >= 250 and mouse_pos[0] <= 500 and mouse_pos[1] >= 530 and mouse_pos[1] <= 630: # retry 
                                                level  = level-1
                                                game.run = True
                                                game.win = False
                                                game.reset_game()

                                                break   
                                            elif mouse_pos[0] >= 530 and mouse_pos[0] <= 780 and mouse_pos[1] >= 530 and mouse_pos[1] <= 630: # continue
                                                for game in home.game_group.sprites():
                                                    if game.level == level : 
                                                        game.run = True
                                                        game.win = False
                                                        break  
                    
                                            break  
                                    
                                    
                    
                        
                                    
                                    
                                












                
                








