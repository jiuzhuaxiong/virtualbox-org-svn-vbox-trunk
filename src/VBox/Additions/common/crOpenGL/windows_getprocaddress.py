# Copyright (c) 2001, Stanford University
# All rights reserved.
#
# See the file LICENSE.txt for information on redistributing this software.

import sys

import apiutil

apiutil.CopyrightC()

print """
/* DO NOT EDIT - THIS FILE GENERATED BY THE getprocaddress.py SCRIPT */
#include "chromium.h"
#include "cr_string.h"
#include "cr_version.h"
#include "stub.h"
#include "icd_drv.h"
#include "cr_gl.h"
#include "cr_error.h"

#ifdef WINDOWS
#pragma warning( disable: 4055 )
#endif

"""

print """
struct name_address {
  const char *name;
  CR_PROC address;
};

PROC WINAPI wglGetProcAddress_prox( LPCSTR name );

static struct name_address functions[] = {
"""


keys = apiutil.GetAllFunctions(sys.argv[1]+"/APIspec.txt")
for func_name in keys:
    if "Chromium" == apiutil.Category(func_name):
        continue
    if func_name == "BoundsInfoCR":
        continue
    if "GL_chromium" == apiutil.Category(func_name):
        pass #continue

    wrap = apiutil.GetCategoryWrapper(func_name)
    name = "gl" + func_name
    address = "cr_gl" + func_name
    if wrap:
        print '#ifdef CR_%s' % wrap
    print '\t{ "%s", (CR_PROC) %s },' % (name, address)
    if wrap:
        print '#endif'


print "\t/* Chromium binding/glue functions */"

for func_name in keys:
    if (func_name == "Writeback" or
        func_name == "BoundsInfoCR"):
        continue
    if apiutil.Category(func_name) == "Chromium":
        print '\t{ "cr%s", (CR_PROC) cr%s },' % (func_name, func_name)

print "\t/* Windows ICD functions */"

for func_name in ( "CopyContext",
    "CreateContext",
    "CreateLayerContext",
    "DeleteContext",
    "DescribeLayerPlane",
    "DescribePixelFormat",
    "GetLayerPaletteEntries",
    "RealizeLayerPalette",
    "SetLayerPaletteEntries",
    "SetPixelFormat",
    "ShareLists",
    "SwapBuffers",
    "SwapLayerBuffers",
    "ReleaseContext",
    "SetContext",
    "ValidateVersion"):
    print '\t{ "Drv%s", (CR_PROC) Drv%s },' % (func_name, func_name)

print '\t{ "DrvGetProcAddress", (CR_PROC) wglGetProcAddress_prox },'

print """
    { NULL, NULL }
};

extern const GLubyte * WINAPI wglGetExtensionsStringEXT_prox( HDC hdc );

CR_PROC CR_APIENTRY crGetProcAddress( const char *name )
{
    int i;
    wglGetExtensionsStringEXTFunc_t wglGetExtensionsStringEXT = wglGetExtensionsStringEXT_prox;

    stubInit();

    for (i = 0; functions[i].name; i++) {
        if (crStrcmp(name, functions[i].name) == 0) {
            /*crDebug("crGetProcAddress(%s) returns %p", name, functions[i].address);*/
            return functions[i].address;
        }
    }
    
    if (!crStrcmp( name, "wglGetExtensionsStringARB" )) return (CR_PROC) wglGetExtensionsStringEXT;

    crDebug("Returning GetProcAddress:NULL for %s", name);
    return NULL;
}

"""



# XXX should crGetProcAddress really handle WGL/GLX functions???
print_foo = """
/* As these are Windows specific (i.e. wgl), define these now.... */
#ifdef WINDOWS
    {
        wglGetExtensionsStringEXTFunc_t wglGetExtensionsStringEXT = NULL;
        wglChoosePixelFormatFunc_t wglChoosePixelFormatEXT = NULL;
        wglGetPixelFormatAttribivEXTFunc_t wglGetPixelFormatAttribivEXT = NULL;
        wglGetPixelFormatAttribfvEXTFunc_t wglGetPixelFormatAttribfvEXT = NULL;
        if (!crStrcmp( name, "wglGetExtensionsStringEXT" )) return (CR_PROC) wglGetExtensionsStringEXT;
        if (!crStrcmp( name, "wglChoosePixelFormatEXT" )) return (CR_PROC) wglChoosePixelFormatEXT;
        if (!crStrcmp( name, "wglGetPixelFormatAttribivEXT" )) return (CR_PROC) wglGetPixelFormatAttribivEXT;
        if (!crStrcmp( name, "wglGetPixelFormatAttribfvEXT" )) return (CR_PROC) wglGetPixelFormatAttribfvEXT;
    }
#endif
"""
