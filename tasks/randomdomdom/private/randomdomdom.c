#include <memory.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <time.h>
#include <unistd.h>

int main() {
  char *ok = "HTTP/1.1 200 OK\r\n\r\n";
  int sock = socket(AF_INET, SOCK_STREAM, 0);
  int u = time(NULL) % 7875;
  char key[40];
  sprintf(key, "<h1>Key is %d</h1>\r\n", u);
  if (sock < 0)
    return 1;
  struct sockaddr_in addr;
  int one = 1;
  setsockopt(sock, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &one, sizeof(one));
  memset(&addr, '0', sizeof addr);
  addr.sin_family = AF_INET;
  addr.sin_port = htons(3344);
  addr.sin_addr.s_addr = htonl(INADDR_ANY);
  if (bind(sock, (struct sockaddr *)&addr, sizeof addr) < 0)
    return 2;
  if (listen(sock, 10) < 0)
    return 3;
  while (1) {
    int conn = accept(sock, NULL, NULL);
    char buff[1024];
    memset(buff, '\0', sizeof buff);
    int readed = read(conn, buff, 1024);
    if (readed == 0)
      return 4;
    if (readed > 14 && strncmp(buff, "GET / HTTP/1.1", 14) == 0) {
      write(conn, ok, strlen(ok));
      write(conn, key, strlen(key));
    } else if (readed > 9 && strncmp(buff, "PATCH /", 7) == 0) {
      char number[3];
      memset(number, 0, sizeof number);
      strncpy(number, buff + 7, 2);
      int n = atoi(number);
      if (n != u % ((u % 100) + 1)) {
        char *err = "HTTP/1.1 409 Conflict\r\n\r\n";
        write(conn, err, strlen(err));
        close(conn);
        return 5;
      }
      write(conn, ok, strlen(ok));
      u *= 211;
      u += 1283;
      u %= 7875;
    }
    close(conn);
  }
  close(sock);
  return 0;
}
