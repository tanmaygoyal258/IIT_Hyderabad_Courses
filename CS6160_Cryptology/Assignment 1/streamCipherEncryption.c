/* Compile with gcc streamCipherEncryption.c -I C:/sodium/include C:/sodium/lib/libsodium.a */
#include<stdio.h>
#include<stdint.h>
#include<string.h>
#include<stdlib.h>
// #include<sodium.h>

void keyGen(uint8_t* key,unsigned int keyLength);
void streamCipherEncrypt(const unsigned char* message,uint8_t* ciphertext,const uint8_t* key, unsigned int length);
int readFromFile(unsigned char messages[][200],const unsigned char* fname);

int main()
{
    int i,num_messages,n;
    unsigned char messages[20][200];
    uint8_t key[200];
    uint8_t ciphertext[200];
    unsigned char inputName[]="input.txt";
    unsigned char optName[]="output.txt";
    FILE *opt;

    // keyGen(key,200);
    num_messages=readFromFile(messages,inputName);

    opt=fopen(optName,"wb");
    for(i=0;i<num_messages;i++)
    {
        n=strlen(messages[i]);
        streamCipherEncrypt(messages[i],ciphertext,key,n);
        for (int i=0;i<n;i++)
            fprintf(opt,"%02x",ciphertext[i]);
        if (i==num_messages-1)
            continue;
        fprintf(opt,"\n");

    }
    fclose(opt);

    return 0;
}

void keyGen(uint8_t* key, unsigned int keyLength)
{
    for (int i=0;i<keyLength;i++)
        key[i]=randombytes_uniform(256);;
}
void streamCipherEncrypt(const unsigned char* message,uint8_t* ciphertext,const uint8_t* key, unsigned int length)
{
    for (int i=0;i<length;i++)
        ciphertext[i]=message[i]^key[i];
}

int readFromFile(unsigned char messages[][200],const unsigned char* fname)
{
    int count=0;
    FILE *ptr;
    if ((ptr=fopen(fname,"r"))==NULL){
        return 0;
    }
    while(!feof(ptr))
    {
        fgets(messages[count],200,ptr);
        messages[count][strcspn(messages[count],"\n")]=0;
        count++;
    }
    fclose(ptr);
    return count;
}
