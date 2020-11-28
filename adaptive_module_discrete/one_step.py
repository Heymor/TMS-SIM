import ctypes
import os

# Load the library
lib = ctypes.CDLL(os.path.abspath("./adaptive_module_discrete/build/adaptive_lib.so"))

# Define the initialization function
lib.AM_Discrete_initialize.argtypes = None
lib.AM_Discrete_initialize.restype = None

# Define the function and the arguments it must get
lib.rt_OneStep.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double)]
lib.rt_OneStep.restype = None

class OneStep(object):
    def __init__(self, init_kp=0, init_ki=0, init_kd=0):
        # Initialize
        lib.rt_Init(ctypes.c_double(init_kp), ctypes.c_double(init_ki), ctypes.c_double(init_kd))

        self.adaptive_output = (ctypes.c_double*3)()


    def one_step(self, measured, reference, tdelta):
        lib.rt_OneStep(ctypes.c_double(measured), ctypes.c_double(reference), ctypes.c_double(tdelta), self.adaptive_output)
        return list(self.adaptive_output)
