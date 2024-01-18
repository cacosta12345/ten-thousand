from ten_thousand.game_logic import GameLogic

class PlayGame:
    def __init__(self, roller=None):
        print("Welcome to Ten Thousand! \nReady to play?")
        self.banker = Banker()
        self.current_round = 1
        self.roller = roller

        play_game = input("(y)es to play or (n)o to decline\n> ").lower()
        if play_game == "n":
            print("OK. Maybe another time")
            return

    def play(self):
        continue_playing = True
        while continue_playing:
            self.play_round()
            continue_playing = self.should_continue()

    def play_round(self):
        print(f"\nRound {self.current_round}")
        num_dice = 6
        current_roll = self.roller(num_dice) if self.roller else GameLogic.roll_dice(num_dice)
        print(f"\nYour roll: {current_roll}")

        score = GameLogic.calculate_score(current_roll)
        print(f"Score for this roll: {score}")

        while True:
            choice = input("Do you want to (B)ank your score, (R)oll again, or (Q)uit? ").upper()

            if choice == 'B':
                self.banker.shelf(score)
                self.banker.bank()
                print(f"\nBanked score: {self.banker.balance}")
                self.current_round += 1
                break
            elif choice == 'R':
                try:
                    num_to_set_aside = int(input("How many dice do you want to set aside? "))
                    self.roll_again(num_dice, num_to_set_aside)
                except ValueError:
                    print("Invalid input. Please enter a number.")
            elif choice == 'Q':
                print(f"Thanks for playing! Final score: {self.banker.balance}")
                return

    def roll_again(self, num_dice, num_to_set_aside):
        if num_to_set_aside < num_dice:
            set_aside_dice = set(input("Enter dice to set aside: "))
            new_roll = self.roller(num_dice) if self.roller else GameLogic.roll_dice(num_dice)
            current_roll = tuple(die for die in new_roll if die not in set_aside_dice)
            self.update_score(current_roll)
        else:
            print("Invalid input. You can't set aside more dice than you have.")

    def update_score(self, current_roll):
        score = GameLogic.calculate_score(current_roll)
        print(f"\nYour new roll: {current_roll}")
        print(f"Score for this roll: {score}")
        if score == 0:
            print("\nBankrupt! You lose all points for this round.")
            self.banker.clear_shelved()
        else:
            self.banker.shelf(score)

    def should_continue(self):
        if self.banker.balance > 0:
            choice = input("Do you want to (C)ontinue or (Q)uit? ").upper()
            return choice == 'C'
        else:
            return True


class Banker:
    def __init__(self):
        self.balance = 0
        self.shelved = 0

    def shelf(self, points):
        self.shelved += points

    def clear_shelved(self):
        self.shelved = 0

    def bank(self):
        self.balance += self.shelved
        self.clear_shelved()


if __name__ == "__main__":
    # Pass GameLogic.roll_dice as the default roller function
    game = PlayGame(roller=GameLogic.roll_dice)
    game.play()