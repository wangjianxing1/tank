import pygame, time, random


class MainGame():
    window = None
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 550

    BACKGROUND_COLOR = pygame.Color(60, 50, 179)
    COLOR_RED = pygame.Color(255, 198, 0)
    # 我的坦克
    TANK_P1 = None

    EnemyTank_list = []
    My_Tank_Bullet_list = []
    Enemy_bullet_list = []
    # 爆炸效果列表
    Explode_list = []
    # 墙壁列表
    Wall_list = []

    def startGame(self):
        pygame.display.init()
        MainGame.window = pygame.display.set_mode((MainGame.SCREEN_WIDTH, MainGame.SCREEN_HEIGHT))
        MainGame.TANK_P1 = self.createMyTank()
        # 创建敌方坦克
        self.createEnemyTank()

        self.createWalls()
        pygame.display.set_caption('坦克大战')
        # 持续刷新窗口
        while True:
            MainGame.window.fill(MainGame.BACKGROUND_COLOR)

            self.getEvent()
            # 将绘制文字得到的小画布，粘贴到窗口中
            MainGame.window.blit(self.getFontSurface('剩余敌方坦克 %d 辆' % len(MainGame.EnemyTank_list)), (5, 5))
            # 展示墙壁
            self.blitWalls()
            # 将我方坦克加入窗口
            if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                MainGame.TANK_P1.displayTank()
            else:
                del MainGame.TANK_P1
                MainGame.TANK_P1 = None
            # 将敌方坦克加入窗口
            self.blitEnemyTank()

            if MainGame.TANK_P1 and not MainGame.TANK_P1.stop:
                MainGame.TANK_P1.move()
                # 调用碰撞墙壁的方法
                MainGame.TANK_P1.hitWalls()
                # 碰撞到敌方坦克
                MainGame.TANK_P1.hitEnemyTank()
            # 调用渲染我方子弹方法
            # self.blitBullet(MainGame.My_Tank_Bullet_list)

            self.blitBullet()
            # 调用渲染敌方子弹方法
            # self.blitBullet(MainGame.Enemy_bullet_list)
            self.blitEnemyBullet()
            # 调用展示爆炸效果
            self.displayExplodes()
            time.sleep(0.01)

            pygame.display.update()

    def createWalls(self):
        for i in range(5):
            wall = Wall(220 * i, 280)
            MainGame.Wall_list.append(wall)

    def blitWalls(self):
        for wall in MainGame.Wall_list:
            if wall.live:
                wall.displayWall()
            else:
                MainGame.Wall_list.remove(wall)

    def createMyTank(self):
        # 创建我方坦克
        # 创建音乐对象
        music = Music('music1/Pop-up Blocked.wav')
        # 调用播放音乐方法
        music.play()
        return MyTank(MainGame.SCREEN_WIDTH / 2 - 30, MainGame.SCREEN_HEIGHT - 80)

    def endGame(self):
        print('谢谢使用')
        exit()

    # 创建敌方坦克
    def createEnemyTank(self):
        # EnemyTank_count = random.randint(2, 6)
        EnemyTank_count = 5
        # left = random.randint(1, EnemyTank_count)
        # top = random.randint(80, 300)
        start_pos = random.randint(80, 105)
        left = 0
        for i in range(EnemyTank_count):
            left += start_pos
            top = 80
            speed = random.randint(1, 4)
            etank = EnemyTank(left, top, speed)
            MainGame.EnemyTank_list.append(etank)

    # 将敌方坦克加入窗口中
    def blitEnemyTank(self):
        for eTank in MainGame.EnemyTank_list:
            if eTank.live:
                eTank.displayTank()
                eTank.randomMove()
                # 调用敌方坦克与墙壁的碰撞方法
                eTank.hitWalls()
                # 撞击我方坦克，停止
                eTank.hitMyTank()
                # 敌方坦克撞敌方坦克，停止
                eTank.hitFriend()
                # 调用敌方坦克射击
                eBullet = eTank.shot()
                # 将子弹存储敌方子弹列表,如果子弹为None，不加入到列表
                if eBullet:
                    MainGame.Enemy_bullet_list.append(eBullet)
            else:
                MainGame.EnemyTank_list.remove(eTank)

    # 将我方子弹加入窗口
    def blitBullet(self):
        for bullet in MainGame.My_Tank_Bullet_list:
            if bullet.live:
                bullet.displayBullet()
                bullet.bulletMove()
                bullet.hitWalls()
                bullet.hitEnemyTank()
            else:
                MainGame.My_Tank_Bullet_list.remove(bullet)

    # 将敌方子弹加入窗口
    def blitEnemyBullet(self):
        for ebullet in MainGame.Enemy_bullet_list:
            if ebullet.live:
                ebullet.displayBullet()
                ebullet.bulletMove()
                ebullet.hitWalls()
                if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                    ebullet.hitMyTank()
            else:
                MainGame.Enemy_bullet_list.remove(ebullet)

    # 获取程序运行所有事件
    def getEvent(self):
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.QUIT:
                self.endGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not MainGame.TANK_P1:
                    print('event.key:', event.key)
                    MainGame.TANK_P1 = self.createMyTank()
                if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        print('向左调头')
                        MainGame.TANK_P1.direction = 'L'
                        MainGame.TANK_P1.stop = False
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        print('向右调头')
                        MainGame.TANK_P1.direction = 'R'
                        MainGame.TANK_P1.stop = False
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        print('向上调头')
                        MainGame.TANK_P1.direction = 'U'
                        MainGame.TANK_P1.stop = False
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        print('向下调头')
                        MainGame.TANK_P1.direction = 'D'
                        MainGame.TANK_P1.stop = False
                    elif event.key == pygame.K_SPACE:
                        if len(MainGame.My_Tank_Bullet_list) < 2:
                            my_bullet = MainGame.TANK_P1.shot()
                            # my_bullet = Bullet(MainGame.TANK_P1)
                            MainGame.My_Tank_Bullet_list.append(my_bullet)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a \
                        or event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_UP \
                        or event.key == pygame.K_w or event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                        MainGame.TANK_P1.stop = True

    def displayExplodes(self):
        for explode in MainGame.Explode_list:
            if explode.live:
                explode.displayExplode()
                time.sleep(0.1)
            else:
                MainGame.Explode_list.remove(explode)

    def getFontSurface(self, text):
        pygame.font.init()
        # fontList = pygame.font.get_fonts()
        # print(fontList)
        font = pygame.font.SysFont('kaiti', 20)
        textSurface = font.render(text, True, MainGame.COLOR_RED)
        return textSurface


class BaseItem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Tank(BaseItem):
    def __init__(self):
        super(BaseItem, self).__init__()
        self.live = True
        self.direction = 'U'
        self.images = {}
        self.speed = 2
        # 指定坦克初始化位置
        self.oldLeft = 100
        self.oldTop = 100

    def move(self):
        # if self.rect.left <= 10 or self.rect.top <= 50 or self.rect.left >= MainGame.SCREEN_WIDTH-80 or self.rect.top >= MainGame.SCREEN_HEIGHT-80:
        #     return
        self.oldLeft = self.rect.left
        self.oldTop = self.rect.top
        if self.direction == 'L' and self.rect.left > 10:
            self.rect.left -= self.speed
        elif self.direction == 'R' and self.rect.left < MainGame.SCREEN_WIDTH - 60:
            self.rect.left += self.speed
        elif self.direction == 'U' and self.rect.top > 30:
            self.rect.top -= self.speed
        elif self.direction == 'D' and self.rect.top < MainGame.SCREEN_HEIGHT - 60:
            self.rect.top += self.speed

    # 撞墙后返回原来位置
    def stay(self):
        self.rect.left = self.oldLeft
        self.rect.top = self.oldTop

    def hitWalls(self):
        for wall in MainGame.Wall_list:
            if pygame.sprite.collide_rect(wall, self):
                self.stay()

    def displayTank(self):
        self.image = self.images[self.direction]
        MainGame.window.blit(self.image, self.rect)


class MyTank(Tank):
    def __init__(self, left, top):
        # Tank.__init__(self, left, top)
        super(MyTank, self).__init__()
        self.images = {
            'U': pygame.image.load('img/mytank_up.jpg'),
            'D': pygame.image.load('img/mytank_down.jpg'),
            'L': pygame.image.load('img/mytank_left.jpg'),
            'R': pygame.image.load('img/mytank_right.jpg')
        }
        self.direction = 'U'
        self.image = self.images[self.direction]
        # 坦克大小
        self.rect = self.image.get_rect()
        print(self.rect)
        # 指定坦克初始化位置
        self.rect.left = left
        self.rect.top = top

        self.speed = 2

        self.stop = True
        self.live = True
        # 记录坦克移动之前的坐标（用于撞墙后坦克还原到原坐标时使用）
        self.oldLeft = self.rect.left
        self.oldTop = self.rect.top

    def shot(self):
        return Bullet(self)

    def hitEnemyTank(self):
        for eTank in MainGame.EnemyTank_list:
            # 敌方坦克撞我方坦克
            if pygame.sprite.collide_rect(self, eTank):
                self.stay()


class EnemyTank(Tank):
    def __init__(self, left, top, speed):
        # Tank.__init__(
        #     self, left, top
        # )
        super(EnemyTank, self).__init__()
        self.images = {
            'U': pygame.image.load('img/enemy_tank_up.jpg'),
            'D': pygame.image.load('img/enemy_tank_down.jpg'),
            'L': pygame.image.load('img/enemy_tank_left.jpg'),
            'R': pygame.image.load('img/enemy_tank_right.jpg')
        }
        self.direction = self.randDirection()
        self.image = self.images[self.direction]
        # 坦克大小
        self.rect = self.image.get_rect()
        print(self.rect)
        # 指定坦克初始化位置
        self.rect.left = left
        self.rect.top = top

        self.speed = speed

        self.stop = True
        self.step = 20

    def randDirection(self):
        num = random.randint(1, 4)
        if num == 1:
            return 'U'
        if num == 2:
            return 'L'
        if num == 3:
            return 'D'
        if num == 4:
            return 'R'

    def randomMove(self):
        if self.step <= 0:
            self.direction = self.randDirection()
            self.step = 60
        else:
            self.move()
            self.step -= 1

    # def displayEnemyTank(self):
    #     super().displayTank()
    def shot(self):
        num = random.randint(1, 500)
        if num < 20:
            return Bullet(self)

    def hitMyTank(self):
        if pygame.sprite.collide_rect(self, MainGame.TANK_P1):
            self.stay()

    # 敌方坦克撞敌方坦克
    def hitFriend(self):
        for eTank in MainGame.EnemyTank_list:
            if eTank is not self and pygame.sprite.collide_rect(self, eTank):
                self.stay()


class Bullet(BaseItem):
    def __init__(self, tank):
        self.image = pygame.image.load('img/bullit.jpg')
        self.direction = tank.direction
        self.rect = self.image.get_rect()
        self.speed = 7
        self.live = True

        if self.direction == 'U':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top - self.rect.height
        elif self.direction == 'D':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.height
        elif self.direction == 'L':
            self.rect.left = tank.rect.left - self.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width / 2
        elif self.direction == 'R':
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width / 2

    def displayBullet(self):
        MainGame.window.blit(self.image, self.rect)

    def bulletMove(self):
        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                self.live = False
        elif self.direction == 'D':
            if self.rect.top < MainGame.SCREEN_HEIGHT - self.rect.height:
                self.rect.top += self.speed
            else:
                self.live = False
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                self.live = False
        elif self.direction == 'R':
            if self.rect.left < MainGame.SCREEN_WIDTH - self.rect.width:
                self.rect.left += self.speed
            else:
                self.live = False

    def hitEnemyTank(self):
        for eTank in MainGame.EnemyTank_list:
            if pygame.sprite.collide_rect(self, eTank):
                # 产生一个爆炸效果
                explode = Explode(eTank)
                MainGame.Explode_list.append(explode)
                self.live = False
                eTank.live = False

    def hitMyTank(self):
        if pygame.sprite.collide_rect(self, MainGame.TANK_P1):
            explode = Explode(MainGame.TANK_P1)
            MainGame.Explode_list.append(explode)
            self.live = False
            MainGame.TANK_P1.live = False
            # del MainGame.TANK_P1
            # MainGame.TANK_P1 = None

    # 子弹与墙壁的碰撞
    def hitWalls(self):
        for wall in MainGame.Wall_list:
            if pygame.sprite.collide_rect(self, wall):
                self.live = False
                wall.hp -= 1
                if wall.hp <= 0:
                    wall.live = False


class Explode():
    def __init__(self, tank):
        self.rect = tank.rect
        self.step = 0
        self.images = [
            pygame.image.load('img/exploy1.jpg'),
            pygame.image.load('img/exploy2.jpg'),
            pygame.image.load('img/exploy3.jpg'),
            pygame.image.load('img/exploy4.jpg')
        ]
        self.image = self.images[self.step]
        self.live = True

    # 展示爆炸效果
    def displayExplode(self):
        if self.step < len(self.images):
            MainGame.window.blit(self.image, self.rect)
            self.image = self.images[self.step]
            self.step += 1
        else:
            self.live = False
            self.step = 0


class Wall(BaseItem):
    def __init__(self, left, top):
        self.image = pygame.image.load('img/steels.jpg')
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        # 判断墙壁是否在窗口中展示
        self.live = True
        # 血量gyt
        self.hp = 100

    def displayWall(self):
        MainGame.window.blit(self.image, self.rect)


class Music():
    def __init__(self, fileName):
        self.fileName = fileName
        pygame.mixer.init()
        pygame.mixer.music.load(self.fileName)

    def play(self):
        pygame.mixer.music.play()


if __name__ == '__main__':
    game = MainGame()
    game.startGame()
