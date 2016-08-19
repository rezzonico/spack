import grp
import os

from spack import *

class Molpro(Package):
    """Molpro is a comprehensive system of ab initio programs for advanced
    molecular electronic structure calculations
    """

    homepage = 'https://www.molpro.net'
    url      = 'http://your.mirror/molpro2015-git-2015-12-18.tar.bz2'

    licensed = True

    version('2015-12-18', '112bbfd21fb543d842465a902b9f2e0c', url='http://your.mirror/molpro2015-git-2015-12-18.tar.bz2')

    variant('openmp', default=False, description='Enable OpenMP parallelism')
    variant('int8', default=True, description='Enable 8-byte integers')
    
    depends_on('libxml2')
    depends_on('mpi')
    depends_on('blas')
    depends_on('lapack')

    def install(self, spec, prefix):
        # Avoid interactive prompt for token
        template = join_path(self.stage.source_path,'utilities','install.template')
        filter_file('read ', '# read ', template)

        # Installation
        mpi_include = self.spec['mpi'].prefix.include
        if 'intelmpi' in spec:
            mpi_include = join_path(self.spec['mpi'].prefix, 'include64')

        int8_opt = '--enable-integer8' if '+int8' in self.spec else '--disable-integer8'
        openmp_opt = '--enable-openmp' if '+openmp' in self.spec else '--disable-openmp'

        configure_opts = [
            'CXX={0}'.format(self.spec['mpi'].mpicxx),
            'FC={0}'.format(self.spec['mpi'].mpifc),
            '--prefix={0}'.format(prefix),
            '--enable-mpp={0}'.format(mpi_include),
            '--with-blas={0}'.format(self.spec['blas'].blas_ld_flags),
            '--with-lapack={0}'.format(self.spec['lapack'].blas_ld_flags),
            '--disable-boost',
            openmp_opt,
            int8_opt
        ]

        configure(*configure_opts)
        filter_file('VERBOSE=@', 'VERBOSE=', 'CONFIG')
        make()
        make("install")
        # Filter molpro script to use srun
        filter_file(
            r'LAUNCHER=[\S ]*',
            r'LAUNCHER="srun %x"',
            join_path(self.prefix, 'molprop_2015_1_linux_x86_64_i8', 'bin', 'molpro')
        )
        # Change group ownership, prevent others to execute
        gid = grp.getgrnam('molpro-soft').gr_gid
        os.chown(self.prefix, -1, gid)
        os.chmod(self.prefix, 0750)
