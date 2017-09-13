from spack import *


class Tensorflow(Package):
    """Tensorflow external package
    """

    homepage = "https://www.tensorflow.org/"
    url = 'fakeurl.tar.gz'
    licensed = True
    only_binary = True

    version('1.3')
    depends_on('python')
    depends_on('cuda')
    depends_on('cudnn')
    depends_on('mpi')

    def install(self, spec, prefix):
        pass

    def setup_environment(self, spack_env, run_env):
        venv_path = '/ssoft/spack/external/tensorflow/\
                     1.3.0/tensorflow_venv_gpu/'
        run_env.set('VIRTUAL_ENV', venv_path)
        run_env.prepend_path('PATH', join_path(venv_path, 'bin'))
