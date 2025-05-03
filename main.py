from get_sprites import *

FONT = get_Font(50)
smol_FONT = get_Font()



class Fruit(Sprite):
    def __init__(self, *groups, pos=None, color=(240,0,0,255), is_snake=False):
        super().__init__(*groups)
        
        if pos is not None: self.pos = pos
        else: self.pos = V2(random.randint(0,CELL_NUM - 1),random.randint(0,CELL_NUM - 1))
        self.is_snake = is_snake

        self.image, self.rect = get_apple()
        self.rect.topleft = (self.pos.x * CELL_SIZE, self.pos.y * CELL_SIZE)

    def randomise(self, positions):
        self.pos = positions[0]
        while self.pos in positions: self.pos = V2(random.randint(0,CELL_NUM - 1),random.randint(0,CELL_NUM - 1))
        self.rect.topleft = (self.pos.x * CELL_SIZE, self.pos.y * CELL_SIZE)

    def draw(self, screen):
        if not self.is_snake:
            screen.blit(self.image, self.rect)



class Snake(Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        self.positions = [V2(5,10),V2(4,10),V2(3,10)]
        self.body = [Fruit(pos=pos, color=(110,208,140,255), is_snake=True) for pos in self.positions]
        self.direction = V2(1,0)

        self.images, _ = get_snake()
        self.new_block = False
        
    def draw(self, screen):
        for i, body in enumerate(self.body):
            # head
            if i == 0:
                direction = self.positions[i] - self.positions[i+1]
                if direction == V2(1,0): self.head = self.images['head right']
                elif direction == V2(-1,0): self.head = self.images['head left']
                elif direction == V2(0,1): self.head = self.images['head down']
                else: self.head = self.images['head up']
                screen.blit(self.head, body.rect)
            # tail
            elif i == len(self.positions) - 1:
                direction = self.positions[i] - self.positions[i-1]
                if direction == V2(1,0): self.tail = self.images['tail right']
                elif direction == V2(-1,0): self.tail = self.images['tail left']
                elif direction == V2(0,1): self.tail = self.images['tail down']
                else: self.tail = self.images['tail up']
                screen.blit(self.tail, body.rect)
            # body
            else:
                a = self.positions[i-1]
                b = self.positions[i]
                c = self.positions[i+1]
                # straight
                if b.x == a.x == c.x: self.body_piece = self.images['body vertical']
                elif b.y == a.y == c.y: self.body_piece = self.images['body horizontal']
                # corner
                elif a - b == V2(0,1) and b - c == V2(1,0): self.body_piece = self.images['corner topright']
                elif a - b == V2(-1,0) and b - c == V2(0,-1): self.body_piece = self.images['corner topright']
                elif a - b == V2(1,0) and b - c == V2(0,-1): self.body_piece = self.images['corner topleft']
                elif a - b == V2(0,1) and b - c == V2(-1,0): self.body_piece = self.images['corner topleft']
                elif a - b == V2(0,-1) and b - c == V2(1,0): self.body_piece = self.images['corner bottomright']
                elif a - b == V2(-1,0) and b - c == V2(0,1): self.body_piece = self.images['corner bottomright']
                elif a - b == V2(1,0) and b - c == V2(0,1): self.body_piece = self.images['corner bottomleft']
                elif a - b == V2(0,-1) and b - c == V2(-1,0): self.body_piece = self.images['corner bottomleft']
                else: self.body_piece = self.images['head up']
                screen.blit(self.body_piece, body.rect)

    def move(self):
        if self.new_block: return self.add_block()
        self.positions = [self.positions[0] + self.direction] + self.positions[:-1]
        self.copy_body = [Fruit(pos=self.positions[0], color=(110,208,140,255), is_snake=True)] + self.body[:-1]
        self.tail = self.body[-1]
        self.tail.kill()
        self.body = self.copy_body

        self.has_moved = True

    def add_block(self):
        self.positions = [self.positions[0] + self.direction] + self.positions[:]
        self.copy_body = [Fruit(pos=self.positions[0], color=(110,208,140,255), is_snake=True)] + self.body[:]
        self.body = self.copy_body
        self.new_block = False

        self.has_moved = True


class MainGameLogic:
    def __init__(self):
        self.group = Group()
        self.fruit = Fruit(self.group)
        self.snake = Snake(self.group)

        self.game_over = False
        self.score = 00

    def draw(self, screen):
        self.group.draw()
        surf = smol_FONT.render(f'SCORE: {self.score}', True, 'white')
        rect = surf.get_frect()
        rect.left = rect.h * 0.5
        rect.top = rect.h * 0.5
        screen.blit(surf, rect)
    
    def update(self):
        self.group.update()

    def update_events(self):
        self.snake.move()
        self.check_fruit_collision()
        self.check_wall_collision()
        self.check_self_collision()

    def check_fruit_collision(self):
        if self.fruit.pos == self.snake.positions[0]:
            self.fruit.randomise(self.snake.positions)
            self.snake.new_block = True
            self.score += 1

    def check_wall_collision(self):
        if not (0 <= self.snake.positions[0].x < CELL_NUM and 0 <= self.snake.positions[0].y < CELL_NUM):
            self.game_over = True

    def check_self_collision(self):
        for pos in self.snake.positions[1:]:
            if pos == self.snake.positions[0]:
                self.game_over = True
                break



class run(APP):
    def init(self):
        self.WIDTH = CELL_SIZE * CELL_NUM
        self.HEIGHT = CELL_SIZE * CELL_NUM

    def setup(self):
        self.SCREEN_EVENT = pygame.USEREVENT
        pygame.time.set_timer(self.SCREEN_EVENT, 150)

        self.main = MainGameLogic()

    def event(self, e):
        if not self.main.game_over: 
            if e.type == self.SCREEN_EVENT:
                self.main.update_events()
            if e.type == pygame.KEYDOWN and self.main.snake.has_moved:
                if e.key == pygame.K_w and not self.main.snake.direction.y > 0:
                    self.main.snake.direction = V2(0,-1)
                    self.main.snake.has_moved = False
                elif e.key == pygame.K_s and not self.main.snake.direction.y < 0:
                    self.main.snake.direction = V2(0,1)
                    self.main.snake.has_moved = False
                elif e.key == pygame.K_a and  not self.main.snake.direction.x > 0:
                    self.main.snake.direction = V2(-1,0)
                    self.main.snake.has_moved = False
                elif e.key == pygame.K_d and not self.main.snake.direction.x < 0:
                    self.main.snake.direction = V2(1,0)
                    self.main.snake.has_moved = False
        else: 
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    del self.main
                    self.main = MainGameLogic()
            

    def update(self):
        if not self.main.game_over: 
            self.main.update()

    def draw(self):
        self.main.draw(self.screen)

        if self.main.game_over:
            
            surf = FONT.render('GAME OVER', True, 'white', 'black')
            rect = surf.get_frect()
            rect.left = APP.HW - rect.w / 2
            rect.bottom = APP.HH - rect.h * 3

            smol_surf = smol_FONT.render('press SPACE to try again!', True, 'white', 'black')
            smol_rect = smol_surf.get_frect()
            smol_rect.left = APP.HW - smol_rect.w / 2
            smol_rect.bottom = APP.HH - smol_rect.h

            self.screen.blit(surf, rect)
            self.screen.blit(smol_surf, smol_rect)




if __name__ == '__main__':
    run()