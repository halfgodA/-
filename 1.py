import pygame,time,random
class MainGame():
    window = None#游戏主窗口
    SCREEN_WIDTH=1000
    SCREEN_HEIGHT=500
    COLOR_BLACK=pygame.Color(0,0,0)
    COLOR_RED=pygame.Color(255,0,0)
    #创建我方坦克
    P1_TANK=None
    EnemyTank_List=[]#存储敌方坦克
    EnemyTank_count=5
    #存储我方子弹的列表
    Bullet_List=[]
    Enemy_Bullet_List=[]
    def __init__(self):
        pass
    def startGame(self):
        pygame.display.init()#初始化
        MainGame.window=pygame.display.set_mode([MainGame.SCREEN_WIDTH,MainGame.SCREEN_HEIGHT])#显示窗口
        MainGame.P1_TANK=Tank(400,300)#创建我方坦克
        self.createEnemyTank()

        #设置游戏标题
        #开始游戏方法
        pygame.display.set_caption("坦克大战v1.03")
        while True:
            MainGame.window.fill(MainGame.COLOR_BLACK)
            self.getEvent()
            MainGame.window.blit(self.getTextSurface("剩余敌方坦克%d"%len(MainGame.EnemyTank_List)),(5,5))#文档的内容和位置
            MainGame.P1_TANK.displayTank()#我的坦克的打印
            MainGame.blitEnemyTank(self)
            if MainGame.P1_TANK and not MainGame.P1_TANK.stop:
                MainGame.P1_TANK.move()
            self.blitBullet()
            self.blitEnemyBullet()
            time.sleep(0.02)#减慢循环的速度 优化坦克的移动
            pygame.display.update()
    #创建敌方坦克
    def createEnemyTank(self):
        for i in range(MainGame.EnemyTank_count):
            speed = random.randint(1, 4)
            enemyTank=EnemyTank(random.randint(0,MainGame.SCREEN_WIDTH),random.randint(0,MainGame.SCREEN_HEIGHT),speed)
            MainGame.EnemyTank_List.append(enemyTank)
    def blitEnemyTank(self):
        for enemyTank in MainGame.EnemyTank_List:
            if enemyTank.live == True:
              enemyTank.displayTank()
              enemyTank.randMove()
              enemyBullet = enemyTank.shot()
              if enemyBullet:
                  MainGame.Enemy_Bullet_List.append(enemyBullet)
            else:
                MainGame.EnemyTank_List.remove(enemyTank)
    def blitBullet(self):
        for bullet in MainGame.Bullet_List:
            if bullet.live == False:
                MainGame.Bullet_List.remove(bullet)
            else:
                bullet.displayBullet()
                bullet.Bulletmove()
                bullet.hitEnemyTank()
    def blitEnemyBullet(self):
        for enemyBullet in MainGame.Enemy_Bullet_List:
            if enemyBullet.live == False:
                MainGame.Enemy_Bullet_List.remove(enemyBullet)
            else:
                enemyBullet.displayBullet()
                enemyBullet.Bulletmove()
    def getEvent(self):#获取一切事件
        eventlist=pygame.event.get()#获取所有事件
        for event in eventlist:
            #判断事件是不是退出
            if event.type == pygame.QUIT:
                self.endGame()
            #判断事件类型是不是按下 按下的哪种
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    print("向左掉头")
                    MainGame.P1_TANK.direction = 'L'
                    MainGame.P1_TANK.stop = False
                elif event.key == pygame.K_RIGHT:
                    print("向右掉头")
                    MainGame.P1_TANK.direction = 'R'
                    MainGame.P1_TANK.stop = False
                elif event.key == pygame.K_UP:
                    print("向上掉头")
                    MainGame.P1_TANK.direction = 'U'
                    MainGame.P1_TANK.stop = False
                elif event.key == pygame.K_DOWN:
                    print("向下掉头")
                    MainGame.P1_TANK.direction = 'D'
                    MainGame.P1_TANK.stop = False
                elif event.key == pygame.K_SPACE:
                    print("发射子弹")
                    if len(MainGame.Bullet_List) < 3:
                      m = Bullet(MainGame.P1_TANK)
                      MainGame.Bullet_List.append(m)
                    else:
                        print("子弹数量不足")
                    print("当前屏幕中子弹的数量为%d"%len(MainGame.Bullet_List))
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:
                  MainGame.P1_TANK.stop=True
    def getTextSurface(self,text):
        #初始化字体
        pygame.font.init()
        #选中合适字体
        font=pygame.font.SysFont('kaiti',18)
        #使用对应的字符完成相关内容的呈现
        textSurface=font.render(text,True,MainGame.COLOR_RED)
        return textSurface
    def endGame(self):
        #结束游戏方法
        print("谢谢使用")
        exit()#结束python解释器
class BaseItem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Tank(BaseItem):
    def __init__(self,left,top):
        self.images={
            'U':pygame.image.load("C:\\Users\dell\PycharmProjects\pythonProject\pygame\p1tankU.gif"),
            'D':pygame.image.load("C:\\Users\dell\PycharmProjects\pythonProject\pygame\p1tankD.gif"),
            'L':pygame.image.load("C:\\Users\dell\PycharmProjects\pythonProject\pygame\p1tankL.gif"),
            'R':pygame.image.load("C:\\Users\dell\PycharmProjects\pythonProject\pygame\p1tankR.gif")
        }
        #坦克所在区域

        self.direction='U'#默认方向
        self.image=self.images[self.direction]
        self.rect=self.image.get_rect()
        self.rect.left=left
        self.rect.top=top
        self.speed =5
        self.stop = True#坦克的移动开关
        self.live = True

    def move(self):
        #移动
        if self.direction == 'L':
            if self.rect.left >0:
              self.rect.left -= self.speed
        elif self.direction =='R':
            if self.rect.left + self.rect.height < MainGame.SCREEN_WIDTH:
              self.rect.left += self.speed
        elif self.direction =='U':
            if self.rect.top >0:
              self.rect.top -= self.speed
        elif self.direction =='D':
            if self.rect.top +self.rect.height < MainGame.SCREEN_HEIGHT:
              self.rect.top += self.speed
    def shot(self):
        return Bullet(self)
        #射击
        pass
    def displayTank(self):
        #展示
        #重新设置坦克图片
        self.image=self.images[self.direction]
        #将坦克加入窗口中
        MainGame.window.blit(self.image,self.rect)
class MyTank(Tank):
    def __init__(self):
        pass
class EnemyTank(Tank):
    def __init__(self,left,top,speed):
        super(EnemyTank,self).__init__(left,top)
        #图片集
        self.images = {
            'U': pygame.image.load("C:\\Users\dell\PycharmProjects\pythonProject\pygame\p2tankU.gif"),
            'D': pygame.image.load("C:\\Users\dell\PycharmProjects\pythonProject\pygame\p2tankD.gif"),
            'L': pygame.image.load("C:\\Users\dell\PycharmProjects\pythonProject\pygame\p2tankL.gif"),
            'R': pygame.image.load("C:\\Users\dell\PycharmProjects\pythonProject\pygame\p2tankR.gif")
        }
        # 坦克所在区域
        self.direction = self.randDirction()
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.speed = speed
        self.stop=True
        self.step=50
    #随即移动，在某个方向移动一定距离的时候，随即更改自己的移动方向
    def randDirction(self):
        #随机方向
        self.direction = random.choice(['U', 'D', 'L', 'R'])
        return self.direction
    def randMove(self):
        if self.step <=0:
            self.direction=self.randDirction()
            self.step = 50
        else:
            self.move()
            self.step -= 1
    def displayTank(self):
        super().displayTank()#继承父类的
    def shot(self):
        num = random.randint(0, 1000)
        if num <= 20:
            return Bullet(self)

class Bullet(BaseItem):
    def __init__(self,tank):
        self.image = pygame.image.load("C:\\Users\dell\PycharmProjects\pythonProject\pygame\enemymissile.gif")#子弹图片
        self.direction=tank.direction
        self.rect=self.image.get_rect()
        self.speed=7
        #用来记录子弹是否碰撞
        self.live = True
        #子弹的初始位置
        if self.direction == 'L':
            self.rect.left =tank.rect.left-self.rect.width/2-self.rect.width/2
            self.rect.top=tank.rect.top+tank.rect.width/2-self.rect.width/2
        if self.direction == 'D':
            self.rect.left=tank.rect.left+tank.rect.width/2-self.rect.width/2
            self.rect.top=tank.rect.top+tank.rect.height
        elif self.direction == 'R':
            self.rect.left=tank.rect.left+tank.rect.width
            self.rect.top=tank.rect.top+tank.rect.width/2-self.rect.width/2
        elif self.direction == 'U':
            self.rect.left=tank.rect.left+tank.rect.width/2-self.rect.width/2
            self.rect.top=tank.rect.top-self.rect.height

    def Bulletmove(self):
        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                #修改状态值
                self.live = False
        elif self.direction == 'D':
            if self.rect.top < MainGame.SCREEN_HEIGHT - self.rect.height:
                self.rect.top += self.speed
            else:
                self.live = False
        elif self.direction == 'L':
            if self.rect.left>0:
                self.rect.left -= self.speed
            else:
                self.live = False
        elif self.direction == 'R':
            if self.rect.left < MainGame.SCREEN_WIDTH - self.rect.width:
                self.rect.left += self.speed
            else:
                self.live = False
    def displayBullet(self):
        MainGame.window.blit(self.image,self.rect)
    #我方子弹碰撞敌方坦克
    def hitEnemyTank(self):
        for enemyTank in MainGame.EnemyTank_List:
            if pygame.sprite.collide_rect(self,enemyTank):
                self.live = False
                enemyTank.live = False
                #MainGame.score += 100
class Explode():
    def __init__(self):
        pass
    def displayExplode(self):
        pass
class Wall():
    def __init__(self):
        pass
    def displayWall(self):
        pass
class Music():
    def __init__(self):
        pass
    def play(self):
        #开始播放音乐
        pass
MainGame().startGame()
