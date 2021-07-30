#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
int main()
{
    uid_t ruid, euid, suid;
    getresuid(&ruid, &euid, &suid);
    printf("chroot之前:\nruid=%d\neuid=%d\nsuid=%d\n", ruid, euid, suid);
    chdir("/var/chroot");
    if(chroot("/var/chroot") == 0) {
       printf("chroot成功\n");
    } else{
       printf("Chroot失败!\n");
    return 1;
    }
    //在chroot之后放弃权限
    setresuid(ruid, ruid, ruid);
    getresuid(&ruid, &euid, &suid);
    printf("chroot放弃权限后:\nruid=%d\neuid=%d\nsuid=%d\n", ruid, euid, suid);
    execlp("ls", "ls", (char*)0);
    return 0;
}
