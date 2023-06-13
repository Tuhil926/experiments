#char_list = [108, 97, 117, 114, 101, 110]
#char_list = [101, 109, 105, 110, 105, 99]
#char_list = [110, 32, 99, 114, 121, 101]
#char_list = [114, 112, 116, 101, 120, 32]
#char_list = [117, 98, 104, 115, 105, 102]
#char_list = [22, 155, 98, 255, 136, 62]
#for char in char_list:
#    print(chr(char), end="")
word = "galzuetam"
shift = 0
for i in range(27):
    print(i, end="  ")
    for letter in word:
        print(chr((ord(letter) + i - 97)%26 + 97), end="")
    print()


