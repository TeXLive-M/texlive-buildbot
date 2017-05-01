# Buildbot for TeX Live binaries

This is a buildbot setup that's intended to build TeX Live binaries for various platforms.

* [http://build.contextgarden.net](http://build.contextgarden.net/waterfall)

### Binaries

The list of desired builds includes:

- [x] Full TeX Live tree ([sources](http://tug.org/svn/texlive/trunk/Build/source/))
- [ ] LuaTeX
- [ ] XeTeX
- [ ] Asymptote, including:
  * FFTW (fast Fourier transform library)
  * GSL (GNU Scientific Library)
  * GNU Readline
- [ ] xindy, including:
  * `libffcall`
  * `libsigsegv`
  * `clisp`
- [ ] Biber
- [x] `xz`
- [x] `wget`
- [ ] `gpg`

### Platforms

The desired list of target platforms:
- [x] Mac OS X 10.6
  * `powerpc` (cross-compiled for 10.5)
  * `i386` (cross-compiled for 10.5)
  * `x86_64`
- [x] Solaris 10
  * `sparc`
  * `i386`
  * `x86_64`
- [x] GNU/Linux arm – Raspbian on Raspberry PI
- [x] GNU/Linux Debian 7 & 9
  * `i386`
  * `x86_64`
- [ ] FreeBSD 9 & 11
  * `i386`
  * `amd64`
- [ ] NetBSD
- [x] OpenBSD 6.0 & 6.1
  * `i386`
  * `amd64`
- [ ] MinGW-w64 cross-compiler
  * `win32`
  * `win64`

A separate setup is needed in cases where C++11 is not supported.

### Credits and Special thanks

* Mark and Johnny from [Jožef Stefan Institute](https://www.ijs.si/ijsw/V001/JSI) for providing the main server
* Hans Hagen at [Pragma ADE](http://www.pragma-ade.com/) for providing the VM infrastructure
* Dagobert Michelsen from the [OpenCSW](https://www.opencsw.org/) project for providing access to Solaris machines
* Norbert Preining, Karl Berry, Akira Kakuto and the rest of the TeX Live team

### Contact

This has been set up by Mojca Miklavec with help of Alan Braslau.
Feel free to ask questions on the TeX Live mailing list.
