import datetime
import time

from board import Board
from board import Human
from board import AI
ALPHABET = 'A B C D E F G H I J K L M N O'
class play():
    def __init__(self):
        self.board = Board()

    def print_board(self):
        # width, height = self.board.size, self.board.size  # 棋盘大小

        print("黑子(-1) 用 X 表示\t白子(1) 用 O 表示")
        #
        # for x in range(width):  # 打印行坐标
        #     print("{0:8}".format(x), end='')
        board_str = '\n   ' + ALPHABET[:self.board.size * 2 - 1] + '\n'
        board = self.board
        for i in range(self.board.size):
            for j in range(self.board.size):
                if j == 0:
                    board_str += '{:2}'.format(i + 1)
                if board.board[i, j] == -1:
                    board_str += ' X'
                elif board.board[i, j] == 1:
                    board_str += ' O'
                else:
                    board_str += ' .'
                if j == self.board.size - 1:
                    board_str += '\n'
        # board_str += '  '
        print(board_str)
        # print('\r\n')
        # for i in range(height):
        #     print("{0:4d}".format(i), end='')
        #     for j in range(width):
        #         if self.board.board[i, j] == -1:
        #             print('X'.center(8), end='')
        #         elif self.board.board[i, j] == 1:
        #             print('O'.center(8), end='')
        #         else:
        #             print('-'.center(8), end='')
        #     print('\r\n\r\n')

    def startplay(self):
        human,ai = Human(),AI()
        self.print_board()
        while True:
            self.board,move_pos = human.action(self.board)
            game_result = self.board.game_over(move_pos)
            self.print_board()
            if game_result == 'win' or game_result=='tie':
                print('黑子落棋:{},(-1)胜利，game over\n'.format(move_pos)) if game_result == 'win' else print('黑子落棋:{}, 平局\n'.format(move_pos))
                break
            else:
                print('黑子落棋:{},未分胜利\n'.format(move_pos))
            start = time.time()
            self.board, move_pos = ai.action(self.board,move_pos)
            finish = time.time()-start
            # end = datetime.datetime.now()
            # print('ai')
            # print(move_pos)
            game_result = self.board.game_over(move_pos)
            self.print_board()
            if game_result == 'win' or game_result=='tie':
                print('白子落棋:{},(1)胜利，time:{:0.0f}s game over\n'.format(move_pos,finish)) if game_result == 'win' else print('白子落棋:{}, time:{:0.0f}s 平局\n'.format(move_pos,finish))
                break
            else:
                print('白子落棋:{}, time:{:0.0f}s 未分胜利\n'.format(move_pos,finish))

if __name__ == '__main__':
    play = play()
    play.startplay()