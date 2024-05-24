#include<stdio.h>
#include<stdint.h>

/*This function expands a 16-bit key into a 128-bit key*/
void expandKey(uint8_t* longKey, const uint8_t* shortKey);

/*Test code to illustrate the key expansion*/

int main()
{
    uint8_t shortKey[2]={0xa1,0xb2}; //This is only an example.
    uint8_t longKey[16];

    expandKey(longKey,shortKey);

    for (int i=0;i<16;i++)
        printf("%x ",longKey[i]);

    return 0;
}


void expandKey(uint8_t* longKey, const uint8_t* shortKey)
{
    longKey[0]=shortKey[0];
    longKey[1]=0x94;
    longKey[2]=shortKey[1];
    longKey[3]=0x5a;
    longKey[9]=shortKey[0]^shortKey[1];
    longKey[10]=0xe7;

    for (int i=4;i<=15;i++)
    {
        if ((i==9)||(i==10)) continue;
        longKey[i]=(longKey[i-1]+longKey[i-4])%257;
        if (longKey[i]==256)
            longKey[i]==0;
    }
}
