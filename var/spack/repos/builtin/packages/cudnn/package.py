import os

from spack import *


class Cudnn(Package):
    """The NVIDIA CUDA Deep Neural Network library (cuDNN) is a GPU-accelerated library of primitives for deep neural networks. cuDNN provides highly tuned implementations for standard routines such as forward and backward convolution, pooling, normalization, and activation layers. cuDNN is part of the NVIDIA Deep Learning SDK."""

    homepage = "https://developer.nvidia.com/cudnn"
    
    version('7.0','845ead4b37f1a2a243d7d1b4d42d1d8b',url="file://%s/cudnn-7.0.tgz" % os.getcwd())

    def install(self, spec, prefix):
        install_tree(
            join_path(self.stage.source_path, 'lib64'),
            prefix.lib
        )
        install_tree(
            join_path(self.stage.source_path, 'include'),
            prefix.include
        )

