import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as pt
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.tree import DecisionTreeClassifier

dataset=pd.read_csv("cpdata.csv")
#print(dataset)
X=dataset.iloc[:,[2]].values
Y=dataset.iloc[:,[4]].values

Xtrain,Xtest,Ytrain,Ytest=train_test_split(X,Y,test_size=0.25)




print("Xtest is...")
print(Xtest)

classifier=KNeighborsClassifier(n_neighbors=5, p=2, weights='uniform', algorithm='auto')
#KNeighborsClassifier(n_neighbors=5, p=2, weights='uniform', algorithm='auto')
Ytrain=np.ravel(Ytrain)
classifier.fit(Xtrain,Ytrain)

#Xtest=[[6.23],[2.10],53.00,22.00,25.00] ]

Ypred=classifier.predict((Xtest))
print("Yprediction is...")
print(Ypred)


cm=confusion_matrix(Ytest,Ypred)
#print("Confusion matrix is")
#print(cm)


ac = accuracy_score(Ytest,Ypred)
print("Accuracy ",ac)


DT_pkl_filename = 'Knnnew.pkl'
# Open the file to save as pkl file
DT_Model_pkl = open(DT_pkl_filename, 'wb')
pickle.dump(classifier, DT_Model_pkl)
# Close the pickle instances
DT_Model_pkl.close()

