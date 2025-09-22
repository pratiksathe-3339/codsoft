#Rock-Paper-Scissors Game


import random


VALID_CHOICES = {"rock": "r", "paper": "p", "scissors": "s", "r": "r", "p": "p", "s": "s"}
CHOICE_NAMES = {"r": "rock", "p": "paper", "s": "scissors"}

# Outcome matrix: (player, computer) -> result
# result: 1 = player wins, 0 = tie, -1 = player loses
OUTCOME = {
	("r", "s"): 1,
	("s", "p"): 1,
	("p", "r"): 1,
	("s", "r"): -1,
	("p", "s"): -1,
	("r", "p"): -1,
}


def get_player_choice() -> str:
	"""Prompt user for rock/paper/scissors. Returns canonical short code: r/p/s."""
	while True:
		user_input = input("Choose rock, paper, or scissors (r/p/s): ").strip().lower()
		if user_input in VALID_CHOICES:
			return VALID_CHOICES[user_input]
		print("Invalid choice. Please enter rock, paper, scissors, or r/p/s.")


def get_computer_choice() -> str:
	"""Randomly choose r/p/s for the computer."""
	return random.choice(["r", "p", "s"])


def determine_result(player: str, computer: str) -> int:
	"""Return 1 if player wins, 0 if tie, -1 if player loses."""
	if player == computer:
		return 0
	return OUTCOME.get((player, computer), -OUTCOME.get((computer, player), 0))


def display_round(player: str, computer: str, result: int) -> None:
	print(f"You chose: {CHOICE_NAMES[player]}")
	print(f"Computer chose: {CHOICE_NAMES[computer]}")
	if result == 1:
		print("Result: You win! 🎉")
	elif result == -1:
		print("Result: You lose.  TRY THE BETTER LUCK NEXT TIME 👎!")
	else:
		print("Result: It's a tie. 😐")


def ask_play_again() -> bool:
	while True:
		answer = input("Play again? (y/n): ").strip().lower()
		if answer in ("y", "yes"):
			return True
		if answer in ("n", "no"):
			return False
		print("Please answer with y/yes or n/no.")


def play_game() -> None:
	print("=== Rock • Paper • Scissors ===")
	print("Instructions: Type rock, paper, or scissors (or r/p/s). First to 5 wins optional; just keep playing as you like.")
	player_score = 0
	computer_score = 0
	round_number = 1
	while True:
		print(f"\n-- Round {round_number} --")
		player = get_player_choice()
		computer = get_computer_choice()
		result = determine_result(player, computer)
		display_round(player, computer, result)

		if result == 1:
			player_score += 1
		elif result == -1:
			computer_score += 1

		print(f"Score — You: {player_score} | Computer: {computer_score}")

		if not ask_play_again():
			print("\nThanks for playing! Final Score:")
			print(f"You: {player_score} | Computer: {computer_score}")
			if player_score > computer_score:
				print("Overall: You win the session! 🏆")
			elif player_score < computer_score:
				print("Overall: Computer wins the session. 🤖")
			else:
				print("Overall: It's a draw.")
			break

		round_number += 1


if __name__ == "__main__":
	play_game() 