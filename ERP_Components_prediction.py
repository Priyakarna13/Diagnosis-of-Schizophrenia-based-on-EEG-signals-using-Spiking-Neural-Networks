import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.metrics import confusion_matrix

def predict(input_csv):
  new_model = tf.keras.models.load_model('ERP_Component_Model')
  data = pd.read_csv(input_csv)
  testData = np.genfromtxt(input_csv, delimiter=',',ndmin=2)
  Y_pred=new_model.predict(testData)
  Y_pred = (Y_pred < 0.5).astype(int)
  if np.argmax(Y_pred,axis=1) == [1]:
    return "Schizophrenic"
  else:
    return "Non Schizophrenic"
