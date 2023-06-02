from random import randint


class Game:

    def __init__(self):
        self.board = ["_" for _ in range(0, 9)]
        self.player = User()
        self.computer_symbol = None
        self.computer = None
        self.scoreboard = ScoreBoard()

    def display_board(self):
        print("-------------------")
        for num in range(0, 9, 3):
            print("|", self.board[num:num + 3], "|")
        print("-------------------")

    def start(self):
        self.display_board()
        self.player.symbol_choice()
        self.computer_symbol = "X" if self.player.user_choice == "O" else "O"
        self.computer = Computer(comp_symbol=self.computer_symbol)
        print(f"You chose: {self.player.user_choice}")
        print(f"Computer will play as: {self.computer.comp_symbol}")
        if self.player.user_choice == "O":
            self.main_game(game_status=True, player_turn=True)
        else:
            self.main_game(game_status=True, player_turn=False)

    def check_winner(self):
        winning_combinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8],  # By Column
                                [0, 3, 6], [1, 4, 7], [2, 5, 8],  # By Row
                                [0, 4, 8], [2, 4, 6]]  # By Diagonal
        for combination in winning_combinations:
            positions = [self.board[position] for position in combination]
            if all(position == positions[0] and position != '_' for position in positions):
                print(f'{positions[0]} Wins!')  # Returns the winning symbol
                return True
        if "_" not in self.board:
            print('It is a draw')
            return True
        return False

    def main_game(self, game_status, player_turn):
        while game_status:

            if player_turn:
                self.player.user_turn(self.board)
                if self.check_winner():
                    self.scoreboard.update_user_score()
                    break
                else:
                    self.computer.computer_turn(self.board)
                    self.display_board()
                    if self.check_winner():
                        self.scoreboard.update_comp_score()
                        break
            else:
                self.computer.computer_turn(self.board)
                self.display_board()
                if self.check_winner():
                    self.scoreboard.update_comp_score()
                    break
                self.player.user_turn(self.board)
                if self.check_winner():
                    self.scoreboard.update_user_score()
                    break

        while True:
            self.scoreboard.display_scores()
            play_again = input("Would you like to play again? (y/n) ").strip().upper()
            if play_again == "Y":
                self.restart_game()
                break
            elif play_again == "N":
                print("Goodbye")
                break
            else:
                print("Invalid input. Please enter 'Y' or 'N'.")

    def restart_game(self):
        self.board = ["_" for _ in range(0, 9)]
        self.player.user_choice = None
        self.computer_symbol = None
        self.display_board()
        self.start()


class User:
    def __init__(self):
        self.valid_choice = ['X', 'O']
        self.user_choice = None

    def symbol_choice(self):
        while True:
            self.user_choice = input("Would you like to be the X or the O?: ").upper()
            if self.user_choice not in self.valid_choice:
                print("Please input only 'X' or 'O'!")
                continue
            break
        return self.user_choice

    def user_turn(self, board):
        while True:
            round_choice = input(
                "Where would you like to play? Answer in the format col_num, row_num. Ex: 1,2\n").split(
                ",")
            try:
                col_num = int(round_choice[0]) - 1
                row_num = int(round_choice[1]) - 1
                if (0 <= col_num <= 2) and (0 <= row_num <= 2):
                    place_index = row_num * 3 + col_num
                    if board[place_index] == '_':
                        board[place_index] = self.user_choice
                        break
                else:
                    print("Invalid input. Please provide valid column and row numbers.")
                    continue
            except ValueError:
                print("Invalid input. Please provide both column and row numbers.")
                continue


class Computer:
    def __init__(self, comp_symbol):
        self.comp_symbol = comp_symbol

    def computer_turn(self, board):
        while True:
            col_num = randint(1, 3) - 1
            row_num = randint(1, 3) - 1
            place_index = row_num * 3 + col_num

            if board[place_index] == '_':
                board[place_index] = self.comp_symbol
                break


class ScoreBoard:

    def __init__(self):
        self.user_score = 0
        self.comp_score = 0

    def update_user_score(self):
        self.user_score += 1

    def update_comp_score(self):
        self.comp_score += 1

    def display_scores(self):
        print("Scoreboard:")
        print(f"User: {self.user_score}  Computer: {self.comp_score}")
