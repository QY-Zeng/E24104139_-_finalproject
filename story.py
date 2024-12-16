"""
    故事大綱：由於天災，導致著名廟宇(古蹟)xxx收到大規模的破壞，身為建築師的你，需要透過蒐集星星，來獲得神奇圖紙，已修復廟宇

    靈宿廟 ：「靈宿」意指靈魂寄宿之地，既隱喻星宿，也突顯廟宇是祖先靈魂的安居之所。

"""

"""
在一個遠離城市喧囂的小鎮，矗立著一座古老的廟宇——靈宿廟。這座廟宇擁有數百年的歷史，是鎮上居民的精神寄託，亦是國家級的文化瑰寶。廟宇裡的每一塊石雕、每一幅壁畫，都承載著祖先的智慧與信念。然而，一場突如其來的天災摧毀了這座廟宇，使它成了一片殘垣斷壁，居民們的希望也隨之破碎。

這座廟宇不僅是建築藝術的奇蹟，更肩負著鎮上居民代代相傳的使命：安撫祖先的靈魂，並守護天地間的平衡。

任務的起點
作為一名年輕且富有熱忱的建築師，你來到這座小鎮，決心接下這項艱鉅的任務。然而，當你踏入廟宇的廢墟時，才發現問題遠比想像中複雜。廟宇的結構極其精密，甚至運用了已失傳的古代技術。普通的建築方法根本無法重現它原本的輝煌。

鎮上的長老告訴你一段鮮為人知的傳說：

「廟宇是祖先的靈魂棲息之地，它的修復需要的不僅是技術，還需要星星的指引。每顆星星都是一位祖先的靈魂化身，只有蒐集到這些星星，才能獲得記載著古代建築祕密的圖紙，幫助廟宇重建。」

從此，你踏上了尋找星星與修復廟宇的冒險之旅。

星星與圖紙
每顆星星都藏於天地間，只有透過完成三消挑戰才能蒐集到它們。每當蒐集9顆星星，就能拼湊出一部分廟宇的祕密圖紙。這些圖紙記錄了廟宇各部分的構造與細節，如：



雄偉的大殿，承載著廟宇的靈魂
巧奪天工的屋簷，象徵著祖先的智慧
色彩斑斕的壁畫，訴說著古老的傳說
雕龍畫鳳的柱子，刻畫了千年前的傳奇與榮耀，龍騰虎躍之間似能感受古代匠師的巧思
古樸典雅的石階，每一塊石板上都刻下了時間的印記，訴說著數百年來無數人前來朝聖的腳步聲
古色古香的門窗，刻有祥獸和吉祥符號，代表著守護與祝福
莊嚴肅穆的神像，凝視著前來祈願的人們，傳遞著祖先的教誨與慈愛





隨著圖紙的解鎖，廟宇逐步重建，漸漸恢復它失落的輝煌與靈氣。

劇情與祖先的祝福
每當修復完成一部分廟宇，夜空中便會出現祖先的靈影。他們將向你訴說廟宇的故事，揭示它背後的文化意義與使命：

祖先的祝福：星星並非普通的光芒，而是祖先的靈魂化身。他們透過三消挑戰將力量賦予你，幫助完成修復工作。
廟宇的使命：靈宿廟原本是為守護星星、連結祖先與後代的心靈而建。然而天災破壞了這份平衡，導致祖先的靈魂流散，失去了棲息之所。修復廟宇是為了讓他們得以安息，並重建人與自然的和諧。
隱藏的秘密與終章
當你成功修復廟宇的最後一部分時，星星的光芒匯聚於廟宇上空，點亮了整個小鎮。祖先的靈魂不僅向你道出了感謝，也揭示了一個隱藏已久的真相：

靈宿廟的靈氣，來自祖先與後代心靈的連結。每一位努力修復廟宇的人，實際上都在完成一段跨越時空的心靈對話。

最終，廟宇恢復了它的榮光，小鎮也重拾了希望。而你，作為這段旅程的見證者與推動者，將永遠被星空與歷史銘記。

"""




import pygame
import sys
from setting import *

# 初始化 Pygame
pygame.init()

# 設定視窗大小和字體
screen = pygame.display.set_mode((1024, 700))
font = pygame.font.Font("Font/msjh.ttf", 30)




class Story():
    def __init__(self):
        pass 
    
    
    def story_run(self,story_text):           # display the story  byAI

        # 設定文字和顏色
        text = story_text
        text_color = WHITE
        bg_color = BLACK

        # 主迴圈變數
        clock = pygame.time.Clock()
        displayed_text = ""  # 初始化為空字串
        char_index = 0  # 當前文字索引
        frame_counter = 0  # 幀計數

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # 檢查滑鼠按下事件
                

            # 控制文字顯示速度
            frame_counter += 1
            if frame_counter % 5 == 0:  # 每 5 幀顯示一個字
                if char_index < len(text):
                    current_char = text[char_index]
                    displayed_text += current_char
                    char_index += 1

                    # 自動在逗號和句號後添加換行
                    if current_char in "，。：":
                        displayed_text += "\n"

            # 畫面繪製
            screen.fill(bg_color)

            # 分行顯示文字
            y_offset = 70  # 起始 Y 偏移
            line_height = 40  # 行距
            lines = displayed_text.split("\n")  # 如果文字中包含換行符號
            for line in lines:
                rendered_line = font.render(line, True, text_color)
                screen.blit(rendered_line, (50, y_offset))
                y_offset += line_height

            pygame.display.flip()
            clock.tick(30)  # 控制畫面更新頻率


            
            if char_index >= len(text):
                return  # 結束函式，返回上一層邏輯


    def story_start1(self):  # 遊戲開始的故事顯現
        story1_text = "在一個遠離城市喧囂的小鎮，矗立著一座古老的廟宇——靈宿廟。這座廟宇擁有數百年的歷史，是鎮上居民的精神寄託，亦是國家級的文化瑰寶。廟宇裡的每一塊石雕、每一幅壁畫，都承載著祖先的智慧與信念。然而，一場突如其來的天災摧毀了這座廟宇，使它成了一片殘垣斷壁，居民們的希望也隨之破碎。這座廟宇不僅是建築藝術的奇蹟，更肩負著鎮上居民代代相傳的使命：安撫祖先的靈魂，並守護天地間的平衡。"
        self.story_run(story1_text)
        
    def story_start2(self):  # 遊戲開始的故事顯現
        
        story2_text = "作為一名年輕且富有熱忱的建築師，你來到這座小鎮，決心接下這項艱鉅的任務。然而，當你踏入廟宇的廢墟時，才發現問題遠比想像中複雜。廟宇的結構極其精密，甚至運用了已失傳的古代技術。普通的建築方法根本無法重現它原本的輝煌。"
        self.story_run(story2_text)
        
    def story_start3(self):  # 遊戲開始的故事顯現
        
        story3_text = "鎮上的長老告訴你一段鮮為人知的傳說：廟宇是祖先的靈魂棲息之地，它的修復需要的不僅是技術，還需要星星的指引。每顆星星都是一位祖先的靈魂化身，只有蒐集到這些星星，才能獲得記載著古代建築祕密的圖紙，幫助廟宇重建。從此，你踏上了尋找星星與修復廟宇的冒險之旅。"
        self.story_run(story3_text)

    def story_start4(self):
    
        story4_text = "星星與圖紙：每顆星星都藏於天地間，只有透過完成三消挑戰才能蒐集到它們。每當蒐集9顆星星，就能拼湊出一部分廟宇的祕密圖紙。這些圖紙記錄了廟宇各部分的構造與細節。"
        self.story_run(story4_text)
    

    def story_9stars(self): # 當星星第一次蒐集到9顆以上 (9,10,11)
        story = ""
        self.story_run(story)

    def story_18stars(self): # 當星星第一次蒐集到18顆以上 (18,19,20)
        story = ""
        self.story_run(story)


    def story_27stars(self): # 當星星第一次蒐集到27顆以上 (27,28,29)
        story = ""
        self.story_run(story)

    def story_36stars(self): # 當星星第一次蒐集到36顆以上 (36,37,38)
        story = ""
        self.story_run(story)
   

    def story_45stars(self): # 當星星蒐集到45顆
        story = ""
        self.story_run(story)











    def story_end(self):
        story_end_text = "隱藏的秘密與終章：當你成功修復廟宇的最後一部分時，星星的光芒匯聚於廟宇上空，點亮了整個小鎮。祖先的靈魂不僅向你道出了感謝，也揭示了一個隱藏已久的真相：靈宿廟的靈氣，來自祖先與後代心靈的連結。每一位努力修復廟宇的人，實際上都在完成一段跨越時空的心靈對話。最終，廟宇恢復了它的榮光，小鎮也重拾了希望。而你，作為這段旅程的見證者與推動者，將永遠被星空與歷史銘記"
        self.story_run(story_end_text)
    

    
    

