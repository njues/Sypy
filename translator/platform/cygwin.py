"""Support for Cygwin."""

import os
import sys
from pypy.translator.platform.posix import BasePosix

class BaseCygwin(BasePosix):
    name = "cygwin"
    
#    link_flags = tuple(
#                 ['-pthread',]
#                 + os.environ.get('LDFLAGS', '').split())
    link_flags = tuple(
                 []
                 + os.environ.get('LDFLAGS', '').split())
    extra_libs = ('-lrt',)
#    cflags = tuple(
#             ['-O3', '-pthread', '-fomit-frame-pointer',
#              '-Wall', '-Wno-unused']
#             + os.environ.get('CFLAGS', '').split())
    cflags = tuple(
             ['-O3', '-fomit-frame-pointer',
              '-Wall', '-Wno-unused']
             + os.environ.get('CFLAGS', '').split())
    standalone_only = ()
    shared_only = ('-fPIC',)
    so_ext = 'dll'
    exe_ext = 'exe'
    so_prefixes = ('lib', '')
    
    def _args_for_shared(self, args):
        return ['-shared'] + args

    def _include_dirs_for_libffi(self):
        return self._pkg_config("libffi", "--cflags-only-I",
                                ['/usr/include/libffi'])

    def _library_dirs_for_libffi(self):
        return self._pkg_config("libffi", "--libs-only-L",
                                ['/usr/lib/libffi'])

    def library_dirs_for_libffi_a(self):
        # places where we need to look for libffi.a
        # XXX obscuuure!  only look for libffi.a if run with translate.py
        if 'translate' in sys.modules:
            return self.library_dirs_for_libffi() + ['/usr/lib']
        else:
            return []


class Cygwin(BaseCygwin):
    shared_only = ()    # it seems that on 32-bit linux, compiling with -fPIC
                        # gives assembler that asmgcc is not happy about.

class Cygwin64(BaseCygwin):
    pass
