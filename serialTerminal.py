#!/usr/bin/env python3

# file: serialTerminal.py
# simple serial terminal

import serial
import time
import sys
import readline
import glob

def attemptSerConn(port, baudrate):
    
    if (len(glob.glob(port)) == 0):
        print("port not available. check connection.")
        return False
    
    # setup serial connection:
    ser = serial.Serial()
    ser.port = port
    ser.baudrate = baudrate
    ser.timeout = .25			# read timeout
    ser.write_timeout = .25		# write timeout
    ser.inter_byte_timeout = None	# inter-character timeout
    ser.exclusive = True		# exclusive access mode (POSIX only)
    
    try:
        ser.open()
        print("connection successful. press CTRL+C to quit.")
        ser.flushInput()	# flush buffers (just in case)
        ser.flushOutput()
        return ser
        
    except serial.SerialException:
        print("connection failed.\n")
        return False
                

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
    
    # run terminal interface:
    while (True):
        try:
            command = raw_input(">").strip()
            if (command == ""):
                continue
            ser.write(command + "\r")
            responses = ser.readlines() #.strip()
            for resp in responses:
                print(resp.strip())
                
        except serial.SerialException:
            choice = raw_input("serial connection failed. retry? (Y/n) ").strip()
            if (choice == "Y" or choice == ""):
                ser = attemptSerConn(port, baudrate)
                if (not ser):
                    return 1
                else:
                    continue
            else:
                return 1
            
        except KeyboardInterrupt: # If CTRL+C is pressed
            ser.close()		# close serial connection
            print("\n",)
            return 0

# run
if __name__ == "__main__":
    exit(main(sys.argv))
