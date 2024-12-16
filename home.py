import pygame
import random
from setting import *
from game import *
from story import *
import sys


pygame.init()
pygame.font.init()        
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#pygame.display.set_caption("遊戲")


clock = pygame.time.Clock()







class Home(pygame.sprite.Sprite) :
    def __init__(self):
        super().__init__()
        self.game_group = pygame.sprite.Group()
        self.run = True                              # home run
        self.all_star = 0                            #計算所有的關卡獲得的星星數量 




    def game_start(self):     # 當遊戲開始時 -> 產生15個關卡
        
        # 初始化參數
        dots = 0  # 小數點的數量
        loading_text = "loading"
        level = 1 
        # 主迴圈
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
        
            # 更新邏輯
            dots = (dots + 1) % 7  # 循環顯示 0~6 個小數點
        
            # 畫面更新
            screen.fill((30, 30, 30))  # 背景顏色
            text_surface = font.render(loading_text + "." * dots, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(512, 550))
            screen.blit(text_surface, text_rect)
            pygame.display.flip()
            clock.tick(5)  # 每秒更新 5 次
            
            self.game_group.add(Game(level))
            level = level + 1 

            if level >= 16:
                """
                story = Story()
                story.story_start1()
                story.story_start2()
                story.story_start3()
                story.story_start4()
                """
                return
        
        
       

    def display_home(self):  # 顯示主畫面 -> 關卡以及星星數、切換到修復廟宇的按鍵

        screen.fill(WHITE)
    
        RECT_WIDTH = 180
        RECT_HEIGHT = 200


        
        for game in self.game_group.sprites():
            if game.level == 1 :
                self.all_star = game.count_star
            else:
                self.all_star = self.all_star  + game.count_star 


        
            
        # 繪製星星
        center1 = (60, 35)  # 星星的中心點
        outer_radius = 15   # 外圍半徑
        inner_radius = 10   # 內部半徑
        star_points1 = self.calculate_star_points(center1, outer_radius, inner_radius)
        pygame.draw.rect(screen, YELLOW, (30, 10, 120, 45))
        self.draw_text(screen,f" * {self.all_star}",30,BLACK, False ,80,20)
                        
                          
        
        pygame.draw.polygon(screen, RED, star_points1)
                                







    
        for row in range(3):  # 3 行
            for col in range(5):  # 5 列
                level = row*5 + col + 1
                 

                
                x = 30 + col * (RECT_WIDTH +10)
                y = 60 + row * (RECT_HEIGHT+10)
                

                for game in self.game_group.sprites():
                    if game.level == level:
                        
                        # 計算五角星頂點
                        center1 = (x+30, y+170)  # 星星的中心點
                        center2 = (x+90, y+170)  # 星星的中心點
                        center3 = (x+150, y+170)  # 星星的中心點
                        outer_radius = 30   # 外圍半徑
                        inner_radius = 20   # 內部半徑
                        star_points1 = self.calculate_star_points(center1, outer_radius, inner_radius)
                        star_points2 = self.calculate_star_points(center2, outer_radius, inner_radius)
                        star_points3 = self.calculate_star_points(center3, outer_radius, inner_radius)

                        
                        if game.play == True and game.win == True:  # 遊戲通關了

                            
                            pygame.draw.rect(screen, YELLOW, (x, y, RECT_WIDTH, RECT_HEIGHT))
                            self.draw_text(screen,f"{level}",30,BLACK, False ,x+10,y+10)
                        
                            if game.count_star == 3:
                                # 繪製星星
                                pygame.draw.polygon(screen, RED, star_points1)
                                pygame.draw.polygon(screen, RED, star_points2)
                                pygame.draw.polygon(screen, RED, star_points3)
                            elif game.count_star ==2:
                                pygame.draw.polygon(screen, RED, star_points1)
                                pygame.draw.polygon(screen, RED, star_points2)
                                pygame.draw.polygon(screen, GRAY, star_points3)
                            elif game.count_star ==1: 
                                pygame.draw.polygon(screen, RED, star_points1)
                                pygame.draw.polygon(screen, GRAY, star_points2)
                                pygame.draw.polygon(screen, GRAY, star_points3)
                        

                        elif game.play == True and game.win == False: # 可以玩該關卡，但遊戲並未通關

                            pygame.draw.rect(screen, YELLOW, (x, y, RECT_WIDTH, RECT_HEIGHT))
                            self.draw_text(screen,f"{level}",30,BLACK, False ,x+10,y+10)
                            if game.count_star == 3:
                                # 繪製星星
                                pygame.draw.polygon(screen, RED, star_points1)
                                pygame.draw.polygon(screen, RED, star_points2)
                                pygame.draw.polygon(screen, RED, star_points3)
                            elif game.count_star ==2:
                                pygame.draw.polygon(screen, RED, star_points1)
                                pygame.draw.polygon(screen, RED, star_points2)
                                pygame.draw.polygon(screen, GRAY, star_points3)
                            elif game.count_star ==1: 
                                pygame.draw.polygon(screen, RED, star_points1)
                                pygame.draw.polygon(screen, GRAY, star_points2)
                                pygame.draw.polygon(screen, GRAY, star_points3)
                            else:
                                pygame.draw.polygon(screen, GRAY, star_points1)
                                pygame.draw.polygon(screen, GRAY, star_points2)
                                pygame.draw.polygon(screen, GRAY, star_points3)






                        elif game.play == False : # 還不能玩該關卡 必須要前面的關卡通關後才會開啟
                            pygame.draw.rect(screen, GRAY, (x, y, RECT_WIDTH, RECT_HEIGHT))
                            self.draw_text(screen,f"{level}",30,BLACK, False ,x+10,y+10)
                            

                        
        pygame.display.flip()



    def get_user_input(self,x,y):  # 利用得到的位置來判斷所點擊的關卡是否能玩  -
        
        if y >= 60 and x >= 30 : 
            row = (y - 60) // (RECT_HEIGHT + 10)
            col = (x - 30) // (RECT_WIDTH + 10)
            level = row * 5 + col + 1


            for game in self.game_group.sprites():
                if game.level == level and game.play == True :
                    return [game.level,True]

                elif game.level == level and game.play == False:
                    return [game.level,False]
                else : 
                    #return[0,False]
                    pass
        else :
            return[None,False]
                








    def draw_text(self, surface, text, size, color, bold, x, y):
        font = pygame.font.Font("Font/BoutiqueBitmap9x9_Bold_1.9.ttf", size=size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.x = x
        text_rect.top = y
        surface.blit(text_surface, text_rect) 





    def calculate_star_points(self,center, radius, inner_radius, num_points=5): # by AI
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




