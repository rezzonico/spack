from spack.provider_contracts import BlasProviderContract, LapackProviderContract
from spack import *


class Mkl(LapackProviderContract, BlasProviderContract, Package):
    homepage = 'https://software.intel.com/en-us/articles/intel-mkl-113-release-notes/'
    url = 'fakeurl'
    licensed = True
    only_binary = True

    version('11.3')

    provides('blas')
    provides('lapack')

    def install(self, spec, prefix):
        tty.message('mpi : using Intel MKL external package')

    @property
    def blas_include_flags(self):
        if '%intel' in self.spec:
            return '-mkl'
        else:
            raise RuntimeError('MKL support for non-Intel compilers still to be implemented')

    @property
    def blas_ld_flags(self):
        return self.blas_include_flags

    @property
    def lapack_include_flags(self):
        return self.blas_include_flags

    @property
    def lapack_ld_flags(self):
        return self.blas_include_flags
