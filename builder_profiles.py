#!/usr/bin/env python
#
# Builder profile:
# - platform (os)
# - environmental variables (like compiler)
# - make and tar command to be used
# - is it capable of building C++11 code?
class BuilderProfile(object):
    def __init__(self, platform, env = {}, cmd_make = 'make', cmd_tar = 'tar', cxx11 = True):
        self.platform = platform
        self.env      = env
        self.cmd_make = cmd_make
        self.cmd_tar  = cmd_tar
        self.cxx11    = cxx11

# Builder:
# - slave name
# - code (to distinguish locations of builders)
# - builder profile
# - name of the builder
# - architecture of the builder
# - official tl name
# - should we upload binaries?
class BuildWorker(object):
    def __init__(self, slave, code, profile, name, arch, tlname, upload = False):
        self.slave    = slave
        self.code     = code
        self.profile  = profile
        self.name     = name
        self.arch     = arch
        self.tlname   = tlname
        self.upload   = upload

        self.platform = profile.platform
        self.env      = profile.env
        self.cmd_make = profile.cmd_make
        self.cmd_tar  = profile.cmd_tar
        self.cxx11    = profile.cxx11

env_darwin10 = {}
for arch in ['ppc', 'i386', 'x86_64']:
    env_darwin10[arch] = {}
    cc = {}
    cxx = {}

    for stdlib in ['', 'libc++', 'libstdc++']:
        env_darwin10[arch][stdlib] = {}

    cc[''] = '/usr/bin/gcc-4.2'
    cxx[''] = '/usr/bin/g++-4.2'
    cc['libc++'] = '/opt/local/bin/clang-mp-5.0'
    cxx['libc++'] = '/opt/local/bin/clang++-mp-5.0 -stdlib=libc++'
    cc['libstdc++'] = '/opt/local/bin/clang-mp-5.0'
    cxx['libstdc++'] = '/opt/local/bin/clang++-mp-5.0 -stdlib=macports-libstdc++ -D_GLIBCXX_USE_CXX11_ABI=0'

    for stdlib in ['', 'libc++', 'libstdc++']:
        if arch == 'x86_64':
            target = '10.6'
        else:
            target = '10.5'
        libdir  = '-L/Developer/SDKs/MacOSX{}.sdk/usr/lib'.format(target)
        sysroot = '-isysroot /Developer/SDKs/MacOSX{}.sdk -mmacosx-version-min={}'.format(target, target)
        ldflags = libdir + ' ' + sysroot

        env_darwin10[arch][stdlib]['CC']     = '{} -arch {}'.format(cc[stdlib], arch)
        env_darwin10[arch][stdlib]['OBJC']   = '{} -arch {}'.format(cc[stdlib], arch)
        env_darwin10[arch][stdlib]['CXX']    = '{} -arch {}'.format(cxx[stdlib], arch)
        env_darwin10[arch][stdlib]['OBJCXX'] = '{} -arch {}'.format(cxx[stdlib], arch)

        for flags in ['CFLAGS', 'OBJCFLAGS', 'CXXFLAGS', 'OBJCXXFLAGS']:
            env_darwin10[arch][stdlib][flags] = '-Os {}'.format(sysroot)
        env_darwin10[arch][stdlib]['LDFLAGS'] = '-Os {}'.format(ldflags)

        env_darwin10[arch][stdlib]['STRIP'] = 'strip -u -r'

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
env_openbsd_old = {
    'CC'             : 'egcc',
    'CXX'            : 'eg++',
}
env_freebsd = {}
env_linux = {}
env_mingw = {}
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

builder_profiles = {
    'solaris10-sparc'  : BuilderProfile(platform = 'solaris', env = env_solaris10,          cmd_make = 'gmake', cmd_tar = 'gtar',   cxx11 = True),
    'solaris10-i386'   : BuilderProfile(platform = 'solaris', env = env_solaris10,          cmd_make = 'gmake', cmd_tar = 'gtar',   cxx11 = True),
    'solaris10-x86_64' : BuilderProfile(platform = 'solaris', env = env_solaris10_64,       cmd_make = 'gmake', cmd_tar = 'gtar',   cxx11 = True),
    'freebsd'          : BuilderProfile(platform = 'freebsd', env = env_freebsd,            cmd_make = 'gmake', cmd_tar = 'gtar',   cxx11 = True),
    'openbsd'          : BuilderProfile(platform = 'openbsd', env = env_openbsd,            cmd_make = 'gmake', cmd_tar = 'gtar',   cxx11 = True),
    'openbsd_old'      : BuilderProfile(platform = 'openbsd', env = env_openbsd_old,        cmd_make = 'gmake', cmd_tar = 'gtar',   cxx11 = True),
    'linux'            : BuilderProfile(platform = 'linux',   env = env_linux,              cmd_make = 'make',  cmd_tar = 'tar',    cxx11 = True),
    'linux-mingw32'    : BuilderProfile(platform = 'mingw',   env = env_mingw['32'],        cmd_make = 'make',  cmd_tar = 'tar',    cxx11 = True),
    'linux-mingw64'    : BuilderProfile(platform = 'mingw',   env = env_mingw['64'],        cmd_make = 'make',  cmd_tar = 'tar',    cxx11 = True),

    'darwin10-i386'             : BuilderProfile(platform = 'darwin',  env = env_darwin10['i386'][''],            cmd_make = 'make',  cmd_tar = 'gnutar', cxx11 = False),
    'darwin10-x86_64'           : BuilderProfile(platform = 'darwin',  env = env_darwin10['x86_64'][''],          cmd_make = 'make',  cmd_tar = 'gnutar', cxx11 = False),
    'darwin10-powerpc'          : BuilderProfile(platform = 'darwin',  env = env_darwin10['ppc'][''],             cmd_make = 'make',  cmd_tar = 'gnutar', cxx11 = False),
    'darwin10_libc++-i386'      : BuilderProfile(platform = 'darwin',  env = env_darwin10['i386']['libc++'],      cmd_make = 'make',  cmd_tar = 'gnutar', cxx11 = True),
    'darwin10_libc++-x86_64'    : BuilderProfile(platform = 'darwin',  env = env_darwin10['x86_64']['libc++'],    cmd_make = 'make',  cmd_tar = 'gnutar', cxx11 = True),
    'darwin10_libstdc++-i386'   : BuilderProfile(platform = 'darwin',  env = env_darwin10['i386']['libstdc++'],   cmd_make = 'make',  cmd_tar = 'gnutar', cxx11 = True),
    'darwin10_libstdc++-x86_64' : BuilderProfile(platform = 'darwin',  env = env_darwin10['x86_64']['libstdc++'], cmd_make = 'make',  cmd_tar = 'gnutar', cxx11 = True),
}

# slave:   name of the slave
# profile: which compiler is being used
# name:    how will the builds be called; for example texlive.darwin-x86_64.prg
builder_list = [
    BuildWorker(slave = 'solaris10-i386',              code = 'csw', profile = builder_profiles['solaris10-i386'],   name = 'solaris-i386.csw',         arch = 'i386',    tlname = 'i386-solaris',        upload = True),
    BuildWorker(slave = 'solaris10-i386',              code = 'csw', profile = builder_profiles['solaris10-x86_64'], name = 'solaris-x86_64.csw',       arch = 'x86_64',  tlname = 'x86_64-solaris',      upload = True),
    BuildWorker(slave = 'solaris10-sparc',             code = 'csw', profile = builder_profiles['solaris10-sparc'],  name = 'solaris-sparc.csw',        arch = 'sparc',   tlname = 'sparc-solaris',       upload = True),
#    BuildWorker(slave = 'pragma-openbsd6.0-i386',      code = 'prg', profile = builder_profiles['openbsd_old'],      name = 'openbsd-i386-6.0.prg',     arch = 'i386',    tlname = 'i386-openbsd6.0',     upload = True),
#    BuildWorker(slave = 'pragma-openbsd6.1-i386',      code = 'prg', profile = builder_profiles['openbsd_old'],      name = 'openbsd-i386-6.1.prg',     arch = 'i386',    tlname = 'i386-openbsd6.1',     upload = True),
    BuildWorker(slave = 'pragma-openbsd6.2-i386',      code = 'prg', profile = builder_profiles['openbsd'],          name = 'openbsd-i386-6.2.prg',     arch = 'i386',    tlname = 'i386-openbsd6.2',     upload = True),
#    BuildWorker(slave = 'pragma-openbsd6.0-amd64',     code = 'prg', profile = builder_profiles['openbsd_old'],      name = 'openbsd-amd64-6.0.prg',    arch = 'amd64',   tlname = 'amd64-openbsd6.0',    upload = True),
#    BuildWorker(slave = 'pragma-openbsd6.1-amd64',     code = 'prg', profile = builder_profiles['openbsd_old'],      name = 'openbsd-amd64-6.1.prg',    arch = 'amd64',   tlname = 'amd64-openbsd6.1',    upload = True),
    BuildWorker(slave = 'pragma-openbsd6.2-amd64',     code = 'prg', profile = builder_profiles['openbsd'],          name = 'openbsd-amd64-6.2.prg',    arch = 'amd64',   tlname = 'amd64-openbsd6.2',    upload = True),
    BuildWorker(slave = 'pragma-freebsd-i386',         code = 'prg', profile = builder_profiles['freebsd'],          name = 'freebsd-i386.prg',         arch = 'i386',    tlname = 'i386-freebsd',        upload = True),
    BuildWorker(slave = 'pragma-freebsd-amd64',        code = 'prg', profile = builder_profiles['freebsd'],          name = 'freebsd-amd64.prg',        arch = 'amd64',   tlname = 'amd64-freebsd',       upload = True),
    BuildWorker(slave = 'pragma-linux-debian9-armhf',  code = 'prg', profile = builder_profiles['linux'],            name = 'linux-armhf-debian9.prg',  arch = 'armhf',   tlname = 'armhf-linux',         upload = True),
    BuildWorker(slave = 'pragma-linux-debian8-i386',   code = 'prg', profile = builder_profiles['linux'],            name = 'linux-i386-debian8.prg',   arch = 'i386',    tlname = 'i386-linux',          upload = True),
    BuildWorker(slave = 'pragma-linux-debian9-i386',   code = 'prg', profile = builder_profiles['linux'],            name = 'linux-i386-debian9.prg',   arch = 'i386',    tlname = None,                  upload = False),
    BuildWorker(slave = 'pragma-linux-debian8-x86_64', code = 'prg', profile = builder_profiles['linux'],            name = 'linux-x86_64-debian8.prg', arch = 'x86_64',  tlname = 'x86_64-linux',        upload = True),
    BuildWorker(slave = 'pragma-linux-debian9-x86_64', code = 'prg', profile = builder_profiles['linux'],            name = 'linux-x86_64-debian9.prg', arch = 'x86_64',  tlname = None,                  upload = False),
#   BuildWorker(slave = 'pragma-linux-debian9-x86_64', code = 'prg', profile = builder_profiles['linux-mingw32'],    name = 'mingw32-i386.prg',         arch = 'win32',   tlname = 'i686-w64-mingw32',    upload = True),
#   BuildWorker(slave = 'pragma-linux-debian9-x86_64', code = 'prg', profile = builder_profiles['linux-mingw64'],    name = 'mingw32-x86_64.prg',       arch = 'win64',   tlname = 'x86_64-w64-mingw32',  upload = True),

#   BuildWorker(slave = 'boris-linux-armel',           code = 'bor', profile = builder_profiles['linux'],            name = 'linux-armel.bor',          arch = 'armel',   tlname = 'armel-linux',         upload = True),

#   BuildWorker(slave = 'darwin10-x86_64',             code = 'prg', profile = builder_profiles['darwin10-powerpc'],       name = 'darwin-powerpc.prg', arch = 'powerpc', tlname = 'powerpc-darwin',      upload = True),
    BuildWorker(slave = 'darwin10-x86_64',             code = 'prg', profile = builder_profiles['darwin10_libc++-i386'],   name = 'darwin-i386.prg',    arch = 'i386',    tlname = 'i386-darwin',         upload = True),
    BuildWorker(slave = 'darwin10-x86_64',             code = 'prg', profile = builder_profiles['darwin10_libc++-x86_64'], name = 'darwin-x86_64.prg',  arch = 'x86_64',  tlname = 'x86_64-darwinlegacy', upload = True),
]

