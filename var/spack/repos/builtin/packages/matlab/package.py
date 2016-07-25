from spack import *

import spack.environment

class Matlab(Package):
    """
    Mock package for Matlab
    """

    homepage = "http://www.mathworks.com/products/matlab/"
    url = 'fakeurl.tar.gz'
    licensed = True
    only_binary = True


    version('R2016a')

    def install(self, spec, prefix):
        pass


    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):

        spack_env.set('MATLAB_ROOT',  '/ssoft/spack/external/MATLAB/R2016a')
        spack_env.prepend_path('PATH', '/ssoft/spack/external/MATLAB/R2016a/bin')
