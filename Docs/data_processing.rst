
Data Pre-processing and Transformation Script
============================================

This script reads a CSV file containing budget data, performs data pre-processing and transformation on the rows and columns, and exports the resulting clean DataFrame to a new CSV file.


Data Pre-processing Steps
--------------------------

Steps 1. 

Reads the input CSV file, performs data pre-processing on rows and columns, and returns a clean DataFrame.
The function reads the CSV file using the pandas library, skips unnecessary rows, and drops empty columns. Further, it renames the columns for better understanding and fills in missing values in the 'DmdCD' column. Finally filters out rows with 'Total' in the 'HOA' column.

.. code-block:: python

    def data_pre_processing(filename):  
        df = pd.read_csv(file, skiprows=1, header=None)
        df = df.drop([0, 1])               # drops 1st & Grand Total rows
        df = df.drop([8,9,10,11], axis=1)  # drops empty columns

        old_column_names = [0, 1, 2, 3, 4, 5, 6, 7]
        new_column_names = ['DmdCd', 'HOA', 'Sanction Budget (April)', 'Addition', 'Saving', 'Revised Budget (A)',
                          ' Expenditure (within selected period) (B)', 'Balance (A-B)']
        df.rename(columns=dict(zip(old_column_names, new_column_names)), inplace=True)  # renames the columns 
  
        df['DmdCd'].fillna(method='ffill', inplace=True)  # fills DmdCd columns with relevant data
        df = df[df['HOA'] != 'Total']   # filters out the row with row item 'Total' in the 'HOA' column 

        return df

Step 2. 

The function splits the 'DmdCd' & 'HOA' columns based on  '-' delimiter, renames the split columns, and returns the re-ordered dataframe. Initially, the function splits the 'DmdCd' column and renames it into 'DemandCode' and 'Demand', next it splits 'HOA' column creating new columns for each split, and the split columns are renamed accordingly. Unnecessary columns are dropped and the remaining columns are re-ordered.

.. code-block:: python

    def split_columns_and_rename(df):
        df[['DemandCode', 'Demand']] = df['DmdCd'].str.split('-', n=1, expand=True)
        df = df.drop(columns='DmdCd')
        split_columns = df["HOA"].str.split("-", expand=True)  
        df = pd.concat([df, split_columns], axis=1)
  
        split_column_names = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        split_column_new_names = ['MajorHead', 'SubMajorHead', 'MinorHead', 'SubMinorHead', 'DetailHead', 'SubDetailHead',
                                'BudgetHead', 'PlanNonPlan', 'VotedCharged', 'StatementofExpenditure']  
        df.rename(columns=dict(zip(split_column_names, split_column_new_names)), inplace=True)
  
        df = df.drop([10, 11, 12], axis=1)
        df = df.drop(columns='HOA')
  
        columns = list(df.columns)            
        df = df[columns[-12:] + columns[0:6]] 
  
        return df

Step 3.

Finally, the main processing function Orchestrates the data processing steps using the above functions, and returns processed DataFrame.

.. code-block:: python

   def clean_dataset():
    '''Orchestrates the data processing steps using the above functions and returns the final processed DataFrame.'''

    input_filename = path.abspath(path.join("../data/treasury_data.csv"))
    output_filename = path.abspath(path.join("../data/hp_oltis_sanctioned_budget"))

    budget_data_df = data_pre_processing(input_filename)
    updated_budget_data_df = split_columns_and_rename(budget_data_df)
    
    updated_budget_data_df.to_csv(output_filename, index=False)
        
    return output_file

