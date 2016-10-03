from spack import *

class Gpaw(Package):
    """GPAW is a density-functional theory (DFT) Python code based on
    the projector-augmented wave (PAW) method and the atomic
    simulation environment (ASE). The wave functions can be described
    with:
    -1- Plane-waves (pw)
    -2- Real-space uniform grids, multigrid methods and the
        finite-difference approximation (fd)
    -3- Atom-centered basis-functions (lcao)"""

    homepage = "https://wiki.fysik.dtu.dk/gpaw"
    url      = "https://pypi.python.org/packages/71/e6/d26db47ec7bc44d21fbefedb61a8572276358b50862da3390c20664d9511/gpaw-1.1.0.tar.gz"

    version('1.1.0', '67a4a10fb96184e55d3d004494b2e003')

    variant('hdf5',         default=True,  description='Compile with HDF5')
    variant('mpi',          default=True,  description='Enables the distributed memory support')

    extends("python")
    depends_on("blas")
    depends_on("lapack")
    depends_on("scalapack", when='+mpi')
    depends_on("hdf5+mpi~cxx", when='+mpi+hdf5')
    depends_on("hdf5", when='~mpi+hdf5')
    depends_on("libxc")
    depends_on("mpi", when='+mpi')
    depends_on("py-numpy")
    depends_on("py-ase")

    def extract_libraries(self, full_path_libraries, customize):
        paths = full_path_libraries.split(' ')
        for library in paths:
            split_path = library.split('/')
            customize['libraries'].append(split_path[-1][3:-len(dso_suffix)-1])
            customize['library_dirs'].append('/'.join(split_path[:-1]))
        
    def write_customize(self):
        customize = { 'include_dirs': [],
                      'library_dirs': [],
                      'extra_link_args': [],
                      'define_macros': [],
                      'mpicompiler': None }

        customize['libraries'] = ["xc"]

        depends = ["blas", "lapack", "libxc"]
        if '+mpi' in self.spec:
            depends.append("mpi")
            depends.append("scalapack")
            customize['compiler'] = self.spec['mpi'].mpicc
            customize['mpicompiler'] = self.spec['mpi'].mpicc 
            customize['mpilinker'] = self.spec['mpi'].mpicc
            customize['scalapack'] = True
            customize['define_macros'].append(('PARALLEL', '1'))

        if '+hdf5' in self.spec:
            depends.append("hdf5")
            customize['hdf5'] = True
            customize['libraries'].extend(['hdf5', 'hdf5_hl'])

        for dep in depends:
            customize['include_dirs'].append(self.spec[dep].prefix.include)
            customize['library_dirs'].append(self.spec[dep].prefix.lib)
            customize['extra_link_args'].append('{0}{1}'.format(self.compiler.cc_rpath_arg,
                                                                self.spec[dep].prefix.lib))

        if 'intelmpi' in self.spec:
            customize['include_dirs'].append(self.spec['mpi'].prefix.include + '64')

        self.extract_libraries(self.spec['blas'].blas_shared_lib, customize)
        self.extract_libraries(self.spec['lapack'].lapack_shared_lib, customize)

        if '+mpi' in self.spec:
            self.extract_libraries(self.spec['scalapack'].scalapack_shared_lib, customize)

        customize['define_macros'].extend([('GPAW_NO_UNDERSCORE_CBLACS', '1'),
                                           ('GPAW_NO_UNDERSCORE_CSCALAPACK', '1')])

        with open('customize.py', 'w') as fh:
            fh.write("libraries = []\n")
            for key, val in customize.iteritems():
                if type(val) is list:
                    fh.write("{0} += {1}\n".format(key, val))
                elif type(val) is str:
                    fh.write("{0} = \'{1}\'\n".format(key, val))
                else:
                    fh.write("{0} = {1}\n".format(key, val))

    def setup_environment(self, spack_env, run_env):
        run_env.set('OMP_NUM_THREADS', '1')

    def install(self, spec, prefix):
        self.write_customize()

        python('setup.py', 'install', '--prefix=%s' % prefix)
