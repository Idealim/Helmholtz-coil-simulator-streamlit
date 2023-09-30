import math
import numpy as np
from typing import Tuple
from hyperopt import hp, fmin, Trials, tpe
from utils import plot_st, plot
import streamlit as st    


def helmholtz_coil(r1, r2, d, mf, nf, ms, ns, R, step, target_value1, target_value2) -> Tuple[np.ndarray, np.ndarray]:
    """
    Calculates the magnetic field strength produced by helmholtz_coil.
    
    Args:
        r (float): 물체 반지름 [단위 : cm]
        d (float): 물체 사이 거리 [단위 : cm]
        mf, nf (int): 첫 번째 코일의 x축, y축 방향으로 감은 개수 
        ms, ns (int): 두 번째 코일의 x축, y축 방향으로 감은 개수
        R (float): Wire의 반지름 [단위 : cm]
        step (float): x축 방향으로 이동 거리 [단위 : cm]
        target_value1 (float): 첫 번째 코일의 목표 H 값 [단위: Oe]
        target_value2 (float): 두 번째 코일의 목표 H 값  [단위: Oe]
    Returns:
        모델의 예측값과 직선의 타겟값을 반환합니다.
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
            while coil_xpos < R + D * (mf - 1):
                first1 = pow(coil_ypos * coil_ypos + (x + coil_xpos) * (x + coil_xpos), 3)
                first = coil_ypos * coil_ypos / math.sqrt(first1)

                resultmf += first
                coil_xpos += D

            result1 += resultmf
            coil_ypos += D

        result2 = 0
        coil_ypos = r2 + R
        while coil_ypos <= r2 + R + D * (ns - 1):
            resultms = 0
            coil_xpos = R
            while coil_xpos < R + D * (ms - 1):
                second1 = pow(coil_ypos * coil_ypos + (d - x + coil_xpos) * (d - x + coil_xpos), 3)
                second = coil_ypos * coil_ypos / math.sqrt(second1)

                resultms += second
                coil_xpos += D

            result2 += resultms
            coil_ypos += D

        result_Acm = (result1 + result2) / 2
        result_Oe = result_Acm / 0.796
        
        results_Oe.append(result_Oe) 
        actual_values.append(calculate_actual_value(x, d, target_value1, target_value2))
        
        x += step
        
    return np.array(results_Oe), np.array(actual_values)


def calculate_actual_value(x, d, target_value1, target_value2) -> float: 
    return (target_value2 - target_value1) * x / d + target_value1


def calculate_mse(actual_value, predicted_value) -> float:
    return np.mean((actual_value - predicted_value)**2)


def optimize(params):
    best_params, best_loss, params = find_optimized_params(params)
    best_params = update_best_params(params, best_params)

    print(best_params)
    predicted_values, actual_values = helmholtz_coil(**best_params)
    
    fig = plot_st(predicted_values, actual_values, step=params['step'], title=best_params)
    
    return best_params, best_loss, fig, predicted_values


def find_optimized_params(params): 
    param_space = {
        'r1': hp.quniform('r1', params['r1']['min'], params['r1']['max'], params['r1']['step']) if isinstance(params['r1'], dict) else params['r1'],
        'r2': hp.quniform('r2', params['r2']['min'], params['r2']['max'], params['r2']['step']) if isinstance(params['r2'], dict) else params['r2'],
        'd': hp.quniform('d', params['d']['min'], params['d']['max'], params['d']['step']) if isinstance(params['d'], dict) else params['d'],
        'mf': hp.quniform('mf', params['mf']['min'], params['mf']['max'], 1) if isinstance(params['mf'], dict) else params['mf'],
        'nf': hp.quniform('nf', params['nf']['min'], params['nf']['max'], 1) if isinstance(params['nf'], dict) else params['nf'],
        'ms': hp.quniform('ms', params['ms']['min'], params['ms']['max'], 1) if isinstance(params['ms'], dict) else params['ms'],
        'ns': hp.quniform('ns', params['ns']['min'], params['ns']['max'], 1) if isinstance(params['ns'], dict) else params['ns'],
        'R': params['R'],
        'step': params['step'],
        'n_iter': params['n_iter'],
        'target_value1': params['target_value1'],
        'target_value2': params['target_value2']
    }

    trial_val = Trials()
    best_params = fmin(
        fn=loss_function, space = param_space, algo= tpe.suggest, 
       max_evals=params['n_iter'], trials=trial_val, rstate=np.random.default_rng(seed=0)
    )
    
    best_loss = trial_val.best_trial['result']['loss']
    
    return best_params,best_loss, params


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
        target_value1=space['target_value1'],
        target_value2=space['target_value2']
    )
                                                                                                                   
    return calculate_mse(actual_values, predicted_values)


def update_best_params(params, best_params):
    for key, value in best_params.items():
        params[key] = value
    del params['n_iter']
    
    return params

def get_line_with_lsm(x, y):
    coefficients = np.polyfit(x, y, 1)
    slope = coefficients[0]
    intercept = coefficients[1]

    return slope, intercept

if __name__ == "__main__":
    """
    # Example of helmholtz_coil
    actual_values, predicted_values = helmholtz_coil(
        r1= 5, r2=5, 
        d=6,  
        mf=12, nf=13, 
        ms=6, ns=4, 
        step= 0.1, R=0.02,
        target_value1=25, target_value2=10)
    print(predicted_values, actual_values)
    print(calculate_mse(predicted_values, actual_values))
    """

    """
    Example of Optimizer
    """
    params =  {
        "r1": hp.quniform('r1', 5, 10, 0.1),
        "r2": 5,
        "d": 5,
        "mf": 5,
        "nf": 5,
        "ms": {
            "min": 1,
            "max": 20
        },
        "ns": {
            "min": 1,
            "max": 20
        },
        "R": 0.02,
        "step": 0.1,
        "n_iter": 1000,
        "target_value1": 25.,
        "target_value2": 10.
    }
    best_params, best_loss, params = find_optimized_params(params)
    best_params = update_best_params(params, best_params)
    
    print(best_params)
    predicted_values, actual_values = helmholtz_coil(**best_params)
     
    plot(predicted_values, actual_values, step=params['step'], best_params=best_params)
    
    

