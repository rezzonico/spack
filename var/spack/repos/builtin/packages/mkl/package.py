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
        spack_env.set('LAPACK_DIR', '/ssoft/spack/external/intel/2016/compilers_and_libraries_2016.3.210/linux/mkl')
        spack_env.set('BLAS_DIR', '/ssoft/spack/external/intel/2016/compilers_and_libraries_2016.3.210/linux/mkl')

    def setup_dependent_package(self, module, dependent_spec):
        spec = self.spec

        blas_libs = ['mkl_intel_lp64', 'mkl_core', 'mkl_sequential']
        scalapack_libs = ['mkl_scalapack_lp64']
        
        if 'intelmpi' in spec or 'mvapich2' in spec:
            scalapack_libs.append('mkl_blacs_intelmpi_lp64')
        elif 'openmpi' in spec:
            scalapack_libs.append('mkl_blacs_openmpi_lp64')
        else:
            scalapack_libs.append('mkl_blacs_lp64')

        mkl_lib = join_path(spec.prefix.lib, 'intel64')

        spec.blas_ld_flags = \
            '-L{0} {1}'.format(mkl_lib,
                               ' '.join(('-l{0}'.format(l) for l in blas_libs)))
        spec.lapack_ld_flags = spec.blas_ld_flags

        spec.blas_static_libs = \
            [join_path(mkl_lib, 'lib{0}.a'.format(l)) for l in blas_libs]
        spec.lapack_static_libs = spec.blas_static_libs

        spec.blas_shared_libs = \
            [join_path(mkl_lib, 'lib{0}.{1}'.format(l, dso_suffix)) for l in blas_libs]
        spec.lapack_shared_libs = spec.blas_shared_libs

        spec.scalapack_ld_flags = \
            '-L{0} {1}'.format(mkl_lib,
                               ' '.join(('-l{0}'.format(l) for l in scalapack_libs)))

        spec.scalapack_static_libs =\
            [join_path(mkl_lib, 'lib{0}.a'.format(l)) for l in scalapack_libs]
        spec.scalapack_shared_libs = \
            [join_path(mkl_lib, 'lib{0}.{1}'.format(l, dso_suffix)) for l in scalapack_libs]

        # Add this for compatibility with builtin lapack/blas providers
        spec.blas_shared_lib = ' '.join(spec.blas_shared_libs)
        spec.lapack_shared_lib = ' '.join(spec.lapack_shared_libs)
        spec.scalapack_shared_lib = ' '.join(spec.scalapack_shared_libs)
