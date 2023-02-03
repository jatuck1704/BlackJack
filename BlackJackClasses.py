from graphics import *
import random


class Card:
    """A single card from the deck, should have a suit, number and value"""
    def __init__(self, suit, face, value):
        self.suit = suit
        self.face = face
        self.value = value
        self.card = []

    def __str__(self):
        return f"Card[{self.face} of {self.suit}s, value: {self.value}]"

    def drawCard(self, x, y, win: GraphWin):
        card = RoundedRectangle(Point(x, y), Point(x + 100, y + 150), 10)
        card.setFill("white")
        number = Text(Point(x + 20, y + 20), f"{self.face[0]}")
        suit = Text(Point(x + 20, y + 50), f"{self.suit[0]}")
        if self.face == "10":
            number = Text(Point(x + 20, y + 20), f"10")
        if self.suit == "Heart" or self.suit == "Diamond":
            number.setTextColor("Red")
            suit.setTextColor("Red")
        number.setSize(20)
        suit.setSize(20)
        self.card.append(card)
        self.card.append(number)
        self.card.append(suit)
        for part in self.card:
            part.draw(win)

    def undrawCard(self):
        for i in range(len(self.card)):
            self.card[-1].undraw()
            self.card.pop(-1)


class Deck:
    def __init__(self):
        self.cards = []
        self.addCards()
        self.shuffle()

    def __str__(self):
        output = "Deck of Cards, Cards:"
        for card in self.cards:
            output += "\n" + str(card)
        output += "\n" + "Number of Cards:" + str(len(self.cards))
        return output

    def addCards(self):
        suits = ["Heart", "Spade", "Club", "Diamond"]
        faces = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
        for suit in suits:
            for i in range(13):
                if i == 0:
                    value = 11
                elif i >= 9:
                    value = 10
                else:
                    value = i + 1
                self.cards.append(Card(suit, faces[i], value))

    def shuffle(self):
        newDeck = []
        for i in range(len(self.cards)):
            newDeck.append(self.cards.pop(random.randrange(len(self.cards))))
        self.cards = newDeck


class Player:
    def __init__(self, money, playerNum):
        self.hand = []
        self.playerNumber = playerNum
        self.value = 0
        self.money = money
        if playerNum == 0:
            self.name = "House"
        else:
            self.name = self.getName()
        self.busted = False
        self.valueText = Text(Point(260 + 333 * (self.playerNumber - 1), 575), f"Hand Value: ")
        self.moneyText = Text(Point(160 + 333 * (self.playerNumber - 1), 575), f"Money: {self.money}")
        self.nameText = Text(Point(60 + 333 * (self.playerNumber - 1), 575), f"Money: {self.name.upper()}")
        self.valueText.setSize(10)
        self.nameText.setSize(10)
        self.moneyText.setSize(10)
        self.moneyText.setTextColor("white")
        self.nameText.setTextColor("white")
        self.valueText.setTextColor("white")
        self.bustText = Text(Point(166 * (self.playerNumber * 2 - 1), 400), "BUST!")
        self.bustText.setSize(30)
        self.bustText.setTextColor("Red")

    def __str__(self):
        output = f"Player[Name: {self.name}, Hand: "
        for card in self.hand:
            output += str(card) + ", "
        output += f"Hand Value: {self.value}]"

    def addCard(self, card, win):
        self.hand.append(card)
        self.drawHand(win)
        self.getHandValue()

    def drawHand(self, win):
        centerX = win.getWidth() // 6 * (self.playerNumber * 2 - 1)

        for i in range(len(self.hand)):
            self.hand[i].undrawCard()
            self.hand[i].drawCard(centerX - (60 * len(self.hand)//2) + (60 * i), 400, win)

    def getName(self):
        win = GraphWin("Player Name", 200, 200)
        namePrompt = Text(Point(win.getWidth() // 2, win.getHeight() // 2 - 50), f"Player {self.playerNumber}'s Name?")
        namePrompt.draw(win)
        nameEntry = Entry(Point(win.getWidth() // 2, win.getHeight() // 2), 20)
        nameEntry.draw(win)
        button = Circle(Point(win.getWidth() // 2 , win.getHeight() // 2 + 40), 15)
        button.setFill("Green")
        button.draw(win)
        while not win.closed:
            click = win.checkMouse()
            if click != None:
                if Circle.testCollision_CircleVsPoint(button, click):
                    name = nameEntry.getText()
                    win.close()
        return name

    def getBet(self):
        win = GraphWin("Place Your Bet", 200, 200)
        betEntry = Entry(Point(100, 100), 15)
        betEntry.draw(win)
        Text(Point(100, 50), f"{self.name.title()}, Place Your Bet").draw(win)
        Text(Point(100, 125), f"Available Money: {self.money}").draw(win)
        while win.checkKey() != "Return" or int(betEntry.getText()) > self.money:
            pass
        self.money -= int(betEntry.getText())
        win.close()
        self.updateInfo()
        return int(betEntry.getText())

    def dispPlayerInfo(self, win):
        self.nameText.draw(win)
        self.moneyText.draw(win)
        self.valueText.draw(win)

    def updateInfo(self):
        self.moneyText.setText(f"Money: {self.money}")
        self.valueText.setText(f"Hand Value: {self.getHandValue()}")

    def bust(self, win):
        self.bustText.draw(win)

    def getHandValue(self):
        value = 0
        for card in self.hand:
            value += card.value
        if value > 21:
            for card in self.hand:
                if card.value == 11:
                    card.value = 1
                    value -= 10
                    return value
            if value > 21:
                self.busted = True
        return value


class House(Player):
    def __init__(self):
        super().__init__(0, 0)
        self.name = "House"
        self.deck = Deck()
        self.cover = RoundedRectangle(Point(500, 100), Point(600, 250), 10)
        self.valueText = Text(Point(500, 75), "House Value: ")
        self.valueText.setTextColor("White")
        self.valueText.setSize(15)
        self.cover.setFill("Black")
        self.covered = False

    def dealCards(self, player: Player, win):
        player.addCard(self.deck.cards.pop(0), win)
        player.updateInfo()

    def drawHand(self, win):
        centerX = 500
        for i in range(len(self.hand)):
            self.hand[i].undrawCard()
            self.hand[i].drawCard((centerX - (60 * len(self.hand) // 2) + (60 * i)), 100, win)
        if len(self.hand) == 2:
            self.drawCover(win)

    def drawCover(self, win):
        self.cover.draw(win)
        self.covered = True

    def uncover(self):
        self.cover.undraw()
        self.covered = False
        self.updateInfo()

    def dispPlayerInfo(self, win):
        self.valueText.draw(win)

    def updateInfo(self):
        if not self.covered:
            self.valueText.setText(f"House Value: {self.getHandValue()}")

    def reset(self, playerList):
        for player in playerList:
            for i in range(len(player.hand)):
                card = player.hand.pop(0)
                card.undrawCard()
                self.deck.cards.append(card)
            player.updateInfo()
            if player.busted:
                player.bustText.undraw()
                player.busted = False
        self.deck.shuffle()


def testDeck():
    deck = Deck()
    print(deck)


def testCard():
    win = GraphWin("BlackJack", 600, 600)
    card = Card("Heart", "Ace", 11)
    card.drawCard(300, 300, win)
    win.getMouse()
    card.undrawCard()
    card.drawCard(400, 300, win)
    win.getMouse()
    card.undrawCard()
    win.getMouse()
    win.close()


def testBet():
    player = Player(200, 1)
    bet = player.getBet()
    print(bet)


if __name__ == '__main__':
    testBet()
