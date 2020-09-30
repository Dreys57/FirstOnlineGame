import pygame
from network import Network
import pickle

pygame.font.init()

windowWidth = 700
windowHeight = 700
window = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Client")


class Button:

    def __init__(self, text, x, y, color):

        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self. width = 150
        self.height = 100

    def DrawButton(self, window):

        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255, 255, 255))

        window.blit(text, (self.x + round(self.width / 2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def ClickButton(self, pos):

        x1 = pos[0]
        y1 = pos[1]

        if (self.x <= x1 <= self.x + self.width) and (self.y <= y1 <= self.y + self.height):

            return True
        else:

            return False


buttons = [Button("Rock", 50, 500, (0, 0, 0)),
           Button("Scissors", 250, 500, (255,0,0)),
           Button("Paper", 450, 500, (0,255,0))]


def RedrawWindow(window, game, p):

    window.fill((128, 128, 128))

    if not(game.Connected()):

        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", 1, (255, 0, 0), True)

        window.blit(text, (windowWidth/2 - text.get_width()/2, windowHeight/2 - text.get_height()/2))

    else:

        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Your Move", 1, (0, 255, 255))

        window.blit(text, (80, 200))

        text = font.render("Opponent", 1, (0, 255, 255))

        window.blit(text, (380, 200))

        moveP1 = game.GetPlayerMove(0)
        moveP2 = game.GetPlayerMove(1)

        if game.AllPlayersChose():

            textP1 = font.render(moveP1, 1, (0 , 0, 0))
            textP2 = font.render(moveP2, 1, (0, 0, 0))

        else:

            if game.p1HasChosen and p == 0:

                textP1 = font.render(moveP1, 1, (0, 0, 0))

            elif game.p1HasChosen:

                textP1 = font.render("Locked in", 1, (0, 0, 0))

            else:

                textP1 = font.render("Waiting...", 1, (0, 0, 0))


            if game.p2HasChosen and p == 1:

                textP2 = font.render(moveP1, 1, (0, 0, 0))

            elif game.p2HasChosen:

                textP2 = font.render("Locked in", 1, (0, 0, 0))

            else:

                textP2 = font.render("Waiting...", 1, (0, 0, 0))

        if p == 1:

            window.blit(textP2, (100, 350))
            window.blit(textP1, (400, 350))

        else:

            window.blit(textP1, (100, 350))
            window.blit(textP2, (400, 350))


        for button in buttons:

            button.DrawButton(window)

    pygame.display.update()


def main():

    run = True
    clock = pygame.time.Clock()
    network = Network()
    player = int(network.getP())
    print("You are player", player)

    while run:

        clock.tick(60)

        try:

            game = network.Send("get")

        except:

            run = False
            print("Couldn't get game")
            break

        if game.AllPlayersChose():

            RedrawWindow(window, game, player)
            pygame.time.delay(500)

            try:

                game = network.Send("reset")

            except:

                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("comicsans", 90)

            if (game.Winner() == 1 and player == 1) or\
                (game.Winner() == 0 and player == 0):

                text = font.render("You have won!", 1, (255, 0, 0))

            elif game.Winner() == -1:

                text = font.render("It's a tie!", 1, (255, 0, 0))

            else:

                text = font.render("You have lost...", 1, (255, 0, 0))

            window.blit(text, (windowWidth/2 - text.get_width()/2, windowHeight/2 - text.get_height()/2))

            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                run = False
                pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    pos = pygame.mouse.get_pos()

                    for button in buttons:

                        if button.ClickButton(pos) and game.Connected():

                            if player == 0:

                                if not game.p1HasChosen:

                                    network.Send(button.text)

                                else:

                                    if not game.p1HasChosen:

                                        network.Send(button.text)

        RedrawWindow(window, game, player)


def MenuScreen():

    run = True
    clock = pygame.time.Clock()

    while run:

        clock.tick(60)
        window.fill((128, 128, 128))

        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Play", 1, (255, 0, 0))

        window.blit(text, (100, 200))
        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()

                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                run = False
    main()


while True:
    MenuScreen()
