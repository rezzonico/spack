##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install tensorflow
#
# You can edit this file again by typing:
#
#     spack edit tensorflow
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *
import subprocess
import os

class Tensorflow(Package):
    """TensorFlow is an open source software library for numerical computation using data flow graphs. Nodes in the graph represent mathematical operations, while the graph edges represent the multidimensional data arrays (tensors) communicated between them. """
    homepage = "https://www.tensorflow.org/"
    url      = "https://github.com/tensorflow/tensorflow/archive/v0.10.0rc0.tar.gz"

    version('0.10.0rc0', 'ba20a3b74a852c7709a06d9bea34ba12',pip='tensorflow',version='0.10.0rc0')
    version('0.9.0rc0' , '036261e252264a53338c4a455d3669c3',pip='tensorflow',version='0.9.0rc0')
    version('0.8.0rc0' , '9ca4f1266785063037263ce341913ef0',pip='tensorflow',version='0.8.0rc0')

    variant('cuda', default=False, description='Compile with CUDA Toolkit')
    depends_on('swig')
    depends_on('cuda', when='+cuda')
    depends_on('py-numpy')
    depends_on('bazel')
    depends_on('jdk')
    extends('python')
    depends_on('py-pip')
    depends_on('py-six')
    depends_on('py-wheel')
 
    parallel = False

    def install(self, spec, prefix):
        # FIXME: Modify the configure line to suit your build system here.
        #       filename = join_path(self.stage.source_path, 'compile.sh')

        #tensorflow_answers = {
        #  'python_location' : spec['python'].prefix.bin,
        #  'google' : 'N',
        #  'gpu' : 'N'
        #}
        #configure = subprocess.Popen(['./configure'],stdin=subprocess.PIPE)
        #for k,v in  tensorflow_answers.iteritems():
        # choice = str(v)
        # configure.stdin.write(choice)

        #configure.wait()
        
        filename = join_path(self.stage.source_path, 'configure')
        filter_file(r'read -p', 'echo', filename)
        filter_file(r'$(which python)', spec['python'].prefix.bin, filename)
        filter_file(r'TF_NEED_GCP=1', 'TF_NEED_GCP=0', filename)
        filename = join_path(self.stage.source_path, 'png.BUILD')
        filter_file(r'./configure --enable-shared=no --with-pic=no', './configure --enable-shared=no --with-pic=no CC=%s'%os.environ['SPACK_CC'], filename)
        filename = join_path(self.stage.source_path, 'farmhash.BUILD')
        filter_file(r'./configure', './configure CC=%s'%os.environ['SPACK_CC'], filename)
        filename = join_path(self.stage.source_path, 'jpeg.BUILD')
        filter_file(r'./configure', './configure CC=%s'%os.environ['SPACK_CC'], filename)
       
       # CUDA support
        filename = join_path(self.stage.source_path, 'configure')
        if '+cuda' in spec:
            filter_file(r'TF_NEED_CUDA=0', 'TF_NEED_CUDA=1', filename)
            filter_file(r'$(which gcc)', os.environ['CC'], filename)

            filter_file(r'/usr/local/cuda', spec['cuda'].prefix, filename)
            filter_file(r'default_cudnn_path=${CUDA_TOOLKIT_PATH}','default_cudnn_path=%s'%spec['cuda'].prefix,filename)
            os.environ['TF_CUDA_COMPUTE_CAPABILITIES'] = '3.5'
        else:
            filter_file(r'TF_NEED_CUDA=1', 'TF_NEED_CUDA=0', filename)

     

        configure()


        if '+cuda' in spec:
          filename = join_path(self.stage.source_path, 'third_party/gpus/crosstool/clang/bin/crosstool_wrapper_driver_is_not_gcc')
          filter_file(r'/home/nvarini/spack/lib/spack/env/gcc/gcc', os.environ['SPACK_CC'], filename)
          filename = join_path(self.stage.source_path, 'third_party/gpus/crosstool/CROSSTOOL')
          string =  join_path(os.environ['GCC_ROOT'],'lib64')
          filter_file(r'cxx_builtin_include_directory: "/usr/lib/gcc/"','cxx_builtin_include_directory: "%s"'%string, filename)
          string =  join_path(os.environ['GCC_ROOT'],'include/c++/4.9.3')
          filter_file(r'cxx_builtin_include_directory: "/usr/local/include"','cxx_builtin_include_directory: "%s"'%string, filename)
          #Executable('bazel')('build',  '-c', 'opt','--config=cuda','--genrule_strategy=standalone', '//tensorflow/tools/pip_package:build_pip_package')
          Executable('bazel')('build',  '-c', 'opt','--config=cuda','//tensorflow/tools/pip_package:build_pip_package')
        else:
          Executable('bazel')('build',  '-c', 'opt', '//tensorflow/tools/pip_package:build_pip_package')
       
        filename = str(join_path(self.stage.source_path, 'tensorflow_pkg'))
        Executable('bazel-bin/tensorflow/tools/pip_package/build_pip_package')('/tmp/tensorflow_pkg5/')
        string=['/tmp/tensorflow_pkg5/tensorflow-%s-py2-none-any.whl'%self.version]
        pip('install',*string)

