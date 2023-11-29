import random

class DominionCard:
    def __init__(self, name, cost, card_type, action=None):
        self.name = name
        self.cost = cost
        self.card_type = card_type
        self.action = action

    def __str__(self):
        return f"{self.name} ({self.card_type})"

class DominionPlayer:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.deck = []
        self.discard_pile = []

    def draw_cards(self, num_cards):
        for _ in range(num_cards):
            if not self.deck:
                self.shuffle_discard_into_deck()
            if self.deck:
                drawn_card = self.deck.pop()
                self.hand.append(drawn_card)

    def shuffle_discard_into_deck(self):
        random.shuffle(self.discard_pile)
        self.deck.extend(self.discard_pile)
        self.discard_pile = []

    def display_hand(self):
        print(f"{self.name}'s hand: {[str(card) for card in self.hand]}")

class DominionGame:
    def __init__(self, players):
        self.players = players
        self.supply = self.create_supply()
        self.current_player_index = 0

    def create_supply(self):
        # Add more card types as needed
        supply = [
            DominionCard("Copper", 0, "Treasure"),
            DominionCard("Silver", 3, "Treasure"),
            DominionCard("Gold", 6, "Treasure"),
            DominionCard("Estate", 2, "Victory"),
            DominionCard("Duchy", 5, "Victory"),
            DominionCard("Province", 8, "Victory"),
            DominionCard("Smithy", 4, "Action", action=self.draw_action),
            DominionCard("Village", 3, "Action", action=self.draw_action),
            # Add more cards...
        ]
        return supply

    def start_game(self):
        for player in self.players:
            self.initialize_player_deck(player)
            player.draw_cards(5)

    def initialize_player_deck(self, player):
        starting_deck = [DominionCard("Copper", 0, "Treasure") for _ in range(7)]
        starting_deck.extend([DominionCard("Estate", 2, "Victory") for _ in range(3)])
        random.shuffle(starting_deck)
        player.deck = starting_deck

    def play_turn(self):
        current_player = self.players[self.current_player_index]
        print(f"\n{current_player.name}'s turn:")
        current_player.display_hand()

        # Example: Draw 1 card
        current_player.draw_cards(1)
        current_player.display_hand()

        # Example: Play an action card
        action_cards = [card for card in current_player.hand if card.card_type == "Action"]
        if action_cards:
            played_card = random.choice(action_cards)
            current_player.hand.remove(played_card)
            played_card.action(current_player)
            current_player.display_hand()

        # Example: Buy a card
        bought_card = self.buy_card("Silver", current_player)
        if bought_card:
            current_player.discard_pile.append(bought_card)
            print(f"{current_player.name} bought {bought_card}")

        # End the turn
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def draw_action(self, player):
        player.draw_cards(3)

    def buy_card(self, card_name, player):
        affordable_cards = [card for card in self.supply if card.name == card_name and card.cost <= 6]
        if affordable_cards:
            chosen_card = random.choice(affordable_cards)
            if player.deck:
                return chosen_card

    def run(self, num_turns):
        self.start_game()
        for _ in range(num_turns):
            self.play_turn()

# Example usage
player1 = DominionPlayer("Player 1")
player2 = DominionPlayer("Player 2")
players = [player1, player2]

dominion_game = DominionGame(players)
dominion_game.run(5)
