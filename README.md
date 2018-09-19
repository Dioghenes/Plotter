# Plotter
A simple plotter for analog values read by a generic ADC written in Python2.7

### Aim
Sometimes, when an oscilloscope or a voltmeter is not available, one can use and external ADC integrated in a microcontroller to perfomr some misurations: this is a basic plotter written in Python which receives data to be shown in a graph in real-time over a USART communication. 

The format of the data sent over the UART line from the microcontroller is simply: *'datum1' 'datum2' ... 'datumn'\n*: Each integer value sent by the microcontroller is divided from the next one by a simple 'space' character. The block of data ends with '\n'. If you don't want to plot all the data transmitted in a transaction, you can specify the index of the single trace to plot.

### Requirements
  * Python2.7
     * serial
  * Arduino or STM boards, or Freescale micros (any type of microcontroller with an ADC and a USART peripheral)

### Usage
 1) Set the Serial port to be used
 2) Set the baudrate used for communication
 3) Set correctly the number of traces sent by the microcontroller
 4) Set to a value comprised between 0 and number_of_traces-1 to plot only one trace (single trace)
 5) Leave to -1 the trace to plot to trace them all
 6) If you want, enable advanced functions
 7) Set zoom scale to zoom the plot in a particular voltage range (instead of whole fullscale)
 8) Set the ADC range to the **actual** voltages used by the ADC (4.7V is different from 5.0V !)
 9) Enable oversampling 1 (5 points average)
 10) Enable oversampling 2 (10 points average)
 11) Press start
