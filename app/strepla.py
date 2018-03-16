# flake8: noqa
"""
ogn@data-ogn:~/ogn-silentwings/app$ sudo netcat -l 80
[sudo] password for ogn: 
POST /ws/desktopStrePla.aspx HTTP/1.1
Accept: */*
Content-Type: application/x-www-form-urlencoded
User-Agent: HTTP Retriever 1.0
Host: data-ogn
Content-Length: 54
Cache-Control: no-cache

cmd=getComp&cToken=guest&uName=guest&uPwd=guest&data=&ogn@data-ogn:~/ogn-silentwings/app$ 

StrePla Server:http://strepla.de/scs/
Port: 80

---- Anfrage StrePla ----
(mB.E]*D@[IPJI)P_POST /scs//ws/desktopStrePla.aspx HTTP/1.1
Accept: */*
Content-Type: application/x-www-form-urlencoded
User-Agent: HTTP Retriever 1.0
Host: strepla.de
Content-Length: 54
Cache-Control: no-cache
Cookie: ASP.NET_SessionId=ktxbfqcj0mz0lgymiuzoh51a

cmd=getComp&cToken=guest&uName=guest&uPwd=guest&data=&

---- Antwort StrePla ----
B.(mEn@t~7[IPI)JPHTTP/1.1 200 OK
Cache-Control: public,must-revalidate
Pragma: public
Content-Type: text/xml; charset=utf-8
Expires: 0
Server: Microsoft-IIS/8.5
X-AspNet-Version: 4.0.30319
X-Powered-By: ASP.NET
Date: Fri, 16 Mar 2018 21:34:21 GMT
Content-Length: 101

<?xml version="1.0"?><scs><error>Wettbewerb mit dem Schluessel guest ist nicht bekannt.</error></scs>

"""
