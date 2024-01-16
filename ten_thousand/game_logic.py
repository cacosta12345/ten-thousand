# Imports the random module, which provides functions for generating random numbers.
import random

# Defines a class named GameLogic
class GameLogic:
    # Declares a static method calculate_score within the GameLogic class. It's a method that doesn't need an
    #instance of the class to be called and doesn't access the instance or class-level data.
    @staticmethod
    def calculate_score(dice_roll):
        # This line checks if the dice_roll tuple represents a straight (1-6). If so, it returns a score of 1500.
        if set(dice_roll) == set(range(1, 7)):
            return 1500
        # Checks if the dice_roll contains exactly three pairs. If so, it also returns a score of 1500.
        if len(dice_roll) == 6 and all(dice_roll.count(value) == 2 for value in set(dice_roll)):
            return 1500

        # Sets the initial score to 0.
        score = 0
        # Creates a dictionary (counts) that maps each unique dice value to its frequency in the roll.
        counts = {x: dice_roll.count(x) for x in set(dice_roll)}

        # Loops through each unique dice value (num) and its count (count) in the counts dictionary.
        for num, count in counts.items():
            # Checks if a particular number appears three or more times.
            if count >= 3:
                # If there are three or more of a kind, and the number is 1, adds 1000 points; otherwise, adds 100 times the number.
                if num == 1:
                    score += 1000
                else:
                    score += num * 100
                # If there are four of the same number, it adds an additional score. For ones, it adds 1000 points; for other numbers, it adds 100 times the number.
                if count == 4:
                    score += 1000 if num == 1 else num * 100
                # If there are five of the same number, it adds more to the score. For ones, it adds 2000 points; for other numbers, it adds 200 times the number.
                elif count == 5:
                    score += 2000 if num == 1 else num * 200
                elif count == 6:
                # If there are six of the same number, it adds even more to the score. For ones, it adds 3000 points; for other numbers, it adds 300 times the number.
                    score += 3000 if num == 1 else num * 300
            # Adds points for any ones or fives that are not part of a triplet or larger group. Each one adds 100 points, and each five adds 50 points.
            elif num == 1 or num == 5:
                score += (100 if num == 1 else 50) * count
        # Returns the total calculated score for the dice roll.
        return score
    
    # Declares a static method roll_dice to simulate rolling dice.
    @staticmethod
    def roll_dice(num_dice):
        # Checks if the number of dice to roll (num_dice) is within the valid range (1 to 6). If not, it raises a ValueError.
        if not 1 <= num_dice <= 6:
            raise ValueError("Number of dice must be between 1 and 6")
        # Generates a tuple of random integers, each between 1 and 6, representing the result of rolling dice. The length of the tuple is determined by num_dice.
        return tuple(random.randint(1, 6) for _ in range(num_dice))

