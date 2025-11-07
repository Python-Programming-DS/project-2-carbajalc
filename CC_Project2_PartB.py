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
