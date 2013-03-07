/*
 * _rlsetup -- install a Python readline implementation
 *
 * Rudely hacked from code written by Fredrik Lundh
 *    <fredrik@pythonware.com>
 *    http://www.pythonware.com
 *
 * Resulting code is the fault of Chris Gonnerman 
 *    <chris.gonnerman@newcenturycomputers.net>
 *
 * Copyright (c) 1999 by Secret Labs AB.
 * Copyright (c) 1999 by Fredrik Lundh.
 *
 * By obtaining, using, and/or copying this software and/or its
 * associated documentation, you agree that you have read, understood,
 * and will comply with the following terms and conditions:
 * 
 * Permission to use, copy, modify, and distribute this software and its
 * associated documentation for any purpose and without fee is hereby
 * granted, provided that the above copyright notice appears in all
 * copies, and that both that copyright notice and this permission notice
 * appear in supporting documentation, and that the name of Secret Labs
 * AB or the author not be used in advertising or publicity pertaining to
 * distribution of the software without specific, written prior
 * permission.
 * 
 * SECRET LABS AB AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO
 * THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
 * FITNESS.  IN NO EVENT SHALL SECRET LABS AB OR THE AUTHOR BE LIABLE FOR
 * ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
 * WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
 * ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
 * OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 * -------------------------------------------------------------------- */

#include "Python.h"

static PyObject* rl_readline;
static PyThreadState *rl_threadstate;


static char*
rl_function(FILE *f1, FILE *f2, char* prompt)
{
    PyObject* res;
    char* p;

    /* switch to original thread state */
    PyThreadState *threadstate;
    threadstate = PyThreadState_Swap(NULL);
    PyEval_RestoreThread(rl_threadstate);

    fprintf(stderr, prompt);

    res = PyObject_CallFunction(rl_readline, NULL);

    if (!res) {
        PyErr_Print();
    } else if (res == Py_None) {
        p = NULL; /* generate KeyboardInterrupt */
    } else if (!PyString_Check(res)) {
        PyErr_SetString(PyExc_ValueError, "readline must return string");
        PyErr_Print();
    } else {
        p = strdup(PyString_AsString(res));
        if (!p) {
            PyErr_NoMemory();
            PyErr_Print();
        }
    }

    Py_DECREF(res);

    PyEval_SaveThread();
    PyThreadState_Swap(threadstate);

    return p;
}

static PyObject*
install_readline(PyObject *self, PyObject* args)
{
    /* install readline hook */

    if (!PyArg_ParseTuple(args, "O", &rl_readline))
        return NULL;

    rl_threadstate = PyThreadState_Get();

    PyOS_ReadlineFunctionPointer = rl_function;

    Py_INCREF(Py_None);
    return Py_None;
}


/* ==================================================================== */
/* module stuff */


static PyMethodDef _functions[] = {
    {"install_readline", (PyCFunction) install_readline, 1},
    {NULL, NULL}
};


void
#ifdef WIN32
__declspec(dllexport)
#endif
init_rlsetup()
{
    Py_InitModule("_rlsetup", _functions);
}


/* end of file. */
