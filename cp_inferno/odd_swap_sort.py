possible = True
def merge_sort(list1, left_index, right_index):
    global possible
    if left_index >= right_index:
        return
    if possible:
        middle = (left_index + right_index) // 2
        merge_sort(list1, left_index, middle)
        merge_sort(list1, middle + 1, right_index)
        merge(list1, left_index, right_index, middle)
    else:
        return

    # Defining a function for merge the list


def merge(list1, left_index, right_index, middle):
    global possible
    # Creating subparts of a lists
    left_sublist = list1[left_index:middle + 1]
    right_sublist = list1[middle + 1:right_index + 1]

    # Initial values for variables that we use to keep
    # track of where we are in each list1
    left_sublist_index = 0
    right_sublist_index = 0
    sorted_index = left_index

    # traverse both copies until we get run out one element
    while left_sublist_index < len(left_sublist) and right_sublist_index < len(right_sublist):

        # If our left_sublist has the smaller element, put it in the sorted
        # part and then move forward in left_sublist (by increasing the pointer)
        if left_sublist[left_sublist_index] > right_sublist[right_sublist_index]:
            if (left_sublist[left_sublist_index] + right_sublist[right_sublist_index]) % 2 == 0:
                possible = False
                return
            list1[sorted_index] = right_sublist[right_sublist_index]
            right_sublist_index = right_sublist_index + 1
        else:
            list1[sorted_index] = left_sublist[left_sublist_index]
            left_sublist_index = left_sublist_index + 1
            # Otherwise add it into the right sublist

            # move forward in the sorted part
        sorted_index = sorted_index + 1

        # we will go through the remaining elements and add them
    while left_sublist_index < len(left_sublist):
        list1[sorted_index] = left_sublist[left_sublist_index]
        left_sublist_index = left_sublist_index + 1
        sorted_index = sorted_index + 1

    while right_sublist_index < len(right_sublist):
        list1[sorted_index] = right_sublist[right_sublist_index]
        right_sublist_index = right_sublist_index + 1
        sorted_index = sorted_index + 1


t = int(input())
for i in range(t):
    possible = True
    n = int(input())
    A = [int(x) for x in input().split()]
    merge_sort(A, 0, n - 1)
    if possible:
        print("Yes")
    else:
        print("No")