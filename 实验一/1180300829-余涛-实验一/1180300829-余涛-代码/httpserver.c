#include<sys/types.h>
#include<sys/socket.h>
#include<unistd.h>
#include<stdio.h>
#include<netinet/in.h>        //sockaddr_in 库
#include<arpa/inet.h>         //inet_addr()函数的库
#include<string.h>
#include<sys/wait.h>

void lose_root_permission_temporary(uid_t uid_tran);
void lose_root_permission_permanent(uid_t uid_tran);


// 4.1 程序临时性放弃root权限
void lose_root_permission_temporary(uid_t uid_tran)
{
    uid_t ruid, euid, suid;
    getresuid(&ruid, &euid, &suid);
    if (euid == 0)
    {
        // 临时性放弃root权限
        int is_seteuid = seteuid(uid_tran);
        getresuid(&ruid, &euid, &suid);
        if (euid > 0)
        {
            printf("问题四.一：临时性放弃root权限成功\n");
        }
        else
        {
            printf("问题四.一：临时性放弃root权限失败\n");
        }
        printf("ruid = %d, euid = %d, suid = %d\n", ruid, euid, suid);
    }
    else
    {
        printf("问题四.一：无 root 权限, 无法放弃root权限\n");
    }
}

// 4.2永久性放弃root权限
void lose_root_permission_permanent(uid_t uid_tran)
{
    uid_t ruid, euid, suid;
    getresuid(&ruid, &euid, &suid);
    if (euid != 0 && (ruid == 0 || suid == 0))
    {
        setuid(0);
        getresuid(&ruid, &euid, &suid);
    }
    if (euid == 0)
    {
        // 永久性放弃root权限
        setresuid(uid_tran, uid_tran, uid_tran);
        getresuid(&ruid, &euid, &suid);
        if (ruid > 0 && euid > 0 && suid > 0)
        {
            printf("问题四.二：永久性放弃root权限成功\n");
        }
        else
        {
            printf("问题四.二：永久性放弃root权限失败\n");
        }
        printf("ruid = %d, euid = %d, suid = %d\n", ruid, euid, suid);
    }
    else
    {
        printf("问题四.二：无 root 权限, 无法放弃root权限\n");
    }
}

int main(int argc, char* argv[])
{
    // 以下的三个 id 分别对应了实际用户ID，有效用户ID，保存的用户ID
    uid_t ruid, euid, suid;
    getresuid(&ruid, &euid, &suid);
    printf("初始 uid 为：ruid = %d, euid = %d, suid = %d\n",
        ruid, euid, suid);
    // 1. 提供 http 网络服务，需要设置 setuid 位, 否则会失败
    printf("问题一：提供 http 网络服务\n");
    int server_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (server_socket < 0)
    {
        printf("erro \n");
    }
    // bind 绑定
    struct sockaddr_in server_sockaddr;
    memset(&server_sockaddr, 0, sizeof(server_sockaddr));
    server_sockaddr.sin_family = AF_INET;
    server_sockaddr.sin_port = htons(80);
    server_sockaddr.sin_addr.s_addr = inet_addr("127.0.0.1");
    int is_bind = bind(server_socket, (struct sockaddr*)&server_sockaddr,
        sizeof(server_sockaddr));
    if (is_bind < 0)
    {
        printf("无权限，绑定失败\n");
    }
    else
    {
        printf("有权限，绑定成功\n");
    }
    getresuid(&ruid, &euid, &suid);
    printf("绑定后的 uid 为：ruid = %d, euid = %d, suid = %d\n",
        ruid, euid, suid);

    // 2. 用户fork进程后，父进程和子进程中euid、ruid、suid的差别
    printf("问题二：用户fork进程后，父进程和子进程中euid、ruid、suid的差别\n");
    if (fork() == 0)
    {
        getresuid(&ruid, &euid, &suid);
        printf("子进程 uid 为：ruid = %d, euid = %d, suid = %d\n",
            ruid, euid, suid);

        // 3. 利用 execl 执行 setuid 程序后，euid、ruid、suid是否有变化
        printf("问题三：利用 execl 执行 setuid 程序后，euid、ruid、suid是否有变化\n");
        execl("./exc", "./exc", (char*)0);
    }
    else
    {
        getresuid(&ruid, &euid, &suid);
        printf("父进程 uid为：ruid = %d, euid = %d, suid = %d\n",
            ruid, euid, suid);

        // 4.两种放弃 root 权限的方式
        lose_root_permission_temporary(1001);  // 临时性放弃root权限
        lose_root_permission_permanent(1001);  // 永久性放弃root权限

        // 5. 比较有环境变量和无环境变量的函数使用的差异。
        // 5.1 有环境变量的函数使用
        if (fork() == 0)
        {
            printf("问题五.一：有环境变量的函数使用\n");
            execlp("exc", "./exc", (char*)0);
        }
        wait(NULL);
        if (fork() == 0)
        {
            // 5.2 无环境变量的函数使用
            printf("问题五.二：无环境变量的函数使用\n");
            execl("./exc", "./exc", (char*)0);
        }
        wait(NULL);
    }
    wait(NULL);
    return 0;
}
