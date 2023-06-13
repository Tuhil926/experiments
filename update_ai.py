print("hello")
# def update_ai():
#     global current_node
#     global current_grid
#     global first_turn
#     if starts == 2:
#         max_score = -1000000
#         max_score_node = current_node.next_nodes[0]
#
#         possible_nodes = []
#         for node in current_node.next_nodes:
#             # if node.check_won(node.make_grid()):
#             #     max_score_node = node
#             #     break
#             #print(node.score, node.can_win, end=" ")
#             next_can_win = False
#             for next_node in node.next_nodes:
#                 #print(next_node.can_win)
#                 if next_node.can_win:
#                     next_can_win = True
#                     break
#             wins = False
#             for next_node in node.next_nodes:
#                 for next_next_node2 in next_node.next_nodes:
#                     if next_next_node2.check_won(next_next_node2.make_grid()):
#                         wins = True
#                         break
#             if not wins and not next_can_win:
#                 possible_nodes.append(node)
#             elif node.score > max_score and not next_can_win:
#                 #print(max_score)
#                 max_score = node.score
#                 max_score_node = node
#         if len(possible_nodes) != 0:
#             max_score_node = random.choice(possible_nodes)
#         for node in current_node.next_nodes:
#             if node.can_win:
#                 max_score_node = node
#         if first_turn:
#             max_score_node = current_node.next_nodes[4]
#             if random.random() < 0.6:
#                 max_score_node = random.choice(current_node.next_nodes)
#             first_turn = False
#
#         current_node = max_score_node
#         print(current_node)
#         current_grid = current_node.make_grid()
#
#         won = current_node.check_won(current_grid)
#         if won == 1:
#             print("You won!")
#             return True
#         elif won == 2:
#             print("I won!")
#             return True
#         if check_draw(current_grid):
#             print("It's a draw!")
#             return True
#
#         move = [int(x) for x in input().split()]
#
#         current_grid[move[0]][move[1]] = 1
#         current_grid_str = make_grid_str(current_grid)
#
#         for node in current_node.next_nodes:
#             if node.grid_str == current_grid_str:
#                 current_node = node
#                 break
#         print(current_node)
#         won = current_node.check_won(current_grid)
#         if won == 1:
#             print("You won!")
#             return True
#         elif won == 2:
#             print("I won!")
#             return True
#         if check_draw(current_grid):
#             print("It's a draw!")
#             return True
#     else:
#         move = [int(x) for x in input().split()]
#
#         current_grid[move[0]][move[1]] = 2
#         current_grid_str = make_grid_str(current_grid)
#
#         for node in current_node.next_nodes:
#             if node.grid_str == current_grid_str:
#                 current_node = node
#                 break
#         print(current_node)
#         won = current_node.check_won(current_grid)
#         if won == 2:
#             print("You won!")
#             return True
#         elif won == 1:
#             print("I won!")
#             return True
#         if check_draw(current_grid):
#             print("It's a draw!")
#             return True
#
#         min_score = 1000000
#         min_score_node = current_node.next_nodes[0]
#         possible_nodes = []
#         for node in current_node.next_nodes:
#             # if node.check_won(node.make_grid()):
#             #     max_score_node = node
#             #     break
#             next_can_win = False
#             for next_node in node.next_nodes:
#                 # print(next_node.can_win)
#                 if next_node.can_win:
#                     next_can_win = True
#                     break
#             wins = False
#             for next_node in node.next_nodes:
#                 for next_next_node2 in next_node.next_nodes:
#                     if next_next_node2.check_won(next_next_node2.make_grid()):
#                         wins = True
#                         break
#             if not wins and not next_can_win:
#                 possible_nodes.append(node)
#             elif node.score < min_score and not next_can_win:
#                 # print(max_score)
#                 min_score = node.score
#                 min_score_node = node
#         if len(possible_nodes) != 0:
#             min_score_node = random.choice(possible_nodes)
#         for node in current_node.next_nodes:
#             if node.can_win:
#                 min_score_node = node
#
#         current_node = min_score_node
#         print(current_node)
#         current_grid = current_node.make_grid()
#
#         won = current_node.check_won(current_grid)
#         if won == 2:
#             print("You won!")
#             return True
#         elif won == 1:
#             print("I won!")
#             return True
#         if check_draw(current_grid):
#             print("It's a draw!")
#             return True
#
