/*Flush and Reload Attack Template Project 4
Name Surname:
Submission Date:
*/

#include<stdio.h>
#include<stdlib.h>
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


	//Create the key for AES-128
	AES_KEY expanded;
	AES_set_encrypt_key(key, 128,&expanded);
	

	//For 500000 times take the measurement and repeat it 10 times. Totally, you should have 5000000 traces.




	//Create random 16 byte plaintext




	
	//Flush the 4th T-table
	



	
	//Measure the timing for the AES encryption function(before and after the encryption you should use the rdtsc function to get clock cycle of the processor. The difference is the timing for encryption.)

	
	AES_encrypt(plaintext,ciphertext,&expanded);
	


	//Output the ciphertext and the corresponding times to .txt file



}
