from sys import byteorder
import pandas as pd
import random
import sys
import struct
import binascii

def float_to_bits(f):
    s = struct.pack('>f', f)
    return struct.unpack('>L', s)[0]

def bits_to_float(b):
    s = struct.pack('>L', b)
    return struct.unpack('>f', s)[0]

def float_to_maxim(f):
    # Get sign bit
    if f > 0:
        sign_bit = 0
    else:
        # Flip to positive, and set sign bit
        f *= -1
        sign_bit = 1

    temperature_bits = [0] * 32
    temperature_bits[13] = sign_bit
    j = 12
    for p in reversed(range(-2, 11)):
        if (f - 2**(p)) >= 0:
            temperature_bits[j] = 1
            f -= 2**(p)
        else:
            temperature_bits[j] = 0
        
        j -= 1
    temperature_bin_str = ''.join(str(e) for e in temperature_bits)
    ba = bytearray(int(temperature_bin_str, 2).to_bytes(len(temperature_bin_str) // 8, byteorder="big"))
    return ba

def maxim_to_float(m):
    print(binascii.hexlify(m))
    print("0x%02x" % m[0])
    f = (m[0] & 0x7F) * 2.0**4
    print(m[0])
    f += (m[1] & 0xFE) / 2.0**4
    print(f)
    f *= (-1)**(m[0] >> 7)
    print(f)

    return f

def insert_error(data_point):
    if random.random() > 0.5:
        # Flip random bit
        # First unpack the float
        data_point = float_to_bits(data_point)

        # Get random bit position
        num_bits = 16
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
        num_bits = data_point.bit_length()
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
# insert_maxim_temperature_errors('./Data/long_ramp_hold_2020-11-13.csv', 'test.csv')
a = float_to_maxim(133.75)
a = maxim_to_float(a)
print(a)

# print(insert_maxim_error(133.75))