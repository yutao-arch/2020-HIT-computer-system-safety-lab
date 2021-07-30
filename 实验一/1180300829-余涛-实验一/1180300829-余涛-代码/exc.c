#include<stdio.h>
#include<unistd.h>
int main()
{
    printf("执行了一个可执行文件用来测试\n");
    uid_t ruid, euid,suid;
    getresuid(&ruid, &euid, &suid);
    printf("利用 exec 执行 setuid 程序后 uid为：ruid = %d, euid = %d, suid = %d\n",ruid, euid, suid);
}
