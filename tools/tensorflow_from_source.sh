#!/bin/bash

set -e

echo "-----------------------------------"
echo "installing apt-get dependencies ..."
echo "-----------------------------------"

sudo apt-get -y install openjdk-8-jdk git python3-dev python3-numpy build-essential python3-pip swig python3-wheel libcurl3-dev


echo "-----------------------------------"
echo "Add Bazel distribution URI as a package source (one time setup) ..."
echo "-----------------------------------"

echo "deb [arch=amd64] http://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list

curl https://bazel.build/bazel-release.pub.gpg | sudo apt-key add -

sudo apt-get -y update
sudo apt-get -y install libibverbs-dev
sudo apt-get -y install bazel
sudo apt-get -y upgrade bazel


echo "-----------------------------------"
echo "cloning tensorflow ..."
echo "-----------------------------------"
git clone https://github.com/tensorflow/tensorflow
cd tensorflow

export PYTHON_BIN_PATH=/usr/bin/python3.5
export PYTHON_LIB_PATH=/usr/local/lib/python3.5/dist-packages
export PYTHONPATH=/lib
export PYTHON_ARG=/lib


export TF_NEED_GCP=0
export TF_NEED_GDR=0
export TF_NEED_CUDA=0
export TF_NEED_HDFS=0
export TF_NEED_OPENCL=0
export TF_NEED_JEMALLOC=0
export TF_ENABLE_XLA=0
export TF_NEED_VERBS=1
export TF_CUDA_CLANG=0
export TF_NEED_MKL=1
export TF_DOWNLOAD_MKL=1
export TF_NEED_MPI=0

export GCC_HOST_COMPILER_PATH=$(which gcc)
export CC_OPT_FLAGS="-march=mkl"

echo "-----------------------------------"
echo "configure tensorflow ..."
echo "-----------------------------------"
bazel clean
./configure

echo "-----------------------------------"
echo "Building tensorflow ..."
echo "-----------------------------------"

# build TensorFlow (add  -s to see executed commands)
# "--copt=" can be "-mavx -mavx2 -mfma  -msse4.2 -mfpmath=both"
# build entire package
bazel build  -c opt --copt=-msse4.2 \
										--copt=-msse4.1 \
										--copt=-mavx \
										--config=mkl //tensorflow/tools/pip_package:build_pip_package

echo "-----------------------------------"
echo "Building build the pip package required for installing TensorFlow in your /tmp/tensorflow_pkg/..."
echo "-----------------------------------"
bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/tensorflow_pkg

echo "tensorflow install will be completed only when you complete the below instructions "
echo "-----------------------------------"
sudo -H pip3 install /tmp/tensorflow_pkg/tensorflow-1.3.0-cp35-cp35m-linux_x86_64.whl

echo "-----------------------------------"
echo "with no spaces after tensorflow hit tab before hitting enter to fill in blanks for the above command"
