import webbrowser


def tree():
    webbrowser.open(decode(abc)[::-1])


def encode(string_to_be_encoded):
    output = ""
    for char in string_to_be_encoded:
        output = output + chr(ord(char) + 1)
    return output


def decode(string_to_be_decoded):
    output = ""
    for char in string_to_be_decoded:
        output = output + chr(ord(char) - 1)
    return output



list = []

list.append(input("Hi. how are you?"))
list.append(input("you're probably wondering what this is.."))
abc = "RYB8dF{8[4b>w@idubx0npd/fcvuvpz/xxx00;tquui"
print("Well, you'll find out")
tree()
print("your inputs: ", list)
print("your reaction to this was priceless XD")
words = "uiftf!bsf!b!gfx!sboepn!xpset/!uifz!ibwf!cffo!fodpefe!tvdi!uibu!uifz!bsf!uif!ofyu!mfuufs/!jg!zpv(sf!sfbejoh!uijt!zpv!qspcbcmz!bmsfbez!gjhvsfe!ju!pvu"





