import pandas as pd
from sklearn.model_selection import train_test_split
# import torch.nn as nn
# from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn import svm
from sklearn.utils import shuffle

class Predictor:
    def __init__(self):
        self.X, self.y = self._prepare_dataset()
        self.model = self._init_model()
    
    def _prepare_dataset(self):
        data = pd.read_csv('credit_risk_dataset.csv')
        data = data.dropna()
        data_zeros = data[data['loan_status'] == 1]
        data_ones = data[data['loan_status'] == 0].head(len(data_zeros))
        data = pd.concat([data_zeros, data_ones])
        one_hot_encoding_cols = ['person_home_ownership', 'loan_intent', 'loan_grade', 'cb_person_default_on_file']
        data = pd.get_dummies(data, columns=one_hot_encoding_cols)
        data = shuffle(data)
        scaler = StandardScaler()
        # loan_status = data['loan_status'].copy()
        data.iloc[:,:] = scaler.fit_transform(data.iloc[:,:].to_numpy())
        # data['loan_status'] = loan_status

        return data.drop(['loan_status'], axis=1), data['loan_status']

    def _init_model(self):
        print(self.y)
        model = RandomForestClassifier(n_estimators=5).fit(self.X, self.y)

        return model

    def _preprocess(self, data):  
        data = data.fillna(0)      
        one_hot_encoding_cols = ['person_home_ownership', 'loan_intent', 'loan_grade', 'cb_person_default_on_file']
        data = pd.get_dummies(data, columns=one_hot_encoding_cols)
        for col in self.X.columns:
            print(col)
            if not col in data.columns:
                data[col] = 0

        scaler = StandardScaler()
        data.iloc[:,:] = scaler.fit_transform(data.iloc[:,:].to_numpy()) # ????
        
        return data

    def predict(self, data):
        data = pd.DataFrame([data])
        data = self._preprocess(data)
        data = data[self.X.columns]
        print(data.columns)
        predict = self.model.predict(data)

        return predict
