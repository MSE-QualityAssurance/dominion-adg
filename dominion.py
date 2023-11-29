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
        self.coins = 0
        self.num_provinces_purchased = 0
        self.game = None

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

    def calculate_victory_points(self):
        vp = sum(card.cost for card in self.deck + self.hand + self.discard_pile if card.card_type == "Victory")
        return vp

    def purchase_card(self, card_name):
        affordable_cards = [card for card in self.game.supply if card.name == card_name and card.cost <= self.coins]
        if affordable_cards:
            chosen_card = random.choice(affordable_cards)
            self.discard_pile.append(chosen_card)
            self.coins -= chosen_card.cost

            # Example: Track the number of Provinces purchased
            if chosen_card.name == "Province":
                self.num_provinces_purchased += 1

            return chosen_card
        return None

class DominionGame:
    def __init__(self, players):
        self.players = players
        self.supply = self.create_supply()
        self.current_player_index = 0

    def create_supply(self):
        supply = [
            DominionCard("Copper", 0, "Treasure"),
            DominionCard("Silver", 3, "Treasure"),
            DominionCard("Gold", 6, "Treasure"),
            DominionCard("Estate", 2, "Victory"),
            DominionCard("Duchy", 5, "Victory"),
            DominionCard("Province", 8, "Victory"),
            DominionCard("Smithy", 4, "Action", action=self.draw_action),
            DominionCard("Village", 3, "Action", action=self.draw_action),
            DominionCard("Cellar", 2, "Action", action=self.cellar_action),
            DominionCard("Market", 5, "Action", action=self.market_action),
            DominionCard("Workshop", 3, "Action", action=self.workshop_action),
            # Add more cards...
        ]
        return supply

    def start_game(self):
        for player in self.players:
            player.game = self
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

    def cellar_action(self, player):
        print(f"{player.name} played Cellar. Discarding cards and drawing replacements.")
        num_discards = len([card for card in player.hand if card.card_type != "Victory"])
        discarded_cards = random.sample(player.hand, num_discards)
        for card in discarded_cards:
            player.hand.remove(card)
            player.discard_pile.append(card)
        player.draw_cards(num_discards)

    def market_action(self, player):
        print(f"{player.name} played Market. Drawing a card, gaining an action, and getting +1 buy and +1 coin.")
        player.draw_cards(1)
        player.draw_action(1)
        player.num_buys += 1
        player.coins += 1

    def workshop_action(self, player):
        print(f"{player.name} played Workshop. Gaining a card costing up to 4 coins.")
        card_to_gain = self.buy_card_up_to_cost(4)
        if card_to_gain:
            player.discard_pile.append(card_to_gain)
            print(f"{player.name} gained {card_to_gain}")

    def buy_card(self, card_name, player):
        affordable_cards = [card for card in self.supply if card.name == card_name and card.cost <= 6]
        if affordable_cards:
            chosen_card = random.choice(affordable_cards)
            if player.deck:
                return chosen_card
        return None

    def buy_card_up_to_cost(self, max_cost):
        affordable_cards = [card for card in self.supply if card.cost <= max_cost]
        if affordable_cards:
            chosen_card = random.choice(affordable_cards)
            return chosen_card
        return None

    def determine_winner(self):
        winners = []
        max_vp = max(player.calculate_victory_points() for player in self.players)
        for player in self.players:
            if player.calculate_victory_points() == max_vp:
                winners.append(player)
        return winners

    def game_over(self):
        provinces_purchased = any(player.num_provinces_purchased >= 3 for player in self.players)
        province_supply_empty = not any(card.name == "Province" for card in self.supply)
        return provinces_purchased or province_supply_empty

    def run(self, num_turns):
        self.start_game()
        for _ in range(num_turns):
            self.play_turn()
            if self.game_over():
                break

        # Game Over - Determine Winner
        winners = self.determine_winner()
        if len(winners) == 1:
            print(f"\n{winners[0].name} wins!")
        else:
            print("\nIt's a tie!")

# Example usage
player1 = DominionPlayer("Player 1")
player2 = DominionPlayer("Player 2")
players = [player1, player2]

dominion_game = DominionGame(players)
dominion_game.run(20)  # Increase the number of turns to allow more time for the game to end
