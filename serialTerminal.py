#!/usr/bin/env python

# file: serialTerminal.py
# simple serial terminal

import serial
import time
import sys

def attemptSerConn(ser):

    CONN_ATTEMPTS = 3  	# number of times to try serial connection
    CONN_INTERVAL = 5 	# time between serial connection attempts (seconds)
    
    print "attempting connection..."
    
    num_attempts = CONN_ATTEMPTS
    
    while(num_attempts > 0):
        try:
            num_attempts -= 1
            ser.open()
            print "connection successful."
            ser.flushInput()	# flush buffers (just in case)
            ser.flushOutput()
            return
        
        except serial.SerialException:
            if (num_attempts > 0):
                time.sleep(CONN_INTERVAL)
                continue
            else:
                print "connection failed for all " + str(CONN_ATTEMPTS) + " attempts.\n"
                exit(1)
                

def main(args):
    if (len(args) != 3):
        print "USAGE: " + args[0] + " <port> <baudrate>"
        exit(0)
        
    # get port and baudrate from arguments
    port = args[1]
    baudrate = int(args[2])
    
    # setup serial connection:
    ser = serial.Serial()
    ser.port = port
    ser.baudrate = baudrate
    ser.bytesize = serial.EIGHTBITS
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    ser.timeout = 1			# read timeout
    ser.xonxoff = False			# software flow control
    ser.rtscts = False			# hardware (RTS/CTS) flow control
    ser.dsrdtr = False			# hardware (DSR/STR) flow control
    #ser.write_timeout = 0		# write timeout
    ser.inter_byte_timeout = None	# inter-character timeout
    ser.exclusive = True		# exclusive access mode (POSIX only)
    
    attemptSerConn(ser) # attempt connection
    
    # run terminal interface:
    try:
        while (True):
            try:
                command = raw_input(">")
                ser.write(command)
                msg = ser.readline().strip()
                print msg
                
            except serial.SerialException:
                choice = raw_input("serial connection failed. retry? (Y/n) ").strip()
                if (choice == "Y" or choice == ""):
                    attemptSerConn(ser)
                    continue
                
                print "\n",
                exit(1)
                
    except KeyboardInterrupt: # If CTRL+C is pressed
        ser.close()		# close serial connection
        print "\n",


# run
if __name__ == "__main__":
    main(sys.argv)
