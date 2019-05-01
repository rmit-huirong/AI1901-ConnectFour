from connectfour.agents.agent import Agent
from connectfour.agents.computer_player import RandomAgent
import random


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
        # print(f"The Agent is going to place the token at: {bestMove}")
        print(f"Evaluation of utility values: {vals}")
        # print("------------------------------------------------------------------------------------------------")
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
        # move = board.last_move
        # print(move[0], move[1])

        players = (1, 2)
        enemy = self.getEnemyAgentID(players)

        return self.checkRows(board, enemy) + self.checkCols(board, enemy) + self.checkBackwardDiagonals(board, enemy) + self.checkForwardDiagonals(board, enemy)

    # check if the current player is StudentAgent itself
    def getEnemyAgentID(self, players):

        if players[0] == self.id:
            return players[1]
        else:
            return players[0]

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
                        print("Count 4, win row")
                        return 10000
                    elif temp.count(self.id) == 3:
                        print("Count 3, row")
                        myValue += 100
                    else:
                        myValue += temp.count(self.id)
                if enemy_has_oppo is False and temp.__contains__(enemy):
                    if temp.count(enemy) == 3:
                        print("count 3, lose row")
                        return -10000
                    else:
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
                        print("Count 4, win col")
                        return 10000
                    elif temp.count(self.id) == 3:
                        print("Count 3, col")
                        myValue += 100
                    else:
                        myValue += temp.count(self.id)
                if enemy_has_oppo is False and temp.__contains__(enemy):
                    if temp.count(enemy) == 3:
                        print("Count 3, lose col")
                        return -10000
                    else:
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
                        print("Count 4, win b diag")
                        return 10000
                    elif temp.count(self.id) == 3:
                        print("Count 3, b diag")
                        myValue += 100
                    else:
                        myValue += temp.count(self.id)
                if enemy_has_oppo is False and temp.__contains__(enemy):
                    if temp.count(enemy) == 3:
                        print("Count 4, lose b diag")
                        return -10000
                    else:
                        myValue += temp.count(enemy)
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
                        print("Count 4, win f diag")
                        return 10000
                    elif temp.count(self.id) == 3:
                        print("Count 3, f diag")
                        myValue += 100
                    else:
                        myValue += temp.count(self.id)
                if enemy_has_oppo is False and temp.__contains__(enemy):
                    if temp.count(enemy) == 3:
                        print("Count 3, lose f diag")
                        return -10000
                    else:
                        myValue += temp.count(enemy)
        return myValue - enemyValue
