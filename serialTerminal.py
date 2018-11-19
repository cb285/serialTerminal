#!/usr/bin/env python3

import serial
import time
import sys
import readline
import glob
import threading

ENDL = "\r"
ENCODING = "ascii"

def attemptSerConn(port, baudrate):
    
    if (len(glob.glob(port)) == 0):
        print("port not available. check connection.")
        return False
    
    # setup serial connection:
    ser = serial.Serial()
    ser.port = port
    ser.baudrate = baudrate
    ser.bytesize = serial.EIGHTBITS
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    ser.timeout = .25			# read timeout
    ser.write_timeout = .25		# write timeout
    ser.inter_byte_timeout = None	# inter-character timeout
    ser.exclusive = True		# exclusive access mode (POSIX only)
    
    #try:
    ser.open()
    print("connection successful. press CTRL+C to quit.")
    ser.flushInput() # flush buffers
    ser.flushOutput()
    return ser

    #except serial.SerialException:
    #print("connection failed.\n")
    #return False

def ser_write(ser, bytes_to_write):

    # write ENDL before sending data
    #ser.write(ENDL.encode(ENCODING))
    
    # for each byte
    for a_byte in bytes_to_write:
        # write byte to serial port
        ser.write(a_byte.encode(ENCODING))

    # write ENDL
    ser.write(ENDL.encode(ENCODING))

def rx_printer(ser):

    out = ""
    
    while(1):
        while(ser.inWaiting() > 0):
            c = ser.read(1).decode(ENCODING)
            if(c == "\r" or c == "\n"):
                out = out.strip()
                if(out != ""):
                    print(out)
                out = ""
            #print(c)
            out += c
    
def main(args):
    if (len(args) != 3):
        print("USAGE: " + args[0] + " <port> <baudrate>")
        exit(0)
        
    # get port and baudrate from arguments
    port = args[1]
    baudrate = int(args[2])
    
    ser = attemptSerConn(port, baudrate) # attempt connection
    
    if (not ser):
        return 1

    # setup receiver thread
    rx_thread = threading.Thread(target=rx_printer, args=(ser,))
    rx_thread.start()
    
    try:
        while(1):
            cmd = input("")
            ser_write(ser, cmd)

    except KeyboardInterrupt: # If CTRL+C is pressed
        ser.close()		# close serial connection
        print("\n",)
        return 0

# run
if __name__ == "__main__":
    exit(main(sys.argv))
