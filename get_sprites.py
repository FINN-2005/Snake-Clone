from mine.pygame_template import *


CELL_SIZE = 40
CELL_NUM = 20



def get_apple(size=(CELL_SIZE, CELL_SIZE)):
    surf = pygame.Surface(size, pygame.SRCALPHA)
    rect = surf.get_frect()

    # apple base
    pygame.draw.circle(surf, 'red', rect.center, rect.w / 2 - (0.1 * rect.w))
    
    # apple stem
    stem_width = rect.w * 0.16
    stem_height = rect.h * 0.3
    stem = pygame.Surface((stem_width, stem_height), pygame.SRCALPHA)
    pygame.draw.rect(stem, (107, 65, 50, 255), (0,0,stem_width,stem_height), 0, 5)
    stem_rect = stem.get_frect()
    stem_rect.centerx = rect.centerx
    stem_rect.top = rect.top
    surf.blit(stem, stem_rect)

    # apple leaf
    leaf_width = rect.w * 0.35
    leaf_height = rect.h * 0.1
    leaf = pygame.Surface((leaf_width, leaf_height), pygame.SRCALPHA)
    pygame.draw.ellipse(leaf, (0, 200, 0), (0, 0, leaf_width, leaf_height))
    leaf = pygame.transform.rotate(leaf, 45)
    leaf_rect = leaf.get_frect()
    leaf_rect.centerx = rect.centerx + stem_rect.w
    leaf_rect.top = rect.top 
    surf.blit(leaf, leaf_rect)

    return surf, rect

def get_snake(size=(CELL_SIZE, CELL_SIZE)):
    images = dict()
    rects = dict()

    # head up
    surf = pygame.Surface(size, pygame.SRCALPHA)
    rect = surf.get_frect()
    base_rect = pygame.FRect((0,0), (rect.w*(0.6667), rect.h*(0.6667)))
    base_rect.midbottom = rect.midbottom
    base_rect.bottom += 1
    pygame.draw.circle(surf, (0,102,255,255), V2(base_rect.midtop) + V2(-1,0), rect.w * (0.3255), 0)
    pygame.draw.rect(surf, (0,102,255,255), base_rect)
    pygame.draw.circle(surf, (0,102,255,255), base_rect.midleft, base_rect.w * (0.25), 0)
    pygame.draw.circle(surf, (0,102,255,255), base_rect.midright, base_rect.w * (0.25), 0)
    pygame.draw.circle(surf, (255,255,255,255), base_rect.midleft, base_rect.w * (0.18), 0)
    pygame.draw.circle(surf, (255,255,255,255), base_rect.midright, base_rect.w * (0.18), 0)
    pygame.draw.circle(surf, (0,102,255,255), V2(base_rect.midleft) - V2(0, base_rect.h * 0.18 / 2), base_rect.w * (0.08), 0)
    pygame.draw.circle(surf, (0,102,255,255), V2(base_rect.midright) - V2(0, base_rect.h * 0.18 / 2), base_rect.w * (0.08), 0)
    images['head up'] = surf.copy()
    rects['head up'] = rect.copy()

    # head right
    images['head right'] = pygame.transform.rotate(surf, -90).copy()
    rects['head right'] = rect.copy()

    # head down
    images['head down'] = pygame.transform.rotate(surf, -180).copy()
    rects['head down'] = rect.copy()

    # head left
    images['head left'] = pygame.transform.rotate(surf, 90).copy()
    rects['head left'] = rect.copy()


    # tail up
    surf = pygame.Surface(size, pygame.SRCALPHA)
    rect = surf.get_frect()
    base_rect = pygame.FRect((0,0), (rect.w*(0.6667), rect.h*(0.6667)))
    base_rect.midbottom = rect.midbottom
    base_rect.bottom += 1
    base_rect.left += 1
    pygame.draw.circle(surf, (0,102,255,255), V2(base_rect.midtop) + V2(-1,0), rect.w * (0.3252), 0)
    pygame.draw.rect(surf, (0,102,255,255), base_rect)
    images['tail up'] = surf.copy()
    rects['tail up'] = rect.copy()

    # tail right
    images['tail right'] = pygame.transform.rotate(surf, -90).copy()
    rects['tail right'] = rect.copy()

    # tail down
    images['tail down'] = pygame.transform.rotate(surf, -180).copy()
    rects['tail down'] = rect.copy()

    # tail left
    images['tail left'] = pygame.transform.rotate(surf, 90).copy()
    rects['tail left'] = rect.copy()


    # body vertical
    surf = pygame.Surface(size, pygame.SRCALPHA)
    rect = surf.get_frect()
    base_rect = pygame.FRect((0,0), (rect.w*(0.6667), rect.h + 1))
    base_rect.midbottom = rect.midbottom
    base_rect.bottom += 1
    base_rect.left += 1
    pygame.draw.rect(surf, (0,102,255,255), base_rect)
    images['body vertical'] = surf.copy()
    rects['body vertical'] = rect.copy()

    # body horizontal
    images['body horizontal'] = pygame.transform.rotate(surf, 90).copy()
    rects['body horizontal'] = rect.copy()

    # corner topright
    surf = pygame.Surface(size, pygame.SRCALPHA)
    rect = surf.get_frect()
    base_rect = pygame.FRect((0,0), (rect.w*(0.5), rect.h*(0.6667)))
    base_rect.midleft = rect.midleft
    base_rect.y += 2
    pygame.draw.rect(surf, (0,102,255,255), base_rect)
    base_rect = pygame.FRect((0,0), (rect.w*(0.6667), rect.h*(0.5)))
    base_rect.midbottom = rect.midbottom
    pygame.draw.rect(surf, (0,102,255,255), base_rect)
    pygame.draw.circle(surf, (0,102,255,255), rect.bottomleft, rect.w/3)
    pygame.draw.circle(surf, (0,0,0,0), rect.bottomleft, (rect.h - base_rect.h - 7) / 2)
    pygame.draw.circle(surf, (0,102,255,255), V2(base_rect.x, base_rect.top) + V2(base_rect.h/2 + 3, 2), rect.h*(0.3333))    
    images['corner topright'] = surf.copy()
    rects['corner topright'] = rect.copy()

    # corner topleft
    images['corner topleft'] = pygame.transform.rotate(surf, 90).copy().copy()
    rects['corner topleft'] = rect.copy()

    # corner bottomleft
    images['corner bottomleft'] = pygame.transform.rotate(surf, 180).copy().copy()
    rects['corner bottomleft'] = rect.copy()

    # corner bottomright
    images['corner bottomright'] = pygame.transform.rotate(surf, -90).copy().copy()
    rects['corner bottomright'] = rect.copy()

    return images, rects


if __name__ == '__main__':
    class run(APP):
        def setup(self):
            self.images, self.rects = get_snake()

        def draw(self):
            x = 40
            for image, rect in zip(self.images.values(), self.rects.values()):
                rect.x = x
                rect.y = APP.HW
                self.screen.blit(image, rect)
                x += rect.w + 10


    run()