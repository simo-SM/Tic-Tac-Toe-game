# ====================================================================================
# [1] RUN THE APP
# ====================================================================================

import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ====================================================================================
# [4] PLAYER 1 NAME, SYMBOL | PLAYER 2 NAME, SYMBOL
# ====================================================================================

class Player:
    def __init__(self):
        self.name = ""
        self.symbol = ""

    def choose_name(self):
        while True:
            name = input("\033[1;33mEnter your name (letters only): ")
            if name.isalpha():
                self.name = name
                break
            print("\033[1;31mInvalid name. Please use letters only.")

    def choose_symbol(self):
        while True:
            symbol = input(f"{self.name}, \033[1;33mchoose your symbol (a single letter): ")
            if symbol.isalpha() and len(symbol) == 1:
                self.symbol = symbol.upper()
                break
            print("\033[1;31mInvalid symbol. Please choose a single letter.")


# ====================================================================================
# [2] MAIN MENU
# ====================================================================================

class Menu:
    def display_main_menu(self):
        clear_screen()
        print('''

\033[1;33m                                   _____ _         _____             _____       
\033[1;33m                                  |_   _(_) ___   |_   _|_ _  ___   |_   _|__   ___ 
\033[1;33m                                    | | | |/ __|____| |/ _` |/ __|____| |/ _ \ / _ \           
\033[1;33m                                    | | | | (_|_____| | (_| | (_|_____| | (_) |  __/
\033[1;33m                                    |_| |_|\___|    |_|\__,_|\___|    |_|\___/ \___|        
\033[1;33m                                    __ _  __ _ _ __ ___   ___                       
\033[1;33m                                   / _` |/ _` | '_ ` _ \ / _ \                      
\033[1;33m                                  | (_| | (_| | | | | | |  __/                      
\033[1;33m                                   \__, |\__,_|_| |_| |_|\___|                      
\033[1;33m                                   |___/                                            



''')
    
        print("\n\033[1;36mWELCOME TO MY X-O GAME!\033[0m")
        print("\033[1;31m[1]\033[1;32m Start Game")
        print("\033[1;31m[2]\033[1;32m Quit Game")
        choice = input("\033[1;32mEnter your choice (1 or 2): ")
        return choice

    def display_endgame_menu(self):
        print("\n\033[1;35mGame Over!\033[0m")
        print("\033[1;31m[1]\033[1;33m Restart Game")
        print("\033[1;31m[2]\033[1;33m Quit Game")
        return input("\033[1;32mEnter your choice (1 or 2): ")


# ====================================================================================
# [5] BOARD IS DISPLAYED
# ====================================================================================

class Board:
    def __init__(self):
        self.board = [str(i) for i in range(1, 10)]

    def display_board(self):
        color_map = {
            'X': '\033[1;34mX\033[0m',
            'O': '\033[1;31mO\033[0m'
        }

        def colorize(cell):
            return color_map.get(cell.upper(), cell)

        print("\n\033[1;37mCurrent Board:\033[0m")
        for i in range(0, 9, 3):
            row = [colorize(self.board[j]) for j in range(i, i + 3)]
            print(f"| {' | '.join(row)} |")
            if i < 6:
                print("-" * 17)

    def update_board(self, choice, symbol):
        if self.is_valid_move(choice):
            self.board[choice - 1] = symbol
            return True
        return False

    def is_valid_move(self, choice):
        return self.board[choice - 1].isdigit()

    def reset_board(self):
        self.board = [str(i) for i in range(1, 10)]


# ====================================================================================
# [3] GAME START, QUIT THE GAME
# ====================================================================================
# ====================================================================================
# [6] GAME LOOPS UNTIL WIN OR DRAW
# ====================================================================================

class Game:
    def __init__(self):
        self.players = [Player(), Player()]
        self.board = Board()
        self.menu = Menu()
        self.current_player_index = 0

    def start_game(self):
        choice = self.menu.display_main_menu()
        if choice == '1':
            self.setup_players()
            self.play_game()
        else:
            self.quit_game()

    def setup_players(self):
        for i, player in enumerate(self.players, start=1):
            print(f"\n\033[1;34mPlayer {i}, enter your details:\033[0m")
            player.choose_name()
            while True:
                player.choose_symbol()
                if i == 2 and player.symbol == self.players[0].symbol:
                    print("\033[1;31mThis symbol is already taken by Player 1. Choose another.\033[0m")
                else:
                    break

    def play_game(self):
        while True:
            self.play_turn()
            if self.check_win():
                self.board.display_board()
                print(f"\033[1;32m{self.players[self.current_player_index].name} wins!\033[0m")
                choice = self.menu.display_endgame_menu()
                if choice == '1':
                    self.restart_game()
                else:
                    self.quit_game()
                    break
            elif self.check_draw():
                self.board.display_board()
                print("\033[1;33mIt's a draw!\033[0m")
                choice = self.menu.display_endgame_menu()
                if choice == '1':
                    self.restart_game()
                else:
                    self.quit_game()
                    break

    def play_turn(self):
        player = self.players[self.current_player_index]
        self.board.display_board()
        print(f"\033[1;36m{player.name}'s turn ({player.symbol})\033[0m")
        while True:
            try:
                cell_choice = int(input("\033[1;33mChoose a cell (1-9): "))
                if 1 <= cell_choice <= 9 and self.board.update_board(cell_choice, player.symbol):
                    break
                else:
                    print("\033[1;31mInvalid move, try again.")
            except ValueError:
                print("\033[1;31mPlease enter a number between 1 and 9.")
        self.switch_player()

    def check_win(self):
        b = self.board.board
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        for combo in win_combinations:
            if b[combo[0]] == b[combo[1]] == b[combo[2]]:
                return True
        return False

    def check_draw(self):
        return all(not cell.isdigit() for cell in self.board.board)

    def switch_player(self):
        self.current_player_index = 1 - self.current_player_index

    # ====================================================================================
    # [7] RESTART GAME, QUIT GAME
    # ====================================================================================

    def restart_game(self):
        self.board.reset_board()
        self.current_player_index = 0
        clear_screen()
        self.play_game()

    def quit_game(self):
        print("\033[1;34mTHANK YOU FOR PLAYING!\033[0m")


# ====================================================================================
# Start the game
# ====================================================================================

if __name__ == "__main__":
    game = Game()
    game.start_game()
