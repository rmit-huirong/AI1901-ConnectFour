from connectfour.agents.agent import Agent

"""
Student Name:
    Huirong Huang

Student ID:
    s3615907
    
"""


class StudentAgent(Agent):

    def __init__(self, name):
        super().__init__(name)
        self.MaxDepth = 1

    def get_move(self, board):
        """
        Args:
            board: An instance of `Board` that is the current state of the board.

        Returns:
            A tuple of two integers, (row, col)
        """

        valid_moves = board.valid_moves()
        vals = []
        moves = []

        for move in valid_moves:
            next_state = board.next_state(self.id, move[1])
            moves.append(move)
            vals.append(self.dfMiniMax(next_state, 1))

        bestMove = moves[vals.index(max(vals))]
        print("id: ", self.id)
        print(f"The Agent is going to place the token at: {bestMove}")
        print(f"Evaluation of utility values: {vals}")
        print("------------------------------------------------------------------------------------------------")
        return bestMove

    def dfMiniMax(self, board, depth):
        # Goal return column with maximized scores of all possible next states

        if depth == self.MaxDepth:
            return self.evaluateBoardState(board)

        valid_moves = board.valid_moves()
        vals = []
        moves = []

        for move in valid_moves:
            if depth % 2 == 1:
                next_state = board.next_state(self.id % 2 + 1, move[1])
            else:
                next_state = board.next_state(self.id, move[1])

            moves.append(move)
            vals.append(self.dfMiniMax(next_state, depth + 1))

        if depth % 2 == 1:
            print(vals)
            if len(vals) != 0:
                bestVal = min(vals)
            else:
                bestVal = 0
        else:
            print(vals)
            if len(vals) != 0:
                bestVal = max(vals)
            else:
                bestVal = 0

        print(bestVal)
        return bestVal

    def evaluateBoardState(self, board):
        """
        Your evaluation function should look at the current state and return a score for it. 
        As an example, the random agent provided works as follows:
            If the opponent has won this game, return -1.
            If we have won the game, return 1.
            If neither of the players has won, return a random number.
        """

        """
        These are the variables and functions for board objects which may be helpful when creating your Agent.
        Look into board.py for more information/descriptions of each, or to look for any other definitions which may help you.

        Board Variables:
            board.width 
            board.height
            board.last_move
            board.num_to_connect
            board.winning_zones
            board.score_array 
            board.current_player_score

        Board Functions:
            get_cell_value(row, col)
            try_move(col)
            valid_move(row, col)
            valid_moves()
            terminal(self)
            legal_moves()
            next_state(turn)
            winner()
        """

        # # print the valid moves on board for current player
        move = board.last_move
        # print("current: ", move[0], move[1])

        # enemy agent's id
        enemy = self.id % 2 + 1

        value = self.evaluateRows(board, enemy) + self.evaluateCols(board, enemy) + self.evaluateBackwardDiagonals(board, enemy) + self.evaluateForwardDiagonals(board, enemy)
        # print(value)
        return value
    # evaluation of rows (-)
    def evaluateRows(self, board, enemy):

        myValue = 0
        enemyValue = 0

        # 0 <= x < 6
        for x in range(0, board.DEFAULT_HEIGHT):

            # 0 <= y < 4
            for y in range(0, board.DEFAULT_WIDTH - board.num_to_connect + 1):
                # print(x, y)
                # create a list for storing temporary tokens for row
                temp = []
                for col in range(0, board.num_to_connect):
                    temp.append(board.get_cell_value(x, y + col))

                # boolean value to check if there is any opponent token in the list
                has_oppo = False

                # boolean value to check if there is any enemy's opponent token in the list
                enemy_has_oppo = False

                for curr in temp:
                    if curr == enemy:
                        has_oppo = True
                    if curr == self.id:
                        enemy_has_oppo = True

                # if there isn't opponent token and at least one my side token
                if has_oppo is False and temp.__contains__(self.id):
                    # print("a1")
                    # condition: [1,X,1,1] place "1" in X cell, must win in this move
                    #     win -> [1,1,1,1]
                    if temp.count(self.id) == 4:
                        # print("win: [1,X,1,1]")
                        return 1000000

                    # if there are only three my side tokens
                    elif temp.count(self.id) == 3:
                        if y + board.num_to_connect < board.DEFAULT_WIDTH:

                            # condition: [_,1,X,1,_] place "1" in X cell, must win after next move
                            #         -> [_,1,1,1,_]
                            #         -> [_,1,1,1,2] or [2,1,1,1,_]
                            #     win -> [1,1,1,1,2] or [2,1,1,1,1]
                            if x == board.last_move[0] and y + temp.index(self.id) + 1 == board.last_move[1] and board.get_cell_value(x, y) == 0 and board.get_cell_value(x, y + board.num_to_connect) == 0:
                                next_board1 = board.next_state(enemy, y)
                                next_board2 = board.next_state(enemy, y + board.num_to_connect)
                                if next_board1 != 0 and next_board2 != 0:
                                    # print("winnable: [_,1,X,1,_]")
                                    myValue += 10000
                        else:
                            myValue += 1000

                    # if there are only two my side tokens
                    elif temp.count(self.id) == 2:
                        myValue += 100
                    else:
                        myValue += 10

                # if there is at least one enemy's opponent token
                if enemy_has_oppo is True and temp.__contains__(enemy):
                    # print("a2")
                    # print("has ", temp.count(enemy), " enemies")

                    # if there are only three enemy's tokens
                    if temp.count(enemy) == 3:

                        # condition: [2,2,X,2] place "1" in X cell, or will lose after this move
                        #      ok -> [2,2,1,2]
                        #    lose -> [2,2,2,2]
                        # print("1: ", board.last_move[0])
                        # print("2: ", board.last_move[1])
                        # print("3: ", x)
                        # print("4: ", y)
                        # print("5: ", y + temp.index(self.id))
                        # print("6: ", board.get_cell_value(5, 6))
                        # print("7: ", board.get_cell_value(4, 6))
                        # print("8: ", board.get_cell_value(4, 4))
                        if board.last_move[0] == x and board.last_move[1] == y + temp.index(self.id):
                            # print("lose: [2,2,X,2]")
                            # print("row+1")
                            myValue += 100000

                    # if there are only two enemy's tokens
                    elif temp.count(enemy) == 2:
                        if x == board.last_move[0] and y == board.last_move[1] and temp[temp.index(enemy) + 1] == enemy and temp.index(enemy) in range(1, board.num_to_connect - 2):

                            # condition: [_,X,2,2,_] place "1" in X cell, or will lose after next move
                            #      ok -> [2,1,2,2,_] or [_,1,2,2,2]
                            #            -----------
                            #         -> [_,2,2,2,_]
                            #    lose -> [2,2,2,2,_] or [_,2,2,2,2]
                            if y - 1 >= 0:
                                if board.get_cell_value(x, y - 1) == 0:
                                    next_board1 = board.next_state(enemy, y - 1)
                                    next_board2 = board.next_state(enemy, y + board.num_to_connect - 1)
                                    if next_board1 != 0 and next_board2 != 0:
                                        # print("losable: [_,X,2,2,_]")
                                        myValue += 10000
                        if x == board.last_move[0] and y == board.last_move[1] - board.num_to_connect + 1 and temp[temp.index(enemy) + 1] == enemy and temp.index(enemy) in range(1, board.num_to_connect - 2):

                            # condition: [_,2,2,X,_] place "1" in X cell, or will lose after next move
                            #      ok -> [2,2,2,1,_] or [_,2,2,1,2]
                            #            -----------
                            #         -> [_,2,2,2,_]
                            #    lose -> [2,2,2,2,_] or [_,2,2,2,2]
                            if y + board.num_to_connect < board.DEFAULT_WIDTH:
                                if board.get_cell_value(x, y + board.num_to_connect) == 0:
                                    next_board1 = board.next_state(enemy, y)
                                    next_board2 = board.next_state(enemy, y + board.num_to_connect)
                                    if next_board1 != 0 and next_board2 != 0:
                                        # print("losable: [_,2,2,X,_]")
                                        myValue += 10000
                        if y + board.num_to_connect < board.DEFAULT_WIDTH:

                            # condition: [_,2,X,2,_] place "1" in X cell, or will lose after next move
                            #      ok -> [2,2,1,2,_] or [_,2,1,2,2]
                            #            -----------
                            #         -> [_,2,2,2,_]
                            #    lose -> [2,2,2,2,_] or [_,2,2,2,2]
                            if x == board.last_move[0] and y + temp.index(self.id) == board.last_move[1] and board.get_cell_value(x, y) == 0 and board.get_cell_value(x, y + board.num_to_connect) == 0:
                                next_board1 = board.next_state(enemy, y)
                                next_board2 = board.next_state(enemy, y + board.num_to_connect)
                                if next_board1 != 0 and next_board2 != 0:
                                    # print("losable: [_,2,X,2,_]")
                                    myValue += 10000

                # if there is not any enemy's opponent token and at least one enemy's token
                if enemy_has_oppo is False and temp.__contains__(enemy):
                    # print("a3")
                    # print(x, y)
                    # if there are only three enemy's tokens
                    if temp.count(enemy) == 3:
                        # print("b1")
                        next_board = board.next_state(enemy, y + temp.index(0))
                        if next_board != 0:

                            # condition: [2,2,_,2] place "1" in X cell, must lose after this move
                            #            [1,2,X,1]
                            #            ---------
                            #         -> [2,2,_,2]
                            #            [1,2,1,1]
                            #            ---------
                            #    lose -> [2,2,2,2]
                            #            [1,2,1,1]
                            if x == board.last_move[0] - 1:
                                # print("lose: [2,2,_,2]")
                                # print("      [1,2,X,1]")
                                # print("row1")
                                enemyValue += 100000

                            # conditions: general -- [2,_,2,2] they include above?
                            else:
                                # print("lose: [2,_,2,2]")
                                # print("row2")
                                enemyValue += 100000

                        # condition: [2,2,_,2] place "1" in X cell, may lose in the end
                        #            [1,2,_,1]
                        #            [1,1,X,2]
                        #            ---------
                        #      ok -> [2,2,_,2]
                        #            [1,2,_,1]
                        #            [1,1,1,2]
                        else:
                            # print("losable: [2,2,_,2]")
                            # print("         [1,2,_,1]")
                            # print("         [1,1,X,2]")
                            # print("c3")
                            enemyValue += 100

                    # if there is only two enemy's tokens
                    elif temp.count(enemy) == 2:
                        # print("other conditions")
                        enemyValue += 100
                    else:
                        enemyValue += 10
        return myValue - enemyValue

    # evaluation of columns (|)
    def evaluateCols(self, board, enemy):

        myValue = 0
        enemyValue = 0

        # 0 <= y < 7
        for y in range(0, board.DEFAULT_WIDTH):

            # 0 <= x < 3
            for x in range(0, board.DEFAULT_HEIGHT - board.num_to_connect + 1):

                # create a list for storing temporary tokens for col
                temp = []
                for row in range(0, board.num_to_connect):
                    temp.append(board.get_cell_value(x + row, y))

                # boolean value to check if there is any opponent token in the list
                has_oppo = False

                # boolean value to check if there is any enemy's opponent token in the list
                enemy_has_oppo = False

                for curr in temp:
                    if curr == enemy:
                        has_oppo = True
                    if curr == self.id:
                        enemy_has_oppo = True

                # if there isn't opponent token and at least one my side token
                if has_oppo is False and temp.__contains__(self.id):

                    # condition: [X] place "1" in X cell, must win in this move
                    #            [1]
                    #            [1]
                    #            [1]
                    #            ---
                    #     win -> [1]
                    #            [1]
                    #            [1]
                    #            [1]
                    if temp.count(self.id) == 4:
                        # print("win: [X]")
                        # print("     [1]")
                        # print("     [1]")
                        # print("     [1]")
                        return 1000000

                    # if there are only three my side tokens
                    elif temp.count(self.id) == 3:

                        # condition: [_] place "1" in X cell, may win in the end
                        #            [X]
                        #            [1]
                        #            [1]
                        #            ---
                        #      ok -> [_]
                        #            [1]
                        #            [1]
                        #            [1]
                        if x - 1 == board.last_move[0] and y == board.last_move[1] and board.get_cell_value(x - 1, y) == 0:
                            myValue += 1000

                    # if there are only two my side tokens
                    elif temp.count(self.id) == 2:
                        myValue += 100
                    else:
                        myValue += 10

                # if there is at least one enemy's opponent token
                if enemy_has_oppo is True and temp.__contains__(enemy):

                    # if there are only three enemy's tokens
                    if temp.count(enemy) == 3:

                        # condition: [X] place "1" in X cell, or will lose after this move
                        #            [2]
                        #            [2]
                        #            [2]
                        #            ---
                        #    lose -> [2]
                        #            [2]
                        #            [2]
                        #            [2]
                        if board.last_move[0] == x and board.last_move[1] == y:
                            # print("losable: [X]")
                            # print("         [2]")
                            # print("         [2]")
                            # print("         [2]")
                            myValue += 100000

                # if there is not any enemy's opponent token and at least one enemy's token
                if enemy_has_oppo is False and temp.__contains__(enemy):
                    # print("enemy")

                    # if there are only three enemy's tokens
                    if temp.count(enemy) == 3:
                        next_board = board.next_state(enemy, y)

                        # condition: [_] place "1" in another cell, must lose after this move
                        #            [2]
                        #            [2]
                        #            [2]
                        #            ---
                        #    lose -> [2]
                        #            [2]
                        #            [2]
                        #            [2]
                        if next_board != 0:
                            # print("lose: [_]")
                            # print("      [2]")
                            # print("      [2]")
                            # print("      [2]")
                            # print("col")
                            enemyValue += 100000

                    # if there is only two enemy's tokens
                    elif temp.count(enemy) == 2:
                        # print("other conditions")
                        enemyValue += 100
                    else:
                        enemyValue += 10
        return myValue - enemyValue

    # evaluation of backward diagonals (/)
    def evaluateBackwardDiagonals(self, board, enemy):

        myValue = 0
        enemyValue = 0

        # 3 <= x < 6
        for x in range(board.num_to_connect - 1, board.DEFAULT_HEIGHT):

            # 0 <= y < 4
            for y in range(0, board.DEFAULT_WIDTH - board.num_to_connect + 1):

                # create a list for storing temporary tokens for backward diagonal
                temp = []
                for back_diag in range(0, board.num_to_connect):
                    temp.append(board.get_cell_value(x - back_diag, y + back_diag))

                # boolean value to check if there is any opponent token in the list
                has_oppo = False

                # boolean value to check if there is any enemy's opponent token in the list
                enemy_has_oppo = False

                for curr in temp:
                    if curr == enemy:
                        has_oppo = True
                    if curr == self.id:
                        enemy_has_oppo = True

                # if there isn't opponent token and at least one my side token
                if has_oppo is False and temp.__contains__(self.id):

                    # condition: [_,_,_,X] place "1" in X cell, must win in this move
                    #            [_,_,1,2]
                    #            [_,1,2,1]
                    #            [1,1,2,1]
                    if temp.count(self.id) == 4:
                        # print("win: [_,_,_,X]")
                        # print("win: [_,_,1,2]")
                        # print("win: [_,1,2,1]")
                        # print("win: [1,1,2,1]")
                        return 1000000

                    # if there are only three my side tokens
                    elif temp.count(self.id) == 3:
                        if x - board.num_to_connect >= 0 and y + board.num_to_connect < board.DEFAULT_WIDTH:

                            # condition: [_,_,_,_,_] place "1" in X cell, must win after next move
                            #            [_,_,_,1,1]
                            #            [_,_,X,1,2]
                            #            [_,1,2,2,1]
                            #            [_,2,1,1,2]
                            if x - temp.index(self.id) - 1 == board.last_move[0] and y + temp.index(self.id) + 1 == board.last_move[1] and board.get_cell_value(x, y) == 0 and board.get_cell_value(x - board.num_to_connect, y + board.num_to_connect) == 0:
                                next_board1 = board.next_state(enemy, y)
                                next_board2 = board.next_state(enemy, y + board.num_to_connect)
                                if next_board1 != 0 and next_board2 != 0:
                                    # print("winnable: [_,_,_,_,_]")
                                    # print("          [_,_,_,1,1]")
                                    # print("          [_,_,X,1,2]")
                                    # print("          [_,1,2,2,1]")
                                    # print("          [_,2,1,1,2]")
                                    myValue += 10000
                        else:
                            myValue += 5000

                    # if there are only two my side tokens
                    elif temp.count(self.id) == 2:
                        myValue += 500
                    else:
                        myValue += 50

                # if there is at least one enemy's opponent token
                if enemy_has_oppo is True and temp.__contains__(enemy):

                    # if there are only three enemy's tokens
                    if temp.count(enemy) == 3:

                        # condition: [_,_,_,2] place "1" in X cell, or will lose after this move
                        #            [_,_,X,1]
                        #            [_,2,1,1]
                        #            [2,1,2,2]
                        if board.last_move[0] == x - temp.index(self.id) and board.last_move[1] == y + temp.index(self.id):
                            # print("lose: [_,_,_,2]")
                            # print("      [_,_,X,1]")
                            # print("      [_,2,1,1]")
                            # print("      [2,1,2,2]")
                            myValue += 100000

                    # if there are only two enemy's tokens
                    elif temp.count(enemy) == 2:
                        if board.last_move[0] == x and board.last_move[1] == y and temp[temp.index(enemy) + 1] == enemy and temp.index(enemy) in range(1, board.num_to_connect - 2):

                            # condition: [_,_,_,_,_] place "1" in X cell, or will lose after next move
                            #            [_,_,_,2,1]
                            #            [_,_,2,1,2]
                            #            [_,X,1,2,1]
                            #            [_,2,1,1,2]
                            if x + 1 < board.DEFAULT_HEIGHT and y - 1 >= 0:
                                if board.get_cell_value(x + 1, y - 1) == 0:
                                    next_board1 = board.next_state(enemy, y - 1)
                                    next_board2 = board.next_state(enemy, y + board.num_to_connect - 1)
                                    if next_board1 != 0 and next_board2 != 0:
                                        # print("losable: [_,_,_,_,_]")
                                        # print("         [_,_,_,2,1]")
                                        # print("         [_,_,2,1,2]")
                                        # print("         [_,X,1,2,1]")
                                        # print("         [_,2,1,1,2]")
                                        myValue += 10000
                        if board.last_move[0] == x - board.num_to_connect + 1 and board.last_move[1] == y + board.num_to_connect - 1 and temp[temp.index(enemy) + 1] == enemy and temp.index(enemy) in range(1, board.num_to_connect - 2):

                            # condition: [_,_,_,_,_] place "1" in X cell, or will lose after next move
                            #            [_,_,_,X,1]
                            #            [_,_,2,1,2]
                            #            [_,2,1,2,1]
                            #            [_,2,1,1,2]
                            if x - board.num_to_connect >= 0 and y + board.num_to_connect < board.DEFAULT_WIDTH:
                                if board.get_cell_value(x - board.num_to_connect, y + board.num_to_connect) == 0:
                                    next_board1 = board.next_state(enemy, y)
                                    next_board2 = board.next_state(enemy, y + board.num_to_connect)
                                    if next_board1 != 0 and next_board2 != 0:
                                        # print("losable: [_,_,_,_,_]")
                                        # print("         [_,_,_,X,1]")
                                        # print("         [_,_,2,1,2]")
                                        # print("         [_,2,1,2,1]")
                                        # print("         [_,2,1,1,2]")
                                        myValue += 10000
                        if x - board.num_to_connect >= 0 and y + board.num_to_connect < board.DEFAULT_WIDTH:

                            # condition: [_,_,_,_,_] place "1" in X cell, or will lose after next move
                            #            [_,_,_,2,1]
                            #            [_,_,X,1,2]
                            #            [_,2,1,2,1]
                            #            [_,2,1,1,2]
                            if x - temp.index(self.id) == board.last_move[0] and y + temp.index(self.id) == board.last_move[1] and board.get_cell_value(x, y) == 0 and board.get_cell_value(x - board.num_to_connect, y + board.num_to_connect) == 0:
                                next_board1 = board.next_state(enemy, y)
                                next_board2 = board.next_state(enemy, y + board.num_to_connect)
                                if next_board1 != 0 and next_board2 != 0:
                                    # print("losable: [_,_,_,_,_]")
                                    # print("         [_,_,_,2,1]")
                                    # print("         [_,_,X,1,2]")
                                    # print("         [_,2,1,2,1]")
                                    # print("         [_,2,1,1,2]")
                                    myValue += 10000

                # if there is not any enemy's opponent token and at least one enemy's token
                if enemy_has_oppo is False and temp.__contains__(enemy):

                    # if there are only three enemy's tokens
                    if temp.count(enemy) == 3:
                        next_board = board.next_state(enemy, y + temp.index(0))
                        if next_board != 0:

                            # condition: [_,_,_,2] place "1" in X cell, must lose after this move
                            #            [_,_,_,1]
                            #            [_,2,X,2]
                            #            [2,2,1,1]
                            if x - temp.index(0) == board.last_move[0] - 1:
                                # print("lose: [_,_,_,2]")
                                # print("      [_,_,_,1]")
                                # print("      [_,2,X,2]")
                                # print("      [2,2,1,1]")
                                # print("bdiag1")
                                enemyValue += 100000

                            # conditions: general -- [_,_,_,2] they include above?
                            #                        [_,_,_,1]
                            #                        [_,2,1,2]
                            #                        [2,2,2,1]
                            else:
                                # print("lose: [_,_,_,2]")
                                # print("      [_,_,_,1]")
                                # print("      [_,2,1,2]")
                                # print("      [2,2,2,1]")
                                # print("bdiag2")
                                enemyValue += 100000

                        # condition: [_,_,_,2] place "1" in X cell, may lose in the end
                        #            [_,_,_,1]
                        #            [_,2,_,2]
                        #            [2,2,X,1]
                        else:
                            # print("losable: [_,_,_,2]")
                            # print("         [_,_,_,1]")
                            # print("         [_,2,_,2]")
                            # print("         [2,2,X,1]")
                            enemyValue += 500

                    # if there is only two enemy's tokens
                    elif temp.count(enemy) == 2:
                        # print("other conditions")
                        enemyValue += 500
                    else:
                        enemyValue += 50
        return myValue - enemyValue

    # evaluation of forward diagonals (\)
    def evaluateForwardDiagonals(self, board, enemy):

        myValue = 0
        enemyValue = 0

        # 0 <= x < 3
        for x in range(0, board.DEFAULT_HEIGHT - board.num_to_connect + 1):

            # 0 <= y < 4
            for y in range(0, board.DEFAULT_WIDTH - board.num_to_connect + 1):
                # create a list for storing temporary tokens for forward diagonal
                temp = []
                for for_diag in range(0, board.num_to_connect):
                    temp.append(board.get_cell_value(x + for_diag, y + for_diag))

                # boolean value to check if there is any opponent token in the list
                has_oppo = False

                # boolean value to check if there is any enemy's opponent token in the list
                enemy_has_oppo = False

                for curr in temp:
                    if curr == enemy:
                        has_oppo = True
                    if curr == self.id:
                        enemy_has_oppo = True

                # if there isn't opponent token and at least one my side token
                if has_oppo is False and temp.__contains__(self.id):

                    # condition: [X,_,_,_] place "1" in X cell, must win in this move
                    #            [2,1,_,_]
                    #            [1,2,1,_]
                    #            [1,2,1,1]
                    if temp.count(self.id) == 4:
                        # print("win: [X,_,_,_]")
                        # print("win: [2,1,_,_]")
                        # print("win: [1,2,1,_]")
                        # print("win: [1,2,1,1]")
                        return 1000000

                    # if there are only three my side tokens
                    elif temp.count(self.id) == 3:
                        if x + board.num_to_connect < board.DEFAULT_HEIGHT and y + board.num_to_connect < board.DEFAULT_WIDTH:

                            # condition: [_,_,_,_,_] place "1" in X cell, must win after next move
                            #            [1,1,_,_,_]
                            #            [2,1,X,_,_]
                            #            [1,2,2,1,_]
                            #            [2,1,1,2,_]
                            if x + temp.index(self.id) + 1 == board.last_move[0] and y + temp.index(self.id) + 1 == board.last_move[1] and board.get_cell_value(x, y) == 0 and board.get_cell_value(x + board.num_to_connect, y + board.num_to_connect) == 0:
                                next_board1 = board.next_state(enemy, y)
                                next_board2 = board.next_state(enemy, y + board.num_to_connect)
                                if next_board1 != 0 and next_board2 != 0:
                                    # print("winnable: [_,_,_,_,_]")
                                    # print("          [1,1,_,_,_]")
                                    # print("          [2,1,X,_,_]")
                                    # print("          [1,2,2,1,_]")
                                    # print("          [2,1,1,2,_]")
                                    myValue += 10000
                        else:
                            myValue += 5000

                    # if there are only two my side tokens
                    elif temp.count(self.id) == 2:
                        myValue += 500
                    else:
                        myValue += 50

                # if there is at least one enemy's opponent token
                if enemy_has_oppo is True and temp.__contains__(enemy):

                    # if there are only three enemy's tokens
                    if temp.count(enemy) == 3:

                        # condition: [2,_,_,_] place "1" in X cell, or will lose after this move
                        #            [1,X,_,_]
                        #            [1,1,2,_]
                        #            [2,2,1,2]
                        if board.last_move[0] == x + temp.index(self.id) and board.last_move[1] == y + temp.index(self.id):
                            # print("lose: [2,_,_,_]")
                            # print("      [1,X,_,_]")
                            # print("      [1,1,2,_]")
                            # print("      [2,2,1,2]")
                            myValue += 100000

                    # if there are only two enemy's tokens
                    elif temp.count(enemy) == 2:
                        if board.last_move[0] == x and board.last_move[1] == y and temp[temp.index(enemy) + 1] == enemy and temp.index(enemy) in range(1, board.num_to_connect - 2):

                            # condition: [_,_,_,_,_] place "1" in X cell, or will lose after next move
                            #            [1,2,_,_,_]
                            #            [2,1,2,_,_]
                            #            [1,2,1,X,_]
                            #            [2,1,1,2,_]
                            if x + board.num_to_connect < board.DEFAULT_HEIGHT and y + board.num_to_connect < board.DEFAULT_WIDTH:
                                if board.get_cell_value(x + board.num_to_connect, y + board.num_to_connect):
                                    next_board1 = board.next_state(enemy, y)
                                    next_board2 = board.next_state(enemy, y + board.num_to_connect)
                                    if next_board1 != 0 and next_board2 != 0:
                                        # print("losable: [_,_,_,_,_]")
                                        # print("         [1,2,_,_,_]")
                                        # print("         [2,1,2,_,_]")
                                        # print("         [1,2,1,X,_]")
                                        # print("         [2,1,1,2,_]")
                                        myValue += 10000
                        if board.last_move[0] == x and board.last_move[1] == y and temp[temp.index(enemy) + 1] == enemy and temp.index(enemy) in range(1, board.num_to_connect - 2):

                            # condition: [_,_,_,_,_] place "1" in X cell, or will lose after next move
                            #            [1,X,_,_,_]
                            #            [2,1,2,_,_]
                            #            [1,2,1,2,_]
                            #            [2,1,1,2,_]
                            if x - 1 >= 0 and y - 1 >= 0:
                                if board.get_cell_value(x - 1, y - 1) == 0:
                                    next_board1 = board.next_state(enemy, y - 1)
                                    next_board2 = board.next_state(enemy, y + board.num_to_connect - 1)
                                    if next_board1 != 0 and next_board2 != 0:
                                        # print("losable: [_,_,_,_,_]")
                                        # print("         [1,X,_,_,_]")
                                        # print("         [2,1,2,_,_]")
                                        # print("         [1,2,1,2,_]")
                                        # print("         [2,1,1,2,_]")
                                        myValue += 10000
                        if x + board.num_to_connect < board.DEFAULT_HEIGHT and y + board.num_to_connect < board.DEFAULT_WIDTH:

                            # condition: [_,_,_,_,_] place "1" in X cell, or will lose after next move
                            #            [1,2,_,_,_]
                            #            [2,1,X,_,_]
                            #            [1,2,1,2,_]
                            #            [2,1,1,2,_]
                            if x + temp.index(self.id) == board.last_move[0] and y + temp.index(self.id) == board.last_move[1] and board.get_cell_value(x, y) == 0 and board.get_cell_value(x + board.num_to_connect, y + board.num_to_connect) == 0:
                                next_board1 = board.next_state(enemy, y)
                                next_board2 = board.next_state(enemy, y + board.num_to_connect)
                                if next_board1 != 0 and next_board2 != 0:
                                    # print("losable: [_,_,_,_,_]")
                                    # print("         [1,2,_,_,_]")
                                    # print("         [2,1,X,_,_]")
                                    # print("         [1,2,1,2,_]")
                                    # print("         [2,1,1,2,_]")
                                    myValue += 10000

                # if there is not any enemy's opponent token and at least one enemy's token
                if enemy_has_oppo is False and temp.__contains__(enemy):

                    # if there are only three enemy's tokens
                    if temp.count(enemy) == 3:
                        next_board = board.next_state(enemy, y + temp.index(0))
                        if next_board != 0:

                            # condition: [2,_,_,_] place "1" in X cell, must lose after this move
                            #            [1,_,_,_]
                            #            [2,X,2,_]
                            #            [1,1,2,2]
                            if x + temp.index(0) == board.last_move[0] - 1:
                                # print("lose: [2,_,_,_]")
                                # print("      [1,_,_,_]")
                                # print("      [2,X,2,_]")
                                # print("      [1,1,2,2]")
                                # print("fdiag1")
                                enemyValue += 100000

                            # conditions: general -- [2,_,_,_] they include above?
                            #                        [1,_,_,_]
                            #                        [2,1,2,_]
                            #                        [1,2,2,2]
                            else:
                                # print("lose: [2,_,_,_]")
                                # print("      [1,_,_,_]")
                                # print("      [2,1,2,_]")
                                # print("      [1,2,2,2]")
                                # print("fdiag2")
                                enemyValue += 100000

                        # condition: [2,_,_,_] place "1" in X cell, may lose in the end
                        #            [1,_,_,_]
                        #            [2,_,2,_]
                        #            [1,X,2,2]
                        else:
                            # print("losable: [2,_,_,_]")
                            # print("         [1,_,_,_]")
                            # print("         [2,_,2,_]")
                            # print("         [1,X,2,2]")
                            enemyValue += 500

                    # if there is only two enemy's tokens
                    elif temp.count(enemy) == 2:
                        # print("other conditions")
                        enemyValue += 500
                    else:
                        enemyValue += 50
        return myValue - enemyValue
