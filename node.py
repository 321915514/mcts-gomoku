import random
from collections import defaultdict

import numpy as np


class Node():
    def __init__(self, board=None, parent=None, pre_pos=None):
        self.pre_pos = pre_pos # 最后一次落子位置
        self.board = board  # 棋盘
        self.parent = parent  # 父节点
        self.children = list()
        self.not_visit_pos = None  # 未访问节点
        self.num_of_visit = 0  # 该节点访问次数
        self.num_of_wins = defaultdict(int)  # 该节点胜利次数

    def fully_expended(self):
        """
        判断节点是否完全展开
        :return: TRUE FALSE
        """
        if self.not_visit_pos is None:
            self.not_visit_pos = self.board.get_legal_pos()
        return True if len(self.not_visit_pos) == 0 and len(self.children) != 0 else False

    def non_terminal(self):
        """
        是否为终端节点，即该节点对应的格局是否已分出胜负
        :return:
        """
        game_result = self.board.game_over(self.pre_pos)
        return game_result

    def pick_unvisited(self):
        """
        选择一个未访问的节点并加入当前节点的孩子中
        :return:
        """
        random_index = random.randint(0, len(self.not_visit_pos) - 1)
        move_pos = self.not_visit_pos.pop(random_index)
        new_board = self.board.move(move_pos)
        new_node = Node(new_board, self, move_pos)
        self.children.append(new_node)
        return new_node

    def pick_random(self):
        """
        随即选择该节点的一个孩子扩展
        :return:
        """
        possible_moves = self.board.get_legal_pos()
        random_index = random.randint(0,len(possible_moves) - 1)
        new_board = self.board.move(possible_moves[random_index])
        new_node = Node(new_board, self, possible_moves[random_index])
        return new_node

    def num_of_win(self):
        """
        判断该节点的胜负情况，利用一个实数即可代表黑白二子的胜负差值
        :return:
        """
        win = self.num_of_wins[-self.board.cur_player]
        lose = self.num_of_wins[self.board.cur_player]

        return win - lose

    def best_uct(self, c_param=1.98):
        uct_of_child = np.array(list(
            [child.num_of_win() / child.num_of_visit + c_param * np.sqrt(self.num_of_visit) / child.num_of_visit for
             child in self.children]))
        best_index = np.argmax(uct_of_child)
        return self.children[best_index]