import os
import sys


def split(line):
    inside_double_apostrophe = 0
    inside_single_apostrophe = 0
    words = line.split()
    a = 0
    while a < len(words) - 1:
        if words[a].count("'") % 2 == 1 or words[a].count('"') % 2 == 1 or words[a].count("(") - words[a].count(
                ")") != 0:
            words[a] = words[a] + " " + words[a + 1]
            del words[a + 1]
            a -= 1
        a += 1

    return words


def get_indentation_level(line):
    indentation_level = 0
    number_of_characters = 0
    for letter in line:
        if letter == " ":
            indentation_level += 1/4
            number_of_characters += 1
        elif letter == "\t":
            indentation_level += 1
            number_of_characters += 1
        else:
            break
    return round(indentation_level), number_of_characters


# open input file
file_name = sys.argv[1]
file = open(file_name, "r")
code = file.readlines()
file.close()

processed_code = []

variables = []

prev_indentation_level = 0
for i in range(len(code)):
    indentation_level, number_of_whitespaces_on_left = get_indentation_level(code[i])
    line = code[i][number_of_whitespaces_on_left::].rstrip()

    words = split(line)

    if len(words) == 0:
        indentation_level = prev_indentation_level
    elif words[0] == "include":
        line = "#include" + "<" + words[1] + ">"

    # control statements
    elif words[0] in ["if", "for", "while"]:
        line = line[:-1:] + ")"
        line = words[0] + " (" + line[len(words[0]) + 1::]
    elif words[0] == "else:":
        line = "else"
    elif words[0] == "else" and words[1] == "if":
        line = line[:-2:] + ")"
        line = "else if (" + line[9::]
    elif words[0] == "repeat":
        for i in range(2, len(words)):
            if i != 2:
                words[2] += words[i]
        line = "for(int " + words[1] + " = 0; " + words[1] + " < " + words[2][:-1:] + "; " + words[1] + "++)"
    elif words[0] in ["int", "char", "float", "double"] and line[-1] != ":":
        variables.append(words[1].split("=")[0].split("[")[0])
        line += ";"

    # broilerplates/new syntax
    elif words[0] == "cploop:":
        line = 'int T;\n\tscanf("%d", &T);\n\tfor (int i = 0; i < T; i++)'
    elif words[0] == "main:":
        line = 'int main()'
    elif words[0] == "input":
        type_ = words[1]
        type_short_form = ""
        variable_prefix = "&"
        indentation_required = 0
        if type_ == "int":
            type_short_form = "d"
        elif type_ == "float":
            type_short_form = "f"
        elif type_ == "double":
            type_short_form = "f"
        elif type_ == "char":
            if words[2][-1] == "]":
                type_short_form = "s"
                variable_prefix = ""
            else:
                type_short_form = "c"
        else:
            print("type " + words[1] + "not recognosed")
        if words[2] not in variables and "[" not in words[2]:
            line = type_ + " " + words[2] + ';\n'
            variables.append(words[2])
            indentation_required = 1
        else:
            line = ""
        if "[]" in words[2]:
            words[2] = words[2][:words[2].find("[")]
        if len(words) == 4:
            line += "\t" * (indentation_level * indentation_required) + 'printf(' + words[3] + ');\n'
            indentation_required = 1
        line += "\t" * (indentation_level * indentation_required) + 'scanf("%' + type_short_form + '", ' + variable_prefix + words[2] + ');'

    # remove ":" after function function definitions
    elif line[-1] == ":":
        line = line[:-1:]

    # add semicolon
    else:
        line = line + ";"

    # add braces
    if indentation_level > prev_indentation_level:
        processed_code.append("\t" * prev_indentation_level + "{")
    elif indentation_level < prev_indentation_level:
        for k in range(prev_indentation_level - indentation_level):
            processed_code.append("\t" * (prev_indentation_level - k - 1) + "}")

    processed_code.append("\t" * indentation_level + line)

    prev_indentation_level = indentation_level

# add final braces until indentation becomes 0
for k in range(prev_indentation_level, 0, -1):
    processed_code.append("\t" * (k - 1) + "}")

# create the c file
processed_file = open(file_name[:-3] + "c", "w")

processed_file.write("#include <stdio.h>\n\n")
for line in processed_code:
    processed_file.write(line + "\n")
processed_file.close()

print("Succuessfully compiled to c\n")

# compile and run c file
os.system("gcc " + file_name[:-3] + "c")
choice = input("Press enter to run the code, press any other key and enter to exit: ")
if choice == "":
    print()
    os.system("start a.exe")