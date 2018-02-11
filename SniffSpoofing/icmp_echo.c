/**
	Author: Runzhi Yang
	Function numbers:
	0: ICMP echo spoofing
	1: Eithernet frame spoofing
	3: Sniff and Spoofing
	Reference: http://www.tenouk.com/Module43a.html
**/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <netdb.h>

#include <sys/types.h>
#include <sys/stat.h>
#include <sys/socket.h>

#include <netinet/in_systm.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <netinet/udp.h>
#include <netinet/ip_icmp.h>
#include <netinet/tcp.h>

#include <arpa/inet.h>

#define BUFFER_SIZE 1024
#define true 1
#define false 0

static int verbose_flag = false;

unsigned short in_cksum(unsigned short *addr, int len);

int main(int argc, char **argv){
	int i, sd;
	struct sockaddr_in sin;
	int repeats = 1;
	char buffer[BUFFER_SIZE];
	struct ip *ip = (struct ip *)buffer;
  	struct icmphdr *icmp = (struct icmphdr *)(ip + 1);
  	struct hostent *dst_hp;
	
	if (argc < 3 || argc > 4){
		printf("\nCommand example: %s <source_addr> <destination_address> [repeats]\n", argv[0]);
		exit(1);
	}

	if (argc == 4){
		repeats = atoi(argv[3]);
	}

	for (i = 0; i<repeats; i++){
		bzero(buffer, BUFFER_SIZE);

		sd = socket(AF_INET, SOCK_RAW, IPPROTO_RAW);
		if(sd < 0) {
		    perror("socket() error"); exit(-1);
		}
		sin.sin_family = AF_INET;

		if((ip->ip_src.s_addr = inet_addr(argv[1])) == -1){
         	printf("Cannot resolve source host", argv[1]);
        	exit(1);
     	}

     	if((dst_hp = gethostbyname(argv[2])) == NULL){
			if((ip->ip_dst.s_addr = inet_addr(argv[2])) == -1){
			 fprintf(stderr, "%s: Can't resolve, unknown host\n", argv[2]);
			 exit(1);
			}
        } else {
            bcopy(dst_hp->h_addr_list[0], &ip->ip_dst.s_addr, dst_hp->h_length);
        }

        ip->ip_v = 4;
        //This is the ip header length, 20 bytes-> 5
        ip->ip_hl = 5;
        ip->ip_tos = 0x0;
        ip->ip_len = htons(BUFFER_SIZE);
        // What is this?
        ip->ip_id = 0;
        ip->ip_off = 0x0;
        ip->ip_ttl = htons(64);
        //Uper layer protocol number
        ip->ip_p = IPPROTO_ICMP;
        //Set to 0 before calculating the checksum
        ip->ip_sum = 0x0;
        //This can go wrong
        ip->ip_sum = htons(in_cksum((unsigned short *)ip, sizeof(struct ip)));

        icmp->type = ICMP_ECHO;
        icmp->code = 0;
        // icmp->icmp_id = htons(50179);
        icmp->checksum = 0;
        icmp->checksum = htons(in_cksum((unsigned short *)icmp, sizeof(struct icmphdr)));

		if(sendto(sd, buffer, sizeof(struct iphdr) + sizeof(struct icmphdr), 0, (struct sockaddr *)&sin, sizeof(sin)) < 0) {
			perror("sendto() error");
			exit(-1);
		}
	}
	close(sd);

	exit (0);
}


/**
	Referenced from Internet Checksum function
	You can find the link from this stack overflow page
**/
unsigned short in_cksum(unsigned short *addr, int len)
{
    int nleft = len;
    int sum = 0;
    u_short answer = 0;
    u_short *w = addr;

    while (nleft > 1){
      sum += *w++;
      nleft -= 2;
    }

    if (nleft == 1)
    {
      *(u_char *) (&answer) = *(u_char *) w;
      sum += answer;
    }
    sum = (sum >> 16) + (sum & 0xffff);
    sum += (sum >> 16);
    answer = ~sum;
    return (answer);
}

















































