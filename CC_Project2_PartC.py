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
