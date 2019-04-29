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
        print(f"Place at: {bestMove}")
        print(f"Evaluation: {vals}")
        print("-----")
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
        print(move[0], move[1])

        # check if bottom middle cell is empty
        # if move[0] == 5 and move[1] == 3:
        #     print("Value is ", board.get_cell_value(5, 3))
        #     return 7
        # else:


        return self.checkLeftRows(board)

        # return random.uniform(0, 1)

    # check if there can be possible win in rows for this valid move
    def checkLeftRows(self, board):

        # if 0 <= move[1] <= 3:
        #     if move[1] + board.num_to_connect - 1 <= board.DEFAULT_WIDTH - 1:
        #         for i in range(1, board.num_to_connect):
        #             if board.get_cell_value(move[0], move[1] + i) == self.id or board.get_cell_value(move[0], move[1] + i) == 0:
        #                 same_count += 1
        #         if same_count == board.num_to_connect:
        #             value += 1
        #
        #     if move[1] + board.num_to_connect - 2 <= board.DEFAULT_WIDTH - 1:
        #         same_count = 1
        #         if move[1] - 1 >= 0 and (board.get_cell_value(move[0], move[1] - 1) == self.id or board.get_cell_value(move[0], move[1] - 1) == 0):
        #             print("Cell ", move[0], move[1] - 1)
        #             same_count += 1
        #             for i in range(1, board.num_to_connect - 1):
        #                 if board.get_cell_value(move[0], move[1] + i) == self.id or board.get_cell_value(move[0], move[1] + i) == 0:
        #                     same_count += 1
        #             if same_count == board.num_to_connect:
        #                 value += 1

        #                i == 1,  2,  3

        value = 0
        move = board.last_move
        pre_cell_value = []
        stuck = False

        # when it is potentially to be placed on left part of the board
        if 0 <= move[1] <= 3:
            # move[1] = 0
            same_count = 1
            for k in range(1, board.num_to_connect):
                if board.get_cell_value(move[0], move[1] + k) == self.id or board.get_cell_value(move[0],move[1] + k) == 0:
                    same_count += 1
                if same_count == board.num_to_connect:
                    value += 1
                    print("common value: ", value)
            for i in range(1, move[1] + 1):
                print("start pre: ", pre_cell_value)
                for pre_value in pre_cell_value:
                    if pre_value == -1:
                        stuck = True
                print("startasdfe: ", pre_cell_value)
                if stuck is True:
                    same_count = 1
                    for k in range(1, board.num_to_connect):
                        if board.get_cell_value(move[0], move[1] + k) == self.id or board.get_cell_value(move[0], move[1] + k) == 0:
                            same_count += 1
                        if same_count == board.num_to_connect:
                            print("if stuck in pre cell")
                            value += 1
                if stuck is False and move[1] - i >= 0 and (board.get_cell_value(move[0], move[1] - i) == self.id or board.get_cell_value(move[0], move[1] - i) == 0):
                    print("starghfghftasdfe: ", pre_cell_value)
                    same_count = 1
                    pre_cell_value.append(self.id)
                    print("startasdfffgfgfgfge: ", pre_cell_value)
                    same_count += i
                    rest = board.num_to_connect - i
                    print(rest)
                    for j in range(1, rest):
                        # move[1] + j won't be out of bounds because 0 <= move[1] <= 3
                        if move[1] + j >= board.DEFAULT_WIDTH or (board.get_cell_value(move[0], move[1] + j) != self.id and board.get_cell_value(move[0], move[1] + j) != 0):
                            print("break")
                            break
                        else:
                            same_count += 1
                    if same_count == board.num_to_connect:
                        value += 1
                        print("count: ", same_count, " value: ", value)
                        print("if not stuck and can have 4 in row", " get i: ", i)
                        print("pre: ", pre_cell_value)
                else:
                    print("sds")
                    pre_cell_value.append(-1)
                    print("count: ", same_count, " value: ", value)
                    print("stuck is false and move[0], move[1] - i is self.id2", " get i: ", i)
                    continue

        return value

