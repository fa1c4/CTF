/*
the same logic as Level1.1
exp:
1. vm connect to the device file /proc/pwncollege
2. write the program to write the password to the device file
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

    const char password[] = "kwrjbkfwhqgtkzza";
    ssize_t written_size = write(fd, password, strlen(password));
    printf("password written to device successfully.\n");
    close(fd);
    return 0;
}
