#include <stdio.h>

int main()
{
	char name[20];
	printf("Enter your name(and age after this): ");
	scanf("%s", name);
	
	int number;
	scanf("%d", &number);
	
	printf("Hello, %s", name);
	printf("The square of %d is %d", number, number * number);
	
	scanf("%d", &number);
}
