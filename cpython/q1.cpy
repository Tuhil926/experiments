main:
    input int n "Enter n: "
    input int m "Enter m: "
    input int q "Enter q: "

    int matrix1[n][m], matrix2[m][q]

    printf("Matrix 1:\n")
    repeat i n:
        printf("Enter row %d: ", i)
        repeat j m:
            input int matrix1[i][j]

    printf("Matrix 2:\n")
    repeat i m:
        printf("Enter row %d: ", i)
        repeat j q:
            input int matrix2[i][j]

    int product_matrix[n][q]
    repeat i n:
        repeat j q:
            product_matrix[i][j] = 0
            repeat k m:
                product_matrix[i][j] += matrix1[i][k] * matrix2[k][j]
                //printf("%d\n", product_matrix[i][j])

    repeat i n:
        repeat j q:
            printf("%d  ", product_matrix[i][j])
        printf("\n")

    input int i