# Plotter
A simple plotter for analog values read by a generic ADC written in Python2.7

### Brief
Basic plotter for Python and serial UART. The format of the data sent over the UART line from the microcontroller
is simply: *'datum1' 'datum2' ... 'datumn'\n* . Each integer value sent over the UART is divided from the next one by a simple 'space' character. The block of data ends with '\n'. If you don't want to plot all the data transmitted in a transaction, you can specify the number of traces to read.
