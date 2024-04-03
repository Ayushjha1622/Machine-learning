# -*- coding: utf-8 -*-
"""K22SK_Regression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1y4i4zqxGwzkwofupngsfW_yREagto8X7
"""

import pandas as pd
dataset=pd.read_csv('/content/auto-mpg.csv',
                    header=None, na_values='?', sep='\s+')

dataset.shape

dataset.isna().sum()

dataset=dataset.dropna()

dataset.shape

from sklearn.preprocessing import LabelEncoder
le=LabelEncoder()
dataset[8]=le.fit_transform(dataset[8])
dataset.head()

import matplotlib.pyplot as plt
import seaborn as sns
sns.pairplot(dataset)
plt.show()

import numpy as np
corr=np.corrcoef(dataset.values.T)
hm=sns.heatmap(corr, annot=True)
plt.show()

dataset=dataset.drop(columns=[6,8])

dataset.shape

target=dataset[1]
features=dataset.drop(columns=[1])
print(features.head())

from sklearn.model_selection import train_test_split
xtrain, xtest, ytrain, ytest=train_test_split(features, target, test_size=0.15)
print(xtrain.shape)
print(xtest.shape)

print(xtrain.describe())

from sklearn.preprocessing import StandardScaler
sc=StandardScaler()
xtrain_sc=sc.fit_transform(xtrain)
xtest_sc=sc.transform(xtest)

from sklearn.linear_model import LinearRegression
lr=LinearRegression()
lr.fit(xtrain_sc, ytrain)

lr_train_results=lr.predict(xtrain_sc)
lr_test_results=lr.predict(xtest_sc)

from sklearn.metrics import mean_squared_error, r2_score
print("Training Results:")
print("MSE:", mean_squared_error(ytrain, lr_train_results))
print("R2 Score:", r2_score(ytrain, lr_train_results))

print("Testing Results:")
print("MSE:", mean_squared_error(ytest, lr_test_results))
print("R2 Score:", r2_score(ytest, lr_test_results))

from sklearn.linear_model import RANSACRegressor

ransac=RANSACRegressor(LinearRegression(), min_samples=50, residual_threshold=0.5)
ransac.fit(xtrain_sc, ytrain)

print(ransac.inlier_mask_)

print(np.sum(ransac.inlier_mask_==True))

outlier=np.logical_not(ransac.inlier_mask_)
print(outlier)

ransac_train_results=ransac.predict(xtrain_sc)
ransac_test_results=ransac.predict(xtest_sc)
print("Training Results:")
print("MSE:", mean_squared_error(ytrain, ransac_train_results))
print("R2 Score:", r2_score(ytrain, ransac_train_results))
print("Testing Results:")
print("MSE:", mean_squared_error(ytest, ransac_test_results))
print("R2 Score:", r2_score(ytest, ransac_test_results))

input=dataset[2]

input.shape

target.shape

plt.scatter(input, target)
plt.show()

trainx, testx, trainy,testy=train_test_split(input, target, test_size=0.15)

trainx=np.array(trainx).reshape(-1,1)
testx=np.array(testx).reshape(-1,1)

lr1=LinearRegression()
lr1.fit(trainx, trainy)

lr1_train=lr1.predict(trainx)
lr1_test=lr1.predict(testx)

print("Training Results:")
print("MSE:", mean_squared_error(trainy, lr1_train))
print("R2 Score:", r2_score(trainy, lr1_train))
print("Testing Results:")
print("MSE:", mean_squared_error(testy, lr1_test))
print("R2 Score:", r2_score(testy, lr1_test))

sorted_input=np.sort(trainx)
plt.scatter(trainx, trainy)
plt.plot(trainx, lr1.predict(trainx), c='red', marker='*')
plt.plot()

ransac1=RANSACRegressor(LinearRegression(), min_samples=50, residual_threshold=0.5)
ransac1.fit(trainx, trainy)

ransac1_train_results=ransac1.predict(trainx)
ransac1_test_results=ransac1.predict(testx)
print("Training Results:")
print("MSE:", mean_squared_error(ransac1_train_results, trainy))
print("R2 Score:", r2_score(ransac1_train_results, trainy))
print("Testing Results:")
print("MSE:", mean_squared_error(ransac1_test_results, testy))
print("R2 Score:", r2_score(ransac1_test_results, testy))

print(np.sum(ransac1.inlier_mask_==True))

inlier=ransac1.inlier_mask_
outlier=np.logical_not(inlier)
plt.scatter(trainx[inlier], trainy[inlier], c='green', label="Inlier")
plt.scatter(trainx[outlier], trainy[outlier], c='red', label="Outlier")
plt.plot(trainx, ransac1.predict(trainx), marker='*', label="Regression Line")
plt.legend()
plt.show()



"""Polynomial **Regression**

"""

from sklearn.preprocessing import PolynomialFeatures

poly=PolynomialFeatures(degree=2)
poly_2_train=poly.fit_transform(trainx)
poly_2_test=poly.transform(testx)

poly_2_train.shape

lr_poly=LinearRegression()
lr_poly.fit(poly_2_train, trainy)

poly2_train_results=lr_poly.predict(poly_2_train)
poly2_test_results=lr_poly.predict(poly_2_test)
print("Training Results:")
print("MSE:", mean_squared_error(poly2_train_results, trainy))
print("R2 Score:", r2_score(poly2_train_results, trainy))
print("Testing Results:")
print("MSE:", mean_squared_error(poly2_test_results, testy))
print("R2 Score:", r2_score(poly2_test_results, testy))

input=sorted(trainx)
plt.scatter(trainx, trainy)
plt.plot(input, lr1.predict(input), c='green', label="Linear")
plt.plot(input, lr_poly.predict(poly.fit_transform(input)), c='red', marker='*', label="Polynomial degree 2")
plt.legend()
plt.show()



"""Regularized Methods of Regression"""

from sklearn.linear_model import Lasso
l1=Lasso()
l1.fit(trainx, trainy)
l1_train_results=l1.predict(trainx)
l1_test_results=l1.predict(testx)
print("Training Results:")
print("MSE:",mean_squared_error(l1_train_results, trainy))
print("R2 Score:", r2_score(l1_train_results, trainy))
print("Testing Results:")
print("MSE:", mean_squared_error(l1_test_results, testy))
print("R2 Score:", r2_score(l1_test_results, testy))

plt.scatter(trainx, trainy)
plt.plot(input, l1.predict(input), c='red', label="Lasso")
plt.legend()
plt.show()

from sklearn.linear_model import Ridge
l2=Ridge()
l2.fit(trainx, trainy)
l2_train_results=l2.predict(trainx)
l2_test_results=l2.predict(testx)
print("Training Results:")
print("MSE:", mean_squared_error(l2_train_results, trainy))
print("R2 Score: ", r2_score(l2_train_results, trainy))
print("Testing Results:")
print("MSE:", mean_squared_error(l2_test_results, testy))
print("R2 Score:", r2_score(l2_test_results, testy))

plt.scatter(trainx, trainy)
plt.plot(input, l1.predict(input), c='red', label="Lasso")
plt.plot(input, l2.predict(input), c="green", label="Ridge")
plt.legend()
plt.show()

from sklearn.linear_model import ElasticNet
l12=ElasticNet()
l12.fit(trainx, trainy)
l12_train_results=l12.predict(trainx)
l12_test_results=l12.predict(testx)
print("Training Results:")
print("MSE:", mean_squared_error(l12_train_results, trainy))
print("R2 Score:",r2_score(l12_train_results, trainy))
print("Testing Results:")
print("MSE:", mean_squared_error(l12_test_results, testy))
print("R2 Score:",r2_score(l12_test_results, testy))



"""DecisionTree Regressor"""

from sklearn.tree import DecisionTreeRegressor
dt=DecisionTreeRegressor()
dt.fit(trainx, trainy)
dt_train_results=dt.predict(trainx)
dt_test_results=dt.predict(testx)
print("Training Results:")
print("MSE:", mean_squared_error(dt_train_results, trainy))
print("R2 Score:", r2_score(dt_train_results, trainy))
print("Testing Results:")
print("MSE:", mean_squared_error(dt_test_results, testy))
print("R2 Score:", r2_score(dt_test_results, testy))

input_test=sorted(testx)
plt.scatter(trainx, trainy)
plt.plot(input, dt.predict(input), c='red', label="Training Result")
plt.plot(input_test, dt.predict(input_test), c='blue', label="Testing Results")
plt.legend()
plt.show()

from sklearn.svm import SVR
svr=SVR()
svr.fit(trainx, trainy)
svr_train_results=svr.predict(trainx)
svr_test_results=svr.predict(testx)
print("Training Results:")
print("MSE:", mean_squared_error(svr_train_results, trainy))
print("R2 Score:",r2_score(svr_train_results, trainy))
print("Testing Results:")
print("MSE:", mean_squared_error(svr_test_results, testy))
print("R2 Score:", r2_score(svr_test_results, testy))

plt.scatter(trainx, trainy)
plt.plot(input, svr.predict(input), c='red')
plt.plot(input_test, svr.predict(input_test), c='green')
plt.show()

