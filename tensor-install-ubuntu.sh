#
# run this file as a shell to get python3 installed:
#
#     sh tensor-install-ubuntu.sh
#
# run this shell script section by section with the simple python
# controller:
#
#    python3 section-shell.py tensor-install-ubuntu.sh 2
#
# This file contains the setup instructions from the TensorFlow
# webpage listed below:
# 
#    https://www.tensorflow.org/install/source
# 
# These instructions are for compiling the TensorFlow system for linux
# based computers:
# 
# section 1: install python3 and build utilities
sudo apt install python3-dev python3-pip

pip3 install -U --user pip numpy wheel
pip3 install -U --user keras_preprocessing --no-deps
pip3 install testresources
pip3 install matplotlib

sudo apt install build-essential
sudo apt install git

exit(0)

#
# installing bazel
#

#
# https://docs.bazel.build/versions/master/install-ubuntu.html
# do the first two steps - the compile will request an earlier
#  simple apt install operations
#

# section 2a: installing bazel support
sudo apt install curl gnupg
curl -fsSL https://bazel.build/bazel-release.pub.gpg | gpg --dearmor > bazel.gpg
sudo mv bazel.gpg /etc/apt/trusted.gpg.d/
echo "deb [arch=amd64] https://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list

# section 2b: install and upgrade bazel
sudo apt update && sudo apt install bazel

#
# Once installed, you can upgrade to a newer version of Bazel as part
# of your normal system updates:
#
# section 2c: installing bazel full-upgrade
sudo apt update && sudo apt full-upgrade
sudo apt update && sudo apt install bazel-3.7.2

#
# The bazel package will always install the latest stable version of
# Bazel. You can install specific, older versions of Bazel in addition
# to the latest one like this:
#
# sudo apt install bazel-1.0.0
#
# This will install Bazel 1.0.0 as /usr/bin/bazel-1.0.0 on your
# system. This can be useful if you need a specific version of Bazel
# to build a project, e.g. because it uses a .bazelversion file to
# explicitly state with which Bazel version it should be built.
#
# Optionally, you can set bazel to a specific version by creating a
# symlink:
#
# sudo ln -s /usr/bin/bazel-1.0.0 /usr/bin/bazel
# bazel --version  # 1.0.0
#

#
# back to the source install - download the tensorflow source
#
# section 3: download tensorflow
mkdir tensorflow
git clone https://github.com/tensorflow/tensorflow.git

#
# the DO CD - MAGIC SECTION TITLE changes the current directory!
#    - REQUIRED for the rest of the process

# section 4a: the cd in the next step is required
pwd

#
# we are moving the the tensorflow directory to configure and
# compile the system
#

# section 4b: DO CD tensorflow
pwd

# configure the build
#
# determine the architecture with which to configure
#
# gcc -march=native -Q --help=target | grep -v valid | grep march
#
# section 5: determine the architecture
echo march=`gcc -march=native -Q --help=target | grep -v valid | grep march | sed -e "s/ //g" -e "s/\t//g" -e "s/-march=//"`
echo "The current recommended ation is to use -march=native, unless there is another specific need."

# section 6a: prepare for ./configure
march=`gcc -march=native -Q --help=target | grep -v valid | grep march | sed -e 's/ //g' -e 's/\t//g' -e 's/-march=//'`;echo "  The next section runs the ./configure script."; echo "  When ./configure asks for options enter your choice for architecture: -march=<choice> -Wno-sign-compare"; echo "  Say no to ROCm, CUDA, and all unless you plan to run with a CUDA board "; echo "  (you do not)."

# section 6b: run ./configure
./configure

# section 7: build non pip standalone tensorflow
bazel build --verbose_failures --config=opt --config=noaws --config=nogcp --config=nohdfs --config=nonccl //tensorflow:tensorflow

# section 8: Build the pip package
bazel build --verbose_failures --config=opt --config=noaws --config=nogcp --config=nohdfs --config=nonccl //tensorflow/tools/pip_package:build_pip_package

# section 9: bazel-bin Build Package
./bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/tensorflow_pkg

# section 10: install the newly created wheel file
pip3 install tensorflow-2.5.0-cp38-cp38-linux_x86_64.whl 

# section 11: stop here
#
#
# https://www.tensorflow.org/install
# https://www.tensorflow.org/learn
# https://www.tensorflow.org/overview
# 
# https://www.tensorflow.org/lite
# https://www.tensorflow.org/lite/guide
# 
# https://www.tensorflow.org/resources/learn-ml

