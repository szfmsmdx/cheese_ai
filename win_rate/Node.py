import numpy as np
from random import randint
from collections import defaultdict


class TreeNode:
    """MCTS Node"""

    def __init__(self, parent=None, pre_pos=None, board=None):
        self.pre_pos = pre_pos  # (0,1)     # 造成这个棋盘的结点下标

        self.parent = parent  # 父结点
        self.children = list()  # 子结点

        self.not_visit_pos = None  # 未访问过的节点

        self.board = board  # 每个结点对应一个棋盘状态

        self.num_of_visit = 0                   # 访问次数N
        self.num_of_wins = defaultdict(int)     # 记录该结点模拟的白子、黑子的胜利次数(defaultdict: 当字典里的key不存在但被查找时，返回0)

    def fully_expanded(self):
        """
        :return: True: 该结点已经完全扩展, False: 该结点未完全扩展
        """
        if self.not_visit_pos is None:      # 如果未访问过的结点为None(初始化为None)则未进行扩展过
            self.not_visit_pos = self.board.get_legal_pos()     # 得到可作为该结点扩展结点的所有下标
        return True if (len(self.not_visit_pos) == 0 and len(self.children) != 0) else False

    def pick_univisted(self):
        """选择一个未访问的结点"""
        random_index = randint(0, len(self.not_visit_pos) - 1)      # 随机选择一个未访问的结点（random.randint: 闭区间）
        move_pos = self.not_visit_pos.pop(random_index)     # 得到一个随机的未访问结点, 并从所有的未访问结点中删除

        new_board = self.board.move(move_pos)    # 模拟落子并返回新棋盘
        new_node = TreeNode(parent=self, pre_pos=move_pos, board=new_board)  # 新棋盘绑定新结点
        self.children.append(new_node)
        return new_node
    
    def pick_univisted_near(self):
        """选择一个未访问的结点，但是按照pre_pos附近的位置就近选择"""
        sorted_possible_moves = sorted(self.not_visit_pos, key=lambda x: pow(x[0] - self.pre_pos[0], 2) + pow(x[1] - self.pre_pos[1], 2))
        idx = randint(0, min(5, len(sorted_possible_moves) - 1))
        move_pos = sorted_possible_moves[idx]
        self.not_visit_pos.remove(move_pos)
        new_board = self.board.move(move_pos)
        new_node = TreeNode(parent=self, pre_pos=move_pos, board=new_board)
        self.children.append(new_node)
        return new_node

    def pick_random(self):
        """选择结点的孩子进行扩展"""
        possible_moves = self.board.get_legal_pos()     # 可以落子的点位
        random_index = randint(0, len(possible_moves) - 1)    # 随机选择一个可以落子的点位（random.randint: 闭区间）
        move_pos = possible_moves[random_index]  # 得到一个随机的可以落子的点位

        new_board = self.board.move(move_pos)  # 模拟落子并返回新棋盘
        new_node = TreeNode(parent=self, pre_pos=move_pos, board=new_board)  # 新棋盘绑定新结点
        return new_node

    def pick_near(self):
        """选择pre_pos附近最近的结点"""
        possible_moves = self.board.get_legal_pos()     # 可以落子的点位
        move_pos = possible_moves[0]
        sorted_possible_moves = sorted(possible_moves, key=lambda x: pow(x[0] - self.pre_pos[0], 2) + pow(x[1] - self.pre_pos[1], 2))
        for pos in sorted_possible_moves:
            if self.board.board[pos[0], pos[1]] == 0:
                move_pos = pos
                break
        new_board = self.board.move(move_pos)
        new_node = TreeNode(parent=self, pre_pos=move_pos, board=new_board)
        return new_node

    def non_terminal(self):
        """
        :return: None: 不是叶子(终端)结点, 'win' or 'tie': 是叶子(终端)结点
        """
        game_result = self.board.game_over(self.pre_pos)
        return game_result

    def num_of_win(self):
        wins = self.num_of_wins[-self.board.next_player]  # 孩子结点的棋盘状态是在父节点的next_player之后形成
        loses = self.num_of_wins[self.board.next_player]
        return wins - loses

    def best_uct(self, c_param=0.5):
        """返回一个自己最好的孩子结点（根据UCT进行比较）"""
        uct_of_children = np.array(list([
            (child.num_of_win() / child.num_of_visit) + c_param * np.sqrt(np.log(self.num_of_visit) / child.num_of_visit)
            for child in self.children
        ]))
        best_index = np.argmax(uct_of_children)
        return self.children[best_index], uct_of_children[best_index]

    def __str__(self):
        return "pre_pos: {}\t pre_player: {}\t num_of_visit: {}\t num_of_wins: {}"\
            .format(self.pre_pos, self.board.board[self.pre_pos[0], self.pre_pos[1]],
                    self.num_of_visit, dict(self.num_of_wins))