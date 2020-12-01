import pandas as pd
import random
import struct

UPSET_THRESHOLD = 0.90

def float_to_bits(f):
    # How many bits is the return value? Why do we return the 0th element?
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
    temperature_bits[31] = sign_bit
    j = 30
    for p in reversed(range(-2, 11)):
        if (f - 2**(p)) >= 0:
            temperature_bits[j] = 1
            f -= 2**(p)
        else:
            temperature_bits[j] = 0
        
        j -= 1

    temperature_bin_str = ''.join(str(e) for e in reversed(temperature_bits))
    ba = bytearray(int(temperature_bin_str, 2).to_bytes(len(temperature_bin_str) // 8, byteorder="big"))
    return ba

def maxim_to_float(m):
    f = (m[0] & 0x7F) * 2.0**4
    f += (m[1] & 0xFE) / 2.0**4
    f *= (-1)**(m[0] >> 7)

    return f

def insert_error(data_point, upset_threshold=UPSET_THRESHOLD):
    if random.random() > upset_threshold:
        # Flip random bit
        # First unpack the float
        data_point = float_to_bits(data_point)

        # Get random bit position
        num_bits = 16 # This is how long the float is when converted to bits?
        rand_bit = random.randrange(num_bits)

        # Flip bit
        data_point ^= 1 << rand_bit

        # Change back to float
        data_point = bits_to_float(data_point)

    return data_point

def insert_maxim_error(data_point, upset_threshold=UPSET_THRESHOLD):
    if random.random() > upset_threshold:
        # Flip a random bit
        # First translate from temperature point to maxim 
        data_point = float_to_maxim(data_point)

        # Get a random bit position
        num_bits = len(data_point) * 8
        rand_bit = random.randrange(num_bits)
        rand_byte = rand_bit // 8
        rand_bit_loc = rand_bit - (rand_byte * 8)

        # Flip bit
        data_point[rand_byte] ^= 1 << rand_bit_loc

        # Change back to float
        data_point = maxim_to_float(data_point)

    return data_point

def insert_maxim_error_perbit(data_point, upset_threshold=.99):
    '''
    Each maxim bit has (1 - upset_threshold) chance of being flipped.
    '''

    data_point = float_to_maxim(data_point)
    num_bits = len(data_point) * 8
    for bitpos in range(num_bits):
        if random.random() > upset_threshold:
            bytepos = bitpos // 8
            bitoffset = bitpos - (bytepos * 8)

            # Flip bit
            data_point[bytepos] ^= 1 << bitoffset

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

    run_data_frame.to_csv(csv_writeout_filepath, sep=',', index=False)

    return run_data_frame

def insert_maxim_temperature_errors(csv_filepath, csv_writeout_filepath):
    run_data_frame = pd.read_csv(csv_filepath)

    meas_cols = get_meas_cols(run_data_frame)
    for row in run_data_frame.itertuples():
        idx = row.Index

        for meas_col in meas_cols: 
            new_val = insert_maxim_error(row[meas_col + 1])
            run_data_frame.at[idx, run_data_frame.columns.values[meas_col]] = new_val
    
    run_data_frame.to_csv(csv_writeout_filepath, sep=',', index=False)

    return run_data_frame