/*
use ioctl to write the flag to /proc/pwncollege
exp:
1. write the 1337 to iotcl 
2. pass the correct password to device
*/
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>

#define IOCTL_CMD 1337
const char DEVICE_PATH[] = "/proc/pwncollege";


int main() {
    int fd = open(DEVICE_PATH, O_WRONLY);
    if (fd < 0) {
        perror("open");
        return 1;
    }

    const char password[] = "gnpxhgdhfyzltgrz";
    ssize_t written_size = ioctl(fd, IOCTL_CMD, password);
    printf("password written to device successfully.\n");
    system("cat /flag");
    close(fd);
    return 0;
}
