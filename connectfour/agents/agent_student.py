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
            bestVal = min(vals)
        else:
            bestVal = max(vals)

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

        # print the valid moves on board for current player
        move = board.last_move
        print("current: ", move[0], move[1])

        # enemy agent's id
        enemy = self.id % 2 + 1

        return self.evaluateRows(board, enemy) + self.evaluateCols(board, enemy) + self.evaluateBackwardDiagonals(board, enemy) + self.evaluateForwardDiagonals(board, enemy)

    # evaluation of rows
    def evaluateRows(self, board, enemy):

        myValue = 0
        enemyValue = 0

        # 0 <= x < 6
        for x in range(0, board.DEFAULT_HEIGHT):

            # 0 <= y < 4
            for y in range(0, board.DEFAULT_WIDTH - board.num_to_connect + 1):

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

                    # condition: [1,X,1,1] place "1" in X cell, must win in this move
                    #     win -> [1,1,1,1]
                    if temp.count(self.id) == 4:
                        print("win: [1,X,1,1]")
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
                                    print("winnable: [_,1,X,1,_]")
                                    myValue += 10000
                        else:
                            myValue += 100

                    # if there are one or two my side token(s)
                    else:
                        myValue += temp.count(self.id)

                # if there is at least one enemy's opponent token
                if enemy_has_oppo is True:

                    # if there are only three enemy's tokens
                    if temp.count(enemy) == 3:

                        # condition: [2,2,X,2] place "1" in X cell, or will lose after this move
                        #      ok -> [2,2,1,2]
                        #    lose -> [2,2,2,2]
                        if board.last_move[0] == x and board.last_move[1] == y + temp.index(self.id):
                            print("losable: [2,2,X,2]")
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
                                        print("losable: [_,X,2,2,_]")
                                        myValue += 10000
                        if x == board.last_move[0] and y == board.last_move[1] - board.num_to_connect + 1 and temp[temp.index(enemy) + 1] == enemy and temp.index(enemy) in range(1, board.num_to_connect - 2):

                            # condition: [_,2,2,X,_] place "1" in X cell, or will lose after next move
                            #      ok -> [2,2,2,1,_] or [_,2,2,1,2]
                            #            -----------
                            #         -> [_,2,2,2,_]
                            #    lose -> [2,2,2,2,_] or [_,2,2,2,2]
                            if y + board.num_to_connect - 1 < board.DEFAULT_WIDTH:
                                if board.get_cell_value(x, y + board.num_to_connect - 1) == 0:
                                    next_board1 = board.next_state(enemy, y - 1)
                                    next_board2 = board.next_state(enemy, y + board.num_to_connect - 1)
                                    if next_board1 != 0 and next_board2 != 0:
                                        print("losable: [_,2,2,X,_]")
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
                                    print("losable: [_,2,X,2,_]")
                                    myValue += 10000

                # if there is not any enemy's opponent token and at least one enemy's token
                if enemy_has_oppo is False and temp.__contains__(enemy):
                    print("enemy")

                    # if there are only three enemy's tokens
                    if temp.count(enemy) == 3:
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
                                print("lose: [2,2,_,2]")
                                print("      [1,2,X,1]")
                                enemyValue += 100000

                            # conditions: general -- [2,_,2,2] they include above?
                            else:
                                print("lose: [2,_,2,2]")
                                enemyValue += 100000

                        # condition: [2,2,_,2] place "1" in X cell, may lose in the end
                        #            [1,2,_,1]
                        #            [1,1,X,2]
                        #            ---------
                        #      ok -> [2,2,_,2]
                        #            [1,2,_,1]
                        #            [1,1,1,2]
                        else:
                            print("losable: [2,2,_,2]")
                            print("         [1,2,_,1]")
                            print("         [1,1,X,2]")
                            enemyValue += 10

                    # if there is one or two enemy's token(s)
                    else:
                        print("other conditions")
                        enemyValue += temp.count(enemy)
        return myValue - enemyValue

    # evaluation of columns
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
                        print("win: [X]")
                        print("     [1]")
                        print("     [1]")
                        print("     [1]")
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
                            myValue += 100

                    # if there are one or two my side token(s)
                    else:
                        myValue += temp.count(self.id)

                # if there is at least one enemy's opponent token
                if enemy_has_oppo is True:

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
                            print("losable: [X]")
                            print("         [2]")
                            print("         [2]")
                            print("         [2]")
                            myValue += 100000

                # if there is not any enemy's opponent token and at least one enemy's token
                if enemy_has_oppo is False and temp.__contains__(enemy):
                    print("enemy")

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
                            print("lose: [_]")
                            print("      [2]")
                            print("      [2]")
                            print("      [2]")
                            enemyValue += 100000

                    # if there is one or two enemy's token(s)
                    else:
                        print("other conditions")
                        enemyValue += temp.count(enemy)
        return myValue - enemyValue

    # check backward diagonal /
    def evaluateBackwardDiagonals(self, board, enemy):

        myValue = 0
        enemyValue = 0

        # 3 <= x < 6
        for x in range(board.num_to_connect - 1, board.DEFAULT_HEIGHT):

            # 0 <= y < 4
            for y in range(0, board.DEFAULT_WIDTH - board.num_to_connect + 1):
                temp = []
                for back_diag in range(0, board.num_to_connect):
                    temp.append(board.get_cell_value(x - back_diag, y + back_diag))
                # print(temp)
                has_oppo = False
                enemy_has_oppo = False
                for curr in temp:
                    if curr == enemy:
                        has_oppo = True
                    if curr == self.id:
                        enemy_has_oppo = True
                if has_oppo is False and temp.__contains__(self.id):
                    if temp.count(self.id) == 4:
                        # print("Count 4, win b diag")
                        return 1000000
                    else:
                        myValue += temp.count(self.id)
                if enemy_has_oppo is True:
                    if temp.count(enemy) == 3:
                        if board.last_move[0] == x - temp.index(self.id) and board.last_move[1] == y + temp.index(self.id):
                            myValue += 100000
                    elif temp.count(enemy) == 2:
                        if board.last_move[0] == x and board.last_move[1] == y and temp[temp.index(enemy) + 1] == enemy and temp.index(enemy) in range(1, board.num_to_connect - 2):
                            # print("Yeah")
                            myValue += 10000
                        if y + board.num_to_connect < board.DEFAULT_WIDTH:
                            if x - temp.index(self.id) == board.last_move[0] and y + temp.index(self.id) == board.last_move[1] and board.get_cell_value(x, y) == 0 and board.get_cell_value(x, y + board.num_to_connect) == 0:
                                myValue += 10000
                if enemy_has_oppo is False and temp.__contains__(enemy):
                    if temp.count(enemy) == 3:
                        next_board = board.next_state(enemy, y + temp.index(0))
                        if next_board != 0:
                            if x - temp.index(0) == board.last_move[0] - 1:
                                # print("count 3, must lose b diag")
                                enemyValue += 10000
                        else:
                            # print("count 3, may lose b diag")
                            enemyValue += 10
        return myValue - enemyValue

    # check forward diagonal \
    def evaluateForwardDiagonals(self, board, enemy):

        myValue = 0
        enemyValue = 0

        # 0 <= x < 3
        for x in range(0, board.DEFAULT_HEIGHT - board.num_to_connect + 1):

            # 0 <= y < 4
            for y in range(0, board.DEFAULT_WIDTH - board.num_to_connect + 1):
                temp = []
                for for_diag in range(0, board.num_to_connect):
                    temp.append(board.get_cell_value(x + for_diag, y + for_diag))
                # print(temp)
                has_oppo = False
                enemy_has_oppo = False
                for curr in temp:
                    if curr == enemy:
                        has_oppo = True
                    if curr == self.id:
                        enemy_has_oppo = True
                if has_oppo is False and temp.__contains__(self.id):
                    if temp.count(self.id) == 4:
                        # print("Count 4, win f diag")
                        return 1000000
                    else:
                        myValue += temp.count(self.id)
                if enemy_has_oppo is True:
                    if temp.count(enemy) == 3:
                        if board.last_move[0] == x + temp.index(self.id) and board.last_move[1] == y + temp.index(self.id):
                            myValue += 100000
                    elif temp.count(enemy) == 2:
                        if board.last_move[0] == x and board.last_move[1] == y and temp[temp.index(enemy) + 1] == enemy and temp.index(enemy) in range(1, board.num_to_connect - 2):
                            # print("Yeah")
                            myValue += 10000
                        if y + board.num_to_connect < board.DEFAULT_WIDTH:
                            if x + temp.index(self.id) == board.last_move[0] and y + temp.index(self.id) == board.last_move[1] and board.get_cell_value(x, y) == 0 and board.get_cell_value(x, y + board.num_to_connect) == 0:
                                myValue += 10000
                if enemy_has_oppo is False and temp.__contains__(enemy):
                    if temp.count(enemy) == 3:
                        next_board = board.next_state(enemy, y + temp.index(0))
                        if next_board != 0:
                            if x + temp.index(0) == board.last_move[0] - 1:
                                # print("count 3, must lose f diag")
                                enemyValue += 10000
                        else:
                            # print("count 3, may lose f diag")
                            enemyValue += 10
        return myValue - enemyValue
