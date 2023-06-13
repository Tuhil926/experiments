h, w = [int(x) for x in input().split()]
s = []
t = []
for i in range(w):
    s.append(list([]))
    t.append(list([]))
for i in range(h):
    string = input()
    for j in range(w):
        s[j].append(string[j])
for i in range(h):
    string = input()
    for j in range(w):
        t[j].append(string[j])
for i in range(w):
    for j in range(w):
        for k in range(w):
            if s[j] == t[j]:
                del s[j]
                del t[j]
                break
        else:
            break
