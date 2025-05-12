import tkinter as tk
from tkinter import messagebox, font
import random
import time
from PIL import Image, ImageTk
import os

# get our hand framework
from blackjack import Hand

class BlackjackUI:
    def __init__(self, root):
        # Initialize the main window
        self.root = root
        self.root.title("Blackjack")
        self.root.geometry("800x600")
        self.root.configure(bg="#004d00")
        self.root.resizable(False, False)

        self.deck = []
        self.player_hand = Hand()
        self.house_hand = Hand()
        self.game_over = False
        
        self.title_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.card_font = font.Font(family="Helvetica", size=14)
        self.button_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.status_font = font.Font(family="Helvetica", size=16)
        
        self.title_frame = tk.Frame(self.root, bg="#004d00")
        self.title_frame.pack(pady=10)
        
        self.house_frame = tk.Frame(self.root, bg="#004d00")
        self.house_frame.pack(pady=10)
        
        self.player_frame = tk.Frame(self.root, bg="#004d00")
        self.player_frame.pack(pady=10)
        
        self.status_frame = tk.Frame(self.root, bg="#004d00")
        self.status_frame.pack(pady=10)
        
        self.button_frame = tk.Frame(self.root, bg="#004d00")
        self.button_frame.pack(pady=20)
        
        self.title_label = tk.Label(
            self.title_frame, 
            text="Blackjack", 
            font=self.title_font, 
            fg="#ffcc00", 
            bg="#004d00"
        )
        self.title_label.pack()
        
        self.house_label = tk.Label(
            self.house_frame,
            text="Dealer's Hand",
            font=self.card_font,
            fg="white",
            bg="#004d00"
        )
        self.house_label.pack()
        
        self.house_cards_frame = tk.Frame(self.house_frame, bg="#004d00")
        self.house_cards_frame.pack(pady=5)
        
        self.house_score_label = tk.Label(
            self.house_frame,
            text="",
            font=self.card_font,
            fg="white",
            bg="#004d00"
        )
        self.house_score_label.pack()
        
        self.player_label = tk.Label(
            self.player_frame,
            text="Player's Hand",
            font=self.card_font,
            fg="white",
            bg="#004d00"
        )
        self.player_label.pack()
        
        self.player_cards_frame = tk.Frame(self.player_frame, bg="#004d00")
        self.player_cards_frame.pack(pady=5)
        
        self.player_score_label = tk.Label(
            self.player_frame,
            text="",
            font=self.card_font,
            fg="white",
            bg="#004d00"
        )
        self.player_score_label.pack()
        
        self.status_label = tk.Label(
            self.status_frame,
            text="",
            font=self.status_font,
            fg="#ffcc00",
            bg="#004d00"
        )
        self.status_label.pack(pady=10)
        
        self.hit_button = tk.Button(
            self.button_frame,
            text="Hit",
            font=self.button_font,
            bg="#ffcc00",
            fg="black",
            width=10,
            command=self.player_hit
        )
        self.hit_button.grid(row=0, column=0, padx=10)
        
        self.stay_button = tk.Button(
            self.button_frame,
            text="Stay",
            font=self.button_font,
            bg="#ffcc00",
            fg="black",
            width=10,
            command=self.player_stay
        )
        self.stay_button.grid(row=0, column=1, padx=10)
        
        self.new_game_button = tk.Button(
            self.button_frame,
            text="New Game",
            font=self.button_font,
            bg="#ffcc00",
            fg="black",
            width=10,
            command=self.new_game
        )
        self.new_game_button.grid(row=0, column=2, padx=10)

        self.new_game()

    def create_deck(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        
        deck = [f"{rank} of {suit}" for suit in suits for rank in ranks]
        random.shuffle(deck)
        return deck

    def draw_card(self):
        if len(self.deck) > 0:
            return self.deck.pop()
        else:
            messagebox.showinfo("Deck Empty", "The deck is empty! Starting a new game.")
            self.new_game()
            return self.draw_card()

    def update_card_display(self):
        for widget in self.house_cards_frame.winfo_children():
            widget.destroy()
        for widget in self.player_cards_frame.winfo_children():
            widget.destroy()
        
        house_cards = self.house_hand.get_cards()
        if self.game_over:
            for i, card in enumerate(house_cards):
                card_label = tk.Label(
                    self.house_cards_frame,
                    text=card,
                    bg="white",
                    fg="black",
                    padx=10,
                    pady=20,
                    relief=tk.RAISED,
                    borderwidth=2
                )
                card_label.grid(row=0, column=i, padx=5)
            self.house_score_label.config(text=f"Total: {self.house_hand.calculate_value()}")
        else:
            hidden_label = tk.Label(
                self.house_cards_frame,
                text="Hidden Card",
                bg="red",
                fg="white",
                padx=10,
                pady=20,
                relief=tk.RAISED,
                borderwidth=2
            )
            hidden_label.grid(row=0, column=0, padx=5)
            
            for i, card in enumerate(house_cards[1:]):
                card_label = tk.Label(
                    self.house_cards_frame,
                    text=card,
                    bg="white",
                    fg="black",
                    padx=10,
                    pady=20,
                    relief=tk.RAISED,
                    borderwidth=2
                )
                card_label.grid(row=0, column=i+1, padx=5)
            self.house_score_label.config(text="") 
        
        player_cards = self.player_hand.get_cards()
        for i, card in enumerate(player_cards):
            card_label = tk.Label(
                self.player_cards_frame,
                text=card,
                bg="white",
                fg="black",
                padx=10,
                pady=20,
                relief=tk.RAISED,
                borderwidth=2
            )
            card_label.grid(row=0, column=i, padx=5)
        
        self.player_score_label.config(text=f"Total: {self.player_hand.calculate_value()}")
        
    def new_game(self):
        self.deck = self.create_deck()
        self.player_hand.clear()
        self.house_hand.clear()
        self.game_over = False
        
        self.player_hand.add_card(self.draw_card())
        self.house_hand.add_card(self.draw_card())
        self.player_hand.add_card(self.draw_card())
        self.house_hand.add_card(self.draw_card())
        
        self.update_card_display()
        self.status_label.config(text="Your turn: Hit or Stay?")
        
        self.hit_button.config(state=tk.NORMAL)
        self.stay_button.config(state=tk.NORMAL)
        
        if self.player_hand.is_blackjack():
            if self.house_hand.is_blackjack():
                self.end_game("Both have Blackjack! Push!")
            else:
                self.end_game("Blackjack! You win 3:2!")
            
    def player_hit(self):
        if not self.game_over:
            card = self.draw_card()
            self.player_hand.add_card(card)
            
            self.update_card_display()
            
            if self.player_hand.is_busted():
                self.end_game("Bust! You lose.")
            elif self.player_hand.calculate_value() == 21:
                self.player_stay()
                
    def player_stay(self):
        if not self.game_over:
            self.status_label.config(text="Dealer's turn...")
            self.hit_button.config(state=tk.DISABLED)
            self.stay_button.config(state=tk.DISABLED)
            
            self.game_over = True
            self.update_card_display()
            
            self.root.after(1000, self.house_turn)
                
    def house_turn(self):
        house_value = self.house_hand.calculate_value()
        
        if house_value < 17:
            card = self.draw_card()
            self.status_label.config(text=f"Dealer draws: {card}")
            self.house_hand.add_card(card)
            self.update_card_display()
            
            if self.house_hand.is_busted():
                self.end_game("Dealer busts! You win!")
                return
                
            self.root.after(1000, self.house_turn)
        else:
            self.status_label.config(text="Dealer stands.")
            self.root.after(1000, self.determine_winner)
                
    def determine_winner(self):
        house_value = self.house_hand.calculate_value()
        player_value = self.player_hand.calculate_value()
        
        if player_value > house_value:
            self.end_game(f"You win! {player_value} vs {house_value}")
        elif house_value > player_value:
            self.end_game(f"Dealer wins. {house_value} vs {player_value}")
        else:
            self.end_game(f"Push! Both have {player_value}")
                
    def end_game(self, message):
        self.game_over = True
        self.status_label.config(text=message)
        self.hit_button.config(state=tk.DISABLED)
        self.stay_button.config(state=tk.DISABLED)
        self.update_card_display()

if __name__ == "__main__":
    root = tk.Tk()
    game = BlackjackUI(root)
    root.mainloop()