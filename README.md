# Plotter
A simple plotter for analog values read by a generic ADC written in Python2.7

### Aim
Sometimes, when an oscilloscope or a voltmeter is not available, one can use and external ADC integrated in a microcontroller to perfomr some misurations: this is a basic plotter written in Python which receives data to be shown in a graph in real-time over a USART communication. 

The format of the data sent over the UART line from the microcontroller is simply: *'datum1' 'datum2' ... 'datumn'\n*: Each integer value sent by the microcontroller is divided from the next one by a simple 'space' character. The block of data ends with '\n'. If you don't want to plot all the data transmitted in a transaction, you can specify the index of the single trace to plot.

### Requirements
  * Python2.7
     * serial
  * Arduino or STM boards, or Freescale micros (any type of microcontroller with an ADC and a USART peripheral)
