from ten_thousand.game_logic import GameLogic
from collections import Counter

def play(roller=GameLogic.roll_dice, num_rounds=20):
  
    response = invite_to_play()
    if response == "y":
        start_game(num_rounds, roller)
    else:
        decline_game()

def invite_to_play():
  
    return input("Welcome to Ten Thousand!\nReady to play?(y)es to play or (n)o to decline\n> ").lower()

def start_game(num_rounds, roller):
   
    banked_points = 0
    for round_num in range(1, num_rounds + 1):
        round_points, shelved_points = do_round(round_num, roller, 0)
        if round_points == -1:
            break
        banked_points += shelved_points
        print(f"You banked {shelved_points} points in round {round_num}")
        print(f"Total score is {banked_points} points")

def do_round(round_num, roller, shelved_points):
    
    print(f"\nStarting Round {round_num}")
    num_dice = 6

    while num_dice > 0:
        roll = do_roll(num_dice, roller)
        formatted_roll = format_roll(roll)
        print(formatted_roll)

        valid_input = False
        while not valid_input:
            keeper_string = input("Enter dice to keep, or (q)uit:\n> ")
            if keeper_string.lower() == "q":
                return -1, shelved_points  # Special value for quit

            keepers = convert_keepers(keeper_string)
            if is_valid_input(keepers, roll):
                valid_input = True
            else:
                print("Invalid input. Please enter dice values that match the roll.")

        score = GameLogic.calculate_score(keepers)
        shelved_points += score
        num_dice -= len(keepers)
        print(f"You have {shelved_points} unbanked points and {num_dice} dice remaining")

        next_action = input("(r)oll again, (b)ank your points or (q)uit:\n> ").lower()
        if next_action == "b":
            return shelved_points, shelved_points
        elif next_action == "q":
            print(f"Thanks for playing. You earned {shelved_points} points")
            return -1, shelved_points

    return shelved_points, shelved_points

def is_valid_input(keepers, roll):
   
    
    roll_counter = Counter(roll)
    keeper_counter = Counter(keepers)
    for keeper in keeper_counter:
        if keeper_counter[keeper] > roll_counter[keeper]:
            return False
    return True

def do_roll(num_dice, roller):
    
    return roller(num_dice)

def format_roll(roll):
   
    return f"*** {' '.join(map(str, roll))} ***"

def convert_keepers(keeper_string):
  
    try:
        return tuple(int(die) for die in keeper_string if die.isdigit())
    except ValueError:
        return ()  # or handle the error differently

def decline_game():
  
    print("OK. Maybe another time")

if __name__ == "__main__":
    play()
