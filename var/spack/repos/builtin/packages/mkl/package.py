from spack import *


class Mkl(Package):
    homepage = 'https://software.intel.com/en-us/articles/intel-mkl-113-release-notes/'
    url = 'fakeurl'
    licensed = True
    only_binary = True

    version('11.3')

    provides('blas')
    provides('lapack')
    provides('scalapack')

    def install(self, spec, prefix):
        if '%intel' not in spec:
            raise InstallError('MKL : must use intel compiler')

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        """
        For dependencies, make mpicc's use spack wrapper.
        """
        pass
