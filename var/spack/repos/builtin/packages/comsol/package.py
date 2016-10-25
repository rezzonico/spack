from spack import *

import spack.environment

class Comsol(Package):
    """
    Comsol Multiphysics is a general-purpose software platform
    for modeling and simulating physics-based problems.
    """

    homepage = "http://www.comsol.com"
    url = 'fakeurl.tar.gz'
    licensed = True
    only_binary = True


    version('5.2a')

    def install(self, spec, prefix):
        pass

