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

        self.platform = profile.platform
        self.env      = profile.env
        self.cmd_make = profile.cmd_make
        self.cmd_tar  = profile.cmd_tar
        self.cxx11    = profile.cxx11

        self.build_luametatex = (self.platform in ['darwin', 'freebsd', 'openbsd', 'linux', 'mingw']) and (not 'debian8' in self.name)
        self.build_pplib = (self.platform in ['darwin', 'freebsd', 'openbsd', 'linux']) and (not 'debian8' in self.name)
        self.build_luatex = not (self.platform in ['mingw'])
        self.build_texlive = not (self.platform in ['mingw'])

env_darwin10 = {}
for arch in ['i386', 'x86_64']:
    env_darwin10[arch] = {}

    cc     = '/opt/local/bin/clang-mp-7.0'
    cxx    = '/opt/local/bin/clang++-mp-7.0 -stdlib=libc++'
    target = '10.6'

    libdir  = '-L/Developer/SDKs/MacOSX{}.sdk/usr/lib'.format(target)
    sysroot = '-isysroot /Developer/SDKs/MacOSX{}.sdk -mmacosx-version-min={}'.format(target, target)
    ldflags = libdir + ' ' + sysroot

    env_darwin10[arch]['CC']     = '{} -arch {}'.format(cc,  arch)
    env_darwin10[arch]['OBJC']   = '{} -arch {}'.format(cc,  arch)
    env_darwin10[arch]['CXX']    = '{} -arch {}'.format(cxx, arch)
    env_darwin10[arch]['OBJCXX'] = '{} -arch {}'.format(cxx, arch)

    for flags in ['CFLAGS', 'OBJCFLAGS', 'CXXFLAGS', 'OBJCXXFLAGS']:
        env_darwin10[arch][flags] = '-Os {}'.format(sysroot)
    env_darwin10[arch]['LDFLAGS'] = '-Os {}'.format(ldflags)

    env_darwin10[arch]['STRIP'] = 'strip -u -r'

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
env_darwin = {}
env_mingw = {}
env_mingw['any'] = {}
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
    'linux'            : BuilderProfile(platform = 'linux',   env = env_linux,              cmd_make = 'make',  cmd_tar = 'tar',    cxx11 = True),
    'linux-mingw32'    : BuilderProfile(platform = 'mingw',   env = env_mingw['32'],        cmd_make = 'make',  cmd_tar = 'tar',    cxx11 = True),
    'linux-mingw64'    : BuilderProfile(platform = 'mingw',   env = env_mingw['64'],        cmd_make = 'make',  cmd_tar = 'tar',    cxx11 = True),
    'mingw-cross'      : BuilderProfile(platform = 'mingw',   env = env_mingw['any'],       cmd_make = 'make',  cmd_tar = 'tar',    cxx11 = True),
    'darwin10-i386'    : BuilderProfile(platform = 'darwin',  env = env_darwin10['i386'],   cmd_make = 'make',  cmd_tar = 'gnutar', cxx11 = True),
    'darwin10-x86_64'  : BuilderProfile(platform = 'darwin',  env = env_darwin10['x86_64'], cmd_make = 'make',  cmd_tar = 'gnutar', cxx11 = True),
    'darwin'           : BuilderProfile(platform = 'darwin',  env = env_darwin,             cmd_make = 'make',  cmd_tar = 'gnutar', cxx11 = True),
}

# worker:  name of the worker
# profile: which compiler is being used
# name:    how will the builds be called; for example texlive.darwin-x86_64.prg
builder_list = [
    BuildWorker(worker = 'solaris10-i386',              code = 'csw', profile = builder_profiles['solaris10-i386'],   name = 'solaris-i386.csw',         arch = 'i386',    tlname = 'i386-solaris',        upload = True),
    BuildWorker(worker = 'solaris10-i386',              code = 'csw', profile = builder_profiles['solaris10-x86_64'], name = 'solaris-x86_64.csw',       arch = 'x86_64',  tlname = 'x86_64-solaris',      upload = True),
    BuildWorker(worker = 'pragma-openbsd64-i386',       code = 'prg', profile = builder_profiles['openbsd'],          name = 'openbsd-i386-6.4.prg',     arch = 'i386',    tlname = 'i386-openbsd6.4',     upload = True),
    BuildWorker(worker = 'pragma-openbsd65-i386',       code = 'prg', profile = builder_profiles['openbsd'],          name = 'openbsd-i386-6.5.prg',     arch = 'i386',    tlname = 'i386-openbsd6.5',     upload = True),
    BuildWorker(worker = 'pragma-openbsd64-amd64',      code = 'prg', profile = builder_profiles['openbsd'],          name = 'openbsd-amd64-6.4.prg',    arch = 'amd64',   tlname = 'amd64-openbsd6.4',    upload = True),
    BuildWorker(worker = 'pragma-openbsd65-amd64',      code = 'prg', profile = builder_profiles['openbsd'],          name = 'openbsd-amd64-6.5.prg',    arch = 'amd64',   tlname = 'amd64-openbsd6.5',    upload = True),
    BuildWorker(worker = 'pragma-freebsd-i386',         code = 'prg', profile = builder_profiles['freebsd'],          name = 'freebsd-i386.prg',         arch = 'i386',    tlname = 'i386-freebsd',        upload = True),
    BuildWorker(worker = 'pragma-freebsd-amd64',        code = 'prg', profile = builder_profiles['freebsd'],          name = 'freebsd-amd64.prg',        arch = 'amd64',   tlname = 'amd64-freebsd',       upload = True),
    BuildWorker(worker = 'pragma-linux-debian10-armhf', code = 'prg', profile = builder_profiles['linux'],            name = 'linux-armhf-debian10.prg', arch = 'armhf',   tlname = 'armhf-linux',         upload = True),
    BuildWorker(worker = 'pragma-linux-debian8-i386',   code = 'prg', profile = builder_profiles['linux'],            name = 'linux-i386-debian8.prg',   arch = 'i386',    tlname = 'i386-linux',          upload = True),
    BuildWorker(worker = 'pragma-linux-debian9-i386',   code = 'prg', profile = builder_profiles['linux'],            name = 'linux-i386-debian9.prg',   arch = 'i386',    tlname = 'i386-linux',          upload = False),
    BuildWorker(worker = 'pragma-linux-debian8-x86_64', code = 'prg', profile = builder_profiles['linux'],            name = 'linux-x86_64-debian8.prg', arch = 'x86_64',  tlname = 'x86_64-linux',        upload = True),
    BuildWorker(worker = 'pragma-linux-debian9-x86_64', code = 'prg', profile = builder_profiles['linux'],            name = 'linux-x86_64-debian9.prg', arch = 'x86_64',  tlname = 'x86_64-linux',        upload = False),
    BuildWorker(worker = 'darwin10-x86_64',             code = 'prg', profile = builder_profiles['darwin10-x86_64'],  name = 'darwin10-x86_64.prg',      arch = 'x86_64',  tlname = 'x86_64-darwinlegacy', upload = True),
    BuildWorker(worker = 'darwin17-x86_64',             code = 'prg', profile = builder_profiles['darwin'],           name = 'darwin-x86_64.prg',        arch = 'x86_64',  tlname = 'x86_64-darwin',       upload = False),
    BuildWorker(worker = 'pragma-linux-debian10-x86_64', code = 'prg', profile = builder_profiles['mingw-cross'],     name = 'mingw-x86_64.prg',         arch = 'x86_64',  tlname = 'x86_64-w64-mingw32',  upload = True),
    BuildWorker(worker = 'pragma-linux-debian10-x86_64', code = 'prg', profile = builder_profiles['mingw-cross'],     name = 'mingw-i686.prg',           arch = 'i386',    tlname = 'i686-w64-mingw32',    upload = True),
]

