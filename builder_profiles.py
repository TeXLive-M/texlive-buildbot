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
env_darwin10_cxx11 = {}
for arch in ['ppc', 'i386', 'x86_64']:
    env_darwin10[arch]       = {}
    env_darwin10_cxx11[arch] = {}

    if arch == 'x86_64':
        target = '10.6'
    else:
        target = '10.5'
    libdir  = '-L/Developer/SDKs/MacOSX{}.sdk/usr/lib'.format(target)
    sysroot = '-isysroot /Developer/SDKs/MacOSX{}.sdk -mmacosx-version-min={}'.format(target, target)
    cc      = '/usr/bin/gcc-4.2 -arch {}'.format(arch)
    cxx     = '/usr/bin/g++-4.2 -arch {}'.format(arch)
    cc11    = 'clang-mp-3.9 -arch {}'.format(arch)
    cxx11   = 'clang++-mp-3.9 -stdlib=libc++ -arch {}'.format(arch)
    ldflags = libdir + ' ' + sysroot

    env_darwin10[arch]['CC']     = cc
    env_darwin10[arch]['OBJC']   = cc
    env_darwin10[arch]['CXX']    = cxx
    env_darwin10[arch]['OBJCXX'] = cxx

    for flags in ['CFLAGS', 'OBJCFLAGS', 'CXXFLAGS', 'OBJCXXFLAGS']:
        env_darwin10[arch][flags]       = sysroot
        env_darwin10_cxx11[arch][flags] = sysroot
    env_darwin10[arch]['LDFLAGS']       = ldflags
    env_darwin10_cxx11[arch]['LDFLAGS'] = ldflags

    env_darwin10[arch]['STRIP']       = 'strip -u -r'
    env_darwin10_cxx11[arch]['STRIP'] = 'strip -u -r'

env_solaris10 = {
    'CC'      : '/opt/csw/bin/gcc-5.2',
    'CXX'     : '/opt/csw/bin/g++-5.2',
    'PATH'    : [ '${PATH}', '/usr/ccs/bin'],
    'TL_MAKE' : 'gmake',
#   'GREP'    : 'ggrep',
}
env_solaris10_64 = {
    'CC'      : '/opt/csw/bin/gcc-5.2 -m64',
    'CXX'     : '/opt/csw/bin/g++-5.2 -m64',
    'PATH'    : [ '${PATH}', '/usr/ccs/bin'],
    'TL_MAKE' : 'gmake',
#   'GREP'    : 'ggrep',
}
env_openbsd = {
    'ICU_LIBS_EXTRA' : '-lpthread',
    'TL_MAKE'        : 'gmake',
}
env_openbsd_cxx11 = {
    'ICU_LIBS_EXTRA' : '-lpthread',
    'TL_MAKE'        : 'gmake',
    'CC'             : 'egcc',
    'CXX'            : 'eg++',
}
env_freebsd = {
    'TL_MAKE' : 'gmake',
}
env_linux = {}

builder_profiles = {
    'solaris10-sparc'  : BuilderProfile(platform = 'solaris', env = env_solaris10,          cmd_make = 'gmake', cmd_tar = 'gtar',   cxx11 = True),
    'solaris10-i386'   : BuilderProfile(platform = 'solaris', env = env_solaris10,          cmd_make = 'gmake', cmd_tar = 'gtar',   cxx11 = True),
    'solaris10-x86_64' : BuilderProfile(platform = 'solaris', env = env_solaris10_64,       cmd_make = 'gmake', cmd_tar = 'gtar',   cxx11 = True),
    'darwin10-i386'    : BuilderProfile(platform = 'darwin',  env = env_darwin10['i386'],   cmd_make = 'make',  cmd_tar = 'gnutar', cxx11 = False),
    'darwin10-x86_64'  : BuilderProfile(platform = 'darwin',  env = env_darwin10['x86_64'], cmd_make = 'make',  cmd_tar = 'gnutar', cxx11 = False),
    'darwin10-powerpc' : BuilderProfile(platform = 'darwin',  env = env_darwin10['ppc'],    cmd_make = 'make',  cmd_tar = 'gnutar', cxx11 = False),
    'openbsd'          : BuilderProfile(platform = 'openbsd', env = env_openbsd,            cmd_make = 'gmake', cmd_tar = 'gtar',   cxx11 = False),
    'openbsd_cxx11'    : BuilderProfile(platform = 'openbsd', env = env_openbsd_cxx11,      cmd_make = 'gmake', cmd_tar = 'gtar',   cxx11 = True),
    'linux'            : BuilderProfile(platform = 'linux',   env = env_linux,              cmd_make = 'make',  cmd_tar = 'tar',    cxx11 = False),
    'linux_cxx11'      : BuilderProfile(platform = 'linux',   env = env_linux,              cmd_make = 'make',  cmd_tar = 'tar',    cxx11 = True),
}

# slave:   name of the slave
# profile: which compiler is being used
# name:    how will the builds be called; for example texlive.darwin-x86_64.prg
builder_list = [
    BuildWorker(slave = 'solaris10-i386',              code = 'csw', profile = builder_profiles['solaris10-i386'],   name = 'solaris-i386.csw',         arch = 'i386',    tlname = 'i386-solaris',        upload = True),
    BuildWorker(slave = 'solaris10-i386',              code = 'csw', profile = builder_profiles['solaris10-x86_64'], name = 'solaris-x86_64.csw',       arch = 'x86_64',  tlname = 'x86_64-solaris',      upload = True),
    BuildWorker(slave = 'solaris10-sparc',             code = 'csw', profile = builder_profiles['solaris10-sparc'],  name = 'solaris-sparc.csw',        arch = 'sparc',   tlname = 'sparc-solaris',       upload = True),
    BuildWorker(slave = 'darwin10-x86_64',             code = 'prg', profile = builder_profiles['darwin10-powerpc'], name = 'darwin-powerpc.prg',       arch = 'powerpc', tlname = 'powerpc-darwin',      upload = True),
    BuildWorker(slave = 'darwin10-x86_64',             code = 'prg', profile = builder_profiles['darwin10-i386'],    name = 'darwin-i386.prg',          arch = 'i386',    tlname = 'i386-darwin',         upload = True),
    BuildWorker(slave = 'darwin10-x86_64',             code = 'prg', profile = builder_profiles['darwin10-x86_64'],  name = 'darwin-x86_64.prg',        arch = 'x86_64',  tlname = 'x86_64-darwinlegacy', upload = True),
    BuildWorker(slave = 'pragma-openbsd6.0-i386',      code = 'prg', profile = builder_profiles['openbsd'],          name = 'openbsd-i386-6.0.prg',     arch = 'i386',    tlname = 'i386-openbsd6.0',     upload = True),
    BuildWorker(slave = 'pragma-openbsd6.1-i386',      code = 'prg', profile = builder_profiles['openbsd'],          name = 'openbsd-i386-6.1.prg',     arch = 'i386',    tlname = 'i386-openbsd6.1',     upload = True),
    BuildWorker(slave = 'pragma-openbsd6.0-amd64',     code = 'prg', profile = builder_profiles['openbsd'],          name = 'openbsd-amd64-6.0.prg',    arch = 'amd64',   tlname = 'amd64-openbsd6.0',    upload = True),
    BuildWorker(slave = 'pragma-openbsd6.1-amd64',     code = 'prg', profile = builder_profiles['openbsd'],          name = 'openbsd-amd64-6.1.prg',    arch = 'amd64',   tlname = 'amd64-openbsd6.1',    upload = True),
    BuildWorker(slave = 'pragma-linux-armhf',          code = 'prg', profile = builder_profiles['linux_cxx11'],      name = 'linux-armhf.prg',          arch = 'armhf',   tlname = 'armhf-linux',         upload = True),
    BuildWorker(slave = 'pragma-linux-debian7-i386',   code = 'prg', profile = builder_profiles['linux'],            name = 'linux-i386-debian7.prg',   arch = 'i386',    tlname = 'i386-linux',          upload = True),
    BuildWorker(slave = 'pragma-linux-debian9-i386',   code = 'prg', profile = builder_profiles['linux'],            name = 'linux-i386-debian9.prg',   arch = 'i386',    tlname = None,                  upload = False),
    BuildWorker(slave = 'pragma-linux-debian7-x86_64', code = 'prg', profile = builder_profiles['linux'],            name = 'linux-x86_64-debian7.prg', arch = 'x86_64',  tlname = 'x86_64-linux',        upload = True),
    BuildWorker(slave = 'pragma-linux-debian9-x86_64', code = 'prg', profile = builder_profiles['linux'],            name = 'linux-x86_64-debian9.prg', arch = 'x86_64',  tlname = None,                  upload = False),
#   BuildWorker(slave = 'pragma-linux-debian9-x86_64', code = 'prg', profile = builder_profiles['linux-mingw32'],    name = 'linux-mingw-w64.prg',      arch = 'win64',   tlname = None,                  upload = False),
]
