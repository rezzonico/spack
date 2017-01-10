import os

from spack import *


class Cudnn(Package):
    """The NVIDIA CUDA Deep Neural Network library (cuDNN) is a GPU-accelerated library of primitives for deep neural networks. cuDNN provides highly tuned implementations for standard routines such as forward and backward convolution, pooling, normalization, and activation layers. cuDNN is part of the NVIDIA Deep Learning SDK."""

    homepage = "https://developer.nvidia.com/cudnn"

    # Packages for different CUDA versions

    version('4.0.cuda7','39f7b583da86cf967a2ffe3d7237f7e4',url="file://%s/cudnn-7.0-linux-x64-v4.0-prod.tar.gz" % os.getcwd())
    
    version('5.1.cuda7','e94182a0bf55f964bc21df322ed7e73b',url="file://%s/cudnn-7.5-linux-x64-v5.1.tgz" % os.getcwd())

    version('5.1.cuda8','2f47a5a17942abd31c95d52745f6f48b',url="file://%s/cudnn-8.0-linux-x64-v5.1.tgz" % os.getcwd())

    depends_on("cuda@7.5.18", when="@4.0.cuda7")
    depends_on("cuda@7.5.18", when="@5.1.cuda7")
    depends_on("cuda@8.0.44", when="@5.1.cuda8")



    def install(self, spec, prefix):
        install_tree(
            join_path(self.stage.source_path, 'lib64'),
            prefix.lib64
        )

        install_tree(
            join_path(self.stage.source_path, 'include'),
            prefix.include
        )

        os.symlink(prefix.lib64,prefix.lib)



