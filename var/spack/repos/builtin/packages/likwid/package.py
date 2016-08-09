from spack import *

import spack.environment

class Likwid(Package):
    """
    LIKWID ( "Like I Know What I'm Doing" ) allows easy access to low level performance counters.
    """

    homepage = "https://github.com/RRZE-HPC/likwid"
    url = 'fakeurl.tar.gz'
    licensed = True
    only_binary = True


    version('4.1.1')

    def install(self, spec, prefix):
        pass


    def setup_environment(self, spack_env, run_env):
        pass

