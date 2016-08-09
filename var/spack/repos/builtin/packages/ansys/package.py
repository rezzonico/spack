from spack import *

import spack.environment

class Ansys(Package):
    """
    Ansys Fluent - To use this software you need to be a member of the ansys-users group

    Please see http://ansys.epfl.ch for further information
    """

    homepage = "http://www.ansys.com"
    url = 'fakeurl.tar.gz'
    licensed = True
    only_binary = True


    version('17.1')

    def install(self, spec, prefix):
        pass


    def setup_environment(self, spack_env, run_env):

        run_env.prepend_path('PATH', '/ssoft/spack/external/ansys/17.1/v171/ansys/bin')
        run_env.prepend_path('PATH', '/ssoft/spack/external/ansys/17.1/v171/CFD-Pos/bin')
        run_env.prepend_path('PATH', '/ssoft/spack/external/ansys/17.1/v171/CFX/bin')
        run_env.prepend_path('PATH', '/ssoft/spack/external/ansys/17.1/v171/Icepak/bin')
        run_env.prepend_path('PATH', '/ssoft/spack/external/ansys/17.1/v171/TurboGrid/bin')
        run_env.prepend_path('PATH', '/ssoft/spack/external/ansys/17.1/v171/autodyn/bin')
        run_env.prepend_path('PATH', '/ssoft/spack/external/ansys/17.1/v171/fluent/bin')
        run_env.prepend_path('PATH', '/ssoft/spack/external/ansys/17.1/v171/polyflow/bin')
        run_env.prepend_path('PATH', '/ssoft/spack/external/ansys/17.1/v171/tgrid/bin')
        run_env.prepend_path('PATH', '/ssoft/spack/external/ansys/17.1/v171/Framework/bin/Linux64')

        run_env.prepend_path('LD_LIBRARY_PATH', '/ssoft/spack/external/ansys/17.1/v171/Framework/bin/Linux64')
        run_env.prepend_path('LD_LIBRARY_PATH', '/ssoft/spack/external/ansys/17.1/v171/polyflow/polyflow17.1.0/lnamd64/libs')

