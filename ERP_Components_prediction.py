import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.metrics import confusion_matrix

def predict(input_csv):
  new_model = tf.keras.models.load_model('D:\\Documents\\FYP\\trial2(backend)\\Uploads\\ERP_Component_Model')
  data = pd.read_csv(input_csv)
  testData = np.genfromtxt(input_csv, delimiter=',')
  t=testData.tolist()
  testData=np.array([t])
  Y_pred=new_model.predict(testData)
  Y_pred = (Y_pred < 0.5).astype(int)
  if np.argmax(Y_pred,axis=1) == [1]:
    return print("Schizophrenic")
  else:
    return print("Non Schizophrenic")
