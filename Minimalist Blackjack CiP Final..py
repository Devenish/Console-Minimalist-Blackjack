"""
This is a console minimalist blackjack game. The player will compete against the computer and play until they used all their
credits or quit. It includes options to place a bet, buy insurance, split, double down.

Thank you to everyone who participated in 2021's Code in Place.

Written by Devenish Smith to serve as final project assignment for Code in Place 2021, hosted by Stanford University.

*** Directory ***
intro() - Display welcome text.
thank_you() - Exit thank you text.
build_cards() - Build details of all 52 cards in a list.
build_deck() - Compile multiple packs of cards into a deck, then shuffle and cut.
refresh_deck() - Refresh deck of cards when it reaches the cut.
on_the_house() - Give a player some courtesy credits when near bankruptcy.
get_opening_bet() - Place opening bets.
start_player_cards() - Deal players first cards.
start_dealer_cards() - Deal dealers first cards.
player_starting_data() - Display players first cards.
dealer_starting_data() - Display dealers first cards.
get_hand_value() - Used to get value of playyrs hand of cards.
display_full_hand() - Used to display full list of all cards in a hand.
deal_new_card() - Used to deal a new card to an existing hand.
get_insurance() - Presents the player with option to purchase insurance.
double_down() - Presents the player with an option to double down.
hit_or_stand() - Used for a player to hit (add another card) or stand.
player_split_hand() - Presents the player with a choice to split a hand and play that hand.
player_main_hand()  - Player will play their Main hand.
dealer_plays_hand() - Dealer will attempt to beat the player.
settlements() - Payouts and summery of the game.
play_another_game() - Ask the user to play again.
black_jack() - The Game of Blackjack, using functions above.
main() - Main includes Intro(), blackjack() and thank_you().
"""

import random
import time

STARTING_BALANCE = int(1000) # Starting credits issued to player.
NUM_OF_DECKS = 3 # How many decks used in an active game.
MED_PAUSE = 0.9 # time to pause for visual delay.

def intro():
    #A welcome message when starting the game.
    print(f"\nWelcome to Minimalist Console Blackjack")


def thank_you():
    #A thank you message when exiting the game.
    print(f"Thank you for playing! \n\nA special thanks to everyone at Code in Place 2021.\n")


def build_cards():
    """Will generate 52 cards to make a deck in two loops, 1 nested.
    Returns: 
        deck_of_cards > list with sublist (integer, integer, string, string) as (Value of 2-11, Num 2-14 "Suit", "Card Name")
        A List of all 52 cards each stored as a sublist (int value, int card num, str suit, str of name).
    """    
    # deck_of_cards is a list store nested list's.
    # (int value, card_num, str suit, str of name)
    deck_of_cards=[]
    # Define each group by suit.
    for suit_num in range (4):
        if suit_num == 0:
            suit_family = "Clubs"
        elif suit_num == 1:
            suit_family = "Diamonds"
        elif suit_num == 2:
            suit_family = "Hearts"
        elif suit_num == 3:
            suit_family = "Spades"
        # Get each card value (13 total) for each given family.
        # Value must start at 1 to build value starting with Ace.
        card_num = 2
        while card_num <= 14:
            card_name = ""
            if card_num <= 10 and card_num > 1:
                card_name = (str(card_num)+" of "+str(suit_family))
                card_value = int(card_num)
            elif card_num == 11:
                card_name = ("Jack of "+str(suit_family))
                card_value = int(10)
            elif card_num == 12:
                card_name = ("Queen of "+str(suit_family))
                card_value = int(10)
            elif card_num == 13:
                card_name = ("King of "+str(suit_family))
                card_value = int(10)
            elif card_num == 14:
                card_name = ("Ace of "+str(suit_family))
                card_value = int(11)
            # card_data is temporary to hold values for each card as a list.
            card_data = (int(card_value), int(card_num), str(suit_family), card_name)
            # appends current card_data ot deck_of_cards list until all 52 cards are created.
            deck_of_cards.append(card_data)
            card_num += 1
    return deck_of_cards


def build_deck(NUM_OF_DECKS, pack_of_cards):
    """Takes number packs needed to build playing deck of cards, 
        then shuffles them in random order.
    Inputs:
        NUM_OF_DECKS:  Integer number of packs of cards used in a playing deck.
        pack_of_cards: List with sublist (integer, integer, string, string) as (Value of 2-11, Num 2-14, "Suit", "Card Name")
        A List of all 52 cards each stored as a sublist (int value, int card num, str suit, str of name).
    Returns:
        card_deck: List with sublist (integer, integer, string, string) as (Value of 2-11, Num 2-14, "Suit", "Card Name")
        Multiple decks of cards combined and shuffled and ready to be dealt.
    """    
    card_deck = []
    for i in range (NUM_OF_DECKS):
        card_deck.extend(pack_of_cards)
    # Shuffles all cards in the deck.
    random.shuffle(card_deck)
    print("\nShuffling new deck...\n")
    return card_deck


def refresh_deck(card_deck, pack_of_cards, NUM_OF_DECKS, cut_num):
    """Build a playing deck with multiple packs of cards and then shuffles them.
        Will also check how often deck needs to be reshuffled from the radom cut.
        Most work is done in build_deck(), this just decides when to do it again.
    Inputs:
        card_deck List with sublist (integer, integer, string, string) as (Value of 2-11, Num 2-14, "Suit", "Card Name")
            Multiple decks of cards combined and shuffled and ready to be dealt.
        pack_of_cards List with sublist (integer, integer, string, string) as (Value of 2-11, Num 2-14, "Suit", "Card Name")
        NUM_OF_DECKS: Constant to determine how many decks are used.
        cut_num: Interger for random number, to determin when to cut cards again.

    Returns:
        card_deck: list of cards refreshed.
        cut_num: Interger for random number, to determin when to cut cards again.
    """    
    # Build a playing deck with multiple packs of cards and then shuffles them.
    # Will also check how often deck needs to be reshuffled from the radom cut.
    cards_left = len(card_deck)
    if cut_num == 0 or cards_left <= cut_num:
        card_deck = build_deck(NUM_OF_DECKS, pack_of_cards)
        cut_num = random.randint(40, 70) 
        time.sleep(MED_PAUSE) 
    return card_deck, cut_num


def on_the_house(player_balance):
    """If player is running low on credits, the house will give more.
    Inputs:
        player_balance: Interger of players running credit balance.
    Returns:
        player_balance: Updated with extra free credit.
    """
    if player_balance <= 10:
        player_balance += 500
        print("Have some fun with an extra 500 credits, courtesy of the House.")
        print(f"Player's new balance is: {player_balance} credits")
        time.sleep(MED_PAUSE)
        input("Press \033[93m<\033[00mEnter\033[93m>\033[00m to continue.")
    return player_balance


def get_opening_bet(player_balance):
    """Player is tasked to make an opening bet. Bet value is a running place holder
        the amount will not be deducted from player_balance until end of the round.
    Inputs:
        player_balance: Integer amount of credits player has available.
    Returns:
        bet_amount: Integer of the amount made by the player for opening bet.
    """    
    
    while True:
        try:
            bet_amount = int(input(f"Your current balance is {player_balance} credits. \nPlace an opening bet: "))
            if bet_amount >= 1 and bet_amount <= int(player_balance):
                break
                #bet_amount = int(input(f"Your current balance is {player_balance} credits. \nPlace an opening bet: "))
        except ValueError:
            continue
    print(f"You have placed a bet of {bet_amount} credits.\nBets are closed, the dealer has begun to deal cards.")
    return bet_amount


def start_player_cards(card_deck):
    """removes data of 2 cards from card_deck to player_hand and returns both.
    Inputs:
        card_deck: List with sublist (integer, integer, string, string) as (Value of 2-11, 2-14, "Suit", "Card Name")
        A List of all 52 cards each stored as a sublist (int value, int card num, str suit, str of name).
    Returns:
        player_hand: List updated with new cards added to list.
        card_deck:: List updated with cards removed from the list.
    """    
    player_hand = []
    for i in range(2):
        player_hand.append(card_deck.pop())
    return player_hand, card_deck


def start_dealer_cards(card_deck):
    """removes data of 2 cards from card_deck to dealer_hand and returns both.
    Inputs:
        card_deck: List with sublist (integer, integer, string, string) as (Value of 2-11, 2-14, "Suit", "Card Name")
        A List of all 52 cards each stored as a sublist (int value, int card num, str suit, str of name).
    Returns:
        dealer_hand: Updated with 2 cards that previously existed in card_deck.
        card_deck: Updated with the removed card data that has been moved to player_hand list.
    """  
    dealer_hand = []
    for i in range(2):
        dealer_hand.append(card_deck.pop())
    return dealer_hand, card_deck


def player_starting_data(player_hand):
    """Designed to be used once and display the players starting hand after being dealt. It will import
        player_hand and display both cards and it's value. Nothing to return.
    Inputs:
        player_hand: List with sublist (integer, integer, string, string) as (Value of 2-11, 2-14, "Suit", "Card Name"). 
    """    
    # Get value of cards.
    # Display the Players hand.
    player_hand_value = get_hand_value(player_hand)
    print(f"\nPlayer has cards: {player_hand[0][3]} and {player_hand[1][3]}.  (Value of: {player_hand_value})")


def dealer_starting_data(dealer_hand):
    """Designed to be used once and display the dealers starting hand after being dealt. It will import
        dealer_hand and display first card down(no info) and second card up with it's value. Nothing to return.
    Inputs:
        dealer_hand: List with sublist (integer, integer, string, string) as (Value of 2-11, 2-14, "Suit", "Card Name").
    """    
    # Display The Dealers hand.
    print(f"House has cards: (Face Down) and {dealer_hand[1][3]}.  (Value of: {dealer_hand[1][0]}+)")


def get_hand_value(player_hand):
    """Imports a hand of cards, then loops through to get a value the hand is worth. It will decide
        if the Ace's are to be counted as 1 or 11. then return the final value as interger.
    Inputs:
        player_hand: List with sublist (integer, string, string) as (Value of 2-11, 2-14, "Suit", "Card Name").
    Returns:
        player_hand_value: Integer reflecting scoring value from player_hand.
    """    
    player_hand_value = 0
    num_of_aces = 0
    # loop for each card in hand, add to player value.
    for i in range(len(player_hand)):
        player_hand_value += player_hand[i][0]
        if player_hand[i][0] == 11:
            num_of_aces += 1
    # test how to handle for Aces of 1 or 11.
    # Under 21, safe and return.
    if player_hand_value <= 21: 
        return player_hand_value
    # No aces and bust.
    elif num_of_aces == 0 and player_hand_value > 21:
        return player_hand_value
    # For each Ace while bust, reflect new value and return.
    else:
        for i in range(num_of_aces):
            if player_hand_value > 21:
                player_hand_value -= 10
            else:
                return player_hand_value
        return int(player_hand_value)


def display_full_hand(source_hand, name):
    """Takes the source_hand of given cards, and then prints out the list of card names ("8 of Hearts")
        and returns nothing.
    Inputs:
        source_hand: List with sublist (integer, integer, string, string) as (Value of 2-11, 2-14, "Suit", "Card Name") 
        name: A string for "Name" of who's hand the cards belong to.
    """    
    cards_in_hand = []
    for i in range(len(source_hand)):
        cards_in_hand.append(source_hand[i][3])
    # Display cards in hand.
    print(f'{name} has cards: {", ".join(cards_in_hand)}')
    player_hand_value = get_hand_value(source_hand)
    # Display the value of those cards.
    print(f"{name} hand value is: {player_hand_value}")


def deal_new_card(source, destination, name):
    """Takes part of a list representing value's of the card from card_pack and moves it to the select hand of cards.
        Prints which card is dealt and then returns both updated list.
    Inputs:
        source: List with sublist (integer, integer, string, string) as (Value of 2-11, 2-14, "Suit", "Card Name")
                such as card_deck.
        destination: List with sublist (integer, integer, string, string) as (Value of 2-11, 2-14, "Suit", "Card Name")
                such as players_hand or dealers_hand
        name: A string for "Name" of who's hand the cards belong to.
    Returns:
        source: Updated to reflect card removed from its list.
        destination: Updated to reflect new card added to its list.
    """    
    # Move card from deck to hand.
    destination.append(source.pop())
    # Get length of card deck.
    last_card_num = len(destination)
    last_card_num -= 1
    # Print's string name of last card dealt.
    print(f"{name} is dealt card: {destination[last_card_num][3]}")
    return source, destination


def get_insurance(dealer_hand, player_hand, bet_amount, player_balance):
    """If dealer has an ace face up and the player has large enough balance, the player is presented with an 
        option to buy insurance if they choose to do so. The insurance_bet value will be updated and returned 
        with game_push to be later tracked for future events.
    Inputs:
        dealer_hand: List with sublist (integer, integer, string, string) as (Value of 2-11, 2-14, "Suit", "Card Name").
        player_hand: list with sublist (integer, integer, string, string) as (Value of 2-11, 2-14, "Suit", "Card Name").
        bet_amount: Integer value for the players current bet.
        player_balance: The running balance of credits teh player has available.
    Returns:
        insurance_bet: Integer representing value of the player taking insurance to be applied against their balance.
        game_push: Boolean to determin if during insurance bet a Push game happend and skip rest of the game.
    """    
    # Set push as not true.
    game_push = False
    player_hand_value = get_hand_value(player_hand)
    # If player already has blackjack, skip insurance option.
    if player_hand_value == 21:
        insurance_bet = 0
        return insurance_bet, game_push
    # Get cost of insurance.
    insurance_bet = round(bet_amount / 2) #House rules
    # Check if dealer face up card has an Ace.
    if dealer_hand[1][0] == 11 and player_balance >= insurance_bet:
        while True: 
            try:
                # Ace found, player prompted to purchase insurance.
                print(f"\nThe House has an Ace. Your balance is: {(player_balance - bet_amount)} credits")
                # "Would you like to buy insurance for {insurance_bet} credits? (Y)es or (N)o: "
                user_action = str(input(f"Would you like to buy insurance for {insurance_bet} credits? \033[93m(\033[00mY\033[93m)\033[00mes or \033[93m(\033[00mN\033[93m)\033[00mo: ")) 
                user_action = user_action.lower()
                if user_action == "y":
                    user_action = "yes"
                elif user_action == "n":
                    user_action = "no"
                # Player buys insurance
                if user_action == "yes":
                    #Dealer has blackjack
                    if dealer_hand[0][0] == 10:
                        print(f"Dealer revels face down card: {dealer_hand[0][3]}")
                        insurance_bet = round(insurance_bet * 2)
                        print(f"Players insurance payout is {insurance_bet} credits.")
                        player_hand_value = get_hand_value(player_hand)
                        if player_hand_value == 21:
                            game_push = True
                    # Player lost insurance bet.
                    else:
                        print(f"The House does not have 21. Insurance bet is lost.")
                        insurance_bet = insurance_bet * -1
                    print(f" Your balance is: {(player_balance - bet_amount) + (insurance_bet)} credits")
                    input("Press \033[93m<\033[00mEnter\033[93m>\033[00m to continue.\n")
                    break
                # Player does not buy insurance.        
                elif user_action == "no":
                    insurance_bet = 0
                    break
            except ValueError:
                continue
    else:
        # Insurance was not an option, the bet value is reset to 0
        insurance_bet = 0
    return insurance_bet, game_push


def double_down(card_deck, player_hand, bet_amount, player_balance):
    """Player is presented with option to double down if hand value is 9, 10 or 11 and
        player_balance has enough credits to cover the bet.
        If they do a new card will be added to their hand and bet amount is doubled. 
    Inputs:
        card_deck: List with sublist (integer, integer, string, string) as (Value of 2-11, 2-14, "Suit", "Card Name")
            A List of all 52 cards each stored as a sublist (int value, int card num, str suit, str of name).
        player_hand: list with sublist (integer, integer, string, string) as (Value of 2-11, 2-14, "Suit", "Card Name").
        bet_amount: Integer value of the current bet amount.
        player_balance: Interger reflecting current value of credits in players bank.
    Returns:
        card_deck: List will reflect the new missing card data.
        player_hand: List will reflect new data added.
        bet_amount: Updated to reflect players choice on bet.
    """
    # Get value of the players hand.
    player_hand_value = get_hand_value(player_hand)

    #Ask player to double down if 2 cards match and has enough balance to cover bet.
    if player_hand_value >= 9 and player_hand_value <= 11 and (player_balance >= (2 * bet_amount)):
        while True: 
            try:
                # Ask user "Would you like to double down? (Y)es or (N)o: "
                user_action = str(input(f"\nWould you like to double down? \033[93m(\033[00mY\033[93m)\033[00mes or \033[93m(\033[00mN\033[93m)\033[00mo: "))
                user_action = user_action.lower()
                if user_action == "y":
                    user_action = "yes"
                elif user_action == "n":
                    user_action = "no"
                if user_action == "yes":
                    #double the bet value if player decides to double down.
                    bet_amount = bet_amount * 2
                    card_deck, player_hand = deal_new_card(card_deck, player_hand, "Player")
                    display_full_hand(player_hand, "Player")
                    print("")
                    return card_deck, player_hand, bet_amount
                elif user_action == "no":
                    break
            except ValueError:
                continue
    return card_deck, player_hand, bet_amount


def hit_or_stand(card_deck, player_hand):
    """Present the user with choice how to play their hand; Hit or Stand. Each time they hit
        card data will be removed from card_deck list and added to player_hand list. If they
        get blackjack or bust they'll be forced to continue forward.
    Inputs:
        card_deck: List with sublist (integer, integer, string, string) as (Value of 2-11, 2-14, "Suit", "Card Name")
            A List of all 52 cards each stored as a sublist (int value, int card num, str suit, str of name).
        player_hand: list with sublist (integer, integer, string, string) as (Value of 2-11, 2-14, "Suit", "Card Name").
    Returns:
        card_deck: Updated to reflect cards removed from list.
        player_hand: Updated to reflect cards added to list.
    """

    # Refresh Player_hand_value.
    player_hand_value = get_hand_value(player_hand)

    # Player plays hand until Blackjack, Bust or Stands.
    while True: 
        try:
            # Ask user "Would you like to (H)it or (S)tand?: "
            user_action = str(input(f"\nWould you like to \033[93m(\033[00mH\033[93m)\033[00mit or \033[93m(\033[00mS\033[93m)\033[00mtand?: "))
            user_action = user_action.lower()
            if user_action == "s":
                user_action = "stand"
            elif user_action == "h":
                user_action = "hit"
            # User decides to "hit".
            if user_action == "hit":
                card_deck, player_hand = deal_new_card(card_deck, player_hand, "Player")
                display_full_hand(player_hand, "Player")
                player_hand_value = get_hand_value(player_hand)
                time.sleep(MED_PAUSE) 
            # User decides to "stand".
            if user_action == "stand":
                print(f"Player stands with a value of {player_hand_value}\n")
                break
            # Test for blackjack.
            if player_hand_value == 21:
                print(f"Blackjack, Congratulations! Player has {player_hand_value}\n")
                break
            # Test for bust.
            if player_hand_value > 21:
                print(f"Bust! Player has exceeded 21.\n")
                break
        except ValueError:
            continue
    # "Press <Enter> to continue."
    input("Press \033[93m<\033[00mEnter\033[93m>\033[00m to continue.")
    print("") #extra space after enter is pressed.
    return card_deck, player_hand


def player_split_hand(card_deck, player_hand, player_balance, bet_amount):
    """Present the player with a choice to split their hand if their player_balance has enough credit.
        If they split data for 1 card will be removed from list player_hand and moved to player_hand2
        and equal bet value will be applied to bet_amount2. Each hand will be dealt an extra card and 
        in this function the player will play the split hand.
    Inputs:
        card_deck: List with sublist (integer, integer, string, string) as (Value of 2-11, 2-14, "Suit", "Card Name")
            A List of all 52 cards each stored as a sublist (int value, int card num, str suit, str of name).
        player_hand: list with sublist (integer, integer, string, string) as (Value of 2-11, 2-14, "Suit", "Card Name") 
        player_balance: Interger reflecting current value of credits in players bank.
        bet_amount: Integer value of the current bet amount.
    Returns:
        card_deck: Updated to reflect cards removed from list.
        player_hand: Updated to reflect cards removed and added to list.
        player_hand2: Updated to reflect cards added to list.
        bet_amount2: Interger valued added based on bet_amount and user choices.
    """    
    # Defined blank list and variable for later use.
    player_hand2 = []
    bet_amount2 = 0
    # Checks if the players hand has two matching chards to split.
    if player_hand[0][0] == player_hand[1][0] and player_balance >= (bet_amount * 2):
        while True:
            try:
                print(f"\nYour balance is: {(player_balance - bet_amount)} credits.")
                # Ask user "Would you like to split for bet_amount credits? (Y)es or (No): "
                user_action = input(f"Would you like to split for {bet_amount} credits? \033[93m(\033[00mY\033[93m)\033[00mes or \033[93m(\033[00mN\033[93m)\033[00mo: ")
                if user_action == "y":
                    user_action = "yes"
                elif user_action == "n":
                    user_action = "no"
                # Player does split
                if user_action == "yes":
                    print("Player has chosen to split.\n")
                    time.sleep(MED_PAUSE)
                    # Move 1 card from first hand to a new hand.
                    player_hand2.append(player_hand.pop(0))
                    bet_amount2 = bet_amount
                    print(f"Player first hand has: {player_hand2[0][3]}")
                    # Deal new card for second hand.
                    card_deck, player_hand2 = deal_new_card(card_deck, player_hand2, "Player")
                    display_full_hand(player_hand2, "Player")
                    player_hand2_value = get_hand_value(player_hand2)
                    if player_hand2_value == 21:
                        print(f"Blackjack, Congratulations! {player_hand2_value}.\n")
                        bet_amount2 = bet_amount2 * 2 #We are extra friendly, 4:1
                    else:
                        # Ask player to double down.
                        card_deck, player_hand2, bet_amount2 = double_down(card_deck, player_hand2, bet_amount2, player_balance)
                        # Let user begin to play split hand.
                        card_deck, player_hand2 = hit_or_stand(card_deck, player_hand2)
                    # Deal remaning hand player_hand a new replacement card and exit.
                    print(f"Player second hand has: {player_hand[0][3]}")
                    card_deck, player_hand = deal_new_card(card_deck, player_hand, "Player")
                    display_full_hand(player_hand, "Player")
                    break
                # Player does not split.
                elif user_action == "no":
                    break
            except ValueError:
                continue
    return card_deck, player_hand, player_hand2, bet_amount2 


def player_main_hand(card_deck, player_hand, bet_amount, player_balance):
    """Final interaction of choices player has in the round to play their hand of cards without going bust. 
        including options to double down, hit and stand with their cards dealt.
    Inputs:
        card_deck: List with sublist (integer, integer, string, string) as (Value of 2-11, 2-14, "Suit", "Card Name")
            A List of all 52 cards each stored as a sublist (int value, int card num, str suit, str of name).
        player_hand: list with sublist (integer, integer, string, string) as (Value of 2-11, 2-14, "Suit", "Card Name"). 
        bet_amount: Integer value of the current bet amount.
        player_balance: Interger reflecting current value of credits in players bank.
    Returns:
        card_deck: Updated to reflect cards removed from list.
        player_hand: Updated to reflect cards added to list.
        bet_amount: Interger valued of the players associated bet
    """
    #Get value of cards.
    player_hand_value = get_hand_value(player_hand)
    
    # Check if player has hit a natural 21 and if true return.
    if player_hand_value == 21:
        print(f"Blackjack, Congratulations! Player has natural {player_hand_value}.\n")
        #bet_amount = bet_amount * 2 #We can be extra friendly, 4:1
        # "Press <Enter> to continue."
        input("Press \033[93m<\033[00mEnter\033[93m>\033[00m to continue.")
        print() #Space it out
        return card_deck, player_hand, bet_amount

    # Ask player to double down.
    card_deck, player_hand, bet_amount = double_down(card_deck, player_hand, bet_amount, player_balance)
    
    # Ask player if hey want to hit or stand while staying under 21.
    # Check if player has previously doubled down based on cards in hand.
    if len(player_hand) == 2:
        card_deck, player_hand = hit_or_stand(card_deck, player_hand)
    return card_deck, player_hand, bet_amount


def dealer_plays_hand(card_deck, dealer_hand, player_hand, player_hand2):
    """Dealer attempts to beat player hand(S) without going bust. It first determins which player_hand is larger in value,
        bust not bust; hand1 or hand2. Once determined the Dealer will attempt to get a higher value with its hand and exit.
    Inputs:
        card_deck card_deck: List with sublist (integer, integer, string, string) as (Value of 2-11, 2-14, "Suit", "Card Name")
            A List of all 52 cards each stored as a sublist (int value, int card num, str suit, str of name).
        dealer_hand: List with sublist (integer, integer, string, string) as (Value of 2-11, 2-14, "Suit", "Card Name"). 
        player_hand: List with sublist (integer, integer, string, string) as (Value of 2-11, 2-14, "Suit", "Card Name"). 
        player_hand2 List with sublist (integer, integer, string, string) as (Value of 2-11, 2-14, "Suit", "Card Name"). 
    Returns:
        card_deck: Updated to reflect cards removed from list.
        dealer_hand: Updated to reflect cards added to list.
    """
    player_hand_value1 = get_hand_value(player_hand)
    player_hand_value2 = get_hand_value(player_hand2)
    dealer_hand_value = get_hand_value(dealer_hand)

    # Determin which hand the dealer needs to beat from split.
    if player_hand_value1 <= 21 and player_hand_value1 >= player_hand_value2:
        player_winning_hand = player_hand_value1
    elif player_hand_value2 <= 21 and player_hand_value2 > player_hand_value1 and player_hand_value2 > 1: 
        player_winning_hand = player_hand_value2
    else:
        player_winning_hand = player_hand_value1

    # Prints dealers current cards to remind the player.
    print(f"Dealer reveals the face down card: {dealer_hand[0][3]}.")
    #print(f"The Houses hand value is: {dealer_hand_value}").
    display_full_hand(dealer_hand, "The House")
    print("")
    time.sleep(MED_PAUSE)

    # Dealer will deal new cards in attempt to beat the players cards.
    if player_winning_hand <= 21:
        max_num = random.randint(18, 19)
        # Random max number dealer feels lucky to go to  without busting.
        while dealer_hand_value <= max_num and dealer_hand_value < player_winning_hand:
            card_deck, dealer_hand = deal_new_card(card_deck, dealer_hand, "The House")
            display_full_hand(dealer_hand, "The House")
            dealer_hand_value = get_hand_value(dealer_hand)
            print()
            time.sleep(MED_PAUSE)

    # Check if the dealer has Blackjack.
    if dealer_hand_value == 21:
        print("Blackjack, the House has 21.\n")
    # Check if the dealer has bust.
    if dealer_hand_value > 21:
        print("Bust, the House has more than 21.\n")
    #"Press <Enter> to continue."
    input("Press \033[93m<\033[00mEnter\033[93m>\033[00m to continue.")
    print("") #give space, after user hit enter.
    return card_deck, dealer_hand


def settlements(dealer_hand, player_hand, player_hand2, bet_amount, bet_amount2, player_balance):
    """Will take in all needed game data for the round, determin the winner for each hand and 
        payoff / collect current bets. The final information is displayed in a summery for the user.
    Inputs:
        dealer_hand: List with sublist (integer, integer, string, string) as (Value of 2-11, 2-14, "Suit", "Card Name"). 
        player_hand: List with sublist (integer, integer, string, string) as (Value of 2-11, 2-14, "Suit", "Card Name"). 
        player_hand2 List with sublist (integer, integer, string, string) as (Value of 2-11, 2-14, "Suit", "Card Name").
        bet_amount: Integer value of the current bet amount.
        bet_amount2: Integer value of the current bet amount.
        player_balance: Interger reflecting current value of credits in players bank. 
    Returns:
        player_balance: Updated to reflect players performance and continue a running balance.
    """
    player_hand_value1 = get_hand_value(player_hand)
    player_hand_value2 = get_hand_value(player_hand2)
    dealer_hand_value = get_hand_value(dealer_hand)

    print("\033[93m#####\033[00m  Game Summery  \033[93m#####\033[00m\n")
    # Check if split was happened, then post if yes.
    if player_hand_value2 > 0:
        # Player bust.
        if player_hand_value2 > 21:
            bet_amount2 = bet_amount2 * -1
            who_won = "Bust, player lost."
            bet_summery = str("Payout: "+(str(bet_amount2)+" credits lost"))
        # If dealer bust, but not player.
        elif dealer_hand_value > 21 and player_hand_value2 <=21: #Just to be sure!
            bet_amount2 = bet_amount2 * 2
            who_won = "The House bust, player wins."
            bet_summery = str("Payout: +"+(str(bet_amount2)+" credits won"))
        # If the hand is a push.
        elif player_hand_value2 == dealer_hand_value:
            who_won = "Winner: Push"
            bet_summery = "Payout: No wins or losses"
            bet_amount2 = 0
        # If player hand wins.   
        elif player_hand_value2 <= 21 and player_hand_value2 > dealer_hand_value:
            bet_amount2 = bet_amount2 * 2
            who_won = "Player Wins!"
            bet_summery = str("Payout: +"+(str(bet_amount2)+" credits won"))
        # The dealer wins.
        elif dealer_hand_value <= 21 and dealer_hand_value > player_hand_value2:
            bet_amount2 = bet_amount2 * -1
            who_won = "The House wins."
            bet_summery = str("Payout: "+(str(bet_amount2)+" credits lost"))
        #Update player balance.
        player_balance += bet_amount2
        # Display summery of hand2 (split).
        display_full_hand(player_hand2, "Player")
        display_full_hand(dealer_hand, "The House")
        time.sleep(MED_PAUSE)
        print(str(f"\n{who_won}"))
        print(str(f"{bet_summery}\n"))
        # "Press <Enter> to continue."
        input("Press \033[93m<\033[00mEnter\033[93m>\033[00m to continue.\n")
        time.sleep(MED_PAUSE)

    #For first hand of cards.
    if player_hand_value1 > 21:
        bet_amount = bet_amount * -1
        who_won = "Bust, player lost."
        bet_summery = str("Payout: "+(str(bet_amount)+" credits lost"))
    # If dealer bust
    elif dealer_hand_value > 21 and player_hand_value1 <=21: #Just to be sure!
        bet_amount = bet_amount * 2
        who_won = "The House bust, player wins."
        bet_summery = str("Payout: +"+(str(bet_amount)+" credits won"))
    # If the hand is a push.
    elif player_hand_value1 == dealer_hand_value:
        who_won = "Winner: Push"
        bet_summery = "Payout: No wins or losses"
        bet_amount = 0
    # If player hand wins.   
    elif player_hand_value1 <= 21 and player_hand_value1 > dealer_hand_value:
        bet_amount = bet_amount * 2
        who_won = "Player Wins"
        bet_summery = str("Payout: +"+(str(bet_amount)+" credits won"))
    # The dealer wins.
    elif dealer_hand_value <= 21 and dealer_hand_value > player_hand_value1:
        bet_amount = bet_amount * -1
        who_won = "The House wins."
        bet_summery = str("Payout: "+(str(bet_amount)+" credits lost"))
        
    # Update player balance
    player_balance += bet_amount
    # Display summery.
    display_full_hand(player_hand, "Player")
    display_full_hand(dealer_hand, "The House")
    time.sleep(MED_PAUSE)
    print(str(f"\n{who_won}"))
    print(str(f"{bet_summery}"))
    print(f"\nFinal player balance is: {player_balance} credits")
    print(f"--------------------------\n")
    time.sleep(MED_PAUSE)
    return int(player_balance)


def play_another_game():
    """Prompt the user if they would like to play another round or exit.
    Returns:
        play_again: Boolean True or False
    """
    #Repeat blackjack() Y/N?
    while True:
        try:
            # Ask if player wants to play again or exit.
            # "Would you like to play again? (Y)es or (N)o: "
            user_action = str(input("Would you like to play again? \033[93m(\033[00mY\033[93m)\033[00mes or \033[93m(\033[00mN\033[93m)\033[00mo: "))
            user_action = user_action.lower()
            if user_action == "y":
                user_action = "yes"
            elif user_action == "n":
                user_action = "no"
            # Player Wants to play again.
            if user_action == "yes":
                print("")
                play_again = True
                break
            elif user_action == "no":
                print("")
                play_again = False
                break
        except ValueError:
            continue
    return play_again


def blackjack():
    """The core function for controlling flow of the game of blackjack. Will run in loop
        until play_another_game() prompts the user to exit. It will collect bets,
        deal cards and payout bets until the player wishes to end.
        
        There are no pre or post requisites.
    """
    #Starting credit balance in the players bank.
    player_balance = STARTING_BALANCE
    
    #Deck of cards to be used in game.
    card_deck = []
    # A future random number to be used where the cut is in the deck.
    cut_num = int(0)
    play_again = True
    # Builds a playing deck of 52 cards to be used in the game.
    pack_of_cards = build_cards()

    # Main game will loop until the player selects not to play again,
    # then it will exit. See play_another_game().
    while play_again == True:
        # Reset player basic details each loop.
        player_hand = []
        player_hand2 = []
        bet_amount = 0
        bet_amount2 = 0

        #Build a playing deck with multiple packs of cards and then shuffles them.
        #Will also check how often deck needs to be reshuffled from the radom cut.
        card_deck, cut_num = refresh_deck(card_deck, pack_of_cards, NUM_OF_DECKS, cut_num)
        
        # Give player extra credits if they are low.
        player_balance = on_the_house(player_balance)

        # Collects amount of players starting bet.
        bet_amount = get_opening_bet(player_balance)
        time.sleep(MED_PAUSE)
        
        # Deals and collects data on first two cards for player and dealer.
        player_hand, card_deck = start_player_cards(card_deck)
        dealer_hand, card_deck = start_dealer_cards(card_deck)
        
        # Prints results of hands dealt of the opening game.
        player_starting_data(player_hand)
        dealer_starting_data(dealer_hand)
        time.sleep(MED_PAUSE)

        # Ask player for insurance and check if house value of 21 is True.
        insurance_bet, game_push = get_insurance(dealer_hand, player_hand, bet_amount, player_balance)
        # Update player_balance if insurance was won or lost.
        player_balance = player_balance + insurance_bet

        # Check if user played an insurance bet.
        # This section will wrap up rest of the game play options.
        if insurance_bet <= 0 and game_push == False:
            # Checks if player can split hand and gives option to do so.
            card_deck, player_hand, player_hand2, bet_amount2 = player_split_hand(card_deck, player_hand, player_balance, bet_amount)
            # Player gets to make his final interactions for this round.
            card_deck, player_hand, bet_amount = player_main_hand(card_deck, player_hand, bet_amount, player_balance)
            time.sleep(MED_PAUSE)
            # Dealer/House tries to beat the players hand.
            card_deck, dealer_hand = dealer_plays_hand(card_deck, dealer_hand, player_hand, player_hand2)
            time.sleep(MED_PAUSE)
        
        #Who wins and lose, tally up the bets.
        player_balance = settlements(dealer_hand, player_hand, player_hand2, bet_amount, bet_amount2, player_balance)
        
        # Ask the user to play another game Y/N.
        play_again = play_another_game()


def main():
# Main function, serves as place holder to add more games.
    #Display intro text.
    intro()
    #Load game of blackjack.
    blackjack()
    #Thank you notice on exit.
    thank_you()

if __name__ == "__main__":
    main()