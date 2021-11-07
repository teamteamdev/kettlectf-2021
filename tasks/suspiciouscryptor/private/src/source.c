#include<stdio.h>
#include <stdlib.h>


char some_function(char a, char b)
{
    char c = a & b;
    char r = ~c;
    return r;
}

char curious_function(char a, char b)
{
    char f = some_function(a, b);
    char s = some_function(a, f);
    return s;
}

char another_curious_function(char a, char b)
{
    char f = some_function(a, b);
    char s = some_function(a, f);
    char t = some_function(b, f);
    char r = some_function(s, t);
    return r;
}

char last_function( char a,  char b)
{
    char s1 = a & b;
    char s2 = another_curious_function(a, b);
    char s3 = another_curious_function(s1, s2);
    char s4 = curious_function(a, b);
    char s5 = s3 & s4;
    char r = another_curious_function(a, s5);
    return r;
}

void generate_key(char key[64], long seed)
{   
    char x;
    for (int i=0; i < 64; i++)
    {
        seed = (128 * seed + 1337) % 127;
        x = seed;
        key[i] = x;

    }
}


int main(int argc, char *argv[]) {
    if (argc != 3)
    {
        printf("Usage: %s {message} {seed}", argv[0]);
        return 0;
    }

    int seed = atol(argv[2]);

    if (seed < 1)
    {
        printf("Seed should be greater than 0");
        return 0;
    }

    if (seed > 10000)
    {
        printf("Seed should be less than 10000");
        return 0;
    }

    FILE *fp;
    char message[64];
    char key[64];
    char t;

    fp = fopen(argv[1], "r");
    fread(message, sizeof(message), 1, fp);
    fclose(fp);

    generate_key(key, seed);
    
    fp = fopen(argv[1], "w");
    for (int i = 0; i < 64; i++)
    {
        t = last_function(message[i], key[i]);
        fputc(t, fp);
    }
    fclose(fp);

    return 0;
}