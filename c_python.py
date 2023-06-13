file = open("file.c", "r")
code = file.readlines()
file.close()
processed_code = []
prev_indentation_level = 0
for i in range(len(code)):
    words = []
    indentation_level = 0
    for letter in code[i]:
        if letter == " ":
            indentation_level += 1/4
        else:
            break
    indentation_level = round(indentation_level)
    start_of_word = indentation_level
    line = code[i][indentation_level::]
    if line[-1] == "\n":
        line = line[:-1:]
        print("dfdfa")
    inside_double_apostrophe = 0
    inside_single_apostrophe = 0
    # for j in range(len(line)):
    #     if line[j] == "'":
    #         if inside_single_apostrophe:
    #             inside_single_apostrophe = 0
    #         else:
    #             inside_single_apostrophe = 1
    #     elif line[j] == '"':
    #         if inside_double_apostrophe:
    #             inside_double_apostrophe = 0
    #         else:
    #             inside_double_apostrophe = 1
    #     if j == len(line) - 1 or line[j] == " " and not (inside_single_apostrophe or inside_double_apostrophe):
    #         if j != start_of_word:
    #             words.append(line[start_of_word:j + 1:])
    #             start_of_word = j
    #         else:
    #             start_of_word = j
    words = line.split()
    if len(words) == 0:
        pass
    elif words[0] == "include":
        line = "#include" + "<" + words[1] + ">"
    elif words[0] in ["if", "for", "while"]:
        line = line[:-1:] + ")"
        line = "if (" + line[3::]
    elif words[0] == "else:":
        line = "else"
    elif words[0] == "else" and words[1] == "if":
        line = line[:-2:] + ")"
        line = "else if (" + line[9::]
    elif line[-1] == ":":
        line = line[:-1:]
    else:
        line = line + ";"
    if indentation_level > prev_indentation_level:
        processed_code.append("\t"*prev_indentation_level + "{")
    elif indentation_level < prev_indentation_level:
        for k in range(prev_indentation_level - indentation_level):
            processed_code.append("\t" * (indentation_level - k - 1) + "}")
    processed_code.append("\t" * indentation_level + line)
    prev_indentation_level = indentation_level

for k in range(prev_indentation_level, 0, -1):
    processed_code.append("\t" * (k - 1) + "}")

processed_file = open("cpython/file_2.c", "w")
for line in processed_code:
    processed_file.write(line + "\n")