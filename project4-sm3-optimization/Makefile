CC = gcc
CFLAGS = -O2 -Wall -I./src/common

SRC = \
    src/basic/sm3_basic.c

OBJ = $(SRC:.c=.o)

all: sm3_basic_test

sm3_basic_test: $(OBJ)
	$(CC) $(CFLAGS) -o $@ $^

clean:
	rm -f $(OBJ) sm3_basic_test
