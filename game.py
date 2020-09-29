class Game:

    def __init__(self, id):

        self.p1HasChosen = False
        self.p2HasChosen = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0, 0]
        self.ties = 0

    def GetPlayerMove(self, playerNumber):

        return self.moves[playerNumber]

    def Play(self, player, move):

        self.moves[player] = move

        if player == 0:
            self.p1HasChosen = True
        else:
            self.p2HasChosen = True

    def Connected(self):

        return self.ready

    def AllPlayersChose(self):

        return self.p1HasChosen and self.p2HasChosen

    def Winner(self):
        p1 = self.moves[0].upper()[0]  # gets the first letter of the player's choice
        p2 = self.moves[1].upper()[0]

        winner = -1  # result if tie

        if (p1 == "R" and p2 == "S") or\
            (p1 == "P" and p2 == "R") or\
            (p1 == "S" and p2 == "P"):

            winner = 0  # player 1 wins

        elif (p2 == "R" and p1 == "S") or\
            (p2 == "P" and p1 == "R") or\
            (p2 == "S" and p1 == "P"):

            winner = 1  # player 2 wins

        return winner

    def ResetChoices(self):

        self.p1HasChosen = False
        self.p2HasChosen = False