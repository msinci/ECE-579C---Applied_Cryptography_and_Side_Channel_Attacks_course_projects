#include<stdio.h>
#include<stdlib.h>
#include <sys/types.h>
#include <stdio.h>
#include <openssl/aes.h>
#include <assert.h>
#include "math.h"
typedef unsigned char     uint8_t;
typedef unsigned short    uint16_t;
typedef unsigned int      uint32_t;
typedef unsigned long int uint64_t;

int spy[32];
int test[256][16]={0};
unsigned long timing=0;

inline void clflush(volatile void * p){
	asm volatile ("clflush (%0)" :: "r"(p));
}

__inline__ void rdtsc(void *m) {
	__asm__ __volatile__ ("rdtscp" : "=a" (*((uint32_t *)(m))), "=d" (*((uint32_t *)(m+4))));
}

int probe[256]={0};

void main(void){

	volatile  i=0;
	int n=0;
	int poskey=0;
	int temp = 0;
	long control[32]={0};
	long control1[32]={0};
	unsigned char plaintext[16]={0};
	unsigned char ciphertext[16];
	unsigned char key[16]={0};
	uint64_t *pointer;
	long time1,time2;
	int j;
	int round=0;
	unsigned char value;
	uint32_t value1;
	uint64_t pointval=0x4043c0;
	uint64_t *p;
	uint64_t *set;
	int count;
	AES_KEY expanded;
	AES_set_encrypt_key(key, 128,
			&expanded) ;
	srand(time(NULL));
	count=0;
        p=pointval;
	//printf("%x\n",*(p));
	//set=p + (15*8);
	
	while(round<500000){
	for (i=0;i<16;i++){
		plaintext[i]=random()%255;
	}
	
	for (i=0;i<256;i++){
		clflush(p+i);
	}
	rdtsc(&time1);
	AES_encrypt(plaintext,ciphertext,&expanded);
	rdtsc(&time2);
	timing=time2-time1;
	for (i=0;i<16;i++){
		printf("%d ",ciphertext[i]);
	}
		printf("%lu \n ",timing);
	
	/*if(timing>1800){
	test[0][ciphertext[0]]+=100;
	}*/
	round++;	
	}
	/*for(i=0;i<256;i++){
	printf("pos %d count %d\n",i,test[0][i]);
	}*/
}
