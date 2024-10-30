import numpy as np
from Node import TreeNode

mcts_times = 2000    # MCTS次数


def monte_carlo_tree_search(board, pre_pos):
    root = TreeNode(board=board, pre_pos=pre_pos)    # 根结点，根结点无父亲
    for i in range(mcts_times):     # 相当于(while resources_left(time, computational power):)即资源限制
        leaf = traverse(root)  # 选择和扩展，leaf = unvisited node（遍历根结点）
        simulation_result = rollout(leaf)   # 模拟
        backpropagate(leaf, simulation_result)  # 反向传播
    # return best_child(root).pre_pos
    # 输出操作以及操作的概率
    node, utc = root.best_uct(c_param=0.2)
    return node.pre_pos, utc


def traverse(node:TreeNode):
    """
    层次遍历该结点及其子结点，遇到叶子结点，遇到未完全扩展的结点则对其进行扩展
    :param node: 某一结点
    :return:
    """
    while node.fully_expanded():    # 该结点已经完全扩展, 选择一个UCT最高的孩子
        node, _ = node.best_uct()
    # 遇到未完成扩展的结点后退出循环，先检查是否为叶子结点
    if node.non_terminal() is not None:     # 是叶子结点(node is terminal)
        return node
    else:           # 不是叶子结点且还没有孩子(in case no children are present)
        return node.pick_univisted_near()    # 扩展访问结点

def rollout(node):
    while True:
        game_result = node.non_terminal()
        if game_result is None:     # 不是叶子结点, 继续模拟
            node = rollout_policy(node)
        else:       # 是叶子结点，结束
            break
    if game_result == 'win' and -node.board.next_player == 1:   # 白子胜(测试过, 没有错误)
        return 1        # 相对于白子是胜利的
    elif game_result == 'win':      # 黑子胜(测试过, 没有错误)
        return -1       # 相对于白子是失败的
    else:   # 平局
        return 0

def rollout_policy(node):
    # return node.pick_random()       # 随机选择了一个结点进行模拟
    return node.pick_near()     # 选择pre_pos附近最近的结点进行模拟

def backpropagate(node, result):
    node.num_of_visit += 1
    node.num_of_wins[result] += 1
    if node.parent:     # 如果不是根结点，则继续更新其父节点
        backpropagate(node.parent, result)
