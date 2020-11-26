from insert_errors import (
    insert_maxim_temperature_errors, get_meas_cols
)
from adaptive_module_discrete.one_step import OneStep
import pandas as pd

def run_sim(csv_filepath, csv_writeout_filepath):
    # Filepath is the filepath to a CSV file that has no errors inserted
    # Insert errors and return edited pandas dataframe
    error_df = insert_maxim_temperature_errors(csv_filepath, csv_writeout_filepath) 

    # Go through dataframe datapoint by datapoint and simulate
    meas_cols = get_meas_cols(error_df)
    for row in error_df.itertuples():
        idx = row.Index

        for meas_col in meas_cols:
            


