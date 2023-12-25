
import pandas as pd
import numpy as np
import torch 
import torch.nn as nn
import torch.nn.functional as F


class NetNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 2, (9,48))
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(2, 1, 1)
        self.fc1 = nn.Linear(3028, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 2)

    def forward(self, x, mx):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.conv2(x)
        x = F.relu(x)
        o = []
        x = torch.flatten(x, 1) # flatten all dimensions except batch
        x = torch.cat((x,mx), axis=1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)
        x = F.relu(x)
        x = self.fc3(x)
        return x


def predict(in1, in2):
    df = pd.read_csv(in1)
    meta_df = pd.read_csv(in2)
    data_list = []
    data_list_m = []
    for i in range(1):
        df_subcon = df.drop(['subject','condition','time_ms'],axis=1)
        record = df_subcon.to_numpy()
        record = np.transpose(record)    
        record = record.tolist()
        dummy = []
        dummy.append(record)
        data_list.append(dummy)

        df_subcon_m = meta_df.drop(['Unnamed: 0','subject',' group'],axis=1)
        df_subcon_m = df_subcon_m.replace(' M',0)
        df_subcon_m = df_subcon_m.replace(' F',1)
        record_m = df_subcon_m.to_numpy()
        record_m = np.transpose(record_m)    
        record_m = record_m.tolist()
        dummy_m = []
        dummy_m.append(record_m)
        data_list_m.append(dummy_m)

    X = torch.Tensor(data_list)
    X_m = torch.Tensor(data_list_m).reshape((1,3))

    model = NetNN()
    model.load_state_dict(torch.load('D:\\Documents\\FYP\\trial2(backend)\\Uploads\\erp_training_model'))
    model.eval()
    out = model(X,X_m)
    if out.argmax(dim=1)[0] == 1:
        return print('Schizophrenic')
    else:
        return print('Non-Schizophrenic')
