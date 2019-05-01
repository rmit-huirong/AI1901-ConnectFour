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

        enemy = self.id % 2 + 1

        return self.checkRows(board, enemy) + self.checkCols(board, enemy) + self.checkBackwardDiagonals(board, enemy) + self.checkForwardDiagonals(board, enemy)

    # check rows
    def checkRows(self, board, enemy):

        myValue = 0
        enemyValue = 0

        # 0 <= x < 6
        for x in range(0, board.DEFAULT_HEIGHT):

            # 0 <= y < 4
            for y in range(0, board.DEFAULT_WIDTH - board.num_to_connect + 1):
                temp = []
                for col in range(0, board.num_to_connect):
                    temp.append(board.get_cell_value(x, y + col))
                print(x, y)
                has_oppo = False
                enemy_has_oppo = False
                for curr in temp:
                    if curr == enemy:
                        has_oppo = True
                    if curr == self.id:
                        enemy_has_oppo = True
                if has_oppo is False and temp.__contains__(self.id):
                    print("WTF")
                    if temp.count(self.id) == 4:
                        print("Count 4, win row")
                        return 1000000
                    elif temp.count(self.id) == 3:
                        if y + board.num_to_connect < board.DEFAULT_WIDTH:
                            print("x: ", x)
                            print("x,y: ", board.last_move[0], board.last_move[1])
                            print("y: ", y)
                            print("temp.index: ", temp.index(self.id))
                            if x == board.last_move[0] and y + temp.index(self.id) + 1 == board.last_move[1] and board.get_cell_value(x, y) == 0 and board.get_cell_value(x, y + board.num_to_connect) == 0:
                                myValue += 10000
                    else:
                        myValue += temp.count(self.id)
                if enemy_has_oppo is True:
                    if temp.count(enemy) == 3:
                        if board.last_move[0] == x and board.last_move[1] == y + temp.index(self.id):
                            print("NO")
                            myValue += 100000
                    elif temp.count(enemy) == 2:
                        if x == board.last_move[0] and y == board.last_move[1] and temp[temp.index(enemy) + 1] == enemy and temp.index(enemy) in range(1, board.num_to_connect - 2):
                            print("Yeah")
                            myValue += 10000
                        if y + board.num_to_connect < board.DEFAULT_WIDTH:
                            if x == board.last_move[0] and y + temp.index(self.id) == board.last_move[1] and board.get_cell_value(x, y) == 0 and board.get_cell_value(x, y + board.num_to_connect) == 0:
                                myValue += 10000
                if enemy_has_oppo is False and temp.__contains__(enemy):
                    print("enemy")
                    if temp.count(enemy) == 3:

                        next_board = board.next_state(enemy, y + temp.index(0))
                        if next_board != 0:
                            if x == board.last_move[0] - 1:
                                print("count 3, must lose row")
                                enemyValue += 10000
                        else:
                            print("count 3, may lose row")
                            enemyValue += 10
                    else:
                        print("hgdhd")
                        myValue += temp.count(enemy)
        return myValue - enemyValue

    # check columns
    def checkCols(self, board, enemy):

        myValue = 0
        enemyValue = 0

        # 0 <= y < 7
        for y in range(0, board.DEFAULT_WIDTH):

            # 0 <= x < 3
            for x in range(0, board.DEFAULT_HEIGHT - board.num_to_connect + 1):
                temp = []
                for row in range(0, board.num_to_connect):
                    temp.append(board.get_cell_value(x + row, y))
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
                        # print("Count 4, win col")
                        return 1000000
                    else:
                        myValue += temp.count(self.id)
                if enemy_has_oppo is True:
                    if temp.count(enemy) == 3:
                        if board.last_move[0] == x + temp.index(self.id) and board.last_move[1] == y + temp.index(self.id):
                            myValue += 100000
                    elif temp.count(enemy) == 2:
                        if x == board.last_move[0] and y == board.last_move[1] and temp[temp.index(enemy) + 1] == enemy and temp.index(enemy) in range(1, board.num_to_connect - 2):
                            # print("Yeah")
                            myValue += 10000
                if enemy_has_oppo is False and temp.__contains__(enemy):
                    # print("enemy")
                    if temp.count(enemy) == 3:
                        next_board = board.next_state(enemy, y + temp.index(0))
                        if next_board != 0:
                            # print("count 3, must lose col")
                            enemyValue += 10000
                        else:
                            # print("count 3, may lose col")
                            enemyValue += 10
                    else:
                        # print("hghd")
                        myValue += temp.count(enemy)
        return myValue - enemyValue

    # check backward diagonal /
    def checkBackwardDiagonals(self, board, enemy):

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
    def checkForwardDiagonals(self, board, enemy):

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
