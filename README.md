# Buildbot for TeX Live binaries

This is a buildbot setup that's intended to build TeX Live binaries for various platforms.

* [http://build.contextgarden.net](http://build.contextgarden.net/waterfall)

### Binaries

The list of desired builds includes:
* Full TeX Live tree ([sources](http://tug.org/svn/texlive/trunk/Build/source/))
* LuaTeX
* XeTeX
* Asymptote, including:
  * FFTW (fast Fourier transform library)
  * GSL (GNU Scientific Library)
  * GNU Readline
* xindy, including:
  * `libffcall`
  * `libsigsegv`
  * `clisp`
* `wget`
* `xz`
* `gpg`

### Platforms

The desired list of target platforms:
* Mac OS X 10.6
  * `x86_64`
  * `i386` (cross-compiled for 10.5)
  * `powerpc` (cross-compiled for 10.5)
  * perhaps a separate setup with support for C++11
* Solaris 10
  * `x86_64`
  * `i386`
  * `sparc`
* Linux Arm / Raspbian on Raspberry PI
* Linux (not sure which version)
  * `x86_64`
  * `i386`
* FreeBSD
* NetBSD
* OpenBSD
* MinGW-w64 cross-compiler
  * `x86_64`
  * `i386`

### Credits and Special thanks

* Mark and Johnny from [Jožef Stefan Institute](https://www.ijs.si/ijsw/V001/JSI) for providing the main server
* Hans Hagen at [Pragma ADE](http://www.pragma-ade.com/) for providing the VM infrastructure
* Dagobert Michelsen from the [OpenCSW](https://www.opencsw.org/) project for providing access to Solaris machines
* Alan Braslau for help with VMs
* Norbert Preining, Karl Berry, Akira Kakuto and the rest of the TeX Live team

### Contact

This has been set up by Mojca Miklavec.
Feel free to ask questions on the TeX Live mailing list.
