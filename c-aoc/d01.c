#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int fuel(int mass) {
  return (mass / 3) - 2;
}

int geometric_fuel(int mass) {
  int sum = 0;
  int m = mass;
  while ((m = fuel(m)) > 0)
    sum += m;
  return sum;
}

int n_lines(char *pathname) {
  FILE *fp = fopen(pathname, "r");
  int lines = 0;
  char ch;
  while(!feof(fp)) {
    ch = fgetc(fp);
    if(ch == '\n')
      lines++;
  }
  return lines;
}

int *parse_ints(size_t N, char *path) {
  int *xs = malloc(N * sizeof(int));
  char buf[4096];
  FILE *fp = fopen(path, "r");
  for (int i = 0; i < N; i++) {
    fgets(buf, sizeof buf, fp);
    xs[i] = atoi(buf);
  }
  return xs;
}

int part1(int *xs, size_t N) {
  int sum = 0;
  for (int i = 0; i < N; i++)
    sum += fuel(xs[i]);
  return sum;
}

int part2(int *xs, size_t N) {
  int sum = 0;
  for (int i = 0; i < N; i++)
    sum += geometric_fuel(xs[i]);
  return sum;
}

int main(int argc, char **argv) {
  for (int i = 0; i < argc; i++)
    printf("%d: %s\n", i, argv[i]);
  char *DEFAULT_PATH = "/home/dmb/aoc-2019/data/d01.txt";
  char *path = (argc > 1 ? argv[1] : DEFAULT_PATH);
  size_t N = n_lines(path);
  printf("n_lines(%s): %ld\n", path, N);
  int *xs = parse_ints(N, path);

  printf("part1: %d\n", part1(xs, N));
  printf("part2: %d\n", part2(xs, N));
}
