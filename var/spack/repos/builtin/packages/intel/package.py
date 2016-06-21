from spack import *

import spack.environment

class Intel(Package):
    """
    Mock package for Intel compilers
    """

    homepage = "http://www.example.com"
    url      = "http://www.example.com/intel-1.0.tar.gz"

    version('16.0')

    def install(self, spec, prefix):
        pass

