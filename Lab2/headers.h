
/* ******************************************************************
 ALTERNATING BIT AND GO-BACK-N NETWORK EMULATOR: VERSION 1.1  J.F.Kurose

   This code should be used for PA2, unidirectional or bidirectional
   data transfer protocols (from A to B. Bidirectional transfer of data
   is for extra credit and is not required).  Network properties:
   - one way network delay averages five time units (longer if there
     are other messages in the channel for GBN), but can be larger
   - packets can be corrupted (either the header or the data portion)
     or lost, according to user-defined probabilities
   - packets will be delivered in the order in which they were sent
     (although some can be lost).
**********************************************************************/
#include <stdbool.h>
#include <stdio.h>
#define BIDIRECTIONAL 0    /* change to 1 if you're doing extra credit */
                           /* and write a routine called B_output */

/* a "msg" is the data unit passed from layer 5 (teachers code) to layer  */
/* 4 (students' code).  It contains the data (characters) to be delivered */
/* to layer 5 via the students transport level protocol entities.         */
struct msg {
  char data[20];
  };

/* a packet is the data unit passed from layer 4 (students code) to layer */
/* 3 (teachers code).  Note the pre-defined packet structure, which all   */
/* students must follow. */
struct pkt {
   int seqnum;
   int acknum;
   int checksum;
   char payload[20];
    };

/*State pattern style, reference:c-faq.com/decl/recurfuncp.html */
// typedef int (*funcptr)();
// typedef funcptr (*ptrfuncptr)();

/*****************sender states***************/
// funcptr waitAboveZero(), waitAckZero(), waitAboveOne(), waitAckOne();

/*****************receiver states*************/
// funcptr waitBelowZero(), waitBelowOne();

int calculate_checkSum(char* input);

bool is_corrupted(int checksum, char* input);

void toggle(int* seqence);

int sequence_A = 0, sequence_B = 0;

int ack_A = 0, ack_B = 0;

bool is_waiting_A = false, is_waiting_B = false;

struct pkt *prev_packet_A;
struct pkt *prev_packet_B;