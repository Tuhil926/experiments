#ethOS - Tuhil
def get_arr_inp():
    arr = [int(x) for x in input()]
    return arr

def sort_pairs(arr1, arr2):
    dic = {}
    for a in range(len(arr1)):
        dic[arr1[a]] = arr2[a]
    arr1.sort()
    return (dic, arr1)

T = int(input())
for i in range(T):
    upvote_vals = get_arr_inp()
    downvote_vals = get_arr_inp()
    rep = 0
    for j in range(5):
        if upvote_vals[j] == 1:
            rep += 1
        elif upvote_vals[j] == 3:
            rep += 4
        elif upvote_vals[j] == 5:
            rep += 6
        elif upvote_vals[j] == 7:
            rep += 9
        if downvote_vals[j] == 1:
            rep -= 1
        elif downvote_vals[j] == 3:
            rep -= 4
        elif downvote_vals[j] == 5:
            rep -= 6
        elif downvote_vals[j] == 7:
            rep -= 9
    print(rep)


