#letters = {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
#           "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"}
letters = "abcdefghijklmnopqrstuvwxyz1234567890"
word = input("Word : ")
words = list(word)
N = len(word)
key = int(input("key : "))
typ = int(input("type : "))
k = []
for i in range(letters.__len__()):
    if word[0] == letters[i]:
        p = i + 29
nocap = p % N + typ
if nocap < 3:
    nocap = 3
for i in range(nocap):
    k.append(((key*(i + 1) - N * i) % (i+4)) - 4)
for i in range(len(k)):
    words[k[i]] = words[k[i]].upper()

print("".join(map(str, words)))
