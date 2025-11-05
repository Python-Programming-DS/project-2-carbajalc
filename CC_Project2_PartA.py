import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn import metrics, svm
from sklearn.model_selection import GridSearchCV
import warnings


# Board Constructor
class Board():
    # constructor initiates board with empty cells
    def __init__(self):
        self.board = [[" ", " ", " "],
                      [" ", " ", " "],
                      [" ", " ", " "]]
    
    # prints board and marks
    def printBoard(self):
        print("-" * 17)
        print("|R\\C| 0 | 1 | 2 |")

        for i in range(len(self.board)): # rows
            print("_" * 17)
            print(f"| {i} | {self.board[i][0]} | {self.board[i][1]} | {self.board[i][2]} |") # prints each row of the board
        print("_" * 17)
        print()

# Game Constructor
class Game():
    # initializes board and turn
    def __init__(self):
        self.board = Board()
        self.turn = 'X'
    
    # switches player turn
    def switchPlayer(self):
        if self.turn == 'X':
            self.turn = 'O'
        else:
            self.turn = "X"
    
    # checks if user entry is valid, return boolean
    def validateEntry(self):
        print(f"{self.turn}'s turn.")
        print(f"Where do you want your {self.turn} placed?")
        row_col = input("Please enter row number and column number separated by a comma.\n")
        row_col = row_col.split(",")
        row = int(row_col[0])
        col = int(row_col[1])
        print(f"You have entered row #{row} and column #{col}")

         # Looping through board
        if row in range(len(self.board.board)): # rows
            if col in range(len(self.board.board[0])): # cols
                if self.board.board[row][col] == " ": # Empty space, valid entry
                    self.board.board[row][col] = self.turn
                    return True
                else: # Non empty space, invalid entry
                    print("That cell is already taken.")
                    print("Please make another selection.\n")
                    return False 
    
        # row or col not in range, invalid entry
        print("Invalid entry: try again.")
        print("Row & column numbers must be either 0, 1, or 2.\n")
        return False
    
    # checks if all board spaces are marked, return boolean
    def checkFull(self):
        # Looping through board
        for i in range(len(self.board.board)): # rows
            for j in range(len(self.board.board[0])): # cols
                if self.board.board[i][j] == " ": # returns false for any empty space
                    return False
        # went through whole loop, no empty space
        return True
    
    # checks if there are any row, col or diag wins, returns boolean
    def checkWin(self):
        row_cols = []

        for i in range(len(self.board.board)): # row
            for j in range(len(self.board.board[0])): # col
                if self.board.board[i][j] == self.turn:
                    row_cols.append([i, j]) # storing all places turn has occupied
    
        if len(row_cols) <= 2: # Needs to have at least 3 marks
            return False

        for x,y in row_cols:
            # Row checking
            count = 0
            for i in range(3):
                if [x+i, y] in row_cols:
                    count += 1
                else:
                    break
            if count == 3:
                return True

            # Column checking
            count = 0
            for i in range(3):
                if [x, y+i] in row_cols:
                    count += 1
                else:
                    break
            if count == 3:
                return True
        
            # Diagonal down-right
            count = 0
            for i in range(3):
                if [x+i, y+i] in row_cols:
                    count += 1
                else:
                    break
            if count == 3:
                return True

            # Diagonal down-left
            count = 0
            for i in range(3):
                if [x+i, y-i] in row_cols:
                    count += 1
                else:
                    break
            if count == 3:
                return True
        
        return False
    
    # checks if game is over, return boolean
    def checkEnd(self):
        board_win = self.checkWin()
        board_full = self.checkFull()

        if board_win == True:
            print(f"{self.turn} IS THE WINNER!!!")
            self.board.printBoard()
            return True
        elif board_full == True:
            print("\nDRAW! NOBODY WINS!\n")
            self.board.printBoard()
            return True
        
        self.board.printBoard()
        return False
    
        # minmax algorithm (optional for player)
    def min_max_move(self, board, turn): # making sure not to mess with self.board and self.turn
        if self.checkWin() and turn == 'X':
            return 1, None
        if self.checkWin() and turn == 'O':
            return -1, None
        if self.checkFull():
            return 0, None

        # Need to see all available moves
        all_moves = []
        board = self.board.board
        turn = self.turn

        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == " ":
                    all_moves.append([i, j])
        
        if turn == 'X': # X is maxmimizer
            best_score = -float('inf') # starting off with lowest score
            best_move = None

            for i,j in all_moves: # Going through all available moves
                board[i][j] = 'X' # trying each move
                score, _ = self.min_max_move(board, 'O') # getting best move for O
                board[i][j] = ' ' # clearning up move
                if score > best_score: # if we get a better score with the move
                    best_score = score
                    best_move = [i, j]
            return best_score, best_move # returning best score and move after all recursions
        
        else: # O is the minimizer, repeated code above but just for O
            best_score = -float('inf')
            best_move = None

            for i,j in all_moves:
                board[i][j] = 'X'
                score, _ = self.min_max_move(board, 'X') # best move for X instead
                board[i][j] = ' '
                if score < best_score: # we're minimizing, so best move with lower score
                    best_score = score
                    best_move = [i, j]
            return best_score, best_move

    # Uses trained model to get the best position on current board
    def MLturn(self, board, best_nn):
        board = self.board.board
        new_board = [[]] # need the correct shape for model

        # Converting board into 1, -1 and 0 format
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == "X":
                    new_board[0].append(1)
                elif board[i][j] == "O":
                    new_board[0].append(-1)
                else:
                    new_board[0].append(0)
        new_board = pd.DataFrame(new_board)

        best_pos = int(best_nn.predict(new_board)[0])

        if best_pos < 3:
            return [0, best_pos]
        elif best_pos < 6:
            return [1, best_pos - 3]
        else:
            return [2, best_pos - 6]

    # runs manual game
    def playGame(self):
        print("New Game: X goes first.")
        print()
        self.board.printBoard()
        play = True

        while play == True:
            # Validating entry
            entry = False
            while entry == False:
                entry = self.validateEntry()
            print("Thank you for your selection.")

            if self.checkEnd() == True:
                 user = input("Another game? Enter Y or y for yes.\n").lower()
                 play = False
                 return user

            self.switchPlayer()
    
    # plays computer game using minmax algorithm
    def playCompGame(self):
        print("New Game: X goes first.")
        print()
        self.board.printBoard()
        play = True

        while play == True:
            if self.turn == 'X':
                _, move = self.min_max_move(self.board, self.turn)
                self.board.board[move[0]][move[1]] = self.turn
            else:
                 # Validating entry
                entry = False
                while entry == False:
                    entry = self.validateEntry()
                print("Thank you for your selection.")

            if self.checkEnd() == True:
                 user = input("Another game? Enter Y or y for yes.\n").lower()
                 play = False
                 return user

            self.switchPlayer()

    # plays computer game using machine learning    
    def playMLGame(self):
        # Building and training model to be used in other functions, so we do not have to repeatedly build a new model each time
        warnings.filterwarnings('ignore')
        tictac_data = pd.read_csv('tictac_single.txt', sep = r'\s+', header = None) # No header, separated by white space instead

        # Splitting into test and train sets (model takes too long to train on all data)
        y = tictac_data[[9]]
        X = tictac_data.drop(columns = 9)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)
        
        nn_model = MLPClassifier()

        # Finding best params for NN
        param_grid = {'hidden_layer_sizes': [100, 150],
                  'activation': ['identity', 'logistic', 'relu'],
                  'solver': ['lbfgs', 'sgd', 'adam']}

        nn_model = GridSearchCV(nn_model, param_grid)
        nn_model.fit(X_train, y_train)

        best_nn = nn_model.best_estimator_

        print("New Game: X goes first.")
        print()
        self.board.printBoard()
        play = True

        while play == True:
            if self.turn == 'X':
                # Validating entry
                entry = False
                while entry == False:
                    entry = self.validateEntry()
                print("Thank you for your selection.")
            else:
                move = self.MLturn(self.board.board, best_nn)
                self.board.board[move[0]][move[1]] = self.turn

            if self.checkEnd() == True:
                 user = input("Another game? Enter Y or y for yes.\n").lower()
                 play = False
                 return user

            self.switchPlayer()
    

def main():
    play = 'y'

    while play.lower() == 'y':
        game_type = input("Manual game or computer game? (M or C)").lower()
        if game_type == 'm':
            game = Game()
            play = game.playGame()
        elif game_type == 'c':
            comp_alg = int(input("Minmax or machine learning? (0 or 1)"))
            if comp_alg == 0:
                game = Game()
                play = game.playCompGame()
            elif comp_alg == 1:
                game = Game()
                play = game.playMLGame()
        else:
            print("Invalid entry. Please put M or C")
    
    print("Thank you for playing!")
   

    


if __name__ == '__main__':
    main()

