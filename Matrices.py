class Matrix:
    def __init__(self, rows):
        self.rows = list(rows)
        self.i = len(self.rows)
        self.j = len(self.rows[0])

    def __str__(self):
        string = ""
        spaces = 1
        for i in range(self.i):
            for j in range(self.j):
                if len(str(self.rows[i][j])) > spaces:
                    spaces = len(str(self.rows[i][j]))
        spaces += 2
        for row in self.rows:
            string += "▌"
            for item in row:
                item_str = str(item)
                string += item_str + " "*(spaces - len(item_str))
            string += "▌\n"

        return string

    def cofactor(self, rows1, i, j):
        rows = []
        for row in rows1:
            rows.append(list(row))
        if len(rows) == 2:
            rows.pop(i)
            rows[0].pop(j)
            return rows[0][0]
        rows.pop(i)
        for row in rows:
            row.pop(j)
        return self.det(rows)

    def det(self, rows1):
        rows = []
        for row in rows1:
            rows.append(list(row))
        if len(rows) == 2:
            return rows[0][0]*rows[1][1] - rows[1][0]*rows[0][1]
        det = 0
        for i in range(len(rows[0])):
            #print(rows)
            det += rows[0][i]*self.cofactor(rows, 0, i)*((-1)**i)
            #print(rows)
        return det

    def determinant(self):
        return self.det(self.rows)

    def transP(self, rows1):
        rows = []
        for i in range(len(rows1[0])):
            row = []
            for j in range(len(rows1)):
                row.append(rows1[j][i])
            rows.append(row)
        return Matrix(rows)

    def transpose(self):
        return self.transP(self.rows)

    def __mul__(self, other):
        if type(other) == Matrix:
            rows = []
            for i in range(self.i):
                row = []
                for j in range(len(other.rows[0])):
                    sum = 0
                    for k in range(self.j):
                        sum += self.rows[i][k]*other.rows[k][j]
                    row.append(sum)
                rows.append(row)
            return Matrix(rows)

        else:
            rows = []
            for row in self.rows:
                rows.append(list(row))
            for i in range(self.i):
                for j in range(self.j):
                    rows[i][j] *= other
            return Matrix(rows)

    def inv(self, rows1):
        rows = []
        for i in range(len(rows1)):
            row = []
            for j in range(len(rows1[0])):
                print(j)
                row.append(self.cofactor(rows1, i, j) * ((-1)**(i + j)))
            rows.append(row)
            print(i)
        return self.transP(rows)*(1/self.det(rows1))

    def inverse(self):
        return self.inv(self.rows)


matrix1 = Matrix([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ])

matrix2 = Matrix([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ]).transpose()

matrix3 = Matrix([[1, 1, 1, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 1, 1, 1, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 1, 1, 1],
                  [1, 0, 0, 1, 0, 0, 1, 0, 0],
                  [0, 1, 0, 0, 1, 0, 0, 1, 0],
                  [0, 0, 1, 0, 0, 1, 0, 0, 1],
                  [1, 0, 0, 0, 1, 0, 0, 0, 1],
                  [0, 0, 1, 0, 1, 0, 1, 0, 0],
                  [1, 0, 1, 0, 0, 0, 0, 0, 0], ])

matrix4 = Matrix([[38, 38, 38, 38, 38, 38, 38, 38, 2], ]).transpose()

print("Finding determinant")
delta = matrix3.determinant()
print("Done!")
if delta == 0:
    print("Delta is 0")
else:
    print(matrix3.inverse()*matrix4)