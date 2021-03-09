In this directory you will find all the code I wrote for the following article https://blog.whiteflag.io/blog/deep-dive-windows-rpc/.

To translate the IDL file:

> midl.exe /app_config RemotePrivilegeCall.idl

To compile the client/server:

> cl.exe /D UNICODE /EHsc RemotePrivilege_c.c client.cpp
> cl.exe /D UNICODE /EHsc RemotePrivilege_s.c server.cpp

Happy hacking :) !
