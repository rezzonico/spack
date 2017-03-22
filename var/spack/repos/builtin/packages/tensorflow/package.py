from spack import *


class Tensorflow(Package):
    """Tensorflow external package
    """

    homepage = "https://www.tensorflow.org/"
    url = 'fakeurl.tar.gz'
    licensed = True
    only_binary = True

    version('0.10.0rc0')
    depends_on('python')
    variant('cuda', default=False, description="Enable CUDA support")
    depends_on('cuda',when='+cuda')
    depends_on('cudnn',when='+cuda')

    def install(self, spec, prefix):
        pass


    def setup_environment(self, spack_env, run_env):

        if '+cuda' in self.spec:   
            venv_path='/ssoft/spack/external/tensorflow/0.10.0rc0/tensorflow_venv_gpu'
            run_env.set('VIRTUAL_ENV',venv_path)
            run_env.prepend_path('PATH',join_path(venv_path,'bin'))
        else:
            venv_path='/ssoft/spack/external/tensorflow/0.10.0rc0/tensorflow_venv_cpu'
            run_env.set('VIRTUAL_ENV',venv_path)
            run_env.prepend_path('PATH',join_path(venv_path,'bin'))
