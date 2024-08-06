#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <linux/input.h>
#include <sys/wait.h> 
#include <signal.h>   
#include <stdbool.h>

// 函数声明
bool check_and_install_curl(void);


#define DEVICE_KEY    "/dev/input/event0"
#define CURL_COMMAND_FORMAT_WIN "curl http://%s:8088/api/shutdown/win?password=1"
#define CURL_COMMAND_FORMAT_DEB "curl http://%s:8088/api/shutdown/debian?password=1"
#define SHUTDOWN_COMMAND_FORMAT "echo %s | sudo -S shutdown -h now"



bool check_and_install_curl(void) {
    // 使用system()函数检查curl是否可用
    int result = system("command -v curl >/dev/null 2>&1");

    // 如果curl不存在（即command -v curl返回非零值）
    if (result != 0) {
        printf("Curl not found. Attempting to install...\n");

        // 尝试使用apt-get安装curl
        result = system("sudo apt-get install -y curl");

        // 检查安装是否成功
        if (result == 0) {
            printf("Curl installed successfully.\n");
            return true; // 安装成功
        } else {
            fprintf(stderr, "Failed to install curl. Exiting...\n");
            return false; // 安装失败
        }
    } else {
        printf("Curl is already installed.\n");
        return true; // 已经存在
    }
}




int execute_command(const char *command) {
    pid_t pid = fork();
    if (pid < 0) {
        perror("fork failed");
        return -1;
    }

    if (pid == 0) { // 子进程
        execlp("sh", "sh", "-c", command, NULL);
        perror("execlp failed"); // 如果到这里，说明execlp执行失败
        exit(EXIT_FAILURE);
    }

    signal(SIGCHLD, SIG_IGN);

    return 0;
}

int main(int argc, char *argv[]) {
    if (!check_and_install_curl()) {
        return 1; // 如果安装curl失败，则退出程序
    }
    const char *win_ip_address = getenv("WINIP");
    const char *deb_ip_address = getenv("DEBIP");
    if (win_ip_address == NULL &&  deb_ip_address == NULL) {
        fprintf(stderr, "环境变量 WIN/DEBIP 未设置\n");
        return 1;
    }

    int fd = -1, ret = -1;
    struct input_event dev;

    // 打开设备文件
    fd = open(DEVICE_KEY, O_RDONLY);
    if (fd < 0) {
        perror("open failure.");
        return -1;
    }
 //   else{
   // 	fprintf(stdout, "等待电源powerkey事件中.....\n");
 //   }
	

    while (1) {
        // 读取一个event事件包
        memset(&dev, 0, sizeof(struct input_event));
        ret = read(fd, &dev, sizeof(struct input_event));
        if (ret != sizeof(struct input_event)) {
            perror("read failure.");
            break;
        }

        // 解析event包，Get发生了什么样的输入事件
/*        printf("------------------------------------\n");
        printf("type:%d\n", dev.type);
        printf("code:%d\n", dev.code);
        printf("value:%d\n", dev.value);
        printf("\n");
*/
        if (dev.type == 1 && dev.code == 116) {
            char win_curl_command[256];
            char deb_curl_command[256];
            snprintf(win_curl_command, sizeof(win_curl_command), CURL_COMMAND_FORMAT_WIN, win_ip_address);
            snprintf(deb_curl_command, sizeof(deb_curl_command), CURL_COMMAND_FORMAT_DEB, deb_ip_address);
            int win_curl_result = execute_command(win_curl_command);
            int deb_curl_result = execute_command(deb_curl_command);
    
            if (win_curl_result == 0 || deb_curl_result == 0) {
                printf("此计算机即将关闭，结束该程序将中断关机操作\n");  
    		sleep(20);
                // curl命令执行成功，执行shutdown命令
                char shutdown_command[256];
                snprintf(shutdown_command, sizeof(shutdown_command), SHUTDOWN_COMMAND_FORMAT, "{password}");
		execute_command(shutdown_command);
            } else {
                fprintf(stderr, "Curl command execution failed.\n");
            }
        }


    }

    // 关闭设备文件
    close(fd);

    return 0;
}
