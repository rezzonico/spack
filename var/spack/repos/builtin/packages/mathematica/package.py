from spack import *

import spack.environment

class Mathematica(Package):
    """
    Mathematica is a symbolic mathematics program

    There are a number of ways to use it:

    mathematica - the GUI based interface
    math        - the command line interace
    mcc         - the MathLink Template Compiler

    See https://reference.wolfram.com/language/tutorial/WolframLanguageScripts.html for how to use it in batch mode
    """

    homepage = "https://www.wolfram.com/mathematica/"
    url = 'fakeurl.tar.gz'
    licensed = True
    only_binary = True


    version('9.0.1')

    def install(self, spec, prefix):
        pass


    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):

        spack_env.set('MATHEMATICA_ROOT',  '/ssoft/spack/external/Mathematica/9.0.1')
        spack_env.prepend_path('PATH', '/ssoft/spack/external/Mathematica/9.0.1/bin')
