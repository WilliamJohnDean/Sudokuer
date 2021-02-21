import pygame, time, argparse
from Grid import Grid

""" TO DO 
    1. Implement animate being optional for the backtrack algorithm
""" 
pygame.font.init()
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("Gamesize", help = "Select the gamesize, accepts 9 or 25.", type = int)
    parser.add_argument("Algorithm", help = "Select the solving algorithm, accepts Backtrack or DLX")
    parser.add_argument("--animate", help = "Backtrack is able to be animated as it goes", action = "store_true")
    args = parser.parse_args()

    if args.animate and args.Algorithm == 'DLX':
        print('Unfortunately, it is currently not possible to animate the DLX Algorithm. More work to come!')
        exit(1)

    winSize = args.Gamesize * 30
    win = pygame.display.set_mode((winSize, winSize))
    pygame.display.set_caption("Sudoku")
    board = Grid(args.Gamesize, args.Gamesize, winSize, winSize, win, args.Algorithm, args.animate) 
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                tick = time.time()
                b = board.solver.solve_gui()
                print(args.Algorithm + ' solution took: ', round(time.time() - tick, 3), ' seconds : ', b)

        # Redraw Window
        win.fill((255,255,255))
        board.draw()
        pygame.display.update()

main()
pygame.quit()