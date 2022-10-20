import random

import numpy as np
from collections import defaultdict

from mcts import mcts


class Board():
    def __init__(self, board=None, size=8, cur_player=-1):
        self.size = size
        self.board = np.zeros((self.size, self.size), int) if board is None else board
        self.cur_player = cur_player
        # print(self.board)
    def is_move_legal(self, move_pos):
        """
        :param move_pos: 元组得到位置
        :return: true or false
        """
        x, y = -100, -100
        if move_pos is not None:
            x, y = move_pos[0], move_pos[1]
        if x < 0 or x > self.size or y < 0 or y > self.size:  # 判断是否溢出棋盘边界
            return False
        if self.board[x, y] != 0:  # 判断是否下在已经有棋子的位置上
            return False
        return True

    def get_legal_pos(self):
        """
        :return: 返回列表
        """
        pos_list = []
        for i in range(0, self.size):
            for j in range(0, self.size):
                if self.board[i][j] == 0:
                    pos_list.append((i, j))
        return pos_list

    def move(self, move_pos):
        """
        走子
        :param move_pos:
        :return: board
        """
        if not self.is_move_legal(move_pos):  # 不合法
            return '棋子不合法'
        new_board = Board(np.copy(self.board), cur_player=-self.cur_player)
        new_board.board[move_pos[0]][move_pos[1]] = self.cur_player
        return new_board

    def board_result(self, move_pos):
        """
        :param move_pos:
        :return: 判断哪方赢
        """

        x, y = move_pos[0], move_pos[1]
        # print(x,y)
        player = self.board[x,y]
        direction = list([[self.board[i][y] for i in range(self.size)]])  # 纵向是否有五颗连子
        direction.append([self.board[x][j] for j in range(self.size)])  # 横向是否有五颗连子
        direction.append(self.board.diagonal(y - x))  # 该点正对角是否有五颗连子
        direction.append(np.fliplr(self.board).diagonal(self.size - 1 - y - x))  # 该点反对角是否有五颗连子
        for i in direction:
            count = 0
            for v in i:
                if v == player:
                    count += 1
                    if count == 5:
                        return True
                else:
                    count = 0
        return False

    def game_over(self, move_pos):
        """
        判断游戏是否结束，
        :param move_pos:
        :return:
        """
        if self.board_result(move_pos):
            return "win"
        elif len(self.get_legal_pos()) == 0:
            return 'tie'
        else:
            return None

    # def get_action_pos(self, board):
    #     """
    #     读取用户输入的数据
    #     :param board:
    #     :return:
    #     """
    #     try:
    #         location = input("输入坐标x,y:")
    #         if isinstance(location, str) and len(location.split(",")) == 2:
    #             move_pos = tuple([int(i) for i in location.split(',')])
    #         else:
    #             move_pos = -1
    #     except:
    #         move_pos = -1
    #
    #     if move_pos == -1 or move_pos not in board.get_legal_pos():
    #         print('落子位置错误')
    #         move_pos = self.get_action_pos(board)
    #
    #     # print('get_action_pos----{}'.format(move_pos))
    #     return move_pos

    # def action(self, board):
    #     """
    #     获得用户落子后的棋盘格局
    #     :param board:
    #     :return:board,move_pos
    #     """
    #     move_pos = self.get_action_pos(board)
    #     board = board.move(move_pos)
    #     return board, move_pos


class Human():
    def __init__(self, player=-1):
        self.player = player

    def get_action_pos(self, board):
        """
        读取用户输入的数据
        :param board:
        :return:
        """
        try:
            location = input("输入坐标x,y:")
            if isinstance(location, str) and len(location.split(",")) == 2:
                move_pos = tuple([int(i) for i in location.split(',')])
            else:
                move_pos = -1
        except:
            move_pos = -1

        if move_pos == -1 or move_pos not in board.get_legal_pos():
            print('落子位置错误')
            move_pos = self.get_action_pos(board)

        # print('get_action_pos----{}'.format(move_pos))
        return move_pos

    def action(self, board):
        """
        获得用户落子后的棋盘格局
        :param board:
        :return:board,move_pos
        """
        move_pos = self.get_action_pos(board)
        board = board.move(move_pos)
        return board, move_pos

class AI():
    def __init__(self, player=1):
        self.player = player

    def action(self,board,pre_pos):
        move_pos = mcts(board,pre_pos)
        board = board.move(move_pos)
        return board,move_pos


