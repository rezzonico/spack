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
        spack_env.set('MKLROOT', '/ssoft/spack/external/intel/2016/compilers_and_libraries_2016.3.210/linux/mkl')
        pass

    def setup_dependent_package(self, module, dependent_spec):
        spec = self.spec
        
        if 'intelmpi' in spec or 'mvapich2' in spec:
            libblacs='-lmkl_blacs_intelmpi_lp64'
        elif 'openmpi' in spec:
            libblacs='-lmkl_blacs_openmpi_lp64'
        else:
            libblacs='-lmkl_blacs_lp64'

        mkl_lib = join_path(spec.prefix.lib, 'lib', 'intel64')
        spec.fc_link = '-L{0} {1} {2} {3}'.format(mkl_lib,
                                                  '-lmkl_scalapack_lp64', libblacs,
                                                  '-lmkl_intel_lp64 -lmkl_core -lmkl_sequential')
        spec.cc_link = '-L{0} {1} {2} {3}'.format(mkl_lib,
                                                  '-lmkl_scalapack_lp64', libblacs,
                                                  '-lmkl_intel_lp64 -lmkl_core -lmkl_sequential')
