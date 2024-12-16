import pygame
import random
from setting import *
import time
from picture import Picture
import numpy as np
from object import *
import math
from animation import * 


pygame.init()
pygame.font.init()        
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#pygame.display.set_caption("遊戲")


clock = pygame.time.Clock()




"""
現在問題 -> 道具沒跑出來(解決道具沒跑出來的問題)
道具被啟動後的部分，以及判斷連線的部分 -> 解決

然後這種類型的圖案 -> 解決，但如果要產生道具的話還沒有寫
    0 0 0
        0
        0
他只消除橫的或是直的三個部分 


需要增加 
1.計分工具  -> 完成
2.關卡目標  -> 完成
3.結束遊戲(達到關卡目標後，或是移動步數變成0，按結束遊戲的鍵) 目前還沒有可玩到一半點擊結束遊戲的按鍵
4.移動步數  -> 完成
5.進入遊戲的頁面 -> 暫時有了
6.結束遊戲的畫面 -> 有了
7.道具被道具啟動到的部分還沒處理  
8. 掉落動畫    -> 已有掉落，但是想改成同時掉落
9. 音樂 可開關音樂的按鍵 -> 已有背景音樂，但還沒寫開關的按鍵、大小聲
10. 教學?? 如何玩
11. 故事
12. 額外道具?(如果有要的話，加上通關遊戲可獲得金幣的部分)
13. 體力? 固定時間恢復 花錢恢復
14. reset遊戲 -> 當玩家想重玩這一關卡(有了，但是history_point 還沒用，就是如果我第二次玩相同關卡，但是獲得的星星數量比較少->會顯示第二次的部分)
15.當遊戲贏了過後，回到home重新點擊這一關卡時，發現她會直接跳出這一關贏的畫面 而不是要重新進入關卡的畫面(解決)
16.消除的動畫，以及音效 


"""




class Game((pygame.sprite.Sprite)):
    def __init__(self,level):
        """ 小關卡 然會會傳入level決定現在玩的是哪一關卡"""

        super().__init__()
        self.clock = pygame.time.Clock()
        self.board = self.generate_board()                  # 在遊戲開始時，產生一個不具有可消除的版面
        self.picture_group = pygame.sprite.Group()          # 元素的group
        self.run = True                                     # 遊戲是否運行
        self.win = False                                    # 遊戲是否通關
        
        self.level = level                                  # 關卡難度
        self.point = 0                                      # 目前分數
        passed = Object(self.level)                         # 關卡目標
        self.object = passed.object
        self.step = passed.step                             # 遊戲步數

        self.one_star = 100                                 # 一顆星的分數
        self.two_star = 250                                 # 二顆星的分數
        self.three_star = 400                               # 三顆星的分數
        self.max = 500                                      # 分數條的最高分數 (畫圖方便)
        self.count_star = 0                                 # 計算目前有幾顆星星了
        
        self.play = False                                   # 是否能玩此關卡，需要上一關通關後，此關才可以玩
        



        self.history_point = 0                              # 歷史最高分(寫在判斷遊戲通關哪邊)
        self.animation_group = pygame.sprite.Group()


        for row in range(GRID_SIZE):                        # 產生Picture 的 object 
            for col in range(GRID_SIZE):
                # 計算每個格子的顯示位置
                x = col * (TILE_SIZE + MARGIN) + MARGIN +250
                y = row * (TILE_SIZE + MARGIN) + MARGIN +20
                picture = Picture(self.board[row][col], x, y)
                self.picture_group.add(picture)
                    


    
    def check_matches_in_board(self, board): # return true or false by AI
        """檢查棋盤是否存在三個的連續圖案"""
        # 檢查橫向匹配
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE - 2):
                if board[row][col] == board[row][col + 1] == board[row][col + 2]:
                    return True
        # 檢查縱向匹配
        for col in range(GRID_SIZE):
            for row in range(GRID_SIZE - 2):
                if board[row][col] == board[row + 1][col] == board[row + 2][col]:
                    return True
        return False

    
    def generate_board(self): # 在遊戲凱開始時  by AI
        """生成隨機且不包含三個連續圖案的棋盤。"""
        while True:
            board = [[random.choice(PICTURE) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
            if not self.check_matches_in_board(board):
                return board
    
    def find_connected(self, matrix, length):  # by AI
        
        # 找出矩陣中相連的數值
    
        rows, cols = len(matrix), len(matrix[0])
        visited = [[False] * cols for _ in range(rows)]
        directions = [(0, 1), (1, 0)]  # 只檢查橫向和縱向
        results = []
    
        def in_bounds(x, y): # by AI
            return 0 <= x < rows and 0 <= y < cols
    
        def dfs(x, y, dx, dy, target, count): # by AI
            """用於追蹤連續數值的深度優先搜索"""
            if count == length:
                return [(x - dx * (length - 1) + i * dx, y - dy * (length - 1) + i * dy) for i in range(length)]
            nx, ny = x + dx, y + dy
            if in_bounds(nx, ny) and not visited[nx][ny] and matrix[nx][ny] == target:
                return dfs(nx, ny, dx, dy, target, count + 1)
            return []
    
        for x in range(rows):
            for y in range(cols):
                if not visited[x][y]:
                    for dx, dy in directions:
                        path = dfs(x, y, dx, dy, matrix[x][y], 1)
                        if len(path) == length:
                            results.append(path)
                            for px, py in path:
                                #visited[px][py] = True
                                pass
        return results
    
    def find_all_connected(self): # by AI
        
        # 找出矩陣中所有長度為 5、4、3 的相連數值，並確保結果不重疊。
    
        all_results = {5: [], 4: [], 3: []}
        matrix = self.board
        for length in [5, 4, 3]:
            results = self.find_connected(matrix, length)
            all_results[length].extend(results)
    
        # print(all_results)

        def remove_subsets(all_results): # by AI
            # 按長度從大到小排序鍵
            lengths = sorted(all_results.keys(), reverse=True)
        
            # 遍歷所有長度
            for i in range(len(lengths)):
                longer_length = lengths[i]
                for j in range(i + 1, len(lengths)):
                    shorter_length = lengths[j]
        
                    # 遍歷短群組，刪除那些是長群組子集的
                    all_results[shorter_length] = [
                        group for group in all_results[shorter_length]
                        if not any(set(group).issubset(set(long_group)) for long_group in all_results[longer_length])
                    ]
        
            return all_results
        
        
        # 呼叫函式
        cleaned_results = remove_subsets(all_results)
        return cleaned_results
    
    

    def remove_match(self,match):  #加入刪除小動畫
        """
        透過matches = {5: [], 4: [], 3: []} 知道在board上哪裡有相連的元素
        如果有五個相連的東西-> 產生彩虹,消除元素
        如果有四個相連的東西 -> 產生箭頭,消除元素
        如果有三個相連的東西 -> 消除元素
        """

        if match[5]: # 有長度為5的
            for i in range(len(match[5])):
                # print("there's a match5 : ",match[5][i])
                match5 = match[5][i] # 取出第i組長度為5的東西 [(,),(,),(,),(,),(,)]
                for j in range (5):
                    row = int(match5[j][0])
                    col = int(match5[j][1])
                    for k in range (len(self.object)): #如果消除的物是關卡目標的話 -> 修改數量 
                        if self.board[row][col] == self.object[k][0] and self.object[k][1] >=1:
                            self.object[k][1]= self.object[k][1] -1 

                    
                    for picture in self.picture_group.sprites():
                        if picture.row == row and picture.col == col :
                            #self.animation_group.add(Explosion(picture.rect.centerx, picture.rect.centery, 50))
                            picture.kill()                                   # 刪除可消除的元素
                            
                            
                    self.board[row][col] = None # 消除元素

                ranbow_row = int(match5[2][0])
                ranbow_col = int(match5[2][1])

                self.board[ranbow_row][ranbow_col] = MATCH5

                for k in range (len(self.object)): #如果消除的物是關卡目標的話 -> 修改數量 
                    if self.object[k][0] == MATCH5 and self.object[k][1] >=1:
                        self.object[k][1] = self.object[k][1] -1 

                    if self.object[k][0] == "point" and self.object[k][1] >=1:
                        self.object[k][1] = self.object[k][1] -5
                        if self.object[k][1] < 0 :
                                self.object[k][1] = 0 
                


                self.point = self.point + 5 
                
                
            
                x = ranbow_col * (TILE_SIZE + MARGIN) + MARGIN +250
                y = ranbow_row * (TILE_SIZE + MARGIN) + MARGIN +20
                picture = Picture(MATCH5, x, y)
                self.picture_group.add(picture)
                # print("self.picture add match5 ")


                
                self.draw(screen)
                pygame.display.update()

      
        if match[4]: # 有長度為4的

            color = 0 
            for i in range(len(match[4])):
                # print("there's a match4 : ",match[4][i])

                
                match4 = match[4][i] # 取出第i組長度為4的東西 [(,),(,),(,),(,)]
                
                for j in range(4):
                    row = int(match4[j][0])
                    col = int(match4[j][1])    

                    for k in range (len(self.object)): #如果消除的物是關卡目標的話 -> 修改數量 
                        if self.board[row][col] == self.object[k][0] and self.object[k][1] >=1:
                            self.object[k][1]= self.object[k][1] -1 


                    for picture in self.picture_group.sprites():
                        if picture.row == row and picture.col == col :
                            #self.animation_group.add(Explosion(picture.rect.centerx, picture.rect.centery, 50))
                            picture.kill()                                   # 刪除可消除的元素
                            
                            
                    self.board[row][col] = None # 消除元素
                        

                arrow_row = int(match4[2][0])
                arrow_col = int(match4[2][1])

                self.board[arrow_row][arrow_col] = MATCH4


                for k in range (len(self.object)): #如果消除的物是關卡目標的話 -> 修改數量 
                    if self.object[k][0] == MATCH4 and self.object[k][1] >=1:
                        self.object[k][1]= self.object[k][1] -1 

                    if self.object[k][0] == "point" and self.object[k][1] >=1:
                        self.object[k][1] = self.object[k][1] -4
                        if self.object[k][1] < 0 :
                                self.object[k][1] = 0 


                
                self.point = self.point + 4 
                              
                x = arrow_col * (TILE_SIZE + MARGIN) + MARGIN +250
                y = arrow_row * (TILE_SIZE + MARGIN) + MARGIN +20
                picture = Picture(MATCH4, x, y)
                self.picture_group.add(picture)
                # print("self.picture add match4 ")

                self.draw(screen)
                pygame.display.update()

            

        if match[3]: # 有長度為3的
            for i in range(len(match[3])):
                match3 = match[3][i] # 取出第i組長度為3的東西 [(,),(,),(,)]
                
                for j in range(3):
                    row = int(match3[j][0])
                    col = int(match3[j][1])

                    for k in range (len(self.object)): #如果消除的物是關卡目標的話 -> 修改數量 
                        if self.board[row][col] == self.object[k][0] and self.object[k][1] >=1:
                            self.object[k][1]= self.object[k][1] -1
                        if self.object[k][0] == "point" and self.object[k][1] >=1:
                            self.object[k][1] = self.object[k][1] -3
                            if self.object[k][1] < 0 :
                                self.object[k][1] = 0 

                    for picture in self.picture_group.sprites():
                        if picture.row == row and picture.col == col :
                            #self.animation_group.add(Explosion(picture.rect.centerx, picture.rect.centery, 50))
                            picture.kill()                                   # 刪除可消除的元素
                            
                    self.point = self.point + 3
                    self.board[row][col] = None # 消除元素
                    


        
        self.draw(screen)
        pygame.display.update()
    
    
    
    def refill_board(self):
        #補充空白方塊。
        for col in range(GRID_SIZE):
            empty_slots = []
            # 找到每一列的空白格子
            for row in range(GRID_SIZE - 1, -1, -1):
                if self.board[row][col] is None:
                    empty_slots.append(row)
                elif empty_slots:
                    empty_row = empty_slots.pop(0)
                    self.board[empty_row][col] = self.board[row][col]
                    self.board[row][col] = None
                    empty_slots.append(row)
                    
                    # 更新圖片位置
                    for picture in self.picture_group.sprites():
                        if picture.row == row and picture.col == col:
                            picture.move_down(screen, empty_row - row)
                            
                            
        
            # 填充空白格子
            for row in empty_slots:
                self.board[row][col] = random.choice(PICTURE)
                x = col * (TILE_SIZE + MARGIN) + MARGIN + 250
                y = row * (TILE_SIZE + MARGIN) + MARGIN + 20
                picture = Picture(self.board[row][col], x, y)
                self.picture_group.add(picture)
        
        # 檢查是否有匹配並處理
        while True:
            if not self.check_matches_in_board(self.board):
                break
            matches = self.find_all_connected()
            if not matches:
                break
            self.remove_match(matches)
            self.refill_board()
    
    
    """
    def refill_board(self):
        補充空白方塊，讓所有方塊的移動和補充分步進行
        move_instructions = []  # 記錄需要移動的方塊及其移動距離
    
        # 1. 計算需要移動的邏輯
        for col in range(GRID_SIZE):
            empty_slots = []
    
            # 找到每列的空白格子並計算移動邏輯
            for row in range(GRID_SIZE - 1, -1, -1):
                if self.board[row][col] is None:
                    empty_slots.append(row)
                elif empty_slots:
                    empty_row = empty_slots.pop(0)
                    self.board[empty_row][col] = self.board[row][col]
                    self.board[row][col] = None
                    empty_slots.append(row)
    
                    # 記錄移動指令
                    move_instructions.append((row, col, empty_row))
    
        # 2. 動畫階段：執行移動動畫
        self.animate_moves(move_instructions)
    
        # 3. 補充空白格子
        self.fill_empty_slots()
        self.draw(screen)
        pygame.display.update()
        # 4. 處理新的匹配（遞迴處理直到無匹配）
        while True:
            matches = self.find_all_connected()
            if not matches:
                break
            self.remove_match(matches)
            self.refill_board()
    
    
    def animate_moves(self, move_instructions):
        執行所有方塊的掉落動畫
        max_steps = 65  # 定義動畫的總步數
        for step in range(max_steps):
            for row, col, target_row in move_instructions:
                distance = (target_row - row) * (TILE_SIZE + MARGIN) / max_steps
                for picture in self.picture_group.sprites():
                    if picture.row == row and picture.col == col:
                        picture.rect.y += distance
    
            # 重繪所有圖片
            self.picture_group.draw(screen)
            pygame.display.flip()
            pygame.time.delay(1)  # 動畫延遲 0.001 秒
    
        # 更新所有圖片的行列屬性
        for row, col, target_row in move_instructions:
            for picture in self.picture_group.sprites():
                if picture.row == row and picture.col == col:
                    picture.row = target_row
                    picture.col = col
                    picture.rect.y = target_row * (TILE_SIZE + MARGIN) + MARGIN + 20
    
    
    def fill_empty_slots(self):
        補充空白格子並執行補充動畫，讓新方塊正確移動到空白位置。
        new_pictures = []  # 記錄新補充的方塊
    
        # 計算每列的空白格子並生成新方塊
        for col in range(GRID_SIZE):
            empty_slots = []  # 記錄該列的空白行
            for row in range(GRID_SIZE):
                if self.board[row][col] is None:
                    empty_slots.append(row)
            
            # 從空白格子的頂端生成新方塊，並記錄其掉落目標
            for target_row in empty_slots:
                # 隨機生成新方塊
                self.board[target_row][col] = random.choice(PICTURE)
                x = col * (TILE_SIZE + MARGIN) + MARGIN + 250
                y = row * (TILE_SIZE + MARGIN) + MARGIN +20  
                picture = Picture(self.board[target_row][col], x, y)
                self.picture_group.add(picture)
                empty_slots.pop(0)
                #picture.row = target_row
                #picture.col = col
                #self.picture_group.add(picture)
                #new_pictures.append((picture, target_row))
        
        # 掉落動畫
        max_steps = 65
        for step in range(max_steps):
            for picture, target_row in new_pictures:
                # 計算目標位置
                target_y = target_row * (TILE_SIZE + MARGIN) + MARGIN + 20
                # 計算每一步的移動距離
                move_distance = (target_y - picture.rect.y) / (max_steps - step)
                picture.rect.y += move_distance
    
            # 重繪畫面
            
            self.picture_group.draw(screen)
            pygame.display.flip()
            pygame.time.delay(1)  # 延遲 1 毫秒以控制動畫速度
    
        # 最後修正位置，避免浮點數誤差
        for picture, target_row in new_pictures:
            picture.rect.y = target_row * (TILE_SIZE + MARGIN) + MARGIN + 20
        
    """       
        
    
   





    
    def handle_click(self, pos):
        """處理滑鼠點擊事件，並執行方塊選取與交換。"""
        # print("handle click")
        col = (pos[0]-250) // (TILE_SIZE + MARGIN)              # 計算row
        row = (pos[1]-20) // (TILE_SIZE + MARGIN)               # 計算col


        
        count_selected = 0                                      # 計算已被選取picture的數量
        selected_picture = []
        
        for picture in self.picture_group.sprites():
            
            if picture.row == row and picture.col == col: # 更改picture的狀態
                picture.get_user_input()  # selected = true



            if picture.selected == True : # 計算目前有幾個被選取
                count_selected = count_selected +1
                selected_picture.append(picture)



        
        # 判斷圖片上選取 
                    
        if count_selected == 1 : # 當版面上的點擊只有一個時
            self.arrow_happened(row,col)  # 當點擊的是arrow時 
            self.ranbow_happened(row,col) # 當點擊的是ranbow時
            
        elif count_selected == 2 : # 判斷是否相鄰 

            self.arrow_happened(row,col)
            self.ranbow_happened(row,col)
           
                                       
            if selected_picture[0].row == selected_picture[1].row and abs(selected_picture[0].col - selected_picture[1].col) == 1 : # 左右的nighbor
                # 相鄰後判斷是否可以消除 
           
                if selected_picture[0].col - selected_picture[1].col == -1 : # picture[0] in left   -> move right                  
                    selected_picture[0].move(selected_picture[1],screen,False,True,False,False)
                else:                                                        # picture[1] in left -> move right
                    selected_picture[1].move(selected_picture[0],screen,False,True,False,False)
                
                selected_picture[0].get_user_input()   # selected = false
                selected_picture[1].get_user_input()   # selected = false

                # 交換self.board的數值
                temp = self.board[selected_picture[0].row][selected_picture[0].col] 
                self.board[selected_picture[0].row][selected_picture[0].col] = self.board[selected_picture[1].row][selected_picture[1].col]
                self.board[selected_picture[1].row][selected_picture[1].col] = temp

                
                if self.check_matches_in_board(self.board) is True :
                    # 有可消除的物件
                    matches = {5: [], 4: [], 3: []}
                    matches = self.find_all_connected()
                    self.remove_match(matches)
                    self.step = self.step-1 
                    if self.step == 0 :
                        self.run = False
                    self.refill_board()
                else:
                    # 沒有可消除物件
                    temp = self.board[selected_picture[0].row][selected_picture[0].col] 
                    self.board[selected_picture[0].row][selected_picture[0].col] = self.board[selected_picture[1].row][selected_picture[1].col]
                    self.board[selected_picture[1].row][selected_picture[1].col] = temp
                    if selected_picture[0].col - selected_picture[1].col == -1 : # picture[0] in left -> move right                    
                        selected_picture[0].move(selected_picture[1],screen,False,True,False,False) 
                    else:                                                        # picture[1] in left -> move right
                        selected_picture[1].move(selected_picture[0],screen,False,True,False,False)
                     
            elif selected_picture[0].col == selected_picture[1].col and abs(selected_picture[0].row - selected_picture[1].row) == 1 : # 上下的neighbor
                # 相鄰後判斷是否可以消除 
                
                if selected_picture[0].row - selected_picture[1].row == -1 : # picture[0] in up   
                    selected_picture[0].move(selected_picture[1],screen,False,False,False,True)  
                else:                                                        # picture[1] in up                    
                    selected_picture[1].move(selected_picture[0],screen,False,False,False,True)
                    
                selected_picture[0].get_user_input() # selected = false
                selected_picture[1].get_user_input() # selected = false

                temp = self.board[selected_picture[0].row][selected_picture[0].col] 
                self.board[selected_picture[0].row][selected_picture[0].col] = self.board[selected_picture[1].row][selected_picture[1].col]
                self.board[selected_picture[1].row][selected_picture[1].col] = temp

                if self.check_matches_in_board(self.board) is True :
                    # 有可消除的物件
                    matches = {5: [], 4: [], 3: []}
                    matches = self.find_all_connected()
                    self.remove_match(matches)
                    self.step = self.step-1
                    if self.step == 0 :
                        self.run = False
                    self.refill_board()
                else:
                    # 沒有可消除物件

                    temp = self.board[selected_picture[0].row][selected_picture[0].col] 
                    self.board[selected_picture[0].row][selected_picture[0].col] = self.board[selected_picture[1].row][selected_picture[1].col]
                    self.board[selected_picture[1].row][selected_picture[1].col] = temp
                    
                    if selected_picture[0].row - selected_picture[1].row == -1 : # picture[0] in up   
                        selected_picture[0].move(selected_picture[1],screen,False,False,False,True)
                        #pygame.display.update()
                                     
                    else:                                                        # picture[1] in up                    
                        selected_picture[1].move(selected_picture[0],screen,False,False,False,True)
                        #pygame.display.update()
                        
                    

            
            else: # not neighbor -> 取消第一個選的 保留第二次選的
                
                for picture in self.picture_group.sprites():
                    if picture.selected == True:
                        picture.get_user_input()
                       
                     
                        

                for picture in self.picture_group.sprites():   
                    if picture.row == row and picture.col == col:
                        picture.get_user_input()  # selected = true
                        

        else:
            pass



    def arrow_happened(self,row,col):
        """
        當該到具被啟動時，會刪除掉一整排橫直的元素
        """
        if self.board[row][col] == MATCH4 :
            
            for r in range (10):   # 10*10 board 
                
            
                for k in range (len(self.object)): #如果消除的物是關卡目標的話 -> 修改數量 
                    if self.board[row][r] == self.object[k][0] and self.object[k][1] >=1:  # 物體
                        self.object[k][1]= self.object[k][1] -1
                    if self.board[r][col] == self.object[k][0] and self.object[k][1] >=1:  # 物體
                        self.object[k][1]= self.object[k][1] -1 
                    if self.object[k][0] == "point" and self.object[k][1] >=1:  # point
                        self.object[k][1] = self.object[k][1] -4
                        if self.object[k][1] < 0 :
                            self.object[k][1] = 0 
                self.board[row][r] = None                         # 設置成被消除
                self.board[r][col] = None                      # 設置成被消除
                for picture in self.picture_group.sprites():   # 刪除物件
                    if picture.row == row and picture.col == r:
                        #self.animation_group.add(Explosion(picture.rect.centerx, picture.rect.centery, 50))
                        picture.kill()
                    if picture.row == r and picture.col == col:
                        #self.animation_group.add(Explosion(picture.rect.centerx, picture.rect.centery, 50))
                        picture.kill()
                        
                
                
            for picture in self.picture_group.sprites():
                if picture.row == row and picture.col == col:
                    picture.get_user_input()            #  把原本選中圖片的狀態改掉
                    
            self.point = self.point + 40                   # 加分數 
            self.step = self.step-1                         # 移動步數減少 
            if self.step == 0 :
                        self.run = False
            self.refill_board()                     # 填滿board  
                    
    def ranbow_happened(self,row,col):
        """
        當該道具被啟動時，會刪除掉在版面上所有的元素
        """
        if self.board[row][col] == MATCH5 :
            for i in range (10):
                for j in range (10) :

                    for k in range (len(self.object)): #如果消除的物是關卡目標的話 -> 修改數量 
                        if self.board[i][j] == self.object[k][0] and self.object[k][1] >=1:
                            self.object[k][1]= self.object[k][1] -1
                        if self.object[k][0] == "point" and self.object[k][1] >=1:
                            self.object[k][1] = self.object[k][1] -1
                            if self.object[k][1] < 0 :
                                self.object[k][1] = 0
                    self.board[i][j] = None
                    
                    for picture in self.picture_group.sprites():
                        if picture.row == i and picture.col == j:
                            #self.animation_group.add(Explosion(picture.rect.centerx, picture.rect.centery, 50))
                            picture.kill()
                            
                   
            for picture in self.picture_group.sprites():
                if picture.row == row and picture.col == col:
                    picture.get_user_input()  
                    
            self.point = self.point + 100
            self.step = self.step-1
            if self.step == 0 :
                        self.run = False
            self.refill_board()


    def draw(self, surface):
        pygame.draw.rect(surface, YELLOW,  (30, 30, 190, 40), 0, 10)  # 左上
        self.draw_text(surface,f"LEVEL:{self.level}", 24, BLACK, False, 80, 35) # 左上文字

        pygame.draw.rect(surface, YELLOW,  (30, 80, 190, 250), 0, 10)  # 左中
        pygame.draw.circle(surface, WHITE, (125,250), 70, 0)   #實心圓 
        self.draw_text(surface,f"Moves",30,BLACK, False ,80,200)     # 步數
        self.draw_text(surface,f"{self.step}",36,BLACK, False ,105,250)  #步數

        self.draw_text(surface,f"Point:{self.point}", 24, BLACK, False, 80, 85)   # 現在的分數


        pygame.draw.rect(surface, WHITE,  (40, 115, 170, 20), 0, 10)  # 左中分數條

        x = self.point/self.max*170
        if x > 170 :
            x = 170
        pygame.draw.rect(surface, GREEN,  (40, 115, x, 20), 0, 10)  # 左中分數條
        x1 = self.one_star / self.max *170 +40
        pygame.draw.rect(surface, BLACK,  (x1, 115, 3, 20), 0, 10)  # 左中分數條 一星線
        x2 = self.two_star / self.max *170 +40
        pygame.draw.rect(surface, BLACK,  (x2, 115, 3, 20), 0, 10)  # 左中分數條 二星線
        x3 = self.three_star / self.max *170 +40
        pygame.draw.rect(surface, BLACK,  (x3, 115, 3, 20), 0, 10)  # 左中分數條 三星線
        

        if self.point >= self.one_star : # 分數超過一星時
            # 計算五角星頂點
            center = (x1, 140)  # 星星的中心點
            outer_radius = 10   # 外圍半徑
            inner_radius = 5    # 內部半徑
            star_points = self.calculate_star_points(center, outer_radius, inner_radius)
            # 繪製星星
            pygame.draw.polygon(screen, RED, star_points)
        if self.point >= self.two_star : # 分數超過二星時
            # 計算五角星頂點
            center1 = (x2, 140)  # 星星的中心點
            center2 = (x2+10, 140)  # 星星的中心點
            outer_radius = 10   # 外圍半徑
            inner_radius = 5    # 內部半徑
            star_points1 = self.calculate_star_points(center1, outer_radius, inner_radius)
            star_points2 = self.calculate_star_points(center2, outer_radius, inner_radius)
            # 繪製星星
            pygame.draw.polygon(screen, RED, star_points1)
            pygame.draw.polygon(screen, RED, star_points2)
        if self.point >= self.three_star : # 分數超過三星時
            # 計算五角星頂點
            center1 = (x3, 140)  # 星星的中心點
            center2 = (x3+10, 140)  # 星星的中心點
            center3 = (x3+20, 140)  # 星星的中心點
            outer_radius = 10   # 外圍半徑
            inner_radius = 5    # 內部半徑
            star_points1 = self.calculate_star_points(center1, outer_radius, inner_radius)
            star_points2 = self.calculate_star_points(center2, outer_radius, inner_radius)
            star_points3 = self.calculate_star_points(center3, outer_radius, inner_radius)
            # 繪製星星
            pygame.draw.polygon(screen, RED, star_points1)
            pygame.draw.polygon(screen, RED, star_points2)
            pygame.draw.polygon(screen, RED, star_points3)

        pygame.draw.rect(surface, YELLOW,  (30, 340, 190, 325), 0, 10)  # 左下的框框
        self.draw_text(surface,f"Object:",24,BLACK, False ,80,360)
        
        for i in range(len(self.object)):
            if(self.object[i][0] == "point"):  #通關目標達到特定分數
                
                self.draw_text(surface,f"{self.object[i][0]}:{self.object[i][1]}",24,BLACK, False ,60,340 + 40*i+50)

            else: # 消除特定物品 
                
                
                ima = pygame.image.load(self.object[i][0])
                ima = pygame.transform.scale(ima, (TILE_SIZE/2, TILE_SIZE/2))
                surface.blit(ima, (80,340+40*i+50))
                self.draw_text(surface,f"* {self.object[i][1]}",24,BLACK, False ,115,340+40*i+50)



        
        pygame.draw.rect(surface, YELLOW,  (SCREEN_WIDTH-100, 50, 80, 600), 0, 10)  #右邊

       
        
        self.picture_group.draw(screen)
        #self.animation_group.draw(screen)
        #self.animation_group.update()
        


    
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

    def end_game(self):
        if any(obj[1] > 0 for obj in self.object):  # 檢查是否所有物件被消除
            self.run = True
            self.win = False
            
        elif all(obj[1] == 0 for obj in self.object):  #遊戲結束 ㄧ
            
            # self.point = self.point + self.step*20  #將剩餘的步數變成分數
            self.history_point = self.point            # 紀錄分數 (之後如果有要重玩此關卡比較方便)


            if self.point >= self.one_star :    #分數有大於一顆星星-> 通關
                self.run = False
                self.win = True

            


            
            else:
                self.run = False
                self.win = False


            
            for picture in self.picture_group.sprites():
                picture.kill()
            


            

            if self.point >= self.three_star:
                self.count_star = 3 
            elif self.point >=self.two_star:
                self.count_star = 2
            elif self.point >= self.one_star:
                self.count_star = 1 
            else :
                self.count_star = 0 
                
                   


            
    
        
        if self.step == 0:  # 檢查步數是否用完
            self.run = False
            if any(obj[1] > 0 for obj in self.object):  # 檢查是否所有物件被消除
             
                self.win = False
                
            elif all(obj[1] == 0 for obj in self.object):  #遊戲結束 ㄧ
                
                
                #self.point = self.point + self.step*20  #將剩餘的步數變成分數
                self.history_point = self.point            # 紀錄分數 (之後如果有要重玩此關卡比較方便)

                if self.point >= self.one_star :    #分數有大於一顆星星-> 通關
                    
                    self.win = True
                else:
                    
                    self.win = False
    
                for picture in self.picture_group.sprites():
                    picture.kill()
                
    
    
                if self.point >= self.three_star:
                    self.count_star = 3 
                elif self.point >=self.two_star:
                    self.count_star = 2
                elif self.point >= self.one_star:
                    self.count_star = 1 
                else :
                    self.count_star = 0 



    
    def run_game(self):
        while self.run:
            # Checking for events
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    
                    self.run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self.handle_click(mouse_pos) 
                    self.end_game()
                    self.draw(screen)
                    
    
            # 繪製畫面
            screen.fill(BLACK)  # 背景填充
            self.draw(screen)
            pygame.display.flip()
    
            clock.tick(FPS)       
            
        

    def reset_game(self): # reset 一些variable
        
        #self.animation_group.empty()
        self.clock = pygame.time.Clock()
        self.board = self.generate_board()                  # 在遊戲開始時，產生一個不具有可消除的版面
        self.picture_group = pygame.sprite.Group()
        self.run = True                                     # 遊戲是否運行
        self.win = False 
        
    
        self.point = 0                                      # 目前分數
        
        passed = Object(self.level)               
        self.object = passed.object
        print(self.object)
        self.step = passed.step                             # 遊戲步數

        self.one_star = 100
        self.two_star = 250
        self.three_star = 400
        self.max = 500
        
        
        for row in range(GRID_SIZE):                        # 產生picture
            for col in range(GRID_SIZE):
                # 計算每個格子的顯示位置
                x = col * (TILE_SIZE + MARGIN) + MARGIN +250
                y = row * (TILE_SIZE + MARGIN) + MARGIN +20
                picture = Picture(self.board[row][col], x, y)
                self.picture_group.add(picture)   
