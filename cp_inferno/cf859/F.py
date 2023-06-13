def get_arr_inp():
    arr = list(map(int, input().split()))
    return arr


def get_dir(inp):
    if inp == "DL":
        return [-1, 1]
    elif inp == "DR":
        return [1, 1]
    elif inp == "UL":
        return [-1, -1]
    else:
        return [1, -1]


def test_collision(n, m, pos1, pos2, dir):
    if pos1 == pos2:
        return True
    if abs(pos2[0] - pos1[0]) != abs(pos2[1] - pos1[1]):
        return False
    if (pos2[0] - pos1[0]) / abs(pos2[0] - pos1[0]) == dir[0] and (pos2[1] - pos1[1]) / abs(pos2[1] - pos1[1]) == dir[1]:
        return True
    else:
        return False

def on_same_line(n, m, pos1, pos2, dir):
    if pos1 == pos2:
        return True
    if abs(pos2[0] - pos1[0]) == abs(pos2[1] - pos1[1]) and (pos2[0] - pos1[0]) / (pos2[1] - pos1[1]) == dir[0]/dir[1]:
        return True
    else:
        return False


def is_same_line(n, m, pos1, pos2, dir1, dir2):
    if dir1[0] != dir2[0] or dir1[1] != dir2[1]:
        return False
    return on_same_line(n, m, pos1, pos2, dir1)


def point_of_incidence(n, m, pos, dir):
    dist_from_top = m - pos[1]
    dist_from_right = n - pos[0]
    dist_from_bot = pos[1] - 1
    dist_from_left = pos[0] - 1
    if dir[0] == 1 and dir[1] == 1:
        if dist_from_right < dist_from_top:
            return ([pos[0] + dist_from_right, pos[1] + dist_from_right], [-1, 1])
        elif dist_from_right > dist_from_top:
            return ([pos[0] + dist_from_top, pos[1] + dist_from_top], [1, -1])
        else:
            return ([pos[0] + dist_from_top, pos[1] + dist_from_top], [-1, -1])
    elif dir[0] == 1 and dir[1] == -1:
        if dist_from_right < dist_from_bot:
            return [pos[0] + dist_from_right, pos[1] - dist_from_right], [-1, -1]
        elif dist_from_right > dist_from_bot:
            return [pos[0] + dist_from_bot, pos[1] - dist_from_bot], [1, 1]
        else:
            return [pos[0] + dist_from_bot, pos[1] - dist_from_bot], [-1, 1]
    elif dir[0] == -1 and dir[1] == 1:
        if dist_from_left < dist_from_top:
            return [pos[0] - dist_from_left, pos[1] + dist_from_left], [1, 1]
        elif dist_from_left > dist_from_top:
            return [pos[0] - dist_from_top, pos[1] + dist_from_top], [-1, -1]
        else:
            return [pos[0] - dist_from_top, pos[1] + dist_from_top], [1, -1]
    elif dir[0] == -1 and dir[1] == -1:
        if dist_from_left < dist_from_bot:
            return [pos[0] - dist_from_left, pos[1] - dist_from_left], [1, -1]
        elif dist_from_left > dist_from_bot:
            return [pos[0] - dist_from_bot, pos[1] - dist_from_bot], [-1, 1]
        else:
            return [pos[0] - dist_from_bot, pos[1] - dist_from_bot], [1, 1]


def is_on_corner_and_mid_bounce(n, m, pos, dir):
    if pos[0] == 1 and pos[1] == 1:
        if dir[0] != dir[1]:
            return True
    elif pos[0] == 1 and pos[1] == m:
        if dir[0] == dir[1]:
            return True
    elif pos[0] == n and pos[1] == 1:
        if dir[0] == dir[1]:
            return True
    elif pos[0] == n and pos[1] == m:
        if dir[0] != dir[1]:
            return True
    else:
        return False
    return False


T = int(input())
for i in range(T):
    a = input().split()
    m, n = int(a[0]), int(a[1])
    pos_init = [int(a[2]), int(a[3])][::-1]
    pos_fin = [int(a[4]), int(a[5])][::-1]
    moving_pos = pos_init.copy()
    direction = get_dir(a[6])
    init_dir = list([direction[0], direction[1]])

    #if i == 532:
    #    for text in a:
    #        print(text, end="")
    #    continue


    if test_collision(n, m, pos_init, pos_fin, direction):
        print(0)
        continue

    number_of_bounces = 0

    if is_on_corner_and_mid_bounce(n, m, pos_init, init_dir):
        pos_init, init_dir = point_of_incidence(n, m, pos_init, init_dir)
        moving_pos, direction = pos_init.copy(), init_dir.copy()
        number_of_bounces += 1

    if test_collision(n, m, pos_init, pos_fin, direction):
        print(number_of_bounces)
        continue

    #print(pos_fin)

    possible = False

    while True:
        moving_pos, direction = point_of_incidence(n, m, moving_pos, direction)
        #print(moving_pos, direction)
        number_of_bounces += 1

        if on_same_line(n, m, moving_pos, pos_fin, direction) and number_of_bounces != 0:
            possible = True
            break

        if is_same_line(n, m, moving_pos, pos_init, direction, init_dir):
            break

    if possible:
        print(number_of_bounces)
    else:
        print(-1)
