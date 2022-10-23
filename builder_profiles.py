#!/usr/bin/env python
#
# Builder profile:
# - platform (os)
# - environmental variables (like compiler)
# - make and tar command to be used
# - is it capable of building C++11 code?
class BuilderProfile(object):
    def __init__(self, platform, env = {}, cmake_defs = {}, cmd_make = 'make', cmd_tar = 'tar', cmake_generator = 'Ninja'):
        self.platform        = platform
        self.env             = env
        self.cmake_defs      = cmake_defs
        self.cmd_make        = cmd_make
        self.cmd_tar         = cmd_tar
        self.cmake_generator = cmake_generator

# Builder:
# - worker name
# - code (to distinguish locations of builders)
# - builder profile
# - name of the builder
# - architecture of the builder
# - official tl name
# - should we upload binaries?
class BuildWorker(object):
    def __init__(self, worker, code, profile, name, arch, tlname, upload = False):
        self.worker   = worker
        self.code     = code
        self.profile  = profile
        self.name     = name
        self.arch     = arch
        self.tlname   = tlname
        self.upload   = upload

        self.platform        = profile.platform
        self.env             = profile.env
        self.cmake_defs      = profile.cmake_defs
        self.cmd_make        = profile.cmd_make
        self.cmd_tar         = profile.cmd_tar
        self.cmake_generator = profile.cmake_generator

        self.build = {}
        self.build['luametatex'] = True
        self.build['pplib']      = (self.platform in ['darwin', 'freebsd', 'openbsd', 'linux'])
        self.build['luatex']     = not ((self.platform in ['windows']) or (self.arch in ['sparc']))
        self.build['texlive']    = not  (self.platform in ['mingw', 'windows'])

env_darwin10 = {}
for arch in ['x86_64']:
    env_darwin10[arch] = {}

    cc     = '/opt/local/bin/clang-mp-11'
    cxx    = '/opt/local/bin/clang++-mp-11 -stdlib=libc++'
    target = '10.6'
    sdk    = '10.6' # '10.7'

    libdir  = '-L/Developer/SDKs/MacOSX{}.sdk/usr/lib'.format(sdk)
    sysroot = '-isysroot /Developer/SDKs/MacOSX{}.sdk -mmacosx-version-min={}'.format(sdk, target)
    ldflags = libdir + ' ' + sysroot

    env_darwin10[arch]['CC']     = '{} -arch {}'.format(cc,  arch)
    env_darwin10[arch]['OBJC']   = '{} -arch {}'.format(cc,  arch)
    env_darwin10[arch]['CXX']    = '{} -arch {}'.format(cxx, arch)
    env_darwin10[arch]['OBJCXX'] = '{} -arch {}'.format(cxx, arch)

    for flags in ['CFLAGS', 'OBJCFLAGS', 'CXXFLAGS', 'OBJCXXFLAGS']:
        env_darwin10[arch][flags] = '-Os {}'.format(sysroot)
    env_darwin10[arch]['LDFLAGS'] = '-Os {}'.format(ldflags)

    env_darwin10[arch]['STRIP'] = 'strip -u -r'
    env_darwin10[arch]['PYTHON'] = '/opt/local/bin/python3.10'

env_solaris10 = {
    'CC'      : '/opt/csw/bin/gcc-5.5',
    'CXX'     : '/opt/csw/bin/g++-5.5',
    'PATH'    : [ '${PATH}', '/usr/ccs/bin'],
#   'GREP'    : 'ggrep',
}
env_solaris10_64 = {
    'CC'      : '/opt/csw/bin/gcc-5.5 -m64',
    'CXX'     : '/opt/csw/bin/g++-5.5 -m64',
    'PATH'    : [ '${PATH}', '/usr/ccs/bin'],
#   'GREP'    : 'ggrep',
}
env_openbsd = {
    'CC'      : 'clang',
    'CXX'     : 'clang++',
}

env_freebsd = {}
env_linux = {}
env_linux_clang = {
    'CC'      : 'clang',
    'CXX'     : 'clang++',
}
env_darwin = {}
env_mingw = {}
env_mingw['any'] = {}
cmake_defs = {}
for arch in ['32', '64']:
    if arch == '32':
        name = 'i686-w64-mingw32'
    else:
        name = 'x86_64-w64-mingw32'

    env_mingw[arch] = {
        'CFLAGS'   : '-mtune=nocona -g -O3 -fno-lto -fno-use-linker-plugin ${CFLAGS}',
        'CXXFLAGS' : '-mtune=nocona -g -O3 -fno-lto -fno-use-linker-plugin ${CXXFLAGS}',
        'LDFLAGS'  : '${LDFLAGS} -fno-lto -fno-use-linker-plugin -static-libgcc -static-libstdc++',
        'RANLIB'   : '{}-ranlib'.format(name),
        'STRIP'    : '{}-strip'.format(name),
    }
    cmake_defs['mingw{}'.format(arch)] = {
        'CMAKE_TOOLCHAIN_FILE' : './cmake/mingw-{}.cmake'.format(arch)
    }

cmake_defs['win-msvc64'] = {}
cmake_defs['win-msvc32'] = { 'CMAKE_GENERATOR_PLATFORM' : 'Win32'   }
cmake_defs['win-arm64']  = { 'CMAKE_GENERATOR_PLATFORM' : 'ARM64'   }
cmake_defs['win-clang']  = { 'CMAKE_GENERATOR_TOOLSET'  : 'ClangCL' }

builder_profiles = {
    'solaris10-sparc'  : BuilderProfile(platform = 'solaris', env = env_solaris10,          cmd_make = 'gmake', cmd_tar = 'gtar', cmake_generator = 'Unix Makefiles'),
    'solaris10-i386'   : BuilderProfile(platform = 'solaris', env = env_solaris10,          cmd_make = 'gmake', cmd_tar = 'gtar', cmake_generator = 'Unix Makefiles'),
    'solaris10-x86_64' : BuilderProfile(platform = 'solaris', env = env_solaris10_64,       cmd_make = 'gmake', cmd_tar = 'gtar', cmake_generator = 'Unix Makefiles'),
    'freebsd'          : BuilderProfile(platform = 'freebsd', env = env_freebsd,            cmd_make = 'gmake', cmd_tar = 'gtar'),
    'openbsd'          : BuilderProfile(platform = 'openbsd', env = env_openbsd,            cmd_make = 'gmake', cmd_tar = 'gtar'),
    'linux'            : BuilderProfile(platform = 'linux',   env = env_linux,              cmd_make = 'make',  cmd_tar = 'tar'),
    'linux-clang'      : BuilderProfile(platform = 'linux',   env = env_linux_clang,        cmd_make = 'make',  cmd_tar = 'tar'),
    'darwin10-x86_64'  : BuilderProfile(platform = 'darwin',  env = env_darwin10['x86_64'], cmd_make = 'make',  cmd_tar = 'gnutar'),
    'darwin'           : BuilderProfile(platform = 'darwin',  env = env_darwin,             cmd_make = 'make',  cmd_tar = 'gnutar'),
    'linux-mingw32'    : BuilderProfile(platform = 'mingw',   env = env_mingw['32']),
    'linux-mingw64'    : BuilderProfile(platform = 'mingw',   env = env_mingw['64']),
    'mingw-cross32'    : BuilderProfile(platform = 'mingw',   env = env_mingw['any'],                    cmake_defs = cmake_defs['mingw32']),
    'mingw-cross64'    : BuilderProfile(platform = 'mingw',   env = env_mingw['any'],                    cmake_defs = cmake_defs['mingw64']),
    'windows-msvc32'   : BuilderProfile(platform = 'windows', cmake_generator = 'Visual Studio 16 2019', cmake_defs = cmake_defs['win-msvc32']),
    'windows-msvc64'   : BuilderProfile(platform = 'windows', cmake_generator = 'Visual Studio 16 2019', cmake_defs = cmake_defs['win-msvc64']),
    'windows-clang'    : BuilderProfile(platform = 'windows', cmake_generator = 'Visual Studio 16 2019', cmake_defs = cmake_defs['win-clang']),
    'windows-arm64'    : BuilderProfile(platform = 'windows', cmake_generator = 'Visual Studio 16 2019', cmake_defs = cmake_defs['win-arm64']),
}

# worker:  name of the worker
# profile: which compiler is being used
# name:    how will the builds be called; for example texlive.darwin-x86_64.prg
builder_list = [
    BuildWorker(worker = 'solaris10-i386',              code = 'csw', profile = builder_profiles['solaris10-i386'],   name = 'solaris-i386.csw',         arch = 'i386',    tlname = 'i386-solaris',        upload = True),
    BuildWorker(worker = 'solaris10-i386',              code = 'csw', profile = builder_profiles['solaris10-x86_64'], name = 'solaris-x86_64.csw',       arch = 'x86_64',  tlname = 'x86_64-solaris',      upload = True),
    BuildWorker(worker = 'solaris10-sparc',             code = 'csw', profile = builder_profiles['solaris10-sparc'],  name = 'solaris-sparc.csw',        arch = 'sparc',   tlname = 'sparc-solaris',       upload = False),
    #BuildWorker(worker = 'jon-openbsd71-ppc',          code = 'jon', profile = builder_profiles['openbsd'],          name = 'openbsd-ppc-7.1.jon',      arch = 'ppc',     tlname = 'ppc-openbsd7.1',      upload = True),
    BuildWorker(worker = 'pragma-openbsd71-amd64',      code = 'prg', profile = builder_profiles['openbsd'],          name = 'openbsd-amd64-7.1.prg',    arch = 'amd64',   tlname = 'amd64-openbsd7.1',    upload = True),
    BuildWorker(worker = 'pragma-openbsd72-amd64',      code = 'prg', profile = builder_profiles['openbsd'],          name = 'openbsd-amd64-7.2.prg',    arch = 'amd64',   tlname = 'amd64-openbsd7.2',    upload = True),
    BuildWorker(worker = 'pragma-freebsd-i386',         code = 'prg', profile = builder_profiles['freebsd'],          name = 'freebsd-i386.prg',         arch = 'i386',    tlname = 'i386-freebsd',        upload = True),
    BuildWorker(worker = 'pragma-freebsd-amd64',        code = 'prg', profile = builder_profiles['freebsd'],          name = 'freebsd-amd64.prg',        arch = 'amd64',   tlname = 'amd64-freebsd',       upload = True),
    BuildWorker(worker = 'pragma-linux-alpine-x86_64',  code = 'prg', profile = builder_profiles['linux-clang'],      name = 'linuxmusl-x86_64-alpine.prg', arch = 'x86_64', tlname = 'x86_64-linuxmusl',  upload = True),
    BuildWorker(worker = 'pragma-linux-debian10-armhf', code = 'prg', profile = builder_profiles['linux'],            name = 'linux-armhf-debian10.prg', arch = 'armhf',   tlname = 'armhf-linux',         upload = True),
    BuildWorker(worker = 'mojca-linux-debian10-aarch64', code = 'moj', profile = builder_profiles['linux'],           name = 'linux-aarch64-debian10.moj', arch = 'aarch64', tlname = 'aarch64-linux',     upload = True),
    BuildWorker(worker = 'pragma-linux-debian9-i386',   code = 'prg', profile = builder_profiles['linux'],            name = 'linux-i386-debian9.prg',   arch = 'i386',    tlname = 'i386-linux',          upload = True),
    BuildWorker(worker = 'pragma-linux-debian9-x86_64', code = 'prg', profile = builder_profiles['linux'],            name = 'linux-x86_64-debian9.prg', arch = 'x86_64',  tlname = 'x86_64-linux',        upload = True),
    BuildWorker(worker = 'mojca-darwin-arm64',          code = 'moj', profile = builder_profiles['darwin'],           name = 'darwin-arm64.moj',         arch = 'arm64',   tlname = 'arm64-darwin',        upload = True),
    BuildWorker(worker = 'darwin10-x86_64',             code = 'moj', profile = builder_profiles['darwin10-x86_64'],  name = 'darwin10-x86_64.moj',      arch = 'x86_64',  tlname = 'x86_64-darwinlegacy', upload = True),
    BuildWorker(worker = 'pragma-linux-debian10-x86_64', code = 'prg', profile = builder_profiles['mingw-cross32'],   name = 'mingw-i686.prg',           arch = 'i386',    tlname = 'i686-w64-mingw32',    upload = True),
    BuildWorker(worker = 'pragma-linux-debian10-x86_64', code = 'prg', profile = builder_profiles['mingw-cross64'],   name = 'mingw-x86_64.prg',         arch = 'x86_64',  tlname = 'x86_64-w64-mingw32',  upload = True),
    BuildWorker(worker = 'pragma-windows10-x86_64',      code = 'prg', profile = builder_profiles['windows-msvc32'],  name = 'windows-i686.prg',         arch = 'i386',    tlname = 'win32',               upload = True),
    BuildWorker(worker = 'pragma-windows10-x86_64',      code = 'prg', profile = builder_profiles['windows-msvc64'],  name = 'windows-x86_64.prg',       arch = 'x86_64',  tlname = 'win64',               upload = True),
    BuildWorker(worker = 'pragma-windows10-x86_64',      code = 'prg', profile = builder_profiles['windows-clang'],   name = 'windows-clang-x86_64.prg', arch = 'x86_64',  tlname = 'win64-clang',         upload = False),
    BuildWorker(worker = 'pragma-windows10-x86_64',      code = 'prg', profile = builder_profiles['windows-arm64'],   name = 'windows-arm64.prg',        arch = 'arm64',   tlname = 'arm64-windows',       upload = True),
]

