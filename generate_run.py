import numpy as np
import pandas as pd

def generate_run(num_points, mean_temp, std_temp, profile_temp, tc_mapping):
    # Create pandas dataframe
    columns = ['Time', 'Profile', 'PWM'] + list(tc_mapping.values()) + ['PlateAverage', 'error']
    df = pd.DataFrame(columns=columns)
    print(df)

    curr_time = 0
    for i in range(num_points):
        df.at[i, 'Time'] = curr_time
        df.at[i, 'Profile'] = profile_temp
        curr_time += np.random.normal(loc=0.40, scale=.010)

        for _, tc_name in tc_mapping.items():
            tc_reading = np.random.normal(loc=mean_temp, scale=std_temp)
            df.at[i, tc_name] = tc_reading
    
    df.to_csv('test.csv', sep=',', index=False)

generate_run(100, 60, .25, 60, tc_mapping={
    0: "bus0dev0",
    1: "bus0dev1",
    2: "bus1dev0",
    3: "bus1dev1"
})