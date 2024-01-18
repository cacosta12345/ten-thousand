from ten_thousand.game_logic import GameLogic

class PlayGame:
    def __init__(self, roller=None):
        
        self.banker = Banker()
        self.current_round = 1
        self.roller = roller

    @staticmethod
    def start_game():
        play_game = input("Welcome to Ten Thousand!\nReady to play?(y)es to play or (n)o to decline\n> ").lower()
        if play_game == "y":
            game = PlayGame(roller=GameLogic.roll_dice)
            game.play()
        else:
            print("OK. Maybe another time")

    def play(self):
        while True:
            if not self.play_round():
                break

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
                break  # Breaks out of the while loop, but doesn't end the game
            elif choice == 'R':
                try:
                    num_to_set_aside = int(input("How many dice do you want to set aside? "))
                    self.roll_again(num_dice, num_to_set_aside)
                except ValueError:
                    print("Invalid input. Please enter a number.")
            elif choice == 'Q':
                print(f"Thanks for playing! Final score: {self.banker.balance}")
                return False  # Ends the game

        return True  # Continues the game

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
    PlayGame.start_game()