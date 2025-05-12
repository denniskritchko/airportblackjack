import random 

class Hand:
    def __init__(self):
        self.cards = []
    
    def add_card(self, card):
        self.cards.append(card)
    
    def get_cards(self):
        return self.cards
    
    def clear(self):
        self.cards = []
    
    def display(self, owner, hide_first=False):
        print(f"{owner}'s hand:")
        if hide_first and len(self.cards) > 0:
            print("Hidden card")
            for card in self.cards[1:]:
                print(card)
        else:
            for card in self.cards:
                print(card)
                
        # Show total if all cards are visible
        if not hide_first:
            print(f"Total: {self.calculate_value()}")
    
    def calculate_value(self):
        # Calculate the value of a hand in blackjack
        value = 0
        aces = 0
        
        for card in self.cards:
            rank = card.split()[0]  # Get the rank part of the card
            
            if rank == 'Ace':
                aces += 1
                value += 11
            elif rank in ['Jack', 'Queen', 'King']:
                value += 10
            else:
                value += int(rank)
                
        # Adjust for aces if needed
        while value > 21 and aces > 0:
            value -= 10
            aces -= 1
            
        return value
    
    def is_blackjack(self):
        return len(self.cards) == 2 and self.calculate_value() == 21
    
    def is_busted(self):
        return self.calculate_value() > 21

def draw_card(deck):
    if len(deck) > 0:
        return deck.pop()
    else:
        print("Deck is empty! Game over.")
        exit()

def print_hands(house_hand, player_hand, hide_house_card=True):
    house_hand.display("House", hide_house_card)
    print()
    player_hand.display("Player")
    print()

def player_turn(deck, player_hand):
    while True:
        if player_hand.is_busted():
            print("You bust! Game over.")
            return False
            
        choice = input("Would you like to (h)it or (s)tay? ").lower()
        
        if choice.startswith('h'):
            card = draw_card(deck)
            print(f"You draw: {card}")
            player_hand.add_card(card)
            player_hand.display("Player")
            print()
            
            if player_hand.is_busted():
                print("You bust! House wins.")
                return False
        elif choice.startswith('s'):
            print("You stay.")
            return True
        else:
            print("Invalid choice. Please enter 'h' or 's'.")

def house_turn(deck, house_hand):
    print("\nHouse's turn:")
    house_hand.display("House")
    
    # House must hit on 16 or lower, and stand on 17 or higher
    while house_hand.calculate_value() < 17:
        card = draw_card(deck)
        print(f"House draws: {card}")
        house_hand.add_card(card)
        house_hand.display("House")
        
        if house_hand.is_busted():
            print("House busts! You win.")
            return False
    
    print("House stays.")
    return True

def determine_winner(house_hand, player_hand):
    house_value = house_hand.calculate_value()
    player_value = player_hand.calculate_value()
    
    if player_hand.is_blackjack() and not house_hand.is_blackjack():
        print("Blackjack! You win 3:2!")
    elif house_hand.is_blackjack() and not player_hand.is_blackjack():
        print("House has blackjack! You lose.")
    elif house_value > player_value:
        print(f"House wins with {house_value} vs your {player_value}.")
    elif player_value > house_value:
        print(f"You win with {player_value} vs house's {house_value}!")
    else:
        print(f"It's a tie! Both have {player_value}.")

def start_game(deck, house_hand, player_hand):
    print("Welcome to blackjack!\n")
    
    # Deal initial cards
    for _ in range(2):
        player_hand.add_card(draw_card(deck))
        house_hand.add_card(draw_card(deck))
    
    # Display initial hands (hide dealer's first card)
    print_hands(house_hand, player_hand)
    
    # Check for blackjack
    if player_hand.is_blackjack():
        if house_hand.is_blackjack():
            print("Both have blackjack! It's a push.")
        else:
            print("Blackjack! You win 3:2!")
        return
    
    # Player's turn
    player_ok = player_turn(deck, player_hand)
    
    # House's turn if player didn't bust
    if player_ok:
        house_ok = house_turn(deck, house_hand)
        
        # Determine winner if neither busted
        if house_ok:
            determine_winner(house_hand, player_hand)

def play_blackjack():
    while True:
        # Create a standard deck of 52 cards
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

        deck = [f"{rank} of {suit}" for suit in suits for rank in ranks]
        random.shuffle(deck)
        
        house_hand = Hand()
        player_hand = Hand()
        
        start_game(deck, house_hand, player_hand)
        
        play_again = input("\nWould you like to play again? (y/n): ").lower()
        if not play_again.startswith('y'):
            print("Thanks for playing!")
            break

# Start the game
if __name__ == "__main__":
    play_blackjack()


