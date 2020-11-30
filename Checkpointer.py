import os
import pandas as pd
import struct
import csv
import time
import binascii

def float_to_hex(f):
    return hex(struct.unpack('<Q', struct.pack('<d', f))[0])

def calc_crc(f_list):
    c = 0
    for f in f_list:
        val = float_to_hex(f)[2:]
        if val == "0":
            val = "0" + val
        c = binascii.crc32(binascii.a2b_hex(val), c)
    return c
    
class Checkpointer: 
    def __init__(self, checkpoint_data_path, filename, data_names):
        """Initializes a Checkpointer, which periodically saves the given data.

        Args:
            checkpoint_data_path (str): A path to where the checkpoint data 
                should be stored as a csv (do not include the .csv filename)
            filename (str): The name of the csv file that should be saved
            data_names(list): A list of the names of
                variables being stored. The order in which this list lists 
                the variables is the order in which the checkpointer will 
                return them.
        """
        self.data_path = checkpoint_data_path
        self.data_names = data_names
        self.filename = filename

        # Create the path if it doesn't exist
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)
        # Create the csv file in path 
        self.data_names.insert(0, "Time")
        self.data_names.append("CRC")
        df = pd.DataFrame(columns=self.data_names) 
        df.to_csv(self.data_path + "/" + self.filename, index=False)

    def create_checkpoint(self, data):
        """Create the checkpoint with the given data, len(data) must ==
            len(self.data_names)
        
        Args:
            data(list): The data to be checkpointed, must be in the 
                same order as self's data_names
        """

        # Subtract 2 for CRC and time
        assert(len(data) == (len(self.data_names) - 2))
        # Insert time in epoch and CRC for row (without time)
        crc = calc_crc(data)
        data.append(crc)
        data.insert(0, time.time())

        # Append data
        filepath = self.data_path + "/" + self.filename
        with open(filepath, 'a') as file:
            writer = csv.writer(file)
            writer.writerow(data)
    
    def get_checkpoint(self):
        """Gets the most recent valid checkpoint data, with the time 
            it was stored appended

            Will return None if no valid checkpoints
        """
        filepath = self.data_path + "/" + self.filename
        with open(filepath, 'r') as file:
            for row in reversed(list(csv.reader(file))):
                # Check if column header
                if row[0] == "Time":
                    break
                
                # Get stored CRC
                stored_crc = row[-1]
                # Get stored time
                time = row[0]
                # Get original data
                data = row[1:-1]
                
                calculated_crc = calc_crc([float(i) for i in data])
                if str(calculated_crc) != stored_crc:
                    # CRCs do not match, get the second to last data
                    print("CRC did not match!")
                    continue
                data.append(time)
            
                return data