import streamlit as st
from model.Calculator import get_line_with_lsm, calculate_mse
from model.ModifiedHelmholtzCoil import modified_helmholtz_coil
from utils import plot_st
import re
import pandas as pd
import numpy as np
import io
from data import measurement_datas, measurement_params


def Analysis_page():
    st.markdown("### 실험값 분석")
    col1, col2= st.columns(2, gap='large')

    with col1:
        st.markdown("#### 실험값 입력")
        measurement = st.selectbox('실험 Case 를 선택해주세요.',
                                ('직접 입력하기','208/22 try1','208/27 try1','208/27 try2','208/27 mean','208/32 try1','208/32 try2','208/32 mean','218/27 try1','218/27 try2','218/27 mean','198/27 try1','198/27 try2','198/27 mean'))

        if measurement == "직접 입력하기":
            params = measurement_params['default']
            measurement_results = []
            st.write("실험값을 직접 입력해주세요.")
        elif st.session_state.best_params is not None:
            st.info("자동으로 Optimizer에서 찾은 최적의 하이퍼파라미터로 업데이트 되었습니다.")
            params = st.session_state.best_params
            params['alpha1'] = 0
            params['alpha2'] = 0
            measurement_results = []
            st.write("실험값을 직접 입력해주세요.")
        else:    
            measurement_params_key = measurement[0:6] # ex. '208/27'
            params = measurement_params[measurement_params_key]
            measurement_results = measurement_datas[measurement]
            st.write(f"실험값: {measurement_results}")


        st.markdown("##### x 좌표 측정 시작값 입력")
        x_start = st.number_input("x 좌표 시작값, 단위: [cm]", value=0.7, min_value = 0.)
        st.markdown("##### x 좌표 측정 종료값 입력")
        x_end = st.number_input("x 좌표 종료값, 단위: [cm]", value=4.7, min_value = 0.)
        st.markdown("##### x 좌표 간격 입력")
        x_step = st.number_input("x 좌표 간격, 단위: [cm]", value=0.5, min_value = 0.)


        x_coordinates = np.array([x_start + i * x_step for i in range(int((x_end - x_start) / x_step) + 1)])
        st.write(f"x 좌표: {x_coordinates}")

        st.markdown("##### H 실험값")
        if measurement != "직접 입력하기":
            is_user_input = st.checkbox("실험값 직접 입력하기")
        else: is_user_input = st.checkbox("실험값 직접 입력하기", value=True)
    
        if is_user_input:
            # 사용자로부터 숫자 입력 받기
            user_input = st.text_input("H 실험값을 입력하세요 (쉼표 혹은 띄어쓰기로 구분):", placeholder="ex. 1, 2, 3 or 1 2 3")

            if user_input:
                measurement_results = []
                for num_str in re.split(r'[, ]+', user_input):
                    try:
                        num = float(num_str)
                        measurement_results.append(num)
                    except ValueError:
                        st.error("숫자로 변환할 수 없습니다. , 또는 띄어쓰기로 데이터값을 구분해주세요.") 
                measurement_results = np.array(measurement_results)
            
        st.write(f"실험값: {measurement_results}")


        if len(x_coordinates) != len(measurement_results):
            st.error("x 좌표값 개수와 입력된 실험값 개수가 다릅니다.")
            st.write(f"x 좌표 개수 : {len(x_coordinates)}, y 좌표 개수 : {len(measurement_results)}")
        else: 
            st.markdown("##### 최소자승법(LSM)으로 직선 구하기")

            slope, intercept = get_line_with_lsm(x_coordinates, measurement_results)
            line_values = np.array(slope*x_coordinates + intercept)
            st.write(f"최소 자승법으로 구한 직선 방정식: y = {slope:.2f}x + {intercept:.2f}")

            mse = calculate_mse(line_values, measurement_results)
            fig1 = plot_st(measurement_results, line_values,
                x=x_coordinates, title=f"Measurement Data[{measurement}] vs Approximate Line",
                description=f"mse: {mse:.4f}\n Approximate Line: y = {slope:.2f}x + {intercept:.2f}\n ") 
            
            st.pyplot(fig1)

            buffer = io.BytesIO()
            fig1.savefig(buffer, format="png", bbox_inches="tight")
            buffer.seek(0)

            st.download_button(label='Download Graph', data=buffer, file_name=f'{measurement}.png',mime='image/png')

    with col2:
        st.markdown("### 모델 vs 실험값")
        st.markdown("##### 첫번째 코일의 반지름(r1)")
        r1 = st.number_input("r1의 고정값을 입력해주세요. 단위:[cm]", key="r1_value", value=float(params['r1']), min_value=0.01)
        st.markdown("##### 두번째 코일의 반지름(r2)")
        r2 = st.number_input("r2의 고정값을 입력해주세요. 단위:[cm]", key="r2_value", value=float(params['r2']), min_value=0.01)
        st.markdown("##### 두 코일 사이의 거리(d)")
        d = st.number_input("d의 고정값을 입력해주세요. 단위:[cm]", key="d_value", value=float(params['d']), min_value=0.01)
        st.markdown("##### 첫번째 코일의 x축 방향으로 감은 횟수(mf)")
        mf = st.number_input("mf의 고정값을 입력해주세요.", key="mf_value", value=int(params['mf']), min_value=1)
        st.markdown("##### 찻번째 코일의 y축 방향으로 감은 횟수(nf)")
        nf = st.number_input("nf의 고정값을 입력해주세요.", key="nf_value", value=int(params['nf']), min_value=1)
        st.markdown("##### 첫번째 코일 마지막 층의 x축 방향으로 감은 개수(alpha1)")
        alpha1 = st.number_input("첫번째 코일 마지막 층의 x축 방향으로 감은 개수를 입력해주세요.", key="alpha1_value", value=params['alpha1'], min_value=0, max_value=mf-1)
        st.markdown("##### 두번째 코일의 x축 방향으로 감은 횟수(ms)")
        ms = st.number_input("ms의 고정값을 입력해주세요.", key="ms_value", value=int(params['ms']), min_value=1)
        st.markdown("##### 두번째 코일의 y축 방향으로 감은 횟수(ns)")
        ns = st.number_input("ns의 고정값을 입력해주세요.", key="ns_value", value=int(params['ns']), min_value=1)
        st.markdown("##### 두번째 코일 마지막 층의 x축 방향으로 감은 개수(alpha2)")
        alpha2 = st.number_input("두번째 코일 마지막 층의 x축 방향으로 감은 개수를 입력해주세요.", key="alpha2_value", value=params['alpha2'], min_value=0, max_value=ms-1) 
        st.markdown("##### Wire Radius(R)")
        R = st.number_input("초기값은 0.025cm입니다. (0.001 단위는 반올림으로 표시됩니다.)  단위: [cm]",key="R_value", value=params['R'],min_value=0.005, max_value=1.,step=0.005)
        
        st.markdown("##### Step size")    
        step = st.number_input(
            "첫 번째 코일에서 두 번째 코일로 이동하는 길이입니다. 값이 작을수록 데이터가 많아집니다. 단위: [cm]", key="step_value",
            value=params['step'],
            min_value=0.025, 
            max_value=20.
        )
            
        target_value1 = st.number_input(
            "첫 번째 코일의 목표 H값 입니다. 단위:[Oe]",
            value=25.,
            min_value = 0.01
        )

        target_value2 = st.number_input(
            "두 번째 코일의 목표 H값 입니다. 단위:[Oe]",
            value=10.,
            min_value = 0.01
        ) 

        btn_run = st.button("모델, 실험값 비교 실행")
        if btn_run:
            model_results, _ = modified_helmholtz_coil(r1, r2, d, mf, nf, ms, ns, alpha1, alpha2, R, step, target_value1, target_value2)
            
            model_x = np.arange(0, step * len(model_results), step).round(decimals=4)
            if len(model_x) > len(model_results):
                model_x = np.delete(model_x, -1)
            
            model_results = pd.Series(model_results, index=model_x)

            mse = calculate_mse(model_results[x_coordinates], measurement_results)
    
            st.markdown("###### 모델, 실험값 비교")
            fig2 = plot_st(measurement_results, model_results , x1= x_coordinates, step=step, title=f"Model[{measurement_params_key}] vs Measurement Data[{measurement}]", description=f"mse: {mse:.4f}")
            st.pyplot(fig2)
            buffer = io.BytesIO()
            fig2.savefig(buffer, format="png", bbox_inches="tight")
            buffer.seek(0)
            st.download_button(label='Download Graph', data=buffer, file_name=f'{measurement_params_key}.png',mime='image/png')









