/*
babykernel.level.2.0.ko: create a device file /proc/pwncollege to wait for user input password
the password is hardcoded in the kernel module: kfjplhjtylqmntng
exp:
1. write the program to write the password to the device file
2. use dmesg to read flag in kernel log
*/
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>

const char DEVICE_PATH[] = "/proc/pwncollege";


int main() {
    int fd = open(DEVICE_PATH, O_WRONLY);
    if (fd < 0) {
        perror("open");
        return 1;
    }

    const char password[] = "kfjplhjtylqmntng";
    ssize_t written_size = write(fd, password, strlen(password));
    printf("password written to device successfully.\n");
    close(fd);
    return 0;
}
