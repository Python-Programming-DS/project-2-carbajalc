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
