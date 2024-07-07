#include <sys/wait.h>
#include <signal.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#define BUFSIZE 10

int remain_time;

void alarm_info(int sig){
	if(sig == SIGALRM){
		if(remain_time > 0){
			printf("%d\n", remain_time);
			alarm(1);
			remain_time--;
		}
		else{
			exit(0);
		}
	}
}

int main(){
	int fd[2];
	int pipe_to_child[2];
	static struct sigaction act;
		
	act.sa_handler = alarm_info;
	sigfillset(&act.sa_mask);
	sigaction(SIGALRM, &act, NULL);
	signal(SIGINT, SIG_IGN);
	if(pipe(fd) == -1 || pipe(pipe_to_child)){
		perror("pipe create failed");
		 return 0;
	}
	
	switch(fork()){
		case -1:
			perror("fork create failed");
			return 1;
		case 0:
			close(pipe_to_child[1]);
			close(fd[0]);
			while(1){
				char input[10];
				scanf("%s", input);
				if(strcmp(input, "exit") == 0){
				        int value = -1;
					write(fd[1], &value, sizeof(value));
				      	break;
				}
				
				int timer = atoi(input);
				char buffer2[10];
				if(timer >= 1 && timer <= 60){
					write(fd[1], &timer,
						       	sizeof(timer));
					read(pipe_to_child[0], buffer2, sizeof(buffer2));
					printf("%s\n", buffer2);
				}
				else continue;


			}
			close(fd[1]);
			close(pipe_to_child[0]);
			break;
		default:
			close(pipe_to_child[0]);
			close(fd[1]);
			int recv_timer;
			char buff[10];
			while(1){
				read(fd[0], &recv_timer, sizeof(recv_timer));
				if(recv_timer == -1){       
					break;
				}
				remain_time = recv_timer;
				printf("-------------------\n");
				
				alarm(1);

				while(1){	
					pause();
				}
				sleep(5);
				write(pipe_to_child[1], "Wake Up!", BUFSIZE);
			}
			wait(0);
			close(fd[0]);
			close(pipe_to_child[1]);
			break;
	}
	return 0;
}
				
	

