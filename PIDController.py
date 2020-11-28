import numpy as np

def clamp(val, minval, maxval):
    return max(min(val, maxval), minval)

class PIDController:

    def __init__(self, K_prop, K_int, K_der, prev_time):
        self.Kp = K_prop    
        self.Ki = K_int
        self.Kd = K_der
        self.prev_time = prev_time
        self.filter_length = 500
        self.prev_error = np.zeros(self.filter_length) #for derivitive calculation
        self.integral_state = 0 #for integral calculation
        self.smoothed_error = 0

        self.count = 0
        self.t = np.zeros(12000)
        self.derivatives = np.zeros(12000)

    def update(self, set_point, curr_temp, curr_time):
        t_step = curr_time - self.prev_time
        new_error = set_point - curr_temp
        prev_filtered_error = self.filter_n(self.prev_error)
        self.prev_error[:-1] = self.prev_error[1:]
        self.prev_error[-1] = new_error
        error = self.filter_n(self.prev_error)
        self.smoothed_error = error
        error_deriv = (error - prev_filtered_error)/t_step

        if self.count < 12000:
            self.t[self.count] = curr_time
            self.derivatives[self.count] = error_deriv
        elif self.count == 12000:
            np.savetxt("deriv.csv", np.array([self.t, self.derivatives]).T, delimiter=',', header="t, deriv")
        self.count += 1

        self.integral_state += error*t_step
        self.integral_state = clamp(self.integral_state, -1000, 1000)

        self.p_comp = self.Kp*error
        self.i_comp = self.Ki*self.integral_state
        self.d_comp = self.Kd*error_deriv
        PID_output = self.p_comp + self.i_comp + self.d_comp
        #update integral and derivitive states

        self.prev_time = curr_time
        if(PID_output > 1):
            PID_output = 1
        elif(PID_output < 0):
            PID_output = 0
        return PID_output

    def filter_n(self, x):
        n = len(x)
        #w = np.arange(1, n+1)/n
        #filtered = np.sum(x*w)
        return sum(x)/n
