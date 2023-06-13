def longest_common_substring_starting_from(element_matches, index, not_checked):
    if len(element_matches) == 0:
        return 0
    lcs = 1
    if index + 1 < len(element_matches):
        for b in range(index + 1, len(element_matches)):
            if not_checked[b] and element_matches[index][0] < element_matches[b][0] and element_matches[index][1] > element_matches[b][1]:
                not_checked[b] = 0
                length = longest_common_substring_starting_from(element_matches, b, not_checked) + 1
                if length > lcs:
                    lcs = length
    return lcs


T = int(input())
for i in range(T):
    N = int(input())
    S = input()
    element_matches = []
    for j in range(N - 1):
        for k in range(j + 1, N)[::-1]:
            if S[j] == S[k]:
                element_matches.append([j, k])
    not_checked = [1 for x in range(len(element_matches))]
    final_lcs = 0
    for j in range(len(element_matches)):
        if not_checked[j]:
            temp_lcs = longest_common_substring_starting_from(element_matches, j, not_checked)
            if temp_lcs > final_lcs:
                final_lcs = temp_lcs
    print(final_lcs)
