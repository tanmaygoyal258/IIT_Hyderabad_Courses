#include<stdio.h>
#include<stdint.h>

/*This function expands a 3-byte(24 bit) input key into a 16-byte(128 bit) key*/
void expandKey(uint8_t* longKey, const uint8_t* shortKey);

/*Test code to illustrate the key expansion*/
/*
int main()
{
    uint8_t shortKey[3]={0xa1,0xb2,0xc3}; //This is only an example.
    uint8_t longKey[16];

    expandKey(longKey,shortKey);

    for (int i=0;i<16;i++)
        printf("%x ",longKey[i]);

    return 0;
}
*/
//The hex value of the expanded key in the test example is:
//a1 94 b2 5a fb 8e 3f 99 93 c0 e7 7f 11 d1 b7 35

void expandKey(uint8_t* longKey, const uint8_t* shortKey)
{
    longKey[0]=shortKey[0];
    longKey[1]=0x94;
    longKey[2]=shortKey[1];
    longKey[3]=0x5a;
    longKey[9]=shortKey[2]&0xf0;
    longKey[10]=0xe7;

    for (int i=4;i<=15;i++)
    {
        if ((i==9)||(i==10)) continue;
        longKey[i]=(longKey[i-1]+longKey[i-4])%257;
        if (longKey[i]==256)
            longKey[i]==0;
    }
}
