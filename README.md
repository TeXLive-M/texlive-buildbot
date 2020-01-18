# Buildbot for TeX Live binaries

This is a buildbot setup that's intended to build TeX Live binaries for various platforms.

* [https://build.contextgarden.net/](https://build.contextgarden.net/#/grid)

### Binaries

The binaries currently being compiled include:
- Full TeX Live tree ([sources](http://tug.org/svn/texlive/trunk/Build/source/))
- LuaTeX
- LuaMetaTeX
- pplib

The list of other build candidates includes:

- Asymptote, including:
  * FFTW (fast Fourier transform library)
  * GSL (GNU Scientific Library)
  * GNU Readline
- xindy, including:
  * `libffcall`
  * `libsigsegv`
  * `clisp`
- Biber
- `xz`
- `wget`
- `gpg`

### Platforms

The binaries are being built on:
- Mac OS X 10.6 (`x86_64`)
- Solaris 10 (`sparc`, `i386`, `x86_64`)
- GNU/Linux (`arm`) – Raspbian on Raspberry PI 4
- GNU/Linux Debian 8 & 9 (`i386`, `x86_64`)
- GNU/Linux Alpine with musl (`x86_64`)
- FreeBSD 12.1
- OpenBSD 6.5 & 6.6 (`i386`, `amd64`)
- MinGW-w64 cross-compiler (`win32`, `win64`)

It might be nice to also include:
- NetBSD
- GNU/Linux (`arm64`)

### Credits and Special thanks

* Mark and Johnny from [Jožef Stefan Institute](https://www.ijs.si/ijsw/V001/JSI) for providing the main server
* Hans Hagen at [Pragma ADE](http://www.pragma-ade.com/) for providing the VM infrastructure
* Dagobert Michelsen from the [OpenCSW](https://www.opencsw.org/) project for providing access to Solaris machines
* Norbert Preining, Karl Berry, Akira Kakuto and the rest of the TeX Live team

### Contact

This has been set up by Mojca Miklavec with help of Alan Braslau.
Feel free to ask questions on the TeX Live mailing list.
