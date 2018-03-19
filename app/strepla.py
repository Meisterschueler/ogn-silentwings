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

--- Anfrage an StrePla mit Log&Pass ---
Frame 253174: 323 bytes on wire (2584 bits), 323 bytes captured (2584 bits) on interface 0
Ethernet II, Src: IntelCor_1c:2e:e7 (e4:42:a6:1c:2e:e7), Dst: AvmAudio_d4:82:05 (e0:28:6d:d4:82:05)
Internet Protocol Version 4, Src: 192.168.178.29, Dst: 91.215.73.165
Transmission Control Protocol, Src Port: 53135, Dst Port: 80, Seq: 1, Ack: 1, Len: 269
Hypertext Transfer Protocol
HTML Form URL Encoded: application/x-www-form-urlencoded
    Form item: "cmd" = "getComp"
    Form item: "cToken" = ""
    Form item: "uName" = "Spreitz-Test"
    Form item: "uPwd" = "ogn-silentwings"
    Form item: "data" = ""


(mB.E5
@[IPt-|PPOST /scs//ws/desktopStrePla.aspx HTTP/1.1
Accept: */*
Content-Type: application/x-www-form-urlencoded
User-Agent: HTTP Retriever 1.0
Host: strepla.de
Content-Length: 66
Cache-Control: no-cache

cmd=getComp&cToken=&uName=Spreitz-Test&uPwd=ogn-silentwings&data=&

--- Antwort von StrePla ---
B.(mEN@t[IP|u:PHTTP/1.1 200 OK
Cache-Control: private
Pragma: public
Content-Type: text/xml; charset=utf-8
Expires: 0
Server: Microsoft-IIS/8.5
Set-Cookie: ASP.NET_SessionId=0sdd52yxhl2ghw0uimddwih5; path=/; HttpOnly
X-AspNet-Version: 4.0.30319
X-Powered-By: ASP.NET
Date: Mon, 19 Mar 2018 17:54:14 GMT
Content-Length: 96

<?xml version="1.0"?><scs><error>Wettbewerb mit dem Schluessel  ist nicht bekannt.</error></scs>

=================================================================
--- Anfrage an StrePla mit Log/Pass/WettbewerbsID ---
(mB.E@[I>P*2PxPOST /scs//ws/desktopStrePla.aspx HTTP/1.1
Accept: */*
Content-Type: application/x-www-form-urlencoded
User-Agent: HTTP Retriever 1.0
Host: strepla.de
Content-Length: 98
Cache-Control: no-cache
Cookie: ASP.NET_SessionId=0sdd52yxhl2ghw0uimddwih5

cmd=getComp&cToken=987060a472d9665b8198a3ce6d50ae43&uName=Spreitz-Test&uPwd=ogn-silentwings&data=&

--- Antwort von StrePla  ---
B.(mE`@t[IP>*4FP	HTTP/1.1 200 OK
Cache-Control: public,must-revalidate
Pragma: public
Content-Type: text/xml; charset=utf-8
Expires: 0
Server: Microsoft-IIS/8.5
X-AspNet-Version: 4.0.30319
X-Powered-By: ASP.NET
Date: Mon, 19 Mar 2018 18:13:52 GMT
Content-Length: 441

<?xml version="1.0"?><scs><competition id="493" name="Live Tracking Test der scoring*StrePla API "><taskTypes><taskType id="1" name="Racing-Task (RT)" /><taskType id="2" name="Speed Assigned Area Task (AAT)" /></taskTypes><classes><class id="1057" name="18m" /><class id="1060" name="Open" /></classes><ruleTypes><ruleType id="877" name="LINE (20 km)&#xA; - KEYHOLE (500 m/10000 m)&#xA; - LINE (1 km)&#xA;" /></ruleTypes></competition></scs>
===============================================================
--- Anfrage an StrePla
(mB.E.3@[IWP%MhP/POST /scs//ws/desktopStrePla.aspx HTTP/1.1
Accept: */*
Content-Type: application/x-www-form-urlencoded
User-Agent: HTTP Retriever 1.0
Host: strepla.de
Content-Length: 141
Cache-Control: no-cache
Cookie: ASP.NET_SessionId=0sdd52yxhl2ghw0uimddwih5

cmd=getTaskCompDays&cToken=987060a472d9665b8198a3ce6d50ae43&uName=Spreitz-Test&uPwd=ogn-silentwings&data=<params><class id="1057"/></params>&

--- Antwort ---
B.(mE,Q@t[IPWh%PaHTTP/1.1 200 OK
Cache-Control: public,must-revalidate
Pragma: public
Content-Type: text/xml; charset=utf-8
Expires: 0
Server: Microsoft-IIS/8.5
X-AspNet-Version: 4.0.30319
X-Powered-By: ASP.NET
Date: Mon, 19 Mar 2018 18:25:25 GMT
Content-Length: 88

<?xml version="1.0"?><scs><compclass id="1057" name="18m"><compdays /></compclass></scs>

=========================================================
--- Anfrage ----
(mB.E.5@[IWP%PGPOST /scs//ws/desktopStrePla.aspx HTTP/1.1
Accept: */*
Content-Type: application/x-www-form-urlencoded
User-Agent: HTTP Retriever 1.0
Host: strepla.de
Content-Length: 141
Cache-Control: no-cache
Cookie: ASP.NET_SessionId=0sdd52yxhl2ghw0uimddwih5

cmd=getTaskCompDays&cToken=987060a472d9665b8198a3ce6d50ae43&uName=Spreitz-Test&uPwd=ogn-silentwings&data=<params><class id="1057"/></params>&

--- Antwort ---
B.(mE,S@t[IPW%gPwHTTP/1.1 200 OK
Cache-Control: public,must-revalidate
Pragma: public
Content-Type: text/xml; charset=utf-8
Expires: 0
Server: Microsoft-IIS/8.5
X-AspNet-Version: 4.0.30319
X-Powered-By: ASP.NET
Date: Mon, 19 Mar 2018 18:25:32 GMT
Content-Length: 88

<?xml version="1.0"?><scs><compclass id="1057" name="18m"><compdays /></compclass></scs>
=========================================================
--- Anfrage ----
(mB.E.7@[IWP%g"P^POST /scs//ws/desktopStrePla.aspx HTTP/1.1
Accept: */*
Content-Type: application/x-www-form-urlencoded
User-Agent: HTTP Retriever 1.0
Host: strepla.de
Content-Length: 141
Cache-Control: no-cache
Cookie: ASP.NET_SessionId=0sdd52yxhl2ghw0uimddwih5

cmd=getTaskCompDays&cToken=987060a472d9665b8198a3ce6d50ae43&uName=Spreitz-Test&uPwd=ogn-silentwings&data=<params><class id="1057"/></params>&

--- Antwort ---
B.(mE,U@t[IPW"%PHTTP/1.1 200 OK
Cache-Control: public,must-revalidate
Pragma: public
Content-Type: text/xml; charset=utf-8
Expires: 0
Server: Microsoft-IIS/8.5
X-AspNet-Version: 4.0.30319
X-Powered-By: ASP.NET
Date: Mon, 19 Mar 2018 18:25:46 GMT
Content-Length: 88

<?xml version="1.0"?><scs><compclass id="1057" name="18m"><compdays /></compclass></scs>
=========================================================
--- Anfrage ----

--- Antwort ---
=========================================================
--- Anfrage ----

--- Antwort ---
=========================================================
--- Anfrage ----

--- Antwort ---
=========================================================
--- Anfrage ----

--- Antwort ---
=========================================================
--- Anfrage ----

--- Antwort ---
=========================================================
--- Anfrage ----

--- Antwort ---

"""

