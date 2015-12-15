from spack import *

class Openblas(Package):
    """OpenBLAS: An optimized BLAS library"""
    homepage = "http://www.openblas.net"
    url      = "http://github.com/xianyi/OpenBLAS/archive/v0.2.15.tar.gz"

    version('0.2.15', 'b1190f3d3471685f17cfd1ec1d252ac9')

    # virtual dependency
    provides('blas')
    provides('lapack')

    def install(self, spec, prefix):
        make('libs', 'netlib', 'shared', 'CC=cc', 'FC=f77')
        make('install', "PREFIX='%s'" % prefix)

        # Blas virtual package should provide blas.a and libblas.a
        with working_dir(prefix.lib):
            symlink('libopenblas.a', 'blas.a')
            symlink('libopenblas.a', 'libblas.a')

    def setup_dependent_environment(self, module, spec, dependent_spec):
        spec['blas'].fc_link = '-L%s -lopenblas' % spec['blas'].prefix.lib
        spec['blas'].cc_link = spec['blas'].fc_link
        spec['blas'].libraries = [ join_path(spec['blas'].prefix.lib, 'libopenblas.a') ]
       
        os.environ['BLA_VENDOR'] = 'Generic'

        spec['lapack'].fc_link = '-L%s -llapack' % spec['lapack'].prefix.lib
        spec['lapack'].cc_link = spec['lapack'].cc_link
        spec['lapack'].libraries = [ join_path(spec['lapack'].prefix.lib, 'liblapack.a') ]
