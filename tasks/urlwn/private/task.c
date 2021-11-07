#include <ctype.h>
#include <memory.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <time.h>
#include <unistd.h>

char fromHex(char a, char b) {
  int res = 0;
  if ('0' <= a && a <= '9')
    res += 16 * (a - '0');
  else
    res += 16 * (tolower(a) - 'a' + 10);
  if ('0' <= b && b <= '9')
    res += (b - '0');
  else
    res += (tolower(b) - 'a' + 10);
  return (char)res;
}

int main(int argc, char **argv) {
  const char *index = "/index";
  const char *getRoot = "GET / HTTP/";
  const char *getSome = "GET /";
  const char *badRequest = "HTTP/1.0 400 Bad Request\r\n\r\n";
  const char *ok = "HTTP/1.0 200 OK\r\n\r\nWhat is it?...\r\n";
  if (argc < 2)
    return -1;
  int port = atoi(argv[1]);
  size_t getSomeLen = strlen(getSome), getRootLen = strlen(getRoot);
  char fn[40];
  char decoded[32];
  char buff[102400];
  int sock = socket(AF_INET, SOCK_STREAM, 0);
  memset(fn, '\0', sizeof fn);
  strcpy(fn, index);
  if (sock < 0)
    return 1;
  struct sockaddr_in addr;
  int one = 1;
  setsockopt(sock, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &one, sizeof(one));
  memset(&addr, '\0', sizeof addr);
  addr.sin_family = AF_INET;
  addr.sin_port = htons(port);
  addr.sin_addr.s_addr = htonl(INADDR_ANY);
  if (bind(sock, (struct sockaddr *)&addr, sizeof addr) < 0)
    return 2;
  if (listen(sock, 10) < 0)
    return 3;
  while (1) {
    int conn = accept(sock, NULL, NULL);
    memset(buff, '\0', sizeof buff);
    int readed = read(conn, buff, sizeof buff);
    if (readed >= getRootLen && strncmp(buff, getRoot, getRootLen) == 0) {
      FILE *fd = fopen(fn, "r");
      memset(buff, '\0', sizeof buff);
      fread(buff, sizeof buff, 1, fd);
      fclose(fd);
      buff[sizeof(buff) - 1] = '\0';
      write(conn, buff, strlen(buff));
    } else if (readed > getSomeLen && strncmp(buff, getSome, getSomeLen) == 0) {
      char path[217];
      memset(path, '\0', sizeof path);
      if (readed > 216 + getSomeLen)
        readed = 216 + getSomeLen;
      for (size_t i = getSomeLen; i < readed; ++i) {
        if (buff[i] == ' ')
          break;
        path[i - getSomeLen] = buff[i];
      }
      size_t n = strlen(path);
      memset(decoded, '\0', sizeof decoded);
      for (size_t i = 2; i < n; i += 3) {
        if (path[i - 2] != '%') {
          write(conn, badRequest, strlen(badRequest));
          n = 0;
          break;
        }
        char a = path[i - 1], b = path[i];
        decoded[i / 3] = fromHex(a, b);
      }
      if (strlen(decoded) > 0 && n > 0) {
        write(conn, ok, strlen(ok));
      } else if (n > 0) {
        write(conn, badRequest, strlen(badRequest));
      }
    }
    close(conn);
  }
  close(sock);
  return 0;
}
