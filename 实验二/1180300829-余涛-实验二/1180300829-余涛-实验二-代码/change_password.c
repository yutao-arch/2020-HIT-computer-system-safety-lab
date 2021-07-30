#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <pwd.h>
#include <sys/types.h>
#include <sys/stat.h>


/*修改密码的函数
* 两个参数分别为用户名和密码
*/
void changePassword(const char* username, const char* password)
{
    extern int errno;
    printf("将用户%s的密码修改为%s\n", username, password);
    FILE* fp;

    fp = fopen("aaa", "r+"); //打开aaa文件
    if(errno != 0)
    {
        perror("aaa");
        return;
    }

    ssize_t bytesNum;
    size_t n = 0;
    char* line;
    long line_start = ftell(fp);
    while((bytesNum = getline(&line, &n, fp)) != -1)  //使用getline函数按行读取aaa的文件
    {
        if(strlen(line) == 0)
        {
            continue;
        }
        char* currentLineUser = strsep(&line, " "); //然后按照空格拆分每一行
        if(strcmp(username, currentLineUser) == 0)  //将空格前的内容与用户名username比较，相同时说明需要修改该行
        {
            char after[1024] = {0};
            int c = 0;
            while(!feof(fp))  //从密码所在行的下一行一直读到文件尾，将读到的内容保存在字符串after内，用于修改后再次写入
            {
                after[c] = fgetc(fp);
                c ++;
            }
            if(c != 0)
            {
                after[c - 1] = '\0';
            }
            fseek(fp, line_start, SEEK_SET);  //将文件指针移到密码所在行开头
            fprintf(fp, "%s %s\n", username, password);  //按照新的username+空格+密码写入并加上换行
            if(c != 0)  //重新写入刚才保存的after内容
            {
                fprintf(fp, "%s", after);
            }
            long total_length = ftell(fp);
            int fd = fileno(fp);
            if(ftruncate(fd, total_length))  //写完后使用ftruncate删除后续的内容，防止修改前比修改后长而出现修改不完全的情况
            {
                perror("passwd");
            }
            fclose(fp);
            return;
        }
        line_start = ftell(fp);
    }
    printf("passwd：没有该用户!");
    return;
}

int main(int argc, char const *argv[]) {
    extern int errno;
    //首先获取进程的ruid，判断执行的用户
    uid_t ruid, euid, suid;
    struct passwd* userStruct;

    getresuid(&ruid, &euid, &suid);
    userStruct = getpwuid(ruid);  //由于获取的仅仅是用户的id，而不是用户名，所以需要调用getpwuid来获取用户的用户名

    printf("该ruid的用户名为%s\n", userStruct->pw_name);
    
    //根据argc，即参数个数进行判断
    switch(argc)
    {
        case 2:  //参数只有一个(argc==2)时，说明只修改该用户自己密码，无需进行权限判断
            changePassword(userStruct->pw_name, argv[1]);
            break;
        case 3:  //参数有两个(argc==3)时，说明该用户想修改其他用户密码，需要判断该用户是否为root
            if(strcmp("root", userStruct->pw_name) == 0)  //如果该用户为root，可以修改密码
            {
                changePassword(argv[1], argv[2]);
            } else  // 如果该用户不为root，设置errno位
            {
                errno = EPERM;
                perror("passwd");
            }
            break;
        default:
            errno = EINVAL;
            perror("passwd");
    }

}

