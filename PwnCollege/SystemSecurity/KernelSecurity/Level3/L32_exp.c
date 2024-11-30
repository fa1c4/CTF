/*
input the correct password and run the win function to get root privilege
exp:
1. input the hardcoded password
2. read the /flag
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

    const char password[] = "vqfdcevtzrwuftds";
    ssize_t written_size = write(fd, password, strlen(password));
    printf("password written to device successfully.\n");
    system("cat /flag");
    close(fd);
    return 0;
}
