import math
from typing import Tuple
import numpy as np
from model.Calculator import calculate_actual_value


def modified_helmholtz_coil(r1, r2, d, mf, nf, ms, ns, alpha1, alpha2, R, step, target_value1, target_value2) -> Tuple[np.ndarray, np.ndarray]:
    """
    Calculates the magnetic field strength produced by helmholtz_coil.
    Add alphad1, alpha2 vesion
    
    Args:
        r (float): 물체 반지름 [단위 : cm]
        d (float): 물체 사이 거리 [단위 : cm]
        mf, nf (int): 첫 번째 코일의 x축, y축 방향으로 감은 개수
        ms, ns (int): 두 번째 코일의 x축, y축 방향으로 감은 개수
        alpha (int): 마지막 층의 x축 방향으로 감은 개수.
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
        # 추가로 감기
        coil_xpos = R

        while coil_xpos < R + D * (alpha1 - 1):
                first1 = pow(coil_ypos * coil_ypos + (x + coil_xpos) * (x + coil_xpos), 3)
                first = coil_ypos * coil_ypos / math.sqrt(first1)

                result1 += first
                coil_xpos += D

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

        coil_xpos = R
        while coil_xpos < R + D * (alpha2 - 1):
            second1 = pow(coil_ypos * coil_ypos + (x + coil_xpos) * (x + coil_xpos), 3)
            second = coil_ypos * coil_ypos / math.sqrt(first1)

            result2 += second
            coil_xpos += D

        result_Acm = (result1 + result2) / 2
        result_Oe = result_Acm / 0.796
        
        results_Oe.append(result_Oe) 
        actual_values.append(calculate_actual_value(x, d, target_value1, target_value2))
        
        x += step
        
    return np.array(results_Oe), np.array(actual_values)

if __name__ == "__main__":
     
     result1, _ = modified_helmholtz_coil(r1= 5, r2=5, 
        d=6,  
        mf=19, nf=10, 
        ms=9, ns=3, 
        alpha1=17,
        alpha2=0,
        step= 0.1, R=0.025,
        target_value1=25, target_value2=10)