int scalar_product(int vector1[], int vector2[])
void vector_product(int vector1[], int vector2[])

int vec_product[3]
main:
    int vector1[3]
    int vector2[3]

    printf("Enter the first vector")
    repeat i 3:
        input int vector1[i]

    printf("Enter the second vector")
    repeat i 3:
        input int vector2[i]

    printf("The scalar product of the two vectors is: %d\n", scalar_product(vector1, vector2))

    vector_product(vector1, vector2)
    printf("The vector product of the two vectors is: (%d, %d, %d)\n", vec_product[0], vec_product[1], vec_product[2])

    input int i


int scalar_product(int vector1[], int vector2[]):
    int product = 0
    repeat i 3:
        product += vector1[i] * vector2[i]
    return(product)

void vector_product(int vector1[], int vector2[]):
    vec_product[0] = vector1[1] * vector2[2] - vector1[2] * vector2[1]
    vec_product[1] = vector1[2] * vector2[0] - vector1[0] * vector2[2]
    vec_product[2] = vector1[0] * vector2[1] - vector1[1] * vector2[0]