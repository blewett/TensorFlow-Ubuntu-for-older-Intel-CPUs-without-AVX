# tensorflow-non-avx-ubuntu-20
This github entry includes scripts and pointers to python wheel[s] file[s] for using TensorFlow on older Intel computers.  This work was processed using Ubuntu 20.04 and followed the instructions from the TensorFlow web site listed below:

  https://www.tensorflow.org/install/source

This compilation disabled the Intel AVX op codes and specified the widely compatible Intel architecture, core2.  Use the following gcc command to check your architecture:

  gcc -march=native -Q --help=target | grep march

The TensorFlow website instructions are very complete and can be completed easily - with some patience.  OK, the process for creating a new wheel file for use with python is fairly tedious.  This page includes a pointer to our wheel file and a checksum script to verify the file.

  https://drive.google.com/drive/folders/1W2yNGUshzrZwub7OPFGRMLMQvt-RluFZ?usp=sharing

Installing the TensorFlow package for python using the TensorFlow wheel file is a one step process:

pip install file
  
We include a python script, Chollet_example.py, which includes the complete tutorial from the tensorflow wedsite:
 
  https://www.tensorflow.org/tutorials/keras/classification
 
Running the Chollet python file is a quick way to test the Tensorflow install and familiarize yourself with the Tensorflow process.
 
