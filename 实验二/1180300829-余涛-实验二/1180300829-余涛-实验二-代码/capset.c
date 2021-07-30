#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/socket.h>

extern int errno;

//绑定端口
void bindSocket(int port)
{

    int server_socket = socket(AF_INET, SOCK_STREAM, 0);
    if(server_socket < 0) 
    {
        printf("http服务执行出现错误!\n");
        return;
    }

    struct sockaddr_in server_sockaddr;
    memset(&server_sockaddr, 0, sizeof(server_sockaddr));
    server_sockaddr.sin_family = AF_INET;
    server_sockaddr.sin_port = htons(port);
    server_sockaddr.sin_addr.s_addr = inet_addr("127.0.0.1");
    if ((bind(server_socket, (struct sockaddr *)&server_sockaddr, sizeof(server_sockaddr))) < 0)
    {
        printf("绑定端口%d出现错误\n", port);
    } else
    {
        printf("绑定端口%d成功!\n", port);
    }
}



int main(int argc, char const *argv[]) {
   bindSocket(80);
}

