from numpy.core.defchararray import index
from insert_errors import (
    insert_maxim_temperature_errors, get_meas_cols
)
from PIDController import PIDController
from adaptive_module_discrete.one_step import OneStep
import pandas as pd

def run_sim(csv_filepath, csv_writeout_filepath):
    # Filepath is the filepath to a CSV file that has no errors inserted
    # Insert errors and return edited pandas dataframe
    error_df = insert_maxim_temperature_errors(csv_filepath, csv_writeout_filepath) 

    # Go through dataframe datapoint by datapoint and simulate
    meas_cols = get_meas_cols(error_df)
    prev_time = 0
    curr_time = 0
    t_delta = 0

    # Setup
    onestep = OneStep(init_kp=0, init_ki=0, init_kd=0)
    pid = PIDController(K_prop=0, K_int=0, K_der=0, prev_time=0)

    for row in error_df.itertuples():
        idx = row.Index

        # Get average temperature
        avg_temp = 0
        for meas_col in meas_cols:
            avg_temp += row[meas_col + 1]
        avg_temp /= len(meas_cols)
        # Set plate average for in the error_df
        error_df.at[idx, 'PlateAverage'] = avg_temp
        
        # Get set point, i.e. profile col in csv
        set_point = row[2]

        # Get t_delta 
        prev_time = curr_time
        curr_time = row[1]
        t_delta = curr_time - prev_time

        # Times to call (substeps)
        num_substep = t_delta // .010

        for substep in range(int(num_substep)):
            # Get and set new coeff
            new_kp, new_ki, new_kd = tuple(onestep.one_step(avg_temp, set_point, (t_delta + substep * 0.010)))
            pid.Kp = new_kp
            pid.Ki = new_ki
            pid.Kd = new_kd

            pid_out = pid.update(set_point=set_point, curr_temp=avg_temp, curr_time=(curr_time + substep * 0.010))
            # Set PID PWM output and error
            error_df.at[idx, 'PWM'] = pid_out
            error_df.at[idx, 'error'] = pid.smoothed_error

    # Write out completed simulation to csv
    error_df.to_csv(csv_writeout_filepath, sep=',', index=False)

run_sim('test.csv', 'test.csv')

