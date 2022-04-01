# STANDARD LIBRARIES
import os

# THIRD PARTY LIBRARIES
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

# LOCAL LIBRARIES
import acquire
import env



def get_zillow_data(use_cache=True):
    '''
    This function acquires the zillow database in SQL. The function requires the
    use of a personalized .env file that contains the user, password, and host credentials.
    It acquires the bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, taxvaluedollarcnt, 
    yearbuilt, taxamount, and fips from the zillow database for all 'Single Family Residential' 
    properties. It identifies the Single Family Residential Properties by filtering 
    for for only those with the '261' propertylandusetypeid that matches the propertylandusetypeid 
    identifying as single-family residential homes in the propertylandusetype table. 
    It returns a dataframe and caches the dataframe 
    (saving it to a .csv file, titled: 'zillow_values.csv'), 
    for faster processing after initial acquisition. The resulting dataframe 
    contains all the selected columns. 
    '''
    
    filename = 'zillow_values.csv'
    
    if os.path.exists(filename):
        print('Reading from csv file...')
        return pd.read_csv(filename)
    
    
    url = f'mysql+pymysql://{env.user}:{env.password}@{env.host}/zillow'
    query =''' 
    SELECT bedroomcnt AS bedrooms, 
                    bathroomcnt AS bathrooms, 
                    calculatedfinishedsquarefeet AS square_feet, 
                    taxvaluedollarcnt AS tax_assessed_value_USD,
                    yearbuilt AS year_built, 
                    taxamount AS tax_amount, 
                    fips AS fed_code
    FROM properties_2017
    
    
    LEFT JOIN propertylandusetype USING(propertylandusetypeid)

    WHERE propertylandusedesc IN ("Single Family Residential",                       
                              "Inferred Single Family Residential"); 
    '''

    print('Getting a fresh copy from SQL database...')
    df = pd.read_sql(query, url)
    print('Saving to csv...')
    df.to_csv(filename, index=False)
    return df


def wrangle_zillow(df):
    '''
    This function takes in a dataframe, sets a dictionary variable that will be used
    to convert data types, drops all rows with null values within the dataframe, then reassigns
    the datatypes to be more functional for exploring and modeling; making fed_code an object,
    as it will not be used in arithmetic, and converts year_built to an int instead of a float in 
    anticipation of applying arithmetic operations using it. 
    '''
    
    convert_dict = {'fed_code': object,
                'year_built': int
               }
     

    # drop rows with nulls
    df = df.dropna(axis = 0)
    
    # convert datatypes
    df = df.astype(convert_dict)
    
    return df


def get_telco_data(use_cache=True):
    filename = 'telco_churn.csv'
    
    if os.path.exists(filename):
        print('Reading from csv file...')
        return pd.read_csv(filename)
    
    
    url = f'mysql+pymysql://{env.user}:{env.password}@{env.host}/telco_churn'
    query = '''
    SELECT customer_id, monthly_charges,tenure 
        FROM customers
        
    '''

    print('Getting a fresh copy from SQL database...')
    df = pd.read_sql(query, url)
    print('Saving to csv...')
    df.to_csv(filename, index=False)
    return df


def wrangle_telco():
    # get dataframe using get_telco_data function
    df = get_telco_data()
    
    # rename column
    df = df.rename(columns={'tenure': 'monthly_tenure'})
    
    return df


def data_split(df, target):
    '''
    This function drops the customer_id column and then splits a dataframe into 
    train, validate, and test in order to explore the data and to create and validate models. 
    It takes in a dataframe and contains an integer for setting a seed for replication. 
    Test is 20% of the original dataset. The remaining 80% of the dataset is 
    divided between valiidate and train, with validate being .30*.80= 24% of 
    the original dataset, and train being .70*.80= 56% of the original dataset. 
    The function returns, train, validate and test dataframes. 
    '''
    df = df.drop(columns=['customer_id'])
    train, test = train_test_split(df, test_size = .2, random_state=123)   
    train, validate = train_test_split(train, test_size=.3, random_state=123)


    print(f'train -> {train.shape}')
    print(f'validate -> {validate.shape}')
    print(f'test -> {test.shape}')
    
    return train, validate, test


















def scale_telco(train, validate, test, scaler_type = MinMaxScaler()):
    
    
    '''
    This function takes in the train validate and test dataframes, columns you want to scale (as a list), 
    a scaler (i.e.MinMaxScaler(), with whatever paramaters you need),
    scaler_name as a string.
    col_names: list of columns to scale
    Scaler_name, should be what you want in the name of your new dataframe columns.
    Adds columns to the train validate and test dataframes. 
    Outputs scaler for doing inverse transforms.
    Ouputs a list of the new column names (what you can use to create the X_train).
    
    example: min_max_scaler, scaled_cols_list = my_scaler(train, validate, test, MinMaxScaler(), 'scaled_min_max')
    
    '''
    
    
    
    
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
    
    train_scaled[other_features] = scaler.transform(train[other_features])
    validate_scaled[other_features] = scaler.transform(validate[other_features])
    test_scaled[other_features] = scaler.transform(test[other_features])
    
    
    # adding target variable to the dataframe
    
    train_scaled[target] = (train[target])
    validate_scaled[target] = (validate[other_features])
    test_scaled[target] = (test[other_features])
    
    return train_scaled, validate_scaled, test_scaled
    

    

