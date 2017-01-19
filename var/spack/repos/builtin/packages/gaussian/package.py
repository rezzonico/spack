from spack import *

import distutils.dir_util

class Gaussian(Package):
    """Description"""

    homepage = "http://www.gaussian.com"

    version('g09-D.01', '8730898096867217fef086386f643b4c',
            url      = "file:///home/ddossant/software/gaussian/g09-D.01.tar.gz")

    def install(self, spec, prefix):
        distutils.dir_util.copy_tree(".", prefix + '/g09')

    def setup_environment(self, spack_env, run_env):
        run_env.set('g09root', prefix + '/g09')
        run_env.set('GAUSS_EXEDIR', prefix + '/g09/bsd:' + prefix + '/g09/local:' + prefix + '/g09')
        run_env.set('GAUSS_LEXEDIR', prefix + '/g09/linda-exe')
        run_env.set('GAUSS_ARCHDIR', prefix + '/g09/arch')
        run_env.set('GAUSS_BSDDIR', prefix + '/g09/bsd')
        run_env.prepend_path('PATH', prefix + '/g09/bsd:' + prefix + '/g09/local:' + prefix + '/g09')
        run_env.prepend_path('LD_LIBRARY_PATH', prefix + '/g09/bsd:' + prefix + '/g09/local:' + prefix + '/g09')

