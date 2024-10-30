from Board import Board
from Player import Human, AI
import os

class Game:
    def __init__(self):
        self.board = Board()    # 初始棋盘(黑子先手)
    def graphic(self):
        """绘制棋盘"""
        os.system('cls')
        print('黑子: x, 白子: o')
        # 先打印列号
        print(' ', end='')
        for x in range(self.board.size):
            print("{0:2}".format(x), end='')
        print()
        for i in range(self.board.size):
            print("{0:1}".format(i), end='')
            for j in range(self.board.size):
                if self.board.board[i, j] == 1:
                    print(' o', end='')
                elif self.board.board[i, j] == -1:
                    print(' x', end='')
                else:
                    print(' .', end='')
            print()

    def start_play(self):
        human, ai = Human(), AI()
        self.graphic()

        while True:
            self.board, move_pos = human.action(self.board)
            game_result = self.board.game_over(move_pos)

            self.graphic()
            if game_result == 'win' or game_result == 'tie':    # 游戏结束
                print('黑子落棋: {}'.format(move_pos), end='')
                print(', 黑子胜利！游戏结束！') if game_result == 'win' else print(', 平局！游戏结束！')
                break

            self.board, move_pos = ai.action(self.board, move_pos)
            game_result = self.board.game_over(move_pos)
            self.graphic()
            if game_result == 'win' or game_result == 'tie':    
                print('白子落棋: {}'.format(move_pos), end='')
                print(', 白子胜利！游戏结束！') if game_result == 'win' else print(', 平局！游戏结束！')
                break   

if __name__ == "__main__":
    game = Game()
    game.start_play()   # 玩家控制黑子，AI控制白子