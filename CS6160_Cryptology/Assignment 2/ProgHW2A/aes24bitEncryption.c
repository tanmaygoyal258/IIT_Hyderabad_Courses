#include"aesLongKeyGen24.c"
#include"aes-libg-example.c"

int readFromFile(uint8_t messages[][20],const unsigned char* fname);

int main()
{
	char fname[30]="aesPlaintexts.txt";
	uint8_t shortKey[3]={0xa1,0xb2,0xc3};
    uint8_t longKey[16];
	uint8_t messages[5][20];
	uint8_t* ciphertext;
	size_t messageLength=16;
	FILE *ptr,*opt;
	int i=0,j,num_messages;

    expandKey(longKey,shortKey);

	
	num_messages=readFromFile(messages,fname);
	printf("%d",num_messages);

	opt=fopen("aesCiphertexts.txt","w");
	i=0;

	for(i=0;i<num_messages;i++)
	{
		printf("\n Message= %s",messages[i]);
		ciphertext=malloc(messageLength);
		aesEncrypt(messages[i],messageLength,ciphertext,longKey);
		for (j=0;j<messageLength;j++)
			fprintf(opt,"%02x",ciphertext[j]);
		fprintf(opt,"\n");
		free(ciphertext);
	}
	fclose(opt);

	return 0;
}

int readFromFile(uint8_t messages[][20],const unsigned char* fname)
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
