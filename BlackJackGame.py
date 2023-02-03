from BlackJackClasses import *
import time


def createPlayers():
    players = []
    for i in range(4):
        if i == 0:
            player = House()
        else:
            player = Player(1000, i)
        players.append(player)
    return players


def setupBack(win: GraphWin):
    win.setBackground("maroon")
    felt = Circle(Point(win.getWidth() // 2, win.getHeight()), win.getHeight())
    felt.setFill("forest green")
    felt.setOutline("saddle brown")
    felt.setWidth(10)
    felt.draw(win)
    for i in range(3):
        section = Rectangle(Point(0, win.getHeight()), Point((win.getWidth() // 3) * (i+1), win.getHeight() - 300))
        section.setWidth(15)
        section.draw(win)


def HitOrStand(player):
    win = GraphWin("Hit Or Stand", 200, 100)
    Text(Point(100, 20), f"What will {player.name} do").draw(win)
    hitBox = Rectangle(Point(0, 30), Point(100, 100))
    hitBox.setFill("Green")
    hitBox.setActiveFill("Green1")
    hitBox.draw(win)
    hitText = Text(Point(50, 65), "Hit")
    hitText.setTextColor("white")
    hitText.setSize(30)
    hitText.draw(win)
    standBox = Rectangle(Point(100, 30), Point(200, 100))
    standBox.setFill("Blue")
    standBox.setActiveFill("Blue1")
    standBox.draw(win)
    standText = Text(Point(150, 65), "Stand")
    standText.setTextColor("White")
    standText.setSize(30)
    standText.draw(win)
    while not win.closed:
        click = win.getMouse()
        if Rectangle.testCollision_RectVsPoint(hitBox, click):
            win.close()
            standBox.undraw()
            standText.undraw()
            hitBox.undraw()
            hitText.undraw()
            return True
        elif Rectangle.testCollision_RectVsPoint(standBox, click):
            win.close()
            standBox.undraw()
            standText.undraw()
            hitBox.undraw()
            hitText.undraw()
            return False


if __name__ == '__main__':
    players = createPlayers()
    win = GraphWin("Black Jack", 1000, 600)
    setupBack(win)
    for player in players:
        player.dispPlayerInfo(win)
    while not win.closed and len(players) > 1:
        bets = []
        for player in players:
            player.updateInfo()
        for i in range(len(players)-1, 0, -1):
            bet = players[i].getBet()
            bets.insert(0, bet)
        print(bets)
        for i in range(2):
            for player in players:
                players[0].dealCards(player, win)
        for i in range(len(players)-1, 0, -1):
            playerTurn = True
            while playerTurn:
                if HitOrStand(players[i]):
                    players[0].dealCards(players[i], win)
                    players[i].updateInfo()
                    if players[i].busted:
                        players[i].bust(win)
                        playerTurn = False
                else:
                    playerTurn = False
        players[0].uncover()
        while players[0].getHandValue() <= 16:
            players[0].dealCards(players[0], win)
            players[0].updateInfo()
            time.sleep(.5)
        for i in range(len(players)-1, 0, -1):
            if not players[i].busted:
                if players[i].getHandValue() > players[0].getHandValue() or players[0].busted:
                    players[i].money += bets[i - 1] * 2
                elif players[i].getHandValue() == players[0].getHandValue():
                    players[i].money += bets[i - 1]
                if players[i].getHandValue() == 21 and len(players[i].hand) == 2:
                    players[i].money += bets[i - 1] // 2
                players[i].updateInfo()
        win.getMouse()
        for i in range(len(players)-1, 0, -1):
            if players[i].money <= 0:
                players[0].reset([players[i]])
                players.pop(i)
        players[0].reset(players)
