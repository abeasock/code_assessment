# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 08:31:22 2017

@author: abeasock
"""

import pandas as pd
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.linear_model import LogisticRegression
from sklearn import metrics


pts = pd.read_csv('C:/Users/abeasock/Documents/Data/Medical Appointments/patients.csv')
appts = pd.read_csv('C:/Users/abeasock/Documents/Data/Medical Appointments/appointments.csv')

# 1. Join the two datasets and keep only matching records.
pt_appts = pd.merge(pts, appts, how='inner', left_on='patient_id', right_on='id')

# 2a. Derive a new variable "day_of_week" to provide the day of the week 
#     the appointment was scheduled for.
pt_appts['date'] = pd.to_datetime(pt_appts['appointment_date'])
pt_appts['day_of_week'] = pt_appts['date'].dt.weekday_name

# 2b. Take a frequency count of 'day_of_week' to examine what day of the week 
#     are patients most likely to not show up for an appointment.
pt_appts['day_of_week'].loc[pt_appts['status']=='No-Show'].value_counts()

# 3. Bin the ages into 10 groups and plot status by age. 
pt_appts['age_group'] = pd.cut(pt_appts['age'], [-1,10,20,30,40,50,60,70,80,90,120], labels=['0-10', '10-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90', '90+'])

sns.countplot(y='age_group', hue='status', data=pt_appts)

# 4. Build a basic model to predict whether a patient shows up for their appointment
pt_appts['target'] = pt_appts['status'].apply(lambda x: 1 if x == 'No-Show' else 0)


# Using `LabelEncoder` to encode strings. This method assigns NaN values to category.
le = LabelEncoder()
pt_appts['gender'] = le.fit_transform(pt_appts['gender'])
pt_appts['sms_reminder'] = le.fit_transform(pt_appts['sms_reminder'])
pt_appts['day_of_week'] = le.fit_transform(pt_appts['day_of_week'])
pt_appts.drop(['id', 'date', 'appointment_date', 'appointment_registration', 'status', 'age_group'], axis=1, inplace=True)


# Set the predictor variables and target variable
target = pt_appts['target']
predictors = pt_appts.drop(['target'], axis=1)

# Partition pt_appts into TRAIN and TEST datasets (70% Train VS 30% Test)
seed = 2342

sss = StratifiedShuffleSplit(target, n_iter=1, test_size=0.3, random_state=seed)

for train_index, test_index in sss:
    X_train, X_test = predictors.iloc[train_index], predictors.iloc[test_index]
    y_train, y_test = target[train_index], target[test_index]
    
# Logistic Regression    
lr = LogisticRegression()

# fit the model
lr.fit(X_train, y_train)

# Make Predictions
lr_predicted = lr.predict(X_test)


print "Logisitic Regression: \n   Accuracy Score:  " + \
      str(format(metrics.accuracy_score(y_test, lr_predicted), '.3f'))  + \
    "\n\nConfusion Matrix: \n" + \
    str(metrics.confusion_matrix(y_test, lr_predicted)) + \
    "\n(row=expected, col=predicted)" 
    
probas = lr.predict_proba(X_test)
lr_preds = probas[:,1]

# calculate the fpr and tpr for all thresholds of the classification
lr_fpr, lr_tpr, lr_threshold = metrics.roc_curve(y_test, lr_preds)
lr_roc_auc = metrics.auc(lr_fpr, lr_tpr)

print "The Area Under the ROC Curve: %f" % lr_roc_auc + \
      "\nGini: " + str(format(2*lr_roc_auc-1, '.3f'))
    
# plot ROC curve
plt.title('ROC Curve')
plt.plot(lr_fpr, lr_tpr, 'b', label = 'AUC = %0.2f' % lr_roc_auc)
plt.legend(loc = 'lower right')
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0, 1])
plt.ylim([0, 1])
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show()