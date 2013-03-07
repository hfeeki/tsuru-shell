readline.py -- Python Readline Alternative for Windows
Copyright 2001, Chris Gonnerman
    <chris.gonnerman@newcenturycomputers.net>

_rlsetup.c -- Python Readline Installer
Copyright (c) 1999 by Secret Labs AB.
Copyright (c) 1999 by Fredrik Lundh.

LICENSE ----------------------------------------------------------------------

By obtaining, using, and/or copying this software and/or its
associated documentation, you agree that you have read, understood,
and will comply with the following terms and conditions:

Permission to use, copy, modify, and distribute this software and its
associated documentation for any purpose and without fee is hereby
granted, provided that the above copyright notice appears in all
copies, and that both that copyright notice and this permission notice
appear in supporting documentation.

THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, 
INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS.  IN NO 
EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT OR 
CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF 
USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR 
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR 
PERFORMANCE OF THIS SOFTWARE.

NOTES ------------------------------------------------------------------------

This software enables line editing and (temporary) history for Python on 
Windows.  The distribution contains a prebuilt DLL for Python 2.0 and 2.1; it
should work fine on 1.5.2 also, but you will have to rebuild the _rlsetup.pyd
first.  Included is a Makefile for using MinGW32's compiler (be sure to use
the MSVCRT version, *not* the CRTDLL version).

Automatic Installation:  Thanks to Alex Martelli for providing a DistUtils
installer for this package!  I have hacked it up a bit, so if it does anything
stupid blame me.  Just run 

    python setup.py install

and it should work fine.

Manual Installation:  Put readline.py and _rlsetup.pyd in your c:\python\lib 
or wherever you put your site packages.  Python.exe will load it automatically.

