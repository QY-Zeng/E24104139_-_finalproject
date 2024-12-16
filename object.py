import pygame
import random
from setting import *


class Object():
    """
    關卡目標：
    1. 消除物品 
    2. 分數達標 
    3. 產生arror的數量
    4. 產生ranbow的數量
    
    """
    def __init__(self,level):
        self.level = level
        self.step = 25
        self.object = []
        if self.level <= 2  :                                      # 第一種：只要達到消除特定圖案的數量，即可通關
            self.object.append([random.choice(PICTURE), 40])
            
        elif self.level > 2 and self.level <= 4 :                  # 第一種：只要達到消除特定圖案的數量，即可通關
            selected_pictures = random.sample(PICTURE, 2)
            self.object.append([selected_pictures[0], 40])
            self.object.append([selected_pictures[1], 50])

        elif self.level >=5 and self.level <= 6: # 
            self.object.append (["point",300+self.level*30])      # 第二種：只要達到分數，即可通關

        elif self.level >= 7 and self.level < 10 :                # 第三種：產生足夠的arrow，即可通關
            self.object.append([MATCH4,10])
            

        elif self.level == 10 :                                  # 第四種：產生足夠的ranbow，即可通關
            self.object.append ([MATCH5,2]) 

        else :   # 關卡大於10之後
            self.object.append([random.choice(PICTURE), 50])
            self.object.append([random.choice(PICTURE),50])     # 消除特定物

        
            