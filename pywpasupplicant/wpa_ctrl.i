/* Heavily cribbed from my python mp3 decoder swig code */

%module wpa_ctrl

%include "exception.i"

%{
#define SWIG_FILE_WITH_INIT
#include "wpa_ctrl.h"
%}

%inline %{
typedef struct {
    struct wpa_ctrl * ctrl_iface;
    int attached;
} DirectWPAInterface;

char reply_buf[2048];

static int rc;
%}

%exception DirectWPAInterface::DirectWPAInterface {
    rc = 0;

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

%exception DirectWPAInterface::ctrl_request {
    rc = 0;

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

%extend DirectWPAInterface {
    DirectWPAInterface(char * ctrl_path)
    {
        DirectWPAInterface * iface = NULL;

        struct wpa_ctrl * ctrl = wpa_ctrl_open(ctrl_path);

        if (NULL == iface)
        {
            rc = -1;
        }
        else
        {
            iface = calloc(1, sizeof(DirectWPAInterface));
            iface->ctrl_iface = ctrl;
            iface->attached = 0;
        }

        return iface;
    }

    ~DirectWPAInterface()
    {
        free($self);

        if ($self->attached)
        {
            rc = wpa_ctrl_detach($self->ctrl_iface);
        }

        wpa_ctrl_close($self->ctrl_iface);
    }

    void ctrl_attach()
    {
        rc = wpa_ctrl_attach($self->ctrl_iface);

        if (rc == 0)
        {
            $self->attached = 1;
        }
    }

    void ctrl_detach()
    {
        rc = wpa_ctrl_detach($self->ctrl_iface);

        if (rc == 0 && $self->attached)
        {
            $self->attached = 0;
        }
    }

    char * ctrl_request(char * request)
    {
        size_t reply_len;

        rc = wpa_ctrl_request($self->ctrl_iface,
            request,
            strlen(request),
            reply_buf,
            &reply_len,
            NULL);

        return reply_buf;
    }
}
