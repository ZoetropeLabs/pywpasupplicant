/* Heavily cribbed from my python mp3 decoder swig code */

%module wpa_ctrl

%include "exception.i"

%{
#define SWIG_FILE_WITH_INIT
#include "wpa_ctrl.h"
%}

%inline %{
typedef struct {
    struct wpa_ctrl ctrl_iface;
} WPAInterface;

char reply_buf[2048];

static int rc;
%}

%exception WPAInterface::WPAInterface {
    $action

    if (rc == -1)
    {
        SWIG_exception_fail(SWIG_RuntimeError, "Error -1 attaching to control interface");
    }
    else if (rc == -2)
    {
        SWIG_exception_fail(SWIG_RuntimeError, "Error -2 attaching to control interface");
    }
}

%exception WPAInterface::ctrl_request {
    $action

    if (rc == -1)
    {
        SWIG_exception_fail(SWIG_RuntimeError, "Error -1 making request");
    }
    else if (rc == -2)
    {
        SWIG_exception_fail(SWIG_RuntimeError, "Error -2 making request");
    }
}

%extend WPAInterface {
    WPAInterface(){
        WPAInterface * iface = calloc(1, sizeof(WPAInterface));
        rc = wpa_ctrl_attach(&(iface->ctrl_iface));

        fprintf(stderr, "%d\n", rc);
        fprintf(stderr, "%d\n", rc == -1);

        return iface;
    }

    ~WPAInterface(){
        free($self);
    }

    char * ctrl_request(char* request)
    {
        size_t reply_len;

        rc = wpa_ctrl_request(&($self->ctrl_iface),
            request,
            strlen(request),
            reply_buf,
            &reply_len,
            NULL);

        return reply_buf;
    }
}
