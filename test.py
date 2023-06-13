import pickle
file = open("users/ANTSS.txt", "rb")
data = pickle.load(file)
print(data)
file.close()
def decode(string, key):
    ascii_chars = []
    for i in range(128):
        ascii_chars.append(chr(i))
    duplicate = list(ascii_chars)
    codes = []
    for i in range(128):
        codes.append(duplicate.pop(key * i % len(duplicate)))
    out = ""
    for letter in string:
        out += ascii_chars[codes.index(letter)]
    return out
for i in range(100, 1000000000):
    if i % 10000 == 0:
        print(i)
    if decode(data[0:len('ANTSS')], i) == "ANTSS":
        print(i)
        break
