# tensorflow-non-avx-ubuntu-20
This github entry includes scripts and pointers to python wheel[s] file[s] for using TensorFlow on older Intel computers.  This work was currently performed on Ubuntu 20.04 using the directions from the Tensorflow web site.

https://www.tensorflow.org/install/source

The compilations disable the Intel AVX op codes and specify the widely compaitible Intel architecture, core2.  Use the following gcc command to check your architecure:

gcc -march=native -Q --help=target

The TensorFlow website instructions are very complete and can be completed with some patience.  As the process for creating a new wheel file for use with python is fairly tedious, a pointer to our wheel file is provided with a checksum script for verifying the file.

https://drive.google.com/drive/folders/1W2yNGUshzrZwub7OPFGRMLMQvt-RluFZ?usp=sharing

Installing the TensorFlow package for python using the TensorFLow wheel file is a one step process:

pip install <file>
  
We include a python script, Chollet_example.py, which includes the complete tutorial from the tensorflow wedsite:
 
 https://www.tensorflow.org/tutorials/keras/classification
 
 Running that python file is a quick way to test the Tensorflow install and familiarize yourslef with the Tensorflow process.
 
