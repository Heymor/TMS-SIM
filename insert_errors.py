import pandas as pd
import random
import sys
import struct

def float_to_bits(f):
    s = struct.pack('>f', f)
    return struct.unpack('>L', s)[0]

def bits_to_float(b):
    s = struct.pack('>L', b)
    return struct.unpack('>f', s)[0]

def float_to_maxim(f):
    return None

def maxim_to_float(m):
    # TODO
    return None

def insert_error(data_point):
    if random.random() > 0.5:
        # Flip random bit
        # First unpack the float
        data_point = float_to_bits(data_point)

        # Get random bit position
        num_bits = sys.getsizeof(data_point)
        rand_bit = random.randrange(num_bits)

        # Flip bit
        data_point ^= 1 << rand_bit

        # Change back to float
        data_point = bits_to_float(data_point)

    return data_point

def insert_maxim_error(data_point):
    if random.random() > 0.5:
        # Flip a random bit
        # First translate from temperature point to maxim 
        data_point = float_to_maxim(data_point)

        # Get a random bit position
        num_bits = sys.getsizeof(data_point)
        rand_bit = random.randrange(num_bits)

        # Flip bit
        # This is assuming it's an int
        data_point ^= 1 << rand_bit

        # Change back to float
        data_point = maxim_to_float(data_point)

    return data_point

def get_meas_cols(dataframe):
    # Gets the indexes of measurements
    meas_cols = []
    i = 0
    for col in dataframe.columns.values:
        if("bus" in col):
            meas_cols.append(i)
        i += 1
    
    return meas_cols

def insert_temperature_errors(csv_filepath, csv_writeout_filepath):
    run_data_frame = pd.read_csv(filepath=csv_filepath)

    meas_cols = get_meas_cols(run_data_frame)
    for row in run_data_frame.itertuples():
        idx = row.Index

        for meas_col in meas_cols:
            new_val = insert_error(row[meas_col + 1])
            run_data_frame.at[idx, run_data_frame.columns.values[meas_col]] = new_val

    run_data_frame.to_csv(csv_writeout_filepath, sep=',')

def insert_maxim_temperature_errors(csv_filepath, csv_writeout_filepath):
    run_data_frame = pd.read_csv(csv_filepath)

    meas_cols = get_meas_cols(run_data_frame)

    for row in run_data_frame.itertuples():
        idx = row.Index

        for meas_col in meas_cols: 
            new_val = insert_maxim_error(row[meas_col + 1])
            run_data_frame.at[idx, run_data_frame.columns.values[meas_col]] = new_val
    
    run_data_frame.to_csv(csv_writeout_filepath, sep=',')

# TODO: This won't work... Need to first fix translation to MAXIM
insert_maxim_temperature_errors('./Data/long_ramp_hold_2020-11-13.csv', 'test.csv')