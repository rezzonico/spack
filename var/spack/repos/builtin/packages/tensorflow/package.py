from spack import *

import spack.environment

class Tensorflow(Package):
    """
    Tensorflow external package
    """

    homepage = "https://www.tensorflow.org/"
    url = 'fakeurl.tar.gz'
    licensed = True
    only_binary = True

    version('0.10.0rc0')
    depends_on('python')
    variant('cuda', default=False, description="Enable CUDA support")
    depends_on('cuda',when='+cuda')

    def install(self, spec, prefix):
        pass


    def setup_environment(self, spack_env, run_env):

        if '+cuda' in self.spec:   
          run_env.set('TENSORFLOW_ROOT',  '/ssoft/spack/external/tensorflow/tensorflow_venv_gpu')
        else:
          run_env.set('TENSORFLOW_ROOT',  '/ssoft/spack/external/tensorflow/tensorflow_venv_cpu')
          
