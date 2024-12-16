import pygame

from setting import *



class Picture(pygame.sprite.Sprite):
    """產生關卡裡面的元素圖片"""
    def __init__(self, pic, x, y):
        super().__init__()
        # Position of the image
        self.x = x
        self.y = y
        
        
        
        # Load and scale the image
        self.image = pygame.image.load(pic)
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        # Set the rect with the top-left corner at (self.x, self.y)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        # Calculate row and column based on position
        self.row = (self.rect.y-20 ) // (TILE_SIZE + MARGIN)
        self.col = (self.rect.x-250) // (TILE_SIZE + MARGIN)
    

        # 是否被選中
        self.selected = False 

    def get_user_input(self):
        """處理使用者輸入事件"""
        self.selected = not self.selected                                            # 切換選中狀態
        

    def draw(self, screen):
        """負責畫出圖片與選中框"""
        screen.blit(self.image, self.rect)
        if self.selected is True:                                                   # 當前被選中時，畫紅框   
            pygame.draw.rect(screen, (255, 0, 0), (self.rect.x-5, self.rect.y-5, 70, 70), 2)
            # pygame.display.update()

    
  



    def move(self, other, screen, left, right, up, down):
        """ 元素的移動，往上下左右移動一格 """
        steps = 65  # 定義移動的步數
        step_size = 1  # 每次移動的單位距離
    
        for _ in range(steps):
            if left:
                self.rect.x -= step_size
                other.rect.x += step_size
            elif right:
                self.rect.x += step_size
                other.rect.x -= step_size
            elif up:
                self.rect.y -= step_size
                other.rect.y += step_size
            elif down:
                self.rect.y += step_size
                other.rect.y -= step_size
    
            # 重繪畫面
            #screen.fill((0, 0, 0))  # 清空畫布（設置背景色為黑色）
            self.draw(screen)
            other.draw(screen)
            pygame.display.flip()
            pygame.time.delay(1)  # 暫停 0.001 秒
    
        # 更新 self 與 other 的 row 和 col 屬性
        self.update_position()
        other.update_position()
    
    def update_position(self):
        """ 更新物件在行列中的位置 """
        self.row = (self.rect.y - 20) // (TILE_SIZE + MARGIN)
        self.col = (self.rect.x - 250) // (TILE_SIZE + MARGIN)
        self.x = self.rect.x
        self.y = self.rect.y


    """
    def move_down(self, screen, dis):
        
        steps= 65 * dis
        step_size = 1  # 每次移動的單位距離
    
        for _ in range(steps):
            # 計算每步移動的距離
            self.rect.y += step_size 
    
            # 重繪畫面
            #screen.fill((0, 0, 0))  # 清空畫布，背景色黑色
            self.draw(screen)
            pygame.display.flip()
            pygame.time.delay(1)  # 暫停 0.001 秒
    
        # 更新行列與座標
        self.update_position()
    """

    
    def move_down(self,screen,dis):  # dis是往下移動的格子數
        # 往下移動dis格，根據傳入的參數做決定  
        
       

        for i in range (65):
             
           # move down
            self.rect.y = self.rect.y + (TILE_SIZE + MARGIN)/65 * dis
            
            self.draw(screen)
            pygame.time.delay(1)  # 暫停 0.001 秒            
    
        self.row = (self.rect.y-20) // (TILE_SIZE + MARGIN)                             # calculate the self's row
        self.col = (self.rect.x-250) // (TILE_SIZE + MARGIN)                            # calculate the self's col

      
        self.x = self.rect.x
        self.y = self.rect.y

    
 

