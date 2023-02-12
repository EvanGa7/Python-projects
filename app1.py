import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __repr__(self):
        return self.rank + ' of ' + self.suit

class Deck:
    def __init__(self):
        self.cards = []
        suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']  
        ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
        for suit in suits:
            for rank in ranks:
                card = Card(suit, rank)
                self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def drawCard(self):
        if self.cards != None:
            random_card = random.choice(self.cards)
            print ("The card that you drew was " + str(random_card))
            self.cards.remove(random_card)
        
    def deal(self):
        return self.cards.pop()

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def addCard(self, card):
        self.cards.append(card)
        card_value = self.get_rank_value(card.rank)
        self.value += card_value
        if card.rank == 'Ace':
            self.aces += 1

    
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

    def get_rank_value(self, rank):
        if rank in ['Jack', 'Queen', 'King']:
            return 10
        elif rank == 'Ace':
            return 11
        else:
            try:
                return int(rank)
            except ValueError:
                print("Invalid rank entered:", rank)
            return None
        
class Blackjack():
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()

        self.players_hand = Hand()
        self.dealers_hand = Hand()
        
        self.players_hand.addCard(self.deck.deal())
        self.players_hand.addCard(self.deck.deal())

        self.dealers_hand.addCard(self.deck.deal())
        self.dealers_hand.addCard(self.deck.deal())


    def play(self):
        print("Your Hand Is: " + str(self.players_hand.cards))
        print("The Dealers Hand Is: " + str(self.dealers_hand.cards))

    def hit(self):
        self.players_hand.addCard(self.deck.deal())
        self.players_hand.adjust_for_ace()

    def stand(self):
        while self.dealers_hand.value <= 21:
            self.dealers_hand.addCard(self.deck.deal())
            self.dealers_hand.adjust_for_ace()
    
    def check_win(self):
        player_wins = False
        player_busts = False
        dealer_wins = False
        dealer_busts = False
        no_winner = False 

        if self.players_hand.value > 21:
            dealer_wins = True
            player_busts = True
        elif self.dealers_hand.value > 21:
            player_wins = True
            dealer_busts = True
        elif self.players_hand.value == 21 and self.dealers_hand.value == 21:
            dealer_wins = True
        elif self.players_hand.value == 21 and self.dealers_hand.value < 21:
            player_wins = True
        elif self.players_hand.value < 21 and self.dealers_hand.value == 21:
            dealer_wins = True
        elif self.players_hand.value != 21 and self.dealers_hand.value != 21 and self.players_hand.value > self.dealers_hand.value:
            player_wins = True
        elif self.players_hand.value != 21 and self.dealers_hand.value != 21 and self.players_hand.value <= self.dealers_hand.value:
            dealer_wins = True
        elif self.players_hand.value > 21 and self.dealers_hand.value > 21:
            no_winner = True

        return player_wins, player_busts, dealer_wins, dealer_busts, no_winner

    def show_results(self):
        player_wins, player_busts, dealer_wins, dealer_busts, no_winner = self.check_win()

        if player_wins:
            print("The Player Wins! ")
        elif player_busts:
            print("The Dealer Wins & The Player Busts! ")
        elif dealer_wins:
            print("The Dealer Wins! ")
        elif dealer_busts:
            print("The Player Wins & The Dealer Busts! ")
        elif no_winner:
            print("The Dealer & The Player Bust!")


if __name__ == '__main__':
    game = Blackjack()

    while True:
        game.play()

        choice = input("Do you want to Hit or Stand? ")
        choice == choice.lower()

        if(choice == "hit"):
            game.hit()
        elif(choice == "stand"):
            game.stand()
            game.play()
            break
    
    game.show_results()