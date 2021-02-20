import tensorflow as tf
import numpy as np 
from tensorflow import keras
from tensorflow.contrib import lite 


converter = lite.TocoConverter.from_keras_model_file("mask5_detector.model.h5")
tflite_model = converter.convert()
open("mask.tflite" , "wb").write(tflite_model)