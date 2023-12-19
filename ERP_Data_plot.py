import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def predict(input_csv):
  data = pd.read_csv(input_csv)
  data_melt = data.melt(id_vars=["subject","condition","time_ms"])
  sns.set(rc = {'figure.figsize':(150,30)})
  sns.lineplot(x = "time_ms", y = "value", data = data_melt, hue = "variable")
  plt.ylabel("EEG electrode value")
  plt.xticks(rotation = 25)
  plt.savefig('ERP_data.png')
  
