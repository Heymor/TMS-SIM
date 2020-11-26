/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * File: AM_Discrete.c
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

#include "AM_Discrete.h"
#include "AM_Discrete_private.h"

/* Block states (default storage) */
DW_AM_Discrete_T AM_Discrete_DW;

/* External inputs (root inport signals with default storage) */
ExtU_AM_Discrete_T AM_Discrete_U;

/* External outputs (root outports fed by signals with default storage) */
ExtY_AM_Discrete_T AM_Discrete_Y;

/* Real-time model */
RT_MODEL_AM_Discrete_T AM_Discrete_M_;
RT_MODEL_AM_Discrete_T *const AM_Discrete_M = &AM_Discrete_M_;

const double P_LEARN_RATE_INIT = 5.0E-7;
const double I_LEARN_RATE_INIT = 1.0E-14;
const double D_LEARN_RATE_INIT = 5.0E-5;
double p_learn_rate;
double i_learn_rate;
double d_learn_rate;


const _Bool decay_learning = true;
const double decay_lambda = 1.0/3600; // When it will be 33% of orig.

/* Model step function */
void AM_Discrete_step(double tdelta)
{
  //  Decay learning rate: Trying to reduce learned oscillations during
  // very long (5+ hour) runs. Use exponential decay differential equation.
  if (decay_learning) {
    p_learn_rate *= (1 - decay_lambda * tdelta);
    i_learn_rate *= (1 - decay_lambda * tdelta);
    d_learn_rate *= (1 - decay_lambda * tdelta);
  }

  real_T denAccum;
  real_T denAccum_0;
  real_T rtb_Gain1;
  real_T Sum1;

  /* Outport: '<Root>/K_p' incorporates:
   *  DiscreteIntegrator: '<Root>/Discrete-Time Integrator'
   */
  AM_Discrete_Y.K_p = AM_Discrete_DW.DiscreteTimeIntegrator_DSTATE;

  /* Outport: '<Root>/K_i' incorporates:
   *  DiscreteIntegrator: '<Root>/Discrete-Time Integrator2'
   */
  AM_Discrete_Y.K_i = AM_Discrete_DW.DiscreteTimeIntegrator2_DSTATE;

  /* Outport: '<Root>/K_d' incorporates:
   *  DiscreteIntegrator: '<Root>/Discrete-Time Integrator1'
   */
  AM_Discrete_Y.K_d = AM_Discrete_DW.DiscreteTimeIntegrator1_DSTATE;

  /* Sum: '<Root>/Sum1' incorporates:
   *  Inport: '<Root>/Yp'
   *  Inport: '<Root>/r'
   */
  Sum1 = AM_Discrete_U.r - AM_Discrete_U.Yp;

  /* DiscreteTransferFcn: '<Root>/Discrete Transfer Fcn' */
  denAccum = (Sum1 - -2.0 * AM_Discrete_DW.DiscreteTransferFcn_states[0]) -
    AM_Discrete_DW.DiscreteTransferFcn_states[1];

  /* Gain: '<Root>/Gain1' incorporates:
   *  Inport: '<Root>/Yp'
   *  Inport: '<Root>/r'
   *  Sum: '<Root>/Sum'
   */
  rtb_Gain1 = -(AM_Discrete_U.Yp - AM_Discrete_U.r);

  /* DiscreteTransferFcn: '<Root>/Discrete Transfer Fcn2' */
  denAccum_0 = (Sum1 - -2.0 * AM_Discrete_DW.DiscreteTransferFcn2_states[0]) -
    AM_Discrete_DW.DiscreteTransferFcn2_states[1];

  /* Update for DiscreteIntegrator: '<Root>/Discrete-Time Integrator1' incorporates:
   *  DiscreteTransferFcn: '<Root>/Discrete Transfer Fcn'
   *  Product: '<Root>/Product2'
   */
  AM_Discrete_DW.DiscreteTimeIntegrator1_DSTATE += ((-1.625E-11 * denAccum +
    1.625E-11 * AM_Discrete_DW.DiscreteTransferFcn_states[0]) + 0.0 *
    AM_Discrete_DW.DiscreteTransferFcn_states[1]) * rtb_Gain1 * d_learn_rate * tdelta;

  /* Update for DiscreteTransferFcn: '<Root>/Discrete Transfer Fcn' */
  AM_Discrete_DW.DiscreteTransferFcn_states[1] =
    AM_Discrete_DW.DiscreteTransferFcn_states[0];
  AM_Discrete_DW.DiscreteTransferFcn_states[0] = denAccum;

  /* Update for DiscreteTransferFcn: '<Root>/Discrete Transfer Fcn1' */
  denAccum = (Sum1 - -2.0 * AM_Discrete_DW.DiscreteTransferFcn1_states[0]) -
    AM_Discrete_DW.DiscreteTransferFcn1_states[1];

  /* Update for DiscreteIntegrator: '<Root>/Discrete-Time Integrator' incorporates:
   *  DiscreteTransferFcn: '<Root>/Discrete Transfer Fcn2'
   *  Gain: '<Root>/Gain'
   *  Product: '<Root>/Product'
   */
  AM_Discrete_DW.DiscreteTimeIntegrator_DSTATE += ((1.047E-5 * denAccum_0 +
    -1.047E-5 * AM_Discrete_DW.DiscreteTransferFcn2_states[0]) + 1.163E-21 *
    AM_Discrete_DW.DiscreteTransferFcn2_states[1]) * rtb_Gain1 * p_learn_rate * tdelta;

  /* Update for DiscreteIntegrator: '<Root>/Discrete-Time Integrator2' incorporates:
   *  DiscreteTransferFcn: '<Root>/Discrete Transfer Fcn1'
   *  Gain: '<Root>/Gain2'
   *  Product: '<Root>/Product1'
   */
  AM_Discrete_DW.DiscreteTimeIntegrator2_DSTATE += (0.0001 *
    AM_Discrete_DW.DiscreteTransferFcn1_states[0] + -1.11E-20 *
    AM_Discrete_DW.DiscreteTransferFcn1_states[1]) * rtb_Gain1 * i_learn_rate * tdelta;

  /* Update for DiscreteTransferFcn: '<Root>/Discrete Transfer Fcn2' */
  AM_Discrete_DW.DiscreteTransferFcn2_states[1] =
    AM_Discrete_DW.DiscreteTransferFcn2_states[0];
  AM_Discrete_DW.DiscreteTransferFcn2_states[0] = denAccum_0;

  /* Update for DiscreteTransferFcn: '<Root>/Discrete Transfer Fcn1' */
  AM_Discrete_DW.DiscreteTransferFcn1_states[1] =
    AM_Discrete_DW.DiscreteTransferFcn1_states[0];
  AM_Discrete_DW.DiscreteTransferFcn1_states[0] = denAccum;

  // NEVER let the integral coefficient go negative.
  AM_Discrete_DW.DiscreteTimeIntegrator2_DSTATE = AM_Discrete_DW.DiscreteTimeIntegrator2_DSTATE < 0 ? 0.0 : AM_Discrete_DW.DiscreteTimeIntegrator2_DSTATE;
  AM_Discrete_DW.DiscreteTimeIntegrator_DSTATE = AM_Discrete_DW.DiscreteTimeIntegrator_DSTATE < 0 ? 0.0 : AM_Discrete_DW.DiscreteTimeIntegrator_DSTATE;
  AM_Discrete_DW.DiscreteTimeIntegrator1_DSTATE = AM_Discrete_DW.DiscreteTimeIntegrator1_DSTATE > 0 ? 0.0 : AM_Discrete_DW.DiscreteTimeIntegrator1_DSTATE;
  AM_Discrete_DW.DiscreteTimeIntegrator2_DSTATE = AM_Discrete_DW.DiscreteTimeIntegrator2_DSTATE > .0005 ? .0005 : AM_Discrete_DW.DiscreteTimeIntegrator2_DSTATE;
}

/* Model initialize function */
void AM_Discrete_initialize(double kp, double ki, double kd)
{
  AM_Discrete_DW.DiscreteTimeIntegrator_DSTATE = kp;
  AM_Discrete_DW.DiscreteTimeIntegrator2_DSTATE = ki;
  AM_Discrete_DW.DiscreteTimeIntegrator1_DSTATE = kd;

  p_learn_rate = P_LEARN_RATE_INIT;
  i_learn_rate = I_LEARN_RATE_INIT;
  d_learn_rate = D_LEARN_RATE_INIT;
}

/* Model terminate function */
void AM_Discrete_terminate(void)
{
  /* (no terminate code required) */
}

/*
 * File trailer for generated code.
 *
 * [EOF]
 */
