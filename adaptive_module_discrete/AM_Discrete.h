/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * File: AM_Discrete.h
 *
 * Code generated for Simulink model 'AM_Discrete'.
 *
 * Model version                  : 1.1
 * Simulink Coder version         : 9.3 (R2020a) 18-Nov-2019
 * C/C++ source code generated on : Wed Nov  4 18:59:54 2020
 *
 * Target selection: ert.tlc
 * Embedded hardware selection: Intel->x86-64 (Windows64)
 * Code generation objectives: Unspecified
 * Validation result: Not run
 */

#ifndef RTW_HEADER_AM_Discrete_h_
#define RTW_HEADER_AM_Discrete_h_
#ifndef AM_Discrete_COMMON_INCLUDES_
# define AM_Discrete_COMMON_INCLUDES_
#include "rtwtypes.h"
#endif                                 /* AM_Discrete_COMMON_INCLUDES_ */

#include "AM_Discrete_types.h"

/* Macros for accessing real-time model data structure */
#ifndef rtmGetErrorStatus
# define rtmGetErrorStatus(rtm)        ((rtm)->errorStatus)
#endif

#ifndef rtmSetErrorStatus
# define rtmSetErrorStatus(rtm, val)   ((rtm)->errorStatus = (val))
#endif

/* Block states (default storage) for system '<Root>' */
typedef struct {
  real_T DiscreteTimeIntegrator_DSTATE;/* '<Root>/Discrete-Time Integrator' */
  real_T DiscreteTimeIntegrator2_DSTATE;/* '<Root>/Discrete-Time Integrator2' */
  real_T DiscreteTimeIntegrator1_DSTATE;/* '<Root>/Discrete-Time Integrator1' */
  real_T DiscreteTransferFcn_states[2];/* '<Root>/Discrete Transfer Fcn' */
  real_T DiscreteTransferFcn2_states[2];/* '<Root>/Discrete Transfer Fcn2' */
  real_T DiscreteTransferFcn1_states[2];/* '<Root>/Discrete Transfer Fcn1' */
} DW_AM_Discrete_T;

/* External inputs (root inport signals with default storage) */
typedef struct {
  real_T Yp;                           /* '<Root>/Yp' */
  real_T r;                            /* '<Root>/r' */
} ExtU_AM_Discrete_T;

/* External outputs (root outports fed by signals with default storage) */
typedef struct {
  real_T K_p;                          /* '<Root>/K_p' */
  real_T K_i;                          /* '<Root>/K_i' */
  real_T K_d;                          /* '<Root>/K_d' */
} ExtY_AM_Discrete_T;

/* Real-time Model Data Structure */
struct tag_RTM_AM_Discrete_T {
  const char_T * volatile errorStatus;
};

/* Block states (default storage) */
extern DW_AM_Discrete_T AM_Discrete_DW;

/* External inputs (root inport signals with default storage) */
extern ExtU_AM_Discrete_T AM_Discrete_U;

/* External outputs (root outports fed by signals with default storage) */
extern ExtY_AM_Discrete_T AM_Discrete_Y;

/* Model entry point functions */
extern void AM_Discrete_initialize(double kp, double ki, double kd);
extern void AM_Discrete_step(double tdelta);
extern void AM_Discrete_terminate(void);

/* Real-time Model object */
extern RT_MODEL_AM_Discrete_T *const AM_Discrete_M;

/*-
 * These blocks were eliminated from the model due to optimizations:
 *
 * Block '<Root>/Kd' : Unused code path elimination
 * Block '<Root>/Ki' : Unused code path elimination
 * Block '<Root>/Kp' : Unused code path elimination
 * Block '<Root>/Scope' : Unused code path elimination
 * Block '<Root>/Gain3' : Eliminated nontunable gain of 1
 */

/*-
 * The generated code includes comments that allow you to trace directly
 * back to the appropriate location in the model.  The basic format
 * is <system>/block_name, where system is the system number (uniquely
 * assigned by Simulink) and block_name is the name of the block.
 *
 * Use the MATLAB hilite_system command to trace the generated code back
 * to the model.  For example,
 *
 * hilite_system('<S3>')    - opens system 3
 * hilite_system('<S3>/Kp') - opens and selects block Kp which resides in S3
 *
 * Here is the system hierarchy for this model
 *
 * '<Root>' : 'AM_Discrete'
 */
#endif                                 /* RTW_HEADER_AM_Discrete_h_ */

/*
 * File trailer for generated code.
 *
 * [EOF]
 */
