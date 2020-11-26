TARGET_EXEC ?= ert_main
TARGET_LIB ?= adaptive_lib.so

CC=gcc
CFLAGS=-Wall -fPIC -MMD -MP

BUILD_DIR ?= ./build
SRC_DIRS ?= ./

SRCS := $(wildcard *.c)
INCL := $(wildcard *.h)
OBJS := $(SRCS:%=$(BUILD_DIR)/%.o)
DEPS := $(OBJS:.o=.d)

INC_FLAGS := -I$(INCL)

LDFLAGS=-g

all: $(BUILD_DIR)/$(TARGET_EXEC) $(BUILD_DIR)/$(TARGET_LIB)

$(BUILD_DIR)/$(TARGET_EXEC): $(OBJS)
	$(CC) $(OBJS) -o $@ $(LDFLAGS)

$(BUILD_DIR)/%.c.o: %.c
	$(MKDIR_P) $(dir $@)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD_DIR)/$(TARGET_LIB): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $@  -shared

.PHONY: clean

clean: 
	$(RM) -r $(BUILD_DIR)

-include $(DEPS)

MKDIR_P ?= mkdir -p