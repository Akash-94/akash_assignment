#!/usr/bin/env python

import pandas as pd
from os import path
import logging

logging.basicConfig(
    level=logging.INFO,
    filename='preprocessing.log',
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def data_pre_processing(filename):
    '''Reads the input CSV file, performs data pre-processing on rows and columns, and returns a clean DataFrame.'''
    
    logger = logging.getLogger("DataPreProcessing")
    logger.info("Starting data pre-processing...")
    
    df = pd.read_csv(filename, skiprows=1, header=None)
    df = df.drop([0, 1])               # drops 1st & Grand Total rows
    df = df.drop([8,9,10,11], axis=1)  # drops empty columns

    old_column_names = [0, 1, 2, 3, 4, 5, 6, 7]
    new_column_names = ['DmdCd', 'HOA', 'Sanction Budget (April)', 'Addition', 'Saving', 'Revised Budget (A)',
                        ' Expenditure (within selected period) (B)', 'Balance (A-B)']
    df.rename(columns=dict(zip(old_column_names, new_column_names)), inplace=True)  # renames the columns 

    df['DmdCd'].fillna(method='ffill', inplace=True)  # fills DmdCd columns with relevant data
    df = df[df['HOA'] != 'Total']   # filters out the row with row item 'Total' in the 'HOA' column 

    logger.info("Data pre-processing completed.")
    return df


def split_columns_and_rename(df):
    '''Splits the desired columns (in this case 'DmdCd', HOA) w.r.t '-' delimiter,
        renames the split columns and returns the re-orderd dataframe'''
    
    logger = logging.getLogger("SplitColumnsAndRename")
    logger.info("Starting splitting columns and renaming...")

    df[['DemandCode', 'Demand']] = df['DmdCd'].str.split('-', n=1, expand=True)  # splits DmdCd column and rename it to DemandCode and Demand respectively
    df = df.drop(columns='DmdCd')
    split_columns = df["HOA"].str.split("-", expand=True)  # splits HOA column
    df = pd.concat([df, split_columns], axis=1)

    split_column_names = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    split_column_new_names = ['MajorHead', 'SubMajorHead', 'MinorHead', 'SubMinorHead', 'DetailHead', 'SubDetailHead',
                              'BudgetHead', 'PlanNonPlan', 'VotedCharged', 'StatementofExpenditure']  # renames the split columns
    df.rename(columns=dict(zip(split_column_names, split_column_new_names)), inplace=True)

    df = df.drop([10, 11, 12], axis=1)
    df = df.drop(columns='HOA')

    columns = list(df.columns)            # converts the columns in to list
    df = df[columns[-12:] + columns[0:6]] # re-orders the cloumns

    logger.info("Splitting columns and renaming completed.")
    return df


def clean_dataset():
    '''Orchestrates the data processing steps using the above functions and returns the final processed DataFrame.'''
    
    logger = logging.getLogger("CleanDataset")

    input_filename = path.abspath(path.join("../data/treasury_data.csv"))
    output_filename = path.abspath(path.join("../data/hp_oltis_sanctioned_budget"))
        
    logger.info("Starting data cleaning and processing...")

    budget_data_df = data_pre_processing(input_filename)
    updated_budget_data_df = split_columns_and_rename(budget_data_df)
    
    logger.info("Writing processed data to CSV...")
    updated_budget_data_df.to_csv(output_filename, index=False)

    logger.info("Data cleaning and processing completed...")
        
    return output_filename
    
if __name__ == "__main__":
    output_filename = clean_dataset()



