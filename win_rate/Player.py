from MCTS import monte_carlo_tree_search


class Human:

    def __init__(self, player=-1):
        self.player = player

    def get_action_pos(self, board):
        """落子"""
        try:
            location = input("Your move(请使用逗号隔开坐标，输入 q 退出游戏): ")
            if isinstance(location, str) and len(location.split(",")) == 2:  # for python3, 检测变量类型
                move_pos = tuple([int(n, 10) for n in location.split(",")])     # 转成不可变的元组
            else:
                move_pos = -1
        except:
            move_pos = -1
        if location == 'q':
            print("Game Over by player, good day!")
            exit()
        elif move_pos == -1 or move_pos not in board.get_legal_pos():
            print("Invalid Move")
            move_pos = self.get_action_pos(board)
        return move_pos

    def action(self, board):
        move_pos = self.get_action_pos(board)
        board = board.move(move_pos)    # 新的棋盘
        return board, move_pos


class AI:
    """AI player"""

    def __init__(self, player=1):
        self.player = player

    @staticmethod
    def action(board, pre_pos):
        move_pos, utc = monte_carlo_tree_search(board, pre_pos)
        with open("./win_rate/move_pos.txt", "a") as f:
            # 写入坐标和概率, 坐标去掉 np.array() 的括号
            f.write(str(int(move_pos[0])) + "," + str(int(move_pos[1])) + " " + str(utc) + "\n")
        board = board.move(move_pos)  # 新的棋盘
        return board, move_pos