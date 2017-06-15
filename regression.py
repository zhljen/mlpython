import pandas as pd
import quandl, math
import numpy as np
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression

df = quandl.get('WIKI/GOOGL')
df = df[['Adj. Open','Adj. High','Adj. Low','Adj. Close', 'Adj. Volume']]
df['HL_PCT'] = (df['Adj. High'] - df['Adj. Close']) / df['Adj. Close'] * 100.0
df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open'] * 100.0
#features
df = df[['Adj. Close','HL_PCT','PCT_change', 'Adj. Volume']]

forecast_col = 'Adj. Close'
df.fillna(-99999, inplace=True)

# 10% out of the data points
forecast_out = int(math.ceil(0.01*len(df)))

print(forecast_out)
df['label'] = df[forecast_col].shift(-forecast_out)
df.dropna(inplace=True)


X = np.array(df.drop(['label'],1))
y = np.array(df['label'])
X = preprocessing.scale(X)
#df.dropna(inplace=True)
y = np.array(df['label'])
print(len(X), len(y))
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)
# linear is good
clf = LinearRegression()
#try to use svm, which is quite worse
#clf = svm.SVR(kernel='poly')
clf.fit(X_train, y_train)
accuracy = clf.score(X_test, y_test)


print(accuracy)
# print (df.head())