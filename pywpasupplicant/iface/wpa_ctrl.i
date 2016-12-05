/* Heavily cribbed from my python mp3 decoder swig code */

%module wpa_ctrl

%{
#define SWIG_FILE_WITH_INIT
#include "wpa_ctrl.h"
%}

%inline %{
typedef struct {
    struct wpa_ctrl ctrl_iface;
} WPAInterface;

char reply_buf[2048];
%}

%extend WPAInterface {
    /*
     * Typemap needs to be declared inside this block because (???)
     */
    %typemap(in) unsigned char* {
      if (!PyByteArray_Check($input)) {
        SWIG_exception_fail(SWIG_TypeError, "in method '" "$symname" "', argument "
                           "$argnum"" of type '" "$type""'");
      }
      $1 = (unsigned char*) PyByteArray_AsString($input);
    }

    WPAInterface(){
        WPAInterface * iface = malloc(sizeof(WPAInterface));
        int rc = wpa_ctrl_attach(&(iface->ctrl_iface));

        if (rc == -1)
        {
            PyErr_SetString(PyExc_RuntimeError, "Error creating wpa_ctrl interface");
            return NULL;
        }
        else if (rc == -2)
        {
            PyErr_SetString(PyExc_RuntimeError, "Timeout creating wpa_ctrl interface");
            return NULL;
        }
        else
        {
            return iface;
        }
    }

    ~WPAInterface(){
        free($self);
    }

    char * ctrl_request(char* request)
    {
        size_t reply_len;

        int rc = wpa_ctrl_request(&($self->ctrl_iface),
            request,
            strlen(request),
            reply_buf,
            &reply_len,
            NULL);

        if (rc == -1)
        {
            return PyErr_Format(PyExc_RuntimeError, "Error with request '%s'", request);
        }
        else if (rc == -2)
        {
            return PyErr_Format(PyExc_RuntimeError, "Timeout with request '%s'", request);
        }
        else
        {
            return reply_buf;
        }
    }
}
