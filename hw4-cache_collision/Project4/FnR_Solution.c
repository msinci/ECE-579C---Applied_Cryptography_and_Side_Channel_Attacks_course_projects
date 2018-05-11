#include<stdio.h>
#include<stdlib.h>
#include <sys/types.h>
#include <stdio.h>
#include <openssl/aes.h>
#include <assert.h>
//#include <openssl/aes_locl.h>
#include "math.h"
typedef unsigned char     uint8_t;
typedef unsigned short    uint16_t;
typedef unsigned int      uint32_t;
typedef unsigned long int uint64_t;
unsigned long timing=0;

inline void clflush(volatile void * p){
	asm volatile ("clflush (%0)" :: "r"(p));
}


__inline__ void rdtsc(void *m) {
	__asm__ __volatile__ ("rdtscp" : "=a" (*((uint32_t *)(m))), "=d" (*((uint32_t *)(m+4))));
}

		
		
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
	uint64_t pointval=0x404440;
	uint64_t *p;
	uint64_t *set;
	int count;
	AES_KEY expanded;
	AES_set_encrypt_key(key, 128,
			&expanded) ;
	srand(time(NULL));
	count=0;
        p=pointval;
	set=p + (15*8);
	
	while(round<100000){
	for (i=0;i<16;i++){
		plaintext[i]=random();
		value=random()%255;
	}
	
	for (i=0;i<256;i++){
		clflush(p+i);
	}

	AES_encrypt(plaintext,ciphertext,&expanded);
	

	rdtsc(&time1);
	value=*p;
	rdtsc(&time2);
	timing=time2-time1;
	for (i=0;i<16;i++){
		printf("%d\n",ciphertext[i]);
	}
		printf("%lu \n ",timing);
}
}
