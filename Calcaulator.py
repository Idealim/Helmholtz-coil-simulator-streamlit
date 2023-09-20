import math
import numpy as np
from typing import Tuple
from hyperopt import hp, fmin, Trials, tpe
from utils import plot_st, plot

def optimize(params):
    best_params, best_loss = find_optimized_params(params)
    print(best_params)
    predicted_values, actual_values = helmholtz_coil(**best_params, R=params['R'], step=params['step'], conpensation=params['conpensation'])
    
    fig = plot_st(predicted_values, actual_values, step=params['step'], best_params=best_params)
    
    return best_params, best_loss, fig, predicted_values
    

def helmholtz_coil(r1, r2, d, mf, nf, ms, ns, R=0.04, step=0.1, conpensation=False) -> Tuple[np.ndarray, np.ndarray]:
    """
    Calculates the magnetic field strength produced by helmholtz_coil.
    
    Args:
        r (float): 물체 반지름 
        d (float): 물체 사이 거리

    Returns:
        Tuple(predicted_value, actual_value)
    """
    x = 0.  
    result_Acm = 0.
    result_Oe = 0.
    D = 2 * R
    
    results_Oe = []
    actual_values = []
    # 값 구하기
    while x <= d: # x 
        result_Acm = 0
        result1 = 0
        coil_ypos = r1 + R
        while coil_ypos <= r1 + R + D * (nf - 1):
            resultmf = 0
            coil_xpos = R
            while coil_xpos < D * (mf - 1):
                first1 = pow(r1 * r1 + (x + coil_xpos) * (x + coil_xpos), 3)
                first = r1 * r1 / math.sqrt(first1)

                resultmf += first
                coil_xpos += D

            result1 += resultmf
            coil_ypos += D

        result2 = 0
        coil_ypos = r2 + R
        while coil_ypos <= r2 + R + D * (ns - 1):
            resultms = 0
            coil_xpos = R
            while coil_xpos < D * (ms - 1):
                second1 = pow(r2 * r2 + (d - x + coil_xpos) * (d - x + coil_xpos), 3)
                second = r2 * r2 / math.sqrt(second1)

                resultms += second
                coil_xpos += D

            result2 += resultms
            coil_ypos += D

        result_Acm = (result1 + result2) / 2
        result_Oe = result_Acm / 0.796
        
        results_Oe.append(result_Oe) 
        actual_values.append(calculate_actual_value(x, d, conpensation))
        
        x += step
        
    return np.array(results_Oe), np.array(actual_values)

def calculate_actual_value(x, d, line_conpensation=False) -> float: 
    return -15 * x / d + 26 if line_conpensation else -15 * x / d + 25

def calculate_mse(actual_value, predicted_value) -> float:
    return np.mean((actual_value - predicted_value)**2)

def find_optimized_params(params): 
    param_space = {
        'r1': hp.quniform('r1', params['r1']['min'], params['r1']['max'], params['r1']['step']),
        'r2': hp.quniform('r2', params['r2']['min'], params['r2']['max'], params['r1']['step']),
        'd': hp.quniform('d', params['d']['min'], params['d']['max'], params['d']['step']),
        'mf': hp.quniform('mf', params['mf']['min'], params['mf']['max'], 1),
        'nf': hp.quniform('nf', params['nf']['min'], params['nf']['max'], 1),
        'ms': hp.quniform('ms', params['ms']['min'], params['ms']['max'], 1),
        'ns': hp.quniform('ns', params['ns']['min'], params['ns']['max'], 1),
        'R': params['R'],
        'step': params['step'],
        'n_iter': params['n_iter'],
        'conpensation': params['conpensation']
    }
    
    trial_val = Trials()
    best_params = fmin(
        fn=loss_function, space = param_space, algo= tpe.suggest, 
       max_evals=params['n_iter'], trials=trial_val, rstate=np.random.default_rng(seed=0)
    )
    
    best_loss = trial_val.best_trial['result']['loss']
    
    return best_params,best_loss 


def loss_function(space) -> float:
    actual_values, predicted_values = helmholtz_coil(
        r1=space['r1'],
        r2=space['r2'],
        d=space['d'],
        mf=space['mf'],
        nf=space['nf'],
        ms=space['ms'],
        ns=space['ns'],
        R=space['R'],
        step=space['step'],
        conpensation=space['conpensation']
    )
                                                                                                                   
    return calculate_mse(actual_values, predicted_values)


# def find_optimized_params(n_iter=100, R = 0.04, step = 0.1): 
#     param_space = {
#         'r1': hp.quniform('r1', 5, 10, 0.1),
#         'r2': hp.quniform('r2', 5, 10, 0.1),
#         'd': hp.quniform('d', 5, 10, 0.1),
#         'mf': hp.quniform('mf', 5, 20, 1),
#         'nf': hp.quniform('nf', 5, 20, 1),
#         'ms': hp.quniform('ms', 1, 20, 1),
#         'ns': hp.quniform('ns', 1, 20, 1),
#         'R': R,
#         'step': step
#     }
    
#     trial_val = Trials()
#     best_params = fmin(
#         fn=loss_function, space = param_space, algo= tpe.suggest, 
#        max_evals=n_iter, trials=trial_val, rstate=np.random.default_rng(seed=0)
#     )
    
#     best_loss = trial_val.best_trial['result']['loss']
    
#     return best_params,best_loss



if __name__ == "__main__":
    """
    # Example of helmholtz_coil
    actual_values, predicted_values = helmholtz_coil(r1= 5, r2=5, d=6, R=0.04, mf=12, nf=13, ms=6, ns=4, step= 0.1)
    print(predicted_values, actual_values)
    print(calculate_mse(predicted_values, actual_values))
    """

    """
    # Example1 of Optimizer
    step = 0.1
    best_params, best_loss = find_optimized_params(n_iter=100,step=step)
    print(best_params)
    predicted_values, actual_values = helmholtz_coil(**best_params, step=step)
    
    plot(predicted_values, actual_values, step=step, best_params=best_params)

    """

    """
    Example2 of Optimizer
    """
    params = {
        'r1': {'min': 5, 'max': 10, 'step': 0.1},
        'r2': {'min': 5, 'max': 10, 'step': 0.1},
        'd': {'min': 5, 'max': 10, 'step': 0.1},
        'mf': {'min': 5, 'max': 20},
        'nf': {'min': 5, 'max': 20},
        'ms': {'min': 1, 'max': 20},
        'ns': {'min': 1, 'max': 20},
        'R': 0.04,
        'step': 0.1, # opt_step
        'n_iter': 100,
        'conpensation': False
    }
    
    best_params, best_loss, fig = find_optimized_params(params)
    print(best_params)
    predicted_values, actual_values = helmholtz_coil(**best_params, R=params['R'], step=params['step'])
     
    plot(predicted_values, actual_values, step=params['step'], best_params=best_params)
    


