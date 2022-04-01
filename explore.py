import warnings
warnings.filterwarnings("ignore")

# STANDARD LIBRARIES
import pandas as pd
import numpy as np

# THIRD PARTY LIBRARIES
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler

# create a function that takes in a dataframe
def plot_variable_pairs(df):
    # plot the columns in a pairplot
    sns.pairplot(train, kind = 'reg', corner = True, plot_kws={'line_kws':{'color':'red'}})
    plt.show()
    

# create a function that accepts
def months_to_years(df, target):
    # create a new column that takes tenure months and converts them to complete years
    df[target]= df.monthly_tenure // 12
    # return the dataframe
    return df
    
    
# function to plot categorical and continuous variables
def plot_categorical_and_continuous(df, cat_col_name, cont_col_name):
   #Plot distribution of categorical variable
    sns.boxplot(df[cat_col_name])
    #labels
    plt.title(cat_col_name)
    plt.xlabel(cat_col_name)
    plt.ylabel('Frequency')
    plt.show()
    #Plot distribution of continuous variable
    sns.distplot(df[cont_col_name])
    #labels
    plt.title(cont_col_name)
    plt.xlabel(cont_col_name)
    plt.ylabel('Frequency')
    plt.show()
    #Plot categorical and continuous variable together
    sns.jointplot(x=cat_col_name, y=cont_col_name, data=df, kind='reg')
    plt.show()
    return df





    
def scale_telco(train, validate, test, scaler_type = MinMaxScaler()):
    features_to_scale = ['monthly_charges', 'tenure']
    other_features = ['customer_id']
    target = 'total_charges'


    # establish empy dataframes for storing scaled datasets
    train_scaled = pd.DataFrame(index = train.index)
    validate_scaled = pd.DataFrame(index = validate.index)
    test_scaled = pd.DataFrame(index = test.index)

    # create and fit the scaler
    scaler = scaler_type.fit(train[features_to_scale])


    # adding scaled features to the scaled dataframes
    train_scaled[features_to_scale] = scaler.transform(train[features_to_scale])
    validate_scaled[features_to_scale] = scaler.transform(validate[features_to_scale])
    test_scaled[features_to_scale] = scaler.transform(test[features_to_scale])


    # adding features that are not scaled back to the dataframe. 

    train_scaled[other_features] = train[other_features]
    validate_scaled[other_features] = validate[other_features]
    test_scaled[other_features] = test[other_features]


    # adding target variable to the dataframe

    train_scaled[target] = (train[target])
    validate_scaled[target] = (validate[target])
    test_scaled[target] = (test[target])

    return train_scaled, validate_scaled, test_scaled



'''    
    # function that plots variable pairs and returns a list of the plots
def plot_variable_pairs(df):
    sns.pairplot(df)
    sns.set(style='whitegrid', palette='muted')
    return plt.show()
'''
    