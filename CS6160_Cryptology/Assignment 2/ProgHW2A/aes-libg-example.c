#include<stdio.h>
#include<stdlib.h>
#include<stdint.h>
#include<gcrypt.h>

#define GCRY_CIPHER GCRY_CIPHER_AES128
#define GCRY_C_MODE GCRY_CIPHER_MODE_ECB // Pick the cipher mode here
 
void aesEncrypt(uint8_t* message,size_t messageLength,uint8_t* ciphertext,uint8_t aesKey[16])
{
    gcry_error_t     gcryError;
    gcry_cipher_hd_t gcryCipherHd;
    size_t           index;
 
    size_t keyLength = gcry_cipher_get_algo_keylen(GCRY_CIPHER);
    size_t blkLength = gcry_cipher_get_algo_blklen(GCRY_CIPHER);
    char * iniVector = "\x0\x0\x0\x0\x0\x0\x0\x0\x0\x0\x0\x0\x0\x0\x0\x0"; // 16 bytes
 
/* Setting up the cipher */
    gcryError = gcry_cipher_open(
        &gcryCipherHd, // gcry_cipher_hd_t *
        GCRY_CIPHER,   // int
        GCRY_C_MODE,   // int
        0);            // unsigned int
    if (gcryError)
    {
        printf("gcry_cipher_open failed:  %s/%s\n",
               gcry_strsource(gcryError),
               gcry_strerror(gcryError));
        return;
    }
    printf("gcry_cipher_open    worked\n");
 
/* Setting the key */
    gcryError = gcry_cipher_setkey(gcryCipherHd, aesKey, keyLength);
    if (gcryError)
    {
        printf("gcry_cipher_setkey failed:  %s/%s\n",
               gcry_strsource(gcryError),
               gcry_strerror(gcryError));
        return;
    }
    printf("gcry_cipher_setkey  worked\n");

/* Setting the iv*/ 
    gcryError = gcry_cipher_setiv(gcryCipherHd, iniVector, blkLength);
    if (gcryError)
    {
        printf("gcry_cipher_setiv failed:  %s/%s\n",
               gcry_strsource(gcryError),
               gcry_strerror(gcryError));
        return;
    }
    printf("gcry_cipher_setiv   worked\n");

/* Encryption */ 
    gcryError = gcry_cipher_encrypt(
        gcryCipherHd, // gcry_cipher_hd_t
        ciphertext,    // void *
        messageLength,    // size_t
        message,    // const void *
        messageLength);   // size_t
    if (gcryError)
    {
        printf("gcry_cipher_encrypt failed:  %s/%s\n",
               gcry_strsource(gcryError),
               gcry_strerror(gcryError));
        return;
    }
    printf("gcry_cipher_encrypt worked\n");
	printf("encBuffer = ");
    for (index = 0; index<messageLength; index++)
        printf(" %02X", ciphertext[index]);
    printf("\n");

  gcry_cipher_close(gcryCipherHd);
}

void aesDecrypt(uint8_t* ciphertext,size_t cipherLength,uint8_t* plaintext,uint8_t aesKey[16])
{

    gcry_error_t     gcryError;
    gcry_cipher_hd_t gcryCipherHd;
    size_t           index;
 
    size_t keyLength = gcry_cipher_get_algo_keylen(GCRY_CIPHER);
    size_t blkLength = gcry_cipher_get_algo_blklen(GCRY_CIPHER);
    char * iniVector = "\x0\x0\x0\x0\x0\x0\x0\x0\x0\x0\x0\x0\x0\x0\x0\x0"; // 16 bytes
 
/* Setting up the cipher */
    gcryError = gcry_cipher_open(
        &gcryCipherHd, // gcry_cipher_hd_t *
        GCRY_CIPHER,   // int
        GCRY_C_MODE,   // int
        0);            // unsigned int
    if (gcryError)
    {
        printf("gcry_cipher_open failed:  %s/%s\n",
               gcry_strsource(gcryError),
               gcry_strerror(gcryError));
        return;
    }
    printf("gcry_cipher_open    worked\n");

/* Setting the key */
    gcryError = gcry_cipher_setkey(gcryCipherHd, aesKey, keyLength);
    if (gcryError)
    {
        printf("gcry_cipher_setkey failed:  %s/%s\n",
               gcry_strsource(gcryError),
               gcry_strerror(gcryError));
        return;
    }
    printf("gcry_cipher_setkey  worked\n");


/* Set iv */ 
    gcryError = gcry_cipher_setiv(gcryCipherHd, iniVector, blkLength);
    if (gcryError)
    {
        printf("gcry_cipher_setiv failed:  %s/%s\n",
               gcry_strsource(gcryError),
               gcry_strerror(gcryError));
        return;
    }
    printf("gcry_cipher_setiv   worked\n");

/* Decryption */ 
    gcryError = gcry_cipher_decrypt(
        gcryCipherHd, // gcry_cipher_hd_t
        plaintext,    // void *
        cipherLength,    // size_t
        ciphertext,    // const void *
        cipherLength);   // size_t
    if (gcryError)
    {
        printf("gcry_cipher_decrypt failed:  %s/%s\n",
               gcry_strsource(gcryError),
               gcry_strerror(gcryError));
        return;
    }
    printf("gcry_cipher_decrypt worked\n");

	printf("Plaintext = ");
    for (index = 0; index<cipherLength; index++)
        printf(" %02X", plaintext[index]);
    printf("\n");

  // clean up after ourselves
    gcry_cipher_close(gcryCipherHd);
}


/*
int main()
{
	uint8_t *message = "0123456789abcde";
	uint8_t *aesKey = "one test AES key";
    size_t messageLength = strlen(message)+1;
	char *ciphertext=malloc(messageLength);
	char *plaintext=malloc(messageLength);

	aesEncrypt(message,messageLength,ciphertext,aesKey);
	aesDecrypt(ciphertext,messageLength,plaintext,aesKey);

	free(ciphertext);
	free(plaintext);
	return 0;
}

*/
