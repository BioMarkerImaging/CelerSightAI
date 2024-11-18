#ifndef _MAGICK_MAGICK_BASECONFIG_H
#define _MAGICK_MAGICK_BASECONFIG_H 1
 
/* magick/magick-baseconfig.h. Generated automatically at end of configure. */
/* config/config.h.  Generated from config.h.in by configure.  */
/* config/config.h.in.  Generated from configure.ac by autoheader.  */

/* Define if building universal (internal helper macro) */
/* #undef AC_APPLE_UNIVERSAL_BUILD */

/* Define if you have AUTOTRACE library */
/* #undef AUTOTRACE_DELEGATE */

/* Define if coders and filters are to be built as modules. */
/* #undef BUILD_MODULES */

/* Define if you have the bzip2 library */
/* #undef BZLIB_DELEGATE */

/* Define if you have CAIRO library */
/* #undef CAIRO_DELEGATE */

/* permit enciphering and deciphering image pixels */
#ifndef MAGICKCORE_CIPHER_SUPPORT
#define MAGICKCORE_CIPHER_SUPPORT 1
#endif

/* coders subdirectory. */
#ifndef MAGICKCORE_CODER_DIRNAME
#define MAGICKCORE_CODER_DIRNAME "coders"
#endif

/* Directory where architecture-dependent configuration files live. */
#ifndef MAGICKCORE_CONFIGURE_PATH
#define MAGICKCORE_CONFIGURE_PATH "/data/mxe/usr/x86_64-w64-mingw32.shared.posix.all/etc/ImageMagick-6/"
#endif

/* Subdirectory of lib where architecture-dependent configuration files live.
   */
#ifndef MAGICKCORE_CONFIGURE_RELATIVE_PATH
#define MAGICKCORE_CONFIGURE_RELATIVE_PATH "ImageMagick-6"
#endif

/* Define if you have DJVU library */
/* #undef DJVU_DELEGATE */

/* Directory where ImageMagick documents live. */
#ifndef MAGICKCORE_DOCUMENTATION_PATH
#define MAGICKCORE_DOCUMENTATION_PATH "/data/mxe/usr/x86_64-w64-mingw32.shared.posix.all/share/doc/ImageMagick-6/"
#endif

/* Define if you have Display Postscript */
/* #undef DPS_DELEGATE */

/* exclude deprecated methods in MagickCore API */
/* #undef EXCLUDE_DEPRECATED */

/* Directory where executables are installed. */
#ifndef MAGICKCORE_EXECUTABLE_PATH
#define MAGICKCORE_EXECUTABLE_PATH "/data/mxe/usr/x86_64-w64-mingw32.shared.posix.all/bin/"
#endif

/* Define if you have FFTW library */
/* #undef FFTW_DELEGATE */

/* filter subdirectory. */
#ifndef MAGICKCORE_FILTER_DIRNAME
#define MAGICKCORE_FILTER_DIRNAME "filters"
#endif

/* Define if you have FLIF library */
/* #undef FLIF_DELEGATE */

/* Define if you have FONTCONFIG library */
/* #undef FONTCONFIG_DELEGATE */

/* Define if you have FlashPIX library */
/* #undef FPX_DELEGATE */

/* Define if you have FREETYPE library */
#ifndef MAGICKCORE_FREETYPE_DELEGATE
#define MAGICKCORE_FREETYPE_DELEGATE 1
#endif

/* Define if you have Ghostscript library or framework */
/* #undef GS_DELEGATE */

/* Define if you have GVC library */
/* #undef GVC_DELEGATE */

/* Define to 1 if you have the `acosh' function. */
#ifndef MAGICKCORE_HAVE_ACOSH
#define MAGICKCORE_HAVE_ACOSH 1
#endif

/* Define to 1 if you have the `aligned_malloc' function. */
/* #undef HAVE_ALIGNED_MALLOC */

/* Define to 1 if you have the <arm/limits.h> header file. */
/* #undef HAVE_ARM_LIMITS_H */

/* Define to 1 if you have the <arpa/inet.h> header file. */
/* #undef HAVE_ARPA_INET_H */

/* Define to 1 if you have the `asinh' function. */
#ifndef MAGICKCORE_HAVE_ASINH
#define MAGICKCORE_HAVE_ASINH 1
#endif

/* Define to 1 if you have the `atanh' function. */
#ifndef MAGICKCORE_HAVE_ATANH
#define MAGICKCORE_HAVE_ATANH 1
#endif

/* Define to 1 if you have the `atexit' function. */
#ifndef MAGICKCORE_HAVE_ATEXIT
#define MAGICKCORE_HAVE_ATEXIT 1
#endif

/* Define to 1 if you have the `atoll' function. */
#ifndef MAGICKCORE_HAVE_ATOLL
#define MAGICKCORE_HAVE_ATOLL 1
#endif

/* define if bool is a built-in type */
/* #undef HAVE_BOOL */

/* Define to 1 if you have the `cabs' function. */
#ifndef MAGICKCORE_HAVE_CABS
#define MAGICKCORE_HAVE_CABS 1
#endif

/* Define to 1 if you have the `carg' function. */
#ifndef MAGICKCORE_HAVE_CARG
#define MAGICKCORE_HAVE_CARG 1
#endif

/* Define to 1 if you have the `cimag' function. */
#ifndef MAGICKCORE_HAVE_CIMAG
#define MAGICKCORE_HAVE_CIMAG 1
#endif

/* Define to 1 if you have the `clock' function. */
#ifndef MAGICKCORE_HAVE_CLOCK
#define MAGICKCORE_HAVE_CLOCK 1
#endif

/* Define to 1 if you have the `clock_getres' function. */
/* #undef HAVE_CLOCK_GETRES */

/* Define to 1 if you have the `clock_gettime' function. */
/* #undef HAVE_CLOCK_GETTIME */

/* Define to 1 if clock_gettime supports CLOCK_REALTIME. */
/* #undef HAVE_CLOCK_REALTIME */

/* Define to 1 if you have the <CL/cl.h> header file. */
/* #undef HAVE_CL_CL_H */

/* Define to 1 if you have the <complex.h> header file. */
#ifndef MAGICKCORE_HAVE_COMPLEX_H
#define MAGICKCORE_HAVE_COMPLEX_H 1
#endif

/* Define to 1 if you have the `creal' function. */
#ifndef MAGICKCORE_HAVE_CREAL
#define MAGICKCORE_HAVE_CREAL 1
#endif

/* Define to 1 if you have the `ctime_r' function. */
/* #undef HAVE_CTIME_R */

/* Define to 1 if you have the declaration of `pread', and to 0 if you don't.
   */
#ifndef MAGICKCORE_HAVE_DECL_PREAD
#define MAGICKCORE_HAVE_DECL_PREAD 0
#endif

/* Define to 1 if you have the declaration of `pwrite', and to 0 if you don't.
   */
#ifndef MAGICKCORE_HAVE_DECL_PWRITE
#define MAGICKCORE_HAVE_DECL_PWRITE 0
#endif

/* Define to 1 if you have the declaration of `strerror_r', and to 0 if you
   don't. */
#ifndef MAGICKCORE_HAVE_DECL_STRERROR_R
#define MAGICKCORE_HAVE_DECL_STRERROR_R 0
#endif

/* Define to 1 if you have the declaration of `strlcpy', and to 0 if you
   don't. */
#ifndef MAGICKCORE_HAVE_DECL_STRLCPY
#define MAGICKCORE_HAVE_DECL_STRLCPY 0
#endif

/* Define to 1 if you have the declaration of `tzname', and to 0 if you don't.
   */
#ifndef MAGICKCORE_HAVE_DECL_TZNAME
#define MAGICKCORE_HAVE_DECL_TZNAME 1
#endif

/* Define to 1 if you have the declaration of `vsnprintf', and to 0 if you
   don't. */
#ifndef MAGICKCORE_HAVE_DECL_VSNPRINTF
#define MAGICKCORE_HAVE_DECL_VSNPRINTF 1
#endif

/* Define to 1 if you have the `directio' function. */
/* #undef HAVE_DIRECTIO */

/* Define to 1 if you have the <dirent.h> header file, and it defines `DIR'.
   */
#ifndef MAGICKCORE_HAVE_DIRENT_H
#define MAGICKCORE_HAVE_DIRENT_H 1
#endif

/* Define to 1 if you have the <dlfcn.h> header file. */
/* #undef HAVE_DLFCN_H */

/* Define to 1 if you have the `erf' function. */
#ifndef MAGICKCORE_HAVE_ERF
#define MAGICKCORE_HAVE_ERF 1
#endif

/* Define to 1 if you have the <errno.h> header file. */
#ifndef MAGICKCORE_HAVE_ERRNO_H
#define MAGICKCORE_HAVE_ERRNO_H 1
#endif

/* Define to 1 if you have the `execvp' function. */
#ifndef MAGICKCORE_HAVE_EXECVP
#define MAGICKCORE_HAVE_EXECVP 1
#endif

/* Define to 1 if you have the `fchmod' function. */
/* #undef HAVE_FCHMOD */

/* Define to 1 if you have the <fcntl.h> header file. */
#ifndef MAGICKCORE_HAVE_FCNTL_H
#define MAGICKCORE_HAVE_FCNTL_H 1
#endif

/* Define to 1 if you have the <float.h> header file. */
#ifndef MAGICKCORE_HAVE_FLOAT_H
#define MAGICKCORE_HAVE_FLOAT_H 1
#endif

/* Define to 1 if you have the `floor' function. */
#ifndef MAGICKCORE_HAVE_FLOOR
#define MAGICKCORE_HAVE_FLOOR 1
#endif

/* Define to 1 if you have the `fork' function. */
/* #undef HAVE_FORK */

/* Define to 1 if fseeko (and presumably ftello) exists and is declared. */
#ifndef MAGICKCORE_HAVE_FSEEKO
#define MAGICKCORE_HAVE_FSEEKO 1
#endif

/* Define to 1 if you have the `ftime' function. */
#ifndef MAGICKCORE_HAVE_FTIME
#define MAGICKCORE_HAVE_FTIME 1
#endif

/* Define to 1 if you have the `ftruncate' function. */
#ifndef MAGICKCORE_HAVE_FTRUNCATE
#define MAGICKCORE_HAVE_FTRUNCATE 1
#endif

/* Define to 1 if you have the `getcwd' function. */
#ifndef MAGICKCORE_HAVE_GETCWD
#define MAGICKCORE_HAVE_GETCWD 1
#endif

/* Define to 1 if you have the `getc_unlocked' function. */
/* #undef HAVE_GETC_UNLOCKED */

/* Define to 1 if you have the `getdtablesize' function. */
/* #undef HAVE_GETDTABLESIZE */

/* Define to 1 if you have the `getentropy' function. */
/* #undef HAVE_GETENTROPY */

/* Define to 1 if you have the `getexecname' function. */
/* #undef HAVE_GETEXECNAME */

/* Define to 1 if you have the `getpagesize' function. */
/* #undef HAVE_GETPAGESIZE */

/* Define to 1 if you have the `getpid' function. */
#ifndef MAGICKCORE_HAVE_GETPID
#define MAGICKCORE_HAVE_GETPID 1
#endif

/* Define to 1 if you have the `getpwnam_r' function. */
/* #undef HAVE_GETPWNAM_R */

/* Define to 1 if you have the `getrlimit' function. */
/* #undef HAVE_GETRLIMIT */

/* Define to 1 if you have the `getrusage' function. */
/* #undef HAVE_GETRUSAGE */

/* Define to 1 if you have the `gettimeofday' function. */
#ifndef MAGICKCORE_HAVE_GETTIMEOFDAY
#define MAGICKCORE_HAVE_GETTIMEOFDAY 1
#endif

/* Define to 1 if you have the `gmtime_r' function. */
/* #undef HAVE_GMTIME_R */

/* [Compile with hugepage support] */
/* #undef HAVE_HUGEPAGES */

/* Define to 1 if the system has the type `intmax_t'. */
#ifndef MAGICKCORE_HAVE_INTMAX_T
#define MAGICKCORE_HAVE_INTMAX_T 1
#endif

/* Define to 1 if the system has the type `intptr_t'. */
#ifndef MAGICKCORE_HAVE_INTPTR_T
#define MAGICKCORE_HAVE_INTPTR_T 1
#endif

/* Define to 1 if you have the <inttypes.h> header file. */
#ifndef MAGICKCORE_HAVE_INTTYPES_H
#define MAGICKCORE_HAVE_INTTYPES_H 1
#endif

/* Define to 1 if you have the `isnan' function. */
#ifndef MAGICKCORE_HAVE_ISNAN
#define MAGICKCORE_HAVE_ISNAN 1
#endif

/* Define to 1 if you have the `j0' function. */
#ifndef MAGICKCORE_HAVE_J0
#define MAGICKCORE_HAVE_J0 1
#endif

/* Define to 1 if you have the `j1' function. */
#ifndef MAGICKCORE_HAVE_J1
#define MAGICKCORE_HAVE_J1 1
#endif

/* Define if you have jemalloc memory allocation library */
/* #undef HAVE_JEMALLOC */

/* Define if you have the <lcms2.h> header file. */
#ifndef MAGICKCORE_HAVE_LCMS2_H
#define MAGICKCORE_HAVE_LCMS2_H 1
#endif

/* Define if you have the <lcms2/lcms2.h> header file. */
/* #undef HAVE_LCMS2_LCMS2_H */

/* Define to 1 if you have the `gcov' library (-lgcov). */
/* #undef HAVE_LIBGCOV */

/* Define to 1 if you have the <limits.h> header file. */
#ifndef MAGICKCORE_HAVE_LIMITS_H
#define MAGICKCORE_HAVE_LIMITS_H 1
#endif

/* Define if you have Linux-compatible sendfile() */
/* #undef HAVE_LINUX_SENDFILE */

/* Define to 1 if you have the <linux/unistd.h> header file. */
/* #undef HAVE_LINUX_UNISTD_H */

/* Define to 1 if you have the `lltostr' function. */
/* #undef HAVE_LLTOSTR */

/* Define to 1 if you have the <locale.h> header file. */
#ifndef MAGICKCORE_HAVE_LOCALE_H
#define MAGICKCORE_HAVE_LOCALE_H 1
#endif

/* Define to 1 if you have the `localtime_r' function. */
/* #undef HAVE_LOCALTIME_R */

/* Define to 1 if the system has the type `long long int'. */
#ifndef MAGICKCORE_HAVE_LONG_LONG_INT
#define MAGICKCORE_HAVE_LONG_LONG_INT 1
#endif

/* Define to 1 if you have the `lstat' function. */
/* #undef HAVE_LSTAT */

/* Define to 1 if you have the <machine/param.h> header file. */
/* #undef HAVE_MACHINE_PARAM_H */

/* Define to 1 if you have the <mach-o/dyld.h> header file. */
/* #undef HAVE_MACH_O_DYLD_H */

/* Define to 1 if you have the <malloc.h> header file. */
#ifndef MAGICKCORE_HAVE_MALLOC_H
#define MAGICKCORE_HAVE_MALLOC_H 1
#endif

/* Define to 1 if <wchar.h> declares mbstate_t. */
#ifndef MAGICKCORE_HAVE_MBSTATE_T
#define MAGICKCORE_HAVE_MBSTATE_T 1
#endif

/* Define to 1 if you have the `memmove' function. */
#ifndef MAGICKCORE_HAVE_MEMMOVE
#define MAGICKCORE_HAVE_MEMMOVE 1
#endif

/* Define to 1 if you have the `memset' function. */
#ifndef MAGICKCORE_HAVE_MEMSET
#define MAGICKCORE_HAVE_MEMSET 1
#endif

/* Define to 1 if you have the <minix/config.h> header file. */
/* #undef HAVE_MINIX_CONFIG_H */

/* Define to 1 if you have the `mkdir' function. */
#ifndef MAGICKCORE_HAVE_MKDIR
#define MAGICKCORE_HAVE_MKDIR 1
#endif

/* Define to 1 if you have the `mkstemp' function. */
#ifndef MAGICKCORE_HAVE_MKSTEMP
#define MAGICKCORE_HAVE_MKSTEMP 1
#endif

/* Define to 1 if you have a working `mmap' system call. */
/* #undef HAVE_MMAP */

/* Define if you have the mtmalloc memory allocation library */
/* #undef HAVE_MTMALLOC */

/* Define to 1 if you have the `munmap' function. */
/* #undef HAVE_MUNMAP */

/* define if the compiler implements namespaces */
/* #undef HAVE_NAMESPACES */

/* Define if g++ supports namespace std. */
/* #undef HAVE_NAMESPACE_STD */

/* Define to 1 if you have the `nanosleep' function. */
/* #undef HAVE_NANOSLEEP */

/* Define to 1 if you have the <ndir.h> header file, and it defines `DIR'. */
/* #undef HAVE_NDIR_H */

/* Define to 1 if you have the <netdb.h> header file. */
/* #undef HAVE_NETDB_H */

/* Define to 1 if you have the <netinet/in.h> header file. */
/* #undef HAVE_NETINET_IN_H */

/* Define to 1 if you have the `newlocale' function. */
/* #undef HAVE_NEWLOCALE */

/* Define to 1 if you have the <OpenCL/cl.h> header file. */
/* #undef HAVE_OPENCL_CL_H */

/* Define to 1 if you have the <OS.h> header file. */
/* #undef HAVE_OS_H */

/* Define to 1 if you have the `pclose' function. */
#ifndef MAGICKCORE_HAVE_PCLOSE
#define MAGICKCORE_HAVE_PCLOSE 1
#endif

/* Define to 1 if you have the `poll' function. */
/* #undef HAVE_POLL */

/* Define to 1 if you have the `popen' function. */
#ifndef MAGICKCORE_HAVE_POPEN
#define MAGICKCORE_HAVE_POPEN 1
#endif

/* Define to 1 if you have the `posix_fadvise' function. */
/* #undef HAVE_POSIX_FADVISE */

/* Define to 1 if you have the `posix_fallocate' function. */
/* #undef HAVE_POSIX_FALLOCATE */

/* Define to 1 if you have the `posix_madvise' function. */
/* #undef HAVE_POSIX_MADVISE */

/* Define to 1 if you have the `posix_memalign' function. */
/* #undef HAVE_POSIX_MEMALIGN */

/* Define to 1 if you have the `posix_spawnp' function. */
/* #undef HAVE_POSIX_SPAWNP */

/* Define to 1 if you have the `pow' function. */
#ifndef MAGICKCORE_HAVE_POW
#define MAGICKCORE_HAVE_POW 1
#endif

/* Define to 1 if you have the `pread' function. */
/* #undef HAVE_PREAD */

/* Define to 1 if you have the <process.h> header file. */
#ifndef MAGICKCORE_HAVE_PROCESS_H
#define MAGICKCORE_HAVE_PROCESS_H 1
#endif

/* Define if you have POSIX threads libraries and header files. */
/* #undef HAVE_PTHREAD */

/* Have PTHREAD_PRIO_INHERIT. */
/* #undef HAVE_PTHREAD_PRIO_INHERIT */

/* Define to 1 if you have the `putenv' function. */
#ifndef MAGICKCORE_HAVE_PUTENV
#define MAGICKCORE_HAVE_PUTENV 1
#endif

/* Define to 1 if you have the `pwrite' function. */
/* #undef HAVE_PWRITE */

/* Define to 1 if you have the `qsort_r' function. */
/* #undef HAVE_QSORT_R */

/* Define to 1 if you have the `raise' function. */
#ifndef MAGICKCORE_HAVE_RAISE
#define MAGICKCORE_HAVE_RAISE 1
#endif

/* Define to 1 if you have the `rand_r' function. */
/* #undef HAVE_RAND_R */

/* Define to 1 if you have the `readlink' function. */
/* #undef HAVE_READLINK */

/* Define to 1 if you have the `realpath' function. */
/* #undef HAVE_REALPATH */

/* Define to 1 if you have the `seekdir' function. */
#ifndef MAGICKCORE_HAVE_SEEKDIR
#define MAGICKCORE_HAVE_SEEKDIR 1
#endif

/* Define to 1 if you have the `select' function. */
/* #undef HAVE_SELECT */

/* Define to 1 if you have the `sendfile' function. */
/* #undef HAVE_SENDFILE */

/* Define to 1 if you have the `setlocale' function. */
#ifndef MAGICKCORE_HAVE_SETLOCALE
#define MAGICKCORE_HAVE_SETLOCALE 1
#endif

/* Define to 1 if you have the `setvbuf' function. */
#ifndef MAGICKCORE_HAVE_SETVBUF
#define MAGICKCORE_HAVE_SETVBUF 1
#endif

/* X11 server supports shape extension */
/* #undef HAVE_SHAPE */

/* X11 server supports shared memory extension */
/* #undef HAVE_SHARED_MEMORY */

/* Define to 1 if you have the `sigaction' function. */
/* #undef HAVE_SIGACTION */

/* Define to 1 if you have the `sigemptyset' function. */
/* #undef HAVE_SIGEMPTYSET */

/* Define to 1 if you have the `socket' function. */
/* #undef HAVE_SOCKET */

/* Define to 1 if you have the `spawnvp' function. */
#ifndef MAGICKCORE_HAVE_SPAWNVP
#define MAGICKCORE_HAVE_SPAWNVP 1
#endif

/* Define to 1 if you have the `sqrt' function. */
#ifndef MAGICKCORE_HAVE_SQRT
#define MAGICKCORE_HAVE_SQRT 1
#endif

/* Define to 1 if you have the `stat' function. */
#ifndef MAGICKCORE_HAVE_STAT
#define MAGICKCORE_HAVE_STAT 1
#endif

/* Define to 1 if you have the <stdarg.h> header file. */
#ifndef MAGICKCORE_HAVE_STDARG_H
#define MAGICKCORE_HAVE_STDARG_H 1
#endif

/* Define to 1 if stdbool.h conforms to C99. */
#ifndef MAGICKCORE_HAVE_STDBOOL_H
#define MAGICKCORE_HAVE_STDBOOL_H 1
#endif

/* Define to 1 if you have the <stddef.h> header file. */
#ifndef MAGICKCORE_HAVE_STDDEF_H
#define MAGICKCORE_HAVE_STDDEF_H 1
#endif

/* Define to 1 if you have the <stdint.h> header file. */
#ifndef MAGICKCORE_HAVE_STDINT_H
#define MAGICKCORE_HAVE_STDINT_H 1
#endif

/* Define to 1 if you have the <stdio.h> header file. */
#ifndef MAGICKCORE_HAVE_STDIO_H
#define MAGICKCORE_HAVE_STDIO_H 1
#endif

/* Define to 1 if you have the <stdlib.h> header file. */
#ifndef MAGICKCORE_HAVE_STDLIB_H
#define MAGICKCORE_HAVE_STDLIB_H 1
#endif

/* Define to 1 if you have the `strcasecmp' function. */
#ifndef MAGICKCORE_HAVE_STRCASECMP
#define MAGICKCORE_HAVE_STRCASECMP 1
#endif

/* Define to 1 if you have the `strcasestr' function. */
/* #undef HAVE_STRCASESTR */

/* Define to 1 if you have the `strchr' function. */
#ifndef MAGICKCORE_HAVE_STRCHR
#define MAGICKCORE_HAVE_STRCHR 1
#endif

/* Define to 1 if you have the `strcspn' function. */
#ifndef MAGICKCORE_HAVE_STRCSPN
#define MAGICKCORE_HAVE_STRCSPN 1
#endif

/* Define to 1 if you have the `strdup' function. */
#ifndef MAGICKCORE_HAVE_STRDUP
#define MAGICKCORE_HAVE_STRDUP 1
#endif

/* Define to 1 if you have the `strerror' function. */
#ifndef MAGICKCORE_HAVE_STRERROR
#define MAGICKCORE_HAVE_STRERROR 1
#endif

/* Define if you have `strerror_r'. */
/* #undef HAVE_STRERROR_R */

/* Define to 1 if cpp supports the ANSI # stringizing operator. */
#ifndef MAGICKCORE_HAVE_STRINGIZE
#define MAGICKCORE_HAVE_STRINGIZE 1
#endif

/* Define to 1 if you have the <strings.h> header file. */
#ifndef MAGICKCORE_HAVE_STRINGS_H
#define MAGICKCORE_HAVE_STRINGS_H 1
#endif

/* Define to 1 if you have the <string.h> header file. */
#ifndef MAGICKCORE_HAVE_STRING_H
#define MAGICKCORE_HAVE_STRING_H 1
#endif

/* Define to 1 if you have the `strlcat' function. */
/* #undef HAVE_STRLCAT */

/* Define to 1 if you have the `strlcpy' function. */
/* #undef HAVE_STRLCPY */

/* Define to 1 if you have the `strncasecmp' function. */
#ifndef MAGICKCORE_HAVE_STRNCASECMP
#define MAGICKCORE_HAVE_STRNCASECMP 1
#endif

/* Define to 1 if you have the `strpbrk' function. */
#ifndef MAGICKCORE_HAVE_STRPBRK
#define MAGICKCORE_HAVE_STRPBRK 1
#endif

/* Define to 1 if you have the `strrchr' function. */
#ifndef MAGICKCORE_HAVE_STRRCHR
#define MAGICKCORE_HAVE_STRRCHR 1
#endif

/* Define to 1 if you have the `strspn' function. */
#ifndef MAGICKCORE_HAVE_STRSPN
#define MAGICKCORE_HAVE_STRSPN 1
#endif

/* Define to 1 if you have the `strstr' function. */
#ifndef MAGICKCORE_HAVE_STRSTR
#define MAGICKCORE_HAVE_STRSTR 1
#endif

/* Define to 1 if you have the `strtod' function. */
/* #undef HAVE_STRTOD */

/* Define to 1 if you have the `strtod_l' function. */
/* #undef HAVE_STRTOD_L */

/* Define to 1 if you have the `strtol' function. */
#ifndef MAGICKCORE_HAVE_STRTOL
#define MAGICKCORE_HAVE_STRTOL 1
#endif

/* Define to 1 if you have the `strtoul' function. */
#ifndef MAGICKCORE_HAVE_STRTOUL
#define MAGICKCORE_HAVE_STRTOUL 1
#endif

/* Define to 1 if `tm_zone' is a member of `struct tm'. */
/* #undef HAVE_STRUCT_TM_TM_ZONE */

/* Define to 1 if you have the <sun_prefetch.h> header file. */
/* #undef HAVE_SUN_PREFETCH_H */

/* Define to 1 if you have the `symlink' function. */
/* #undef HAVE_SYMLINK */

/* Define to 1 if you have the `sysconf' function. */
/* #undef HAVE_SYSCONF */

/* Define to 1 if you have the `system' function. */
#ifndef MAGICKCORE_HAVE_SYSTEM
#define MAGICKCORE_HAVE_SYSTEM 1
#endif

/* Define to 1 if you have the <sys/dir.h> header file, and it defines `DIR'.
   */
/* #undef HAVE_SYS_DIR_H */

/* Define to 1 if you have the <sys/ipc.h> header file. */
/* #undef HAVE_SYS_IPC_H */

/* Define to 1 if you have the <sys/mman.h> header file. */
/* #undef HAVE_SYS_MMAN_H */

/* Define to 1 if you have the <sys/ndir.h> header file, and it defines `DIR'.
   */
/* #undef HAVE_SYS_NDIR_H */

/* Define to 1 if you have the <sys/param.h> header file. */
#ifndef MAGICKCORE_HAVE_SYS_PARAM_H
#define MAGICKCORE_HAVE_SYS_PARAM_H 1
#endif

/* Define to 1 if you have the <sys/resource.h> header file. */
/* #undef HAVE_SYS_RESOURCE_H */

/* Define to 1 if you have the <sys/sendfile.h> header file. */
/* #undef HAVE_SYS_SENDFILE_H */

/* Define to 1 if you have the <sys/socket.h> header file. */
/* #undef HAVE_SYS_SOCKET_H */

/* Define to 1 if you have the <sys/stat.h> header file. */
#ifndef MAGICKCORE_HAVE_SYS_STAT_H
#define MAGICKCORE_HAVE_SYS_STAT_H 1
#endif

/* Define to 1 if you have the <sys/syslimits.h> header file. */
/* #undef HAVE_SYS_SYSLIMITS_H */

/* Define to 1 if you have the <sys/times.h> header file. */
/* #undef HAVE_SYS_TIMES_H */

/* Define to 1 if you have the <sys/time.h> header file. */
#ifndef MAGICKCORE_HAVE_SYS_TIME_H
#define MAGICKCORE_HAVE_SYS_TIME_H 1
#endif

/* Define to 1 if you have the <sys/types.h> header file. */
#ifndef MAGICKCORE_HAVE_SYS_TYPES_H
#define MAGICKCORE_HAVE_SYS_TYPES_H 1
#endif

/* Define to 1 if you have the <sys/uio.h> header file. */
/* #undef HAVE_SYS_UIO_H */

/* Define to 1 if you have the <sys/wait.h> header file. */
/* #undef HAVE_SYS_WAIT_H */

/* Define if you have the tcmalloc memory allocation library */
/* #undef HAVE_TCMALLOC */

/* Define to 1 if you have the `telldir' function. */
#ifndef MAGICKCORE_HAVE_TELLDIR
#define MAGICKCORE_HAVE_TELLDIR 1
#endif

/* Define to 1 if you have the `tempnam' function. */
#ifndef MAGICKCORE_HAVE_TEMPNAM
#define MAGICKCORE_HAVE_TEMPNAM 1
#endif

/* Define to 1 if you have the <tiffconf.h> header file. */
/* #undef HAVE_TIFFCONF_H */

/* Define to 1 if you have the `TIFFIsBigEndian' function. */
/* #undef HAVE_TIFFISBIGENDIAN */

/* Define to 1 if you have the `TIFFIsCODECConfigured' function. */
/* #undef HAVE_TIFFISCODECCONFIGURED */

/* Define to 1 if you have the `TIFFMergeFieldInfo' function. */
/* #undef HAVE_TIFFMERGEFIELDINFO */

/* Define to 1 if you have the `TIFFReadEXIFDirectory' function. */
/* #undef HAVE_TIFFREADEXIFDIRECTORY */

/* Define to 1 if you have the `TIFFReadGPSDirectory' function. */
/* #undef HAVE_TIFFREADGPSDIRECTORY */

/* Define to 1 if you have the `TIFFSetErrorHandlerExt' function. */
/* #undef HAVE_TIFFSETERRORHANDLEREXT */

/* Define to 1 if you have the `TIFFSetTagExtender' function. */
/* #undef HAVE_TIFFSETTAGEXTENDER */

/* Define to 1 if you have the `TIFFSetWarningHandlerExt' function. */
/* #undef HAVE_TIFFSETWARNINGHANDLEREXT */

/* Define to 1 if you have the `TIFFSwabArrayOfTriples' function. */
/* #undef HAVE_TIFFSWABARRAYOFTRIPLES */

/* Define to 1 if you have the `times' function. */
/* #undef HAVE_TIMES */

/* Define to 1 if your `struct tm' has `tm_zone'. Deprecated, use
   `HAVE_STRUCT_TM_TM_ZONE' instead. */
/* #undef HAVE_TM_ZONE */

/* Define to 1 if you don't have `tm_zone' but do have the external array
   `tzname'. */
#ifndef MAGICKCORE_HAVE_TZNAME
#define MAGICKCORE_HAVE_TZNAME 1
#endif

/* Define to 1 if the system has the type `uintmax_t'. */
#ifndef MAGICKCORE_HAVE_UINTMAX_T
#define MAGICKCORE_HAVE_UINTMAX_T 1
#endif

/* Define to 1 if the system has the type `uintptr_t'. */
#ifndef MAGICKCORE_HAVE_UINTPTR_T
#define MAGICKCORE_HAVE_UINTPTR_T 1
#endif

/* Define to 1 if you have the `ulltostr' function. */
/* #undef HAVE_ULLTOSTR */

/* Define if you have umem memory allocation library */
/* #undef HAVE_UMEM */

/* Define to 1 if you have the <unistd.h> header file. */
#ifndef MAGICKCORE_HAVE_UNISTD_H
#define MAGICKCORE_HAVE_UNISTD_H 1
#endif

/* Define to 1 if the system has the type `unsigned long long int'. */
#ifndef MAGICKCORE_HAVE_UNSIGNED_LONG_LONG_INT
#define MAGICKCORE_HAVE_UNSIGNED_LONG_LONG_INT 1
#endif

/* Define to 1 if you have the `uselocale' function. */
/* #undef HAVE_USELOCALE */

/* Define to 1 if you have the `usleep' function. */
#ifndef MAGICKCORE_HAVE_USLEEP
#define MAGICKCORE_HAVE_USLEEP 1
#endif

/* Define to 1 if you have the `utime' function. */
#ifndef MAGICKCORE_HAVE_UTIME
#define MAGICKCORE_HAVE_UTIME 1
#endif

/* Define to 1 if you have the <utime.h> header file. */
#ifndef MAGICKCORE_HAVE_UTIME_H
#define MAGICKCORE_HAVE_UTIME_H 1
#endif

/* Define to 1 if you have the `vfprintf' function. */
#ifndef MAGICKCORE_HAVE_VFPRINTF
#define MAGICKCORE_HAVE_VFPRINTF 1
#endif

/* Define to 1 if you have the `vfprintf_l' function. */
/* #undef HAVE_VFPRINTF_L */

/* Define to 1 if you have the `vsnprintf' function. */
#ifndef MAGICKCORE_HAVE_VSNPRINTF
#define MAGICKCORE_HAVE_VSNPRINTF 1
#endif

/* Define to 1 if you have the `vsnprintf_l' function. */
/* #undef HAVE_VSNPRINTF_L */

/* Define to 1 if you have the `vsprintf' function. */
#ifndef MAGICKCORE_HAVE_VSPRINTF
#define MAGICKCORE_HAVE_VSPRINTF 1
#endif

/* Define to 1 if you have the `waitpid' function. */
/* #undef HAVE_WAITPID */

/* Define to 1 if you have the <wchar.h> header file. */
#ifndef MAGICKCORE_HAVE_WCHAR_H
#define MAGICKCORE_HAVE_WCHAR_H 1
#endif

/* Define to 1 if you have the <xlocale.h> header file. */
/* #undef HAVE_XLOCALE_H */

/* Define to 1 if you have the `_aligned_malloc' function. */
#ifndef MAGICKCORE_HAVE__ALIGNED_MALLOC
#define MAGICKCORE_HAVE__ALIGNED_MALLOC 1
#endif

/* Define to 1 if the system has the type `_Bool'. */
#ifndef MAGICKCORE_HAVE__BOOL
#define MAGICKCORE_HAVE__BOOL 1
#endif

/* Define to 1 if you have the `_exit' function. */
#ifndef MAGICKCORE_HAVE__EXIT
#define MAGICKCORE_HAVE__EXIT 1
#endif

/* Define to 1 if you have the `_NSGetExecutablePath' function. */
/* #undef HAVE__NSGETEXECUTABLEPATH */

/* Define to 1 if you have the `_pclose' function. */
#ifndef MAGICKCORE_HAVE__PCLOSE
#define MAGICKCORE_HAVE__PCLOSE 1
#endif

/* Define to 1 if you have the `_popen' function. */
#ifndef MAGICKCORE_HAVE__POPEN
#define MAGICKCORE_HAVE__POPEN 1
#endif

/* Define to 1 if you have the `_wfopen' function. */
#ifndef MAGICKCORE_HAVE__WFOPEN
#define MAGICKCORE_HAVE__WFOPEN 1
#endif

/* Define to 1 if you have the `_wstat' function. */
/* #undef HAVE__WSTAT */

/* define if your compiler has __attribute__ */
#ifndef MAGICKCORE_HAVE___ATTRIBUTE__
#define MAGICKCORE_HAVE___ATTRIBUTE__ 1
#endif

/* Whether hdri is enabled or not */
#ifndef MAGICKCORE_HDRI_ENABLE_OBSOLETE_IN_H
#define MAGICKCORE_HDRI_ENABLE_OBSOLETE_IN_H 0
#endif

/* Define if you have libheif library */
/* #undef HEIC_DELEGATE */

/* Directory where ImageMagick architecture headers live. */
#ifndef MAGICKCORE_INCLUDEARCH_PATH
#define MAGICKCORE_INCLUDEARCH_PATH "/data/mxe/usr/x86_64-w64-mingw32.shared.posix.all/include/ImageMagick-6/"
#endif

/* Directory where ImageMagick headers live. */
#ifndef MAGICKCORE_INCLUDE_PATH
#define MAGICKCORE_INCLUDE_PATH "/data/mxe/usr/x86_64-w64-mingw32.shared.posix.all/include/ImageMagick-6/"
#endif

/* ImageMagick is formally installed under prefix */
#ifndef MAGICKCORE_INSTALLED_SUPPORT
#define MAGICKCORE_INSTALLED_SUPPORT 1
#endif

/* Define if you have JBIG library */
/* #undef JBIG_DELEGATE */

/* Define if you have JPEG library */
#ifndef MAGICKCORE_JPEG_DELEGATE
#define MAGICKCORE_JPEG_DELEGATE 1
#endif

/* Define if you have LCMS library */
#ifndef MAGICKCORE_LCMS_DELEGATE
#define MAGICKCORE_LCMS_DELEGATE 1
#endif

/* Define if you have OPENJP2 library */
#ifndef MAGICKCORE_LIBOPENJP2_DELEGATE
#define MAGICKCORE_LIBOPENJP2_DELEGATE 1
#endif

/* Directory where architecture-dependent files live. */
#ifndef MAGICKCORE_LIBRARY_PATH
#define MAGICKCORE_LIBRARY_PATH "/data/mxe/usr/x86_64-w64-mingw32.shared.posix.all/lib/ImageMagick-6.9.13/"
#endif

/* Subdirectory of lib where ImageMagick architecture dependent files are
   installed. */
#ifndef MAGICKCORE_LIBRARY_RELATIVE_PATH
#define MAGICKCORE_LIBRARY_RELATIVE_PATH "ImageMagick-6.9.13"
#endif

/* Binaries in libraries path base name (will be during install linked to bin)
   */
#ifndef MAGICKCORE_LIB_BIN_BASEDIRNAME
#define MAGICKCORE_LIB_BIN_BASEDIRNAME "bin"
#endif

/* Define if you have LQR library */
/* #undef LQR_DELEGATE */

/* Define if using libltdl to support dynamically loadable modules and OpenCL
   */
/* #undef LTDL_DELEGATE */

/* Native module suffix */
/* #undef LTDL_MODULE_EXT */

/* Define to the sub-directory where libtool stores uninstalled libraries. */
#ifndef MAGICKCORE_LT_OBJDIR
#define MAGICKCORE_LT_OBJDIR ".libs/"
#endif

/* Define if you have LZMA library */
/* #undef LZMA_DELEGATE */

/* Define to prepend to default font search path. */
/* #undef MAGICK_FONT_PATH */

/* Target Host CPU */
#ifndef MAGICKCORE_MAGICK_TARGET_CPU
#define MAGICKCORE_MAGICK_TARGET_CPU x86_64
#endif

/* Target Host OS */
#ifndef MAGICKCORE_MAGICK_TARGET_OS
#define MAGICKCORE_MAGICK_TARGET_OS mingw32.shared.posix.all
#endif

/* Target Host Vendor */
#ifndef MAGICKCORE_MAGICK_TARGET_VENDOR
#define MAGICKCORE_MAGICK_TARGET_VENDOR w64
#endif

/* Module directory name without ABI part. */
#ifndef MAGICKCORE_MODULES_BASEDIRNAME
#define MAGICKCORE_MODULES_BASEDIRNAME "modules"
#endif

/* Module directory dirname */
/* #undef MODULES_DIRNAME */

/* Magick API method prefix */
/* #undef NAMESPACE_PREFIX */

/* Magick API method prefix tag */
/* #undef NAMESPACE_PREFIX_TAG */

/* Define to 1 if assertions should be disabled. */
/* #undef NDEBUG */

/* Define if you have OPENEXR library */
/* #undef OPENEXR_DELEGATE */

/* Define to the address where bug reports for this package should be sent. */
#ifndef MAGICKCORE_PACKAGE_BUGREPORT
#define MAGICKCORE_PACKAGE_BUGREPORT "https://github.com/ImageMagick/ImageMagick6/issues"
#endif

/* Define to the full name of this package. */
#ifndef MAGICKCORE_PACKAGE_NAME
#define MAGICKCORE_PACKAGE_NAME "ImageMagick"
#endif

/* Define to the full name and version of this package. */
#ifndef MAGICKCORE_PACKAGE_STRING
#define MAGICKCORE_PACKAGE_STRING "ImageMagick 6.9.13-7"
#endif

/* Define to the one symbol short name of this package. */
#ifndef MAGICKCORE_PACKAGE_TARNAME
#define MAGICKCORE_PACKAGE_TARNAME "ImageMagick"
#endif

/* Define to the home page for this package. */
#ifndef MAGICKCORE_PACKAGE_URL
#define MAGICKCORE_PACKAGE_URL "https://legacy.imagemagick.org"
#endif

/* Define to the version of this package. */
#ifndef MAGICKCORE_PACKAGE_VERSION
#define MAGICKCORE_PACKAGE_VERSION "6.9.13-7"
#endif

/* Define if you have PANGOCAIRO library */
/* #undef PANGOCAIRO_DELEGATE */

/* Define if you have PANGO library */
/* #undef PANGO_DELEGATE */

/* enable pipes (|) in filenames */
/* #undef PIPES_SUPPORT */

/* Define if you have PNG library */
/* #undef PNG_DELEGATE */

/* Define to necessary symbol if this constant uses a non-standard name on
   your system. */
/* #undef PTHREAD_CREATE_JOINABLE */

/* Pixel cache memory threshold (defaults to available memory) */
/* #undef PixelCacheThreshold */

/* Number of bits in a pixel Quantum (8/16/32/64) */
#ifndef MAGICKCORE_QUANTUM_DEPTH_OBSOLETE_IN_H
#define MAGICKCORE_QUANTUM_DEPTH_OBSOLETE_IN_H 16
#endif

/* Define if you have RAQM library */
/* #undef RAQM_DELEGATE */

/* Define if you have LIBRAW library */
/* #undef RAW_R_DELEGATE */

/* Define if you have RSVG library */
/* #undef RSVG_DELEGATE */

/* Setjmp/longjmp are thread safe */
#ifndef MAGICKCORE_SETJMP_IS_THREAD_SAFE
#define MAGICKCORE_SETJMP_IS_THREAD_SAFE 1
#endif

/* Sharearch directory name without ABI part. */
#ifndef MAGICKCORE_SHAREARCH_BASEDIRNAME
#define MAGICKCORE_SHAREARCH_BASEDIRNAME "config"
#endif

/* Sharearch directory dirname */
/* #undef SHAREARCH_DIRNAME */

/* Directory where architecture-independent configuration files live. */
#ifndef MAGICKCORE_SHARE_PATH
#define MAGICKCORE_SHARE_PATH "/data/mxe/usr/x86_64-w64-mingw32.shared.posix.all/share/ImageMagick-6/"
#endif

/* Subdirectory of lib where architecture-independent configuration files
   live. */
#ifndef MAGICKCORE_SHARE_RELATIVE_PATH
#define MAGICKCORE_SHARE_RELATIVE_PATH "ImageMagick-6"
#endif

/* The size of `double', as computed by sizeof. */
#ifndef MAGICKCORE_SIZEOF_DOUBLE
#define MAGICKCORE_SIZEOF_DOUBLE 8
#endif

/* The size of `double_t', as computed by sizeof. */
#ifndef MAGICKCORE_SIZEOF_DOUBLE_T
#define MAGICKCORE_SIZEOF_DOUBLE_T 8
#endif

/* The size of `float', as computed by sizeof. */
#ifndef MAGICKCORE_SIZEOF_FLOAT
#define MAGICKCORE_SIZEOF_FLOAT 4
#endif

/* The size of `float_t', as computed by sizeof. */
#ifndef MAGICKCORE_SIZEOF_FLOAT_T
#define MAGICKCORE_SIZEOF_FLOAT_T 4
#endif

/* The size of `long double', as computed by sizeof. */
#ifndef MAGICKCORE_SIZEOF_LONG_DOUBLE
#define MAGICKCORE_SIZEOF_LONG_DOUBLE 16
#endif

/* The size of `size_t', as computed by sizeof. */
#ifndef MAGICKCORE_SIZEOF_SIZE_T
#define MAGICKCORE_SIZEOF_SIZE_T 8
#endif

/* The size of `unsigned long long', as computed by sizeof. */
#ifndef MAGICKCORE_SIZEOF_UNSIGNED_LONG_LONG
#define MAGICKCORE_SIZEOF_UNSIGNED_LONG_LONG 8
#endif

/* The size of `void *', as computed by sizeof. */
#ifndef MAGICKCORE_SIZEOF_VOID_P
#define MAGICKCORE_SIZEOF_VOID_P 8
#endif

/* Define to 1 if the `S_IS*' macros in <sys/stat.h> do not work properly. */
/* #undef STAT_MACROS_BROKEN */

/* Define to 1 if all of the C90 standard headers exist (not just the ones
   required in a freestanding environment). This macro is provided for
   backward compatibility; new code need not use it. */
#ifndef MAGICKCORE_STDC_HEADERS
#define MAGICKCORE_STDC_HEADERS 1
#endif

/* Define to 1 if strerror_r returns char *. */
/* #undef STRERROR_R_CHAR_P */

/* Define if you have POSIX threads libraries and header files. */
/* #undef THREAD_SUPPORT */

/* Define if you have TIFF library */
/* #undef TIFF_DELEGATE */

/* Define to 1 if your <sys/time.h> declares `struct tm'. */
/* #undef TM_IN_SYS_TIME */

/* Enable extensions on AIX 3, Interix.  */
#ifndef _ALL_SOURCE
# define _ALL_SOURCE 1
#endif
/* Enable general extensions on macOS.  */
#ifndef _DARWIN_C_SOURCE
# define _DARWIN_C_SOURCE 1
#endif
/* Enable general extensions on Solaris.  */
#ifndef __EXTENSIONS__
# define __EXTENSIONS__ 1
#endif
/* Enable GNU extensions on systems that have them.  */
#ifndef _GNU_SOURCE
# define _GNU_SOURCE 1
#endif
/* Enable X/Open compliant socket functions that do not require linking
   with -lxnet on HP-UX 11.11.  */
#ifndef _HPUX_ALT_XOPEN_SOCKET_API
# define _HPUX_ALT_XOPEN_SOCKET_API 1
#endif
/* Identify the host operating system as Minix.
   This macro does not affect the system headers' behavior.
   A future release of Autoconf may stop defining this macro.  */
#ifndef _MINIX
/* # undef _MINIX */
#endif
/* Enable general extensions on NetBSD.
   Enable NetBSD compatibility extensions on Minix.  */
#ifndef _NETBSD_SOURCE
# define _NETBSD_SOURCE 1
#endif
/* Enable OpenBSD compatibility extensions on NetBSD.
   Oddly enough, this does nothing on OpenBSD.  */
#ifndef _OPENBSD_SOURCE
# define _OPENBSD_SOURCE 1
#endif
/* Define to 1 if needed for POSIX-compatible behavior.  */
#ifndef _POSIX_SOURCE
/* # undef _POSIX_SOURCE */
#endif
/* Define to 2 if needed for POSIX-compatible behavior.  */
#ifndef _POSIX_1_SOURCE
/* # undef _POSIX_1_SOURCE */
#endif
/* Enable POSIX-compatible threading on Solaris.  */
#ifndef _POSIX_PTHREAD_SEMANTICS
# define _POSIX_PTHREAD_SEMANTICS 1
#endif
/* Enable extensions specified by ISO/IEC TS 18661-5:2014.  */
#ifndef __STDC_WANT_IEC_60559_ATTRIBS_EXT__
# define __STDC_WANT_IEC_60559_ATTRIBS_EXT__ 1
#endif
/* Enable extensions specified by ISO/IEC TS 18661-1:2014.  */
#ifndef __STDC_WANT_IEC_60559_BFP_EXT__
# define __STDC_WANT_IEC_60559_BFP_EXT__ 1
#endif
/* Enable extensions specified by ISO/IEC TS 18661-2:2015.  */
#ifndef __STDC_WANT_IEC_60559_DFP_EXT__
# define __STDC_WANT_IEC_60559_DFP_EXT__ 1
#endif
/* Enable extensions specified by ISO/IEC TS 18661-4:2015.  */
#ifndef __STDC_WANT_IEC_60559_FUNCS_EXT__
# define __STDC_WANT_IEC_60559_FUNCS_EXT__ 1
#endif
/* Enable extensions specified by ISO/IEC TS 18661-3:2015.  */
#ifndef __STDC_WANT_IEC_60559_TYPES_EXT__
# define __STDC_WANT_IEC_60559_TYPES_EXT__ 1
#endif
/* Enable extensions specified by ISO/IEC TR 24731-2:2010.  */
#ifndef __STDC_WANT_LIB_EXT2__
# define __STDC_WANT_LIB_EXT2__ 1
#endif
/* Enable extensions specified by ISO/IEC 24747:2009.  */
#ifndef __STDC_WANT_MATH_SPEC_FUNCS__
# define __STDC_WANT_MATH_SPEC_FUNCS__ 1
#endif
/* Enable extensions on HP NonStop.  */
#ifndef _TANDEM_SOURCE
# define _TANDEM_SOURCE 1
#endif
/* Enable X/Open extensions.  Define to 500 only if necessary
   to make mbstate_t available.  */
#ifndef _XOPEN_SOURCE
/* # undef _XOPEN_SOURCE */
#endif


/* Define if you have WEBPMUX library */
/* #undef WEBPMUX_DELEGATE */

/* Define if you have WEBP library */
/* #undef WEBP_DELEGATE */

/* Define to use the Windows GDI32 library */
/* #undef WINGDI32_DELEGATE */

/* Define if using the dmalloc debugging malloc package */
/* #undef WITH_DMALLOC */

/* Define if you have WMF library */
/* #undef WMF_DELEGATE */

/* Define WORDS_BIGENDIAN to 1 if your processor stores words with the most
   significant byte first (like Motorola and SPARC, unlike Intel). */
#if defined AC_APPLE_UNIVERSAL_BUILD
# if defined __BIG_ENDIAN__
#  define WORDS_BIGENDIAN 1
# endif
#else
# ifndef WORDS_BIGENDIAN
/* #  undef WORDS_BIGENDIAN */
# endif
#endif

/* Location of X11 configure files */
#ifndef MAGICKCORE_X11_CONFIGURE_PATH
#define MAGICKCORE_X11_CONFIGURE_PATH ""
#endif

/* Define if you have X11 library */
/* #undef X11_DELEGATE */

/* Define if you have XML library */
#ifndef MAGICKCORE_XML_DELEGATE
#define MAGICKCORE_XML_DELEGATE 1
#endif

/* Define to 1 if the X Window System is missing or not being used. */
#ifndef MAGICKCORE_X_DISPLAY_MISSING
#define MAGICKCORE_X_DISPLAY_MISSING 1
#endif

/* Build self-contained, embeddable, zero-configuration ImageMagick */
/* #undef ZERO_CONFIGURATION_SUPPORT */

/* Define if you have ZLIB library */
/* #undef ZLIB_DELEGATE */

/* Define if you have ZSTD library */
/* #undef ZSTD_DELEGATE */

/* Number of bits in a file offset, on hosts where this is settable. */
/* #undef _FILE_OFFSET_BITS */

/* enable run-time bounds-checking */
/* #undef _FORTIFY_SOURCE */

/* Define to 1 to make fseeko visible on some hosts (e.g. glibc 2.2). */
/* #undef _LARGEFILE_SOURCE */

/* Define for large files, on AIX-style hosts. */
/* #undef _LARGE_FILES */

/* Define for Solaris 2.5.1 so the uint32_t typedef from <sys/synch.h>,
   <pthread.h>, or <semaphore.h> is not used. If the typedef were allowed, the
   #define below would cause a syntax error. */
/* #undef _UINT32_T */

/* Define for Solaris 2.5.1 so the uint64_t typedef from <sys/synch.h>,
   <pthread.h>, or <semaphore.h> is not used. If the typedef were allowed, the
   #define below would cause a syntax error. */
/* #undef _UINT64_T */

/* Define for Solaris 2.5.1 so the uint8_t typedef from <sys/synch.h>,
   <pthread.h>, or <semaphore.h> is not used. If the typedef were allowed, the
   #define below would cause a syntax error. */
/* #undef _UINT8_T */

/* Define to 1 if type `char' is unsigned and your compiler does not
   predefine this macro.  */
#ifndef __CHAR_UNSIGNED__
/* # undef __CHAR_UNSIGNED__ */
#endif

/* Define to appropriate substitute if compiler does not have __func__ */
/* #undef __func__ */

/* Define to empty if `const' does not conform to ANSI C. */
/* #undef const */

/* Define to `int' if <sys/types.h> doesn't define. */
#ifndef _magickcore_gid_t
#define _magickcore_gid_t int
#endif

/* Define to `__inline__' or `__inline' if that's what the C compiler
   calls it, or to nothing if 'inline' is not supported under any name.  */
#ifndef __cplusplus
/* #undef inline */
#endif

/* Define to the type of a signed integer type of width exactly 16 bits if
   such a type exists and the standard includes do not define it. */
/* #undef int16_t */

/* Define to the type of a signed integer type of width exactly 32 bits if
   such a type exists and the standard includes do not define it. */
/* #undef int32_t */

/* Define to the type of a signed integer type of width exactly 64 bits if
   such a type exists and the standard includes do not define it. */
/* #undef int64_t */

/* Define to the type of a signed integer type of width exactly 8 bits if such
   a type exists and the standard includes do not define it. */
/* #undef int8_t */

/* Define to the widest signed integer type if <stdint.h> and <inttypes.h> do
   not define. */
/* #undef intmax_t */

/* Define to the type of a signed integer type wide enough to hold a pointer,
   if such a type exists, and if the system does not define it. */
/* #undef intptr_t */

/* Define to a type if <wchar.h> does not define. */
/* #undef mbstate_t */

/* Define to `int' if <sys/types.h> does not define. */
/* #undef mode_t */

/* Define to `long int' if <sys/types.h> does not define. */
/* #undef off_t */

/* Define as a signed integer type capable of holding a process identifier. */
/* #undef pid_t */

/* Define to the equivalent of the C99 'restrict' keyword, or to
   nothing if this is not supported.  Do not define if restrict is
   supported only directly.  */
#ifndef _magickcore_restrict
#define _magickcore_restrict __restrict__
#endif
/* Work around a bug in older versions of Sun C++, which did not
   #define __restrict__ or support _Restrict or __restrict__
   even though the corresponding Sun C compiler ended up with
   "#define restrict _Restrict" or "#define restrict __restrict__"
   in the previous line.  This workaround can be removed once
   we assume Oracle Developer Studio 12.5 (2016) or later.  */
#if defined __SUNPRO_CC && !defined __RESTRICT && !defined __restrict__
# define _Restrict
# define __restrict__
#endif

/* Define to `unsigned int' if <sys/types.h> does not define. */
/* #undef size_t */

/* Define to `int' if <sys/types.h> does not define. */
/* #undef ssize_t */

/* Define to `int' if <sys/types.h> doesn't define. */
#ifndef _magickcore_uid_t
#define _magickcore_uid_t int
#endif

/* Define to the type of an unsigned integer type of width exactly 16 bits if
   such a type exists and the standard includes do not define it. */
/* #undef uint16_t */

/* Define to the type of an unsigned integer type of width exactly 32 bits if
   such a type exists and the standard includes do not define it. */
/* #undef uint32_t */

/* Define to the type of an unsigned integer type of width exactly 64 bits if
   such a type exists and the standard includes do not define it. */
/* #undef uint64_t */

/* Define to the type of an unsigned integer type of width exactly 8 bits if
   such a type exists and the standard includes do not define it. */
/* #undef uint8_t */

/* Define to the widest unsigned integer type if <stdint.h> and <inttypes.h>
   do not define. */
/* #undef uintmax_t */

/* Define to the type of an unsigned integer type wide enough to hold a
   pointer, if such a type exists, and if the system does not define it. */
/* #undef uintptr_t */

/* Define to empty if the keyword `volatile' does not work. Warning: valid
   code using `volatile' can become incorrect without. Disable with care. */
/* #undef volatile */
 
/* once: _MAGICK_MAGICK_BASECONFIG_H */
#endif
