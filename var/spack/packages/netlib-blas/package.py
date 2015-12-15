from spack import *
import os


class NetlibBlas(Package):
    """Netlib reference BLAS"""
    homepage = "http://www.netlib.org/lapack/"
    url      = "http://www.netlib.org/lapack/lapack-3.5.0.tgz"

    version('3.5.0', 'b1d3e3e425b2e44a06760ff173104bdf')
    
    variant('fpic', default=False, description="Build with -fpic compiler option")
    variant('shared', default=False, description="Build shared library version")

    # virtual dependency
    provides('blas')

    depends_on('cmake@2.8:')

    patch('netlib-blas.cmake-location.patch', level=1, when="^cmake@3.0:")
    
    # Doesn't always build correctly in parallel
    parallel = False
        
    def install(self, spec, prefix):
        options = [ '-DUSE_OPTIMIZED_BLAS:BOOL=OFF' ] # to force it to create the blas target

        if '+fpic' in spec:
            options.append('-DCMAKE_Fortran_FLAGS:STRING=-fPIC')

        if '+shared' in spec:
            options.append('-DBUILD_SHARED_LIBS:BOOL=ON')

        options.extend(std_cmake_args)
        
        with working_dir('spack-build', create=True):
            cmake('..', *options)

        with working_dir('spack-build/BLAS'):
            make()
            make('test')
            make('install')

        # Blas virtual package should provide blas.a and libblas.a
        with working_dir(prefix.lib):
            if '~shared' in spec:
                symlink('libblas.a', 'blas.a')
                symlink('libblas.a', 'librefblas.a')
            else:
                symlink('libblas.so', 'librefblas.so')
                
    def setup_dependent_environment(self, module, spec, dependent_spec):
        lib_suffix = '.so' if '+shared' in spec['blas'] else '.a'

        spec['blas'].fc_link = '-L%s -lrefblas' % spec['blas'].prefix.lib
        spec['blas'].cc_link = spec['blas'].fc_link
        spec['blas'].libraries = [ join_path(spec['blas'].prefix.lib, 'librefblas%s' % lib_suffix) ]
        
        os.environ['BLA_VENDOR'] = 'Generic'
