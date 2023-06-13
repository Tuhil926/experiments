#include <stdio.h>

int main()
{
	int n;
	printf("Enter n: ");
	scanf("%d", &n);
	int m;
	printf("Enter m: ");
	scanf("%d", &m);
	int q;
	printf("Enter q: ");
	scanf("%d", &q);
	
	int matrix1[n][m], matrix2[m][q];
	
	printf("Matrix 1:\n");
	for(int i = 0; i < n; i++)
	{
		printf("Enter row %d: ", i);
		for(int j = 0; j < m; j++)
		{
			scanf("%d", &matrix1[i][j]);
			
		}
	}
	printf("Matrix 2:\n");
	for(int i = 0; i < m; i++)
	{
		printf("Enter row %d: ", i);
		for(int j = 0; j < q; j++)
		{
			scanf("%d", &matrix2[i][j]);
			
		}
	}
	int product_matrix[n][q];
	for(int i = 0; i < n; i++)
	{
		for(int j = 0; j < q; j++)
		{
			product_matrix[i][j] = 0;
			for(int k = 0; k < m; k++)
			{
				product_matrix[i][j] += matrix1[i][k] * matrix2[k][j];
				//printf("%d\n", product_matrix[i][j]);
				
			}
		}
	}
	for(int i = 0; i < n; i++)
	{
		for(int j = 0; j < q; j++)
		{
			printf("%d    ", product_matrix[i][j]);
		}
		printf("\n\n");
		
	}
	int i;
	scanf("%d", &i);
	
}