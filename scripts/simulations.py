from random import randint, choice
import xlsxwriter

bonus_2 = 2
bonus_3 = 4
bonus_4 = 10
bonus_5 = 14
# TODO: przerobić bonusy na słownik
card_types = ['B', 'G', 'P', 'R', 'Y']
finished = False

# TODO: obsłużyć exchange cards przy pustej ręce
# TODO: obsłużyć discard przy pustym stole

workbook = xlsxwriter.Workbook('winners.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write(0, 0, "Winner")
worksheet.write(0, 1, "P1")
worksheet.write(0, 2, "P2")
worksheet.write(0, 3, "Rounds")
worksheet.write(0, 4, "Game no.")
log = open("log.txt", "w+")

def calculate_bonus(card, player):
    bonus = 0
    number = player.cards.count(card)
    if number == 2:
        bonus += bonus_2
    elif number == 3:
        bonus += bonus_3
    elif number == 4:
        bonus += bonus_4
    elif number == 5:
        bonus += bonus_5
    return bonus

def calculate_score(set, player):
    score = 0
    bonus = 0
    for card in set:
        if card == "B":
            score += 1
        elif card == "G":
            score += 2
        elif card == "P":
            score += 3
        elif card == "R":
            score += 4
        elif card == "Y":
            score += 5
    for type in card_types:
        bonus_to_add = calculate_bonus(type, player)
        bonus += bonus_to_add
        score += bonus_to_add
    return score

def solve_tie():
    player1.cards.sort()
    player2.cards.sort()

    if len(player1.cards) == len(player2.cards):
        for i in range(0, len(player1.cards)):
            if player1.cards[-i] != player2.cards[-i]:
                winner = player1.name if player1.cards[-1] > player2.cards[-1] else player2.name
                return winner
        winner = "Draw"
        return winner
    else:
        winner = player1.name if len(player1.cards) > len(player2.cards) else player2.name
        return winner

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.cards = []
        self.tokens = []
        self.score = 0

    def check_token(self, token):
        playable = True
        opponent = player2 if self == player1 else player1
        if self.hand == [] and (token == "Play"):
            playable = False
        elif len(self.cards) == 6 and (token == "Play" or token == "DrawAndPlay"):
            playable = False
        elif (self.cards == [] or opponent.cards == []) and token == "ExchangeCards":
            playable = False
        elif cards == [] and (token == "DrawAndPlay" or token == "Draw"):
            playable = False
        elif self.cards == [] and token == "Discard":
            playable = False
        return playable

    def choose_token_to_play(self):
        if len(self.cards) == 6 and "Pass" in self.tokens:
            token_to_play = "Pass"
        else:
            token_to_play = choice(self.tokens)
            if self.check_token(token_to_play) is False:
                index = self.tokens.index(token_to_play)
                token_to_play = self.tokens[0] if index == 1 else self.tokens[1]
                if self.check_token(token_to_play) is False:
                    log.write(f"{self.name} tried to play token {token_to_play}\n")
                    token_to_play = "CantPlay"
        self.play_token(token_to_play) 

    def choose_next_token(self):
        if len(self.cards) == 6 and "Pass" in available_tokens:
            token_next = "Pass"
        else:
            token_next = choice(available_tokens)
            if "Play" in self.tokens and token_next == "Play":
                while token_next == "Play":
                    token_next = choice(available_tokens)             
        self.tokens.append(token_next)
        available_tokens.remove(token_next)

    def play_token(self, token):
        log.write(f"{self.name} plays token {token}\n")
        if token == "CantPlay":
            rnd_token = choice(self.tokens)
            self.tokens.remove(rnd_token)
        else:
            self.tokens.remove(token)
        if token == "Play":
            card = choice(self.hand)
            self.hand.remove(card)
            self.cards.append(card)
        elif token == "Draw":
            card_to_draw = choice(cards)   
            self.hand.append(card_to_draw)
            cards.remove(card_to_draw)
        elif token == "DrawAndPlay":
            card = choice(cards)
            cards.remove(card)
            self.cards.append(card)
        elif token == "Discard":
            card = choice(self.cards)
            self.cards.remove(card)
            cards.append(card)
        elif token == "ExchangeCards":
            opponent = player2 if self == player1 else player1
            card_to_give = choice(self.cards)
            card_to_take = choice(opponent.cards)
            self.cards.append(card_to_take)
            opponent.cards.remove(card_to_take)
            self.cards.remove(card_to_give)
            opponent.cards.append(card_to_give)
        elif token == "ExchangeTokens":
            opponent = player2 if self == player1 else player1
            token_to_give = self.tokens[0]
            token_to_take = choice(opponent.tokens)
            self.tokens.append(token_to_take)
            opponent.tokens.remove(token_to_take)
            self.tokens.remove(token_to_give)
            opponent.tokens.append(token_to_give)
        elif token == "Pass":
            if len(self.cards) >= 6:
                finish()      
        
        self.choose_next_token()
        if token == "CantPlay":
            token = rnd_token
            if len(self.cards) == 0:
                loser = self.name
                finish(loser)
            else:
                card_to_discard = choice(self.cards)
                self.cards.remove(card_to_discard)
                cards.append(card_to_discard)           
        available_tokens.append(token)
    
    def play(self):
        self.choose_token_to_play()


player1 = Player("Player 1")
player2 = Player("Player 2")
players = [player1, player2]

def print_info():
    # TODO: rozdzielić print od write
    print("Current game status:")
    log.write(f"Current game status:\n")
    for player in players:
        print(player.name, "hand:", player.hand)
        print(player.name, "cards:", player.cards)
        print(player.name, "tokens:", player.tokens)
        log.write(f"{player.name} hand: {player.hand}\n")
        log.write(f"{player.name} cards: {player.cards}\n")
        log.write(f"{player.name} tokens: {player.tokens}\n")
    print("Available cards:", cards)
    print("Available tokens:", available_tokens)
    print("--------------------")
    log.write(f"Available cards: {cards}\n")
    log.write(f"Available tokens: {available_tokens}\n")
    log.write("---------------------\n")

def initial_deal():
    global cards
    global available_tokens
    cards = ['B', 'B', 'B', 'B', 'B', 'G', 'G', 'G', 'G', 'P', 'P', 'P', 'R', 'R', 'Y']
    available_tokens = ["Discard", "Pass", "ExchangeCards", "ExchangeTokens", "DrawAndPlay"]
    player1.tokens = ["Play", "Draw"]
    player2.tokens = ["Play", "Draw"] 
    player1.cards = []
    player2.cards = []
    player1.hand = []
    player2.hand = []
    player1.score = 0
    player2.score = 0
    # TODO: for na player
    removed = cards[randint(0, len(cards)-1)]
    cards.remove(removed)
    print("Removed card:", removed)
    log.write(f"Removed card: {removed}\n")
    for player in players:
        while len(player.hand) < 4:
            card_to_deal = choice(cards)
            player.hand.append(card_to_deal)
            cards.remove(card_to_deal)
        print(player.name, "initial hand:", player.hand)
        log.write(f"{player.name} initial hand: {player.hand}\n")
    print("Cards available:", cards)
    return None
    

def finish(loser=None):
    global winner
    player1.score += calculate_score(player1.cards, player1)
    player2.score += calculate_score(player2.cards, player2)
    if player1.score == player2.score:
        winner = solve_tie()
    else:
        winner = player1.name if player2.score < player1.score else player2.name
    if loser:
        winner = player1.name if loser == player2.name else player2.name
    print("Winner:", winner)
    print("Points:", player1.score, "vs.", player2.score)
    global finished 
    finished = True

def play_game():
    initial_deal()
    global finished 
    finished = False
    round = 0
    while finished is not True:
        print("Round no.", round+1)
        log.write(f"Round no. {round+1}\n")
        current_player = players[round%2]
        current_player.play()
        if finished is not True:
            print_info()
            pass
        round += 1
        if round > 10000:
            quit()
    return round

for i in range(1, 10001):
    print("This is game no.", i)
    log.write(f"------ GAME No. {i} ------\n")
    rounds = play_game()
    print("That was game no.", i)
    log.write(f"------ GAME No. {i} IS FINISHED ------\n")
    worksheet.write(i, 0, winner)
    worksheet.write(i, 1, player1.score)
    worksheet.write(i, 2, player2.score)
    worksheet.write(i, 3, rounds)
    worksheet.write(i, 4, i)
workbook.close()
log.close()