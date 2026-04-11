#include <stdint.h>
#include <stdio.h>

// FE310 UART0 registers
#define UART0_BASE      0x10013000
#define UART_TXDATA     (*(volatile uint32_t*)(UART0_BASE + 0x00))
#define UART_TXCTRL     (*(volatile uint32_t*)(UART0_BASE + 0x08))

// Enable UART transmitter
void uart_init(void) {
    UART_TXCTRL = 1;
}

// Send one character, wait if buffer full
void uart_putc(char c) {
    while (UART_TXDATA & 0x80000000);
    UART_TXDATA = c;
}

// picolibc calls this when printf has output
int _write(int fd, const char *buf, int len) {
    for (int i = 0; i < len; i++) {
        if (buf[i] == '\n')
            uart_putc('\r');
        uart_putc(buf[i]);
    }
    return len;
}
// picolibc requires stdout to be defined for printf
FILE *const stdout = (FILE *)1;
FILE *const stderr = (FILE *)2;