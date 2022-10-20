import numpy as np
from node import Node

mcts_times = 33000


def traverse(node):
    while node.fully_expended():
        node = node.best_uct()
    if node.non_terminal() is not None:
        return node
    else:
        return node.pick_unvisited()


def rollout(node):
    while True:
        game_result = node.non_terminal()
        if game_result is None:
            node = node.pick_random()
        else:
            break
    if game_result == 'win' and -node.board.cur_player == 1:
        return 1
    elif game_result == 'win':
        return -1
    else:
        return 0


def backpropagate(node, result):
    node.num_of_visit += 1
    node.num_of_wins[result] += 1
    # print("backpropagate run")
    if node.parent:
        backpropagate(node.parent, result)
        # print("backpropagate run")


def best_child(node):
    visit_num_of_children = np.array(list([child.num_of_visit for child in node.children]))
    # print(visit_num_of_children)
    best_index = np.argmax(visit_num_of_children)
    node = node.children[best_index]
    return node


def mcts(board, pre_pos):
    root = Node(board=board, pre_pos=pre_pos)
    # print('mcts pre_pos:{}'.format(root.pre_pos))
    for i in range(0, mcts_times):
        leaf = traverse(root)
        # print("----------traverse run")
        simulation_result = rollout(leaf)
        # print(simulation_result)
        backpropagate(leaf, simulation_result)

    return best_child(root).pre_pos

