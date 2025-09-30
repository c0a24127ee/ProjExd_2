import os
import sys
import pygame as pg
import random
import time


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectかばくだんRect
    戻り値：判定結果タプル（縦方向, 横方向）
    画面内ならTrue/画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向にはみ出ていたら
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向にはみ出ていたら
        tate = False
    return yoko, tate  # 縦横方向の真理値タプル

def gameover(screen:pg.Surface) -> None:  # ゲームオーバー画面
    bo_img = pg.Surface((WIDTH, HEIGHT))  # 空のSurface
    pg.draw.rect(bo_img, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    bo_img.set_alpha(200)  # 透明度
    font = pg.font.Font(None, 80)
    txt = font.render("GAMEOVER", True, (255, 255, 255))  # テキスト
    txt_rct = txt.get_rect()
    txt_rct.center = WIDTH // 2, HEIGHT // 2
    bo_img.blit(txt, txt_rct)
    kkk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    kkk_rct1 = kkk_img.get_rect()
    kkk_rct1.center = WIDTH // 2 - 200, HEIGHT // 2  # 左
    bo_img.blit(kkk_img, kkk_rct1)

    kkk_rct2 = kkk_img.get_rect()
    kkk_rct2.center = WIDTH // 2 + 200, HEIGHT // 2  # 右
    bo_img.blit(kkk_img, kkk_rct2)

    screen.blit(bo_img, (0, 0))
    pg.display.update()
    time.sleep(5)

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_imgs = []

    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    bb_accs = [a for a in range(1, 11)] # 加速度のリスト
    
    return bb_imgs, bb_accs

    


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")

    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20,20))  # 空のSurface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 赤い円
    bb_img.set_colorkey((0, 0, 0))  # 四隅の黒いのが消える
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)  # 爆弾座標
    vx, vy = +5, +5  # 爆弾の速度
    

    
    clock = pg.time.Clock()
    tmr = 0
    bb_imgs, bb_accs = init_bb_imgs()
    avx = vx * bb_accs[min(tmr//500, 9)]
    bb_img = bb_imgs[min(tmr//500, 9)]
    
    
    while True:
        bb_imgs, bb_accs = init_bb_imgs()
        avx = vx * bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return  # ゲームオーバー

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]  # 横方向
                sum_mv[1] += mv[1]  # 縦方向
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)



        
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        bb_rct.move_ip(vx,vy)
        yoko,tate = check_bound(bb_rct)
        if not yoko:  # 横方向にはみ出ていたら
            vx *=-1       
        if not tate:  # 縦方向にはみ出ていたら
            vy *=-1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
    
