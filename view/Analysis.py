import streamlit as st
from model.Calculator import helmholtz_coil, get_line_with_lsm, calculate_mse
from utils import plot_st
import re
import pandas as pd
import numpy as np

def Analysis_page():
    col1, col2= st.columns(2, gap='large')
    with col1:
        if st.session_state.best_params is not None:   
            st.markdown("##### 첫번째 코일의 반지름(r1)")
            r1 = st.number_input("r1의 고정값을 입력해주세요. 단위:[cm]", value=st.session_state.best_params['r1'], min_value=0.01)
            st.markdown("##### 두번째 코일의 반지름(r2)")
            r2 = st.number_input("r2의 고정값을 입력해주세요. 단위:[cm]", value=st.session_state.best_params['r2'], min_value=0.01)
            st.markdown("##### 두 코일 사이의 거리(d)")
            d = st.number_input("d의 고정값을 입력해주세요. 단위:[cm]", value=st.session_state.best_params['d'], min_value=0.01)
            st.markdown("##### 첫번째 코일의 x축 방향으로 감은 횟수(mf)")
            mf = st.number_input("mf의 고정값을 입력해주세요.", value=int(st.session_state.best_params['mf']), min_value=1)
            st.markdown("##### 찻번째 코일의 y축 방향으로 감은 횟수(nf)")
            nf = st.number_input("nf의 고정값을 입력해주세요.", value=int(st.session_state.best_params['nf']), min_value=1)
            st.markdown("##### 두번째 코일의 x축 방향으로 감은 횟수(ms)")
            ms = st.number_input("ms의 고정값을 입력해주세요.", value=int(st.session_state.best_params['ms']), min_value=1)
            st.markdown("##### 두번째 코일의 y축 방향으로 감은 횟수(ns)")
            ns = st.number_input("ns의 고정값을 입력해주세요.", value=int(st.session_state.best_params['ns']), min_value=1)
            st.markdown("##### Wire Radius(R)")
            R = st.number_input("초기값은 0.025cm입니다. (0.001 단위는 반올림으로 표시됩니다.)  단위: [cm]",value=st.session_state.best_params['R'],min_value=0.005, max_value=1.,step=0.005)
            
            st.markdown("##### Step size")    
            step = st.number_input(
                "첫 번째 코일에서 두 번째 코일로 이동하는 길이입니다. 값이 작을수록 데이터가 많아집니다. 단위: [cm]",
                value=st.session_state.best_params['step'],
                min_value=0.025, 
                max_value=20.
            )
            
            st.markdown("##### 목표 직선 시각화")
            plot_on = st.toggle('목표 직선 시각화')
            if plot_on:
                target_value1 = st.number_input(
                    "첫 번째 코일의 목표 H값 입니다. 단위:[Oe]",
                    value=st.session_state.best_params['target_value1'],
                    min_value = 0.01
                )

                target_value2 = st.number_input(
                    "두 번째 코일의 목표 H값 입니다. 단위:[Oe]",
                    value=st.session_state.best_params['target_value2'],
                    min_value = 0.01
                ) 
        else:
            st.markdown("##### 첫번째 코일의 반지름(r1)")
            r1 = st.number_input("r1의 고정값을 입력해주세요. 단위:[cm]", value=5.0, min_value=0.01)
            st.markdown("##### 두번째 코일의 반지름(r2)")
            r2 = st.number_input("r2의 고정값을 입력해주세요. 단위:[cm]", value=5.0, min_value=0.01)
            st.markdown("##### 두 코일 사이의 거리(d)")
            d = st.number_input("d의 고정값을 입력해주세요. 단위:[cm]", value=5.6, min_value=0.01)
            st.markdown("##### 첫번째 코일의 x축 방향으로 감은 횟수(mf)")
            mf = st.number_input("mf의 고정값을 입력해주세요.", value=19, min_value=1)
            st.markdown("##### 찻번째 코일의 y축 방향으로 감은 횟수(nf)")
            nf = st.number_input("nf의 고정값을 입력해주세요.", value=11, min_value=1)
            st.markdown("##### 두번째 코일의 x축 방향으로 감은 횟수(ms)")
            ms = st.number_input("ms의 고정값을 입력해주세요.", value=9, min_value=1)
            st.markdown("##### 두번째 코일의 y축 방향으로 감은 횟수(ns)")
            ns = st.number_input("ns의 고정값을 입력해주세요.", value=3, min_value=1)
            st.markdown("##### Wire Radius(R)")
            R = st.number_input("초기값은 0.025cm입니다. (주의)0.001 단위는 반올림으로 표시됩니다. 단위: [cm]",value=0.025,min_value=0.005, max_value=1.,step=0.005)
            
            st.markdown("##### Step size")    
            step = st.number_input(
                "첫 번째 코일에서 두 번째 코일로 이동하는 길이입니다. 값이 작을수록 데이터가 많아집니다. 단위: [cm]",
                value=0.1,
                min_value=0.025, 
                max_value=20.
            )
            
            st.markdown("##### 목표 직선 시각화")
            plot_on = st.toggle('목표 직선 시각화')
            if plot_on:
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

        btn_run = st.button("실행")
        if btn_run:
            if plot_on:
                results, target_values = helmholtz_coil(r1, r2, d, mf, nf, ms, ns, R, step, target_value1, target_value2)
            else:
                results, target_values = helmholtz_coil(r1, r2, d, mf, nf, ms, ns, R, step, target_value1=0., target_value2=0.)
            st.markdown("###### 시각화")
            fig = st.pyplot(plot_st(results, target_values, step=step, title="Model vs Target Line"))
            st.markdown("###### 모델 예측값")
            st.write(results)

    with col2:
        st.markdown("#### 실험값 입력")
        st.markdown("##### x 좌표 측정 시작값 입력")
        x_start = st.number_input("x 좌표 시작값, 단위: [cm]", value=0.3, min_value = 0.)
        st.markdown("##### x 좌표 측정 종료값 입력")
        x_end = st.number_input("x 좌표 종료값, 단위: [cm]", value=4.7, min_value = 0.)
        st.markdown("##### x 좌표 간격 입력")
        x_step = st.number_input("x 좌표 간격, 단위: [cm]", value=0.5, min_value = 0.)
        st.markdown("##### H 측정값 입력")


        # 사용자로부터 숫자 입력 받기
        user_input = st.text_input("H 측정값을 입력하세요 (쉼표 혹은 띄어쓰기로 구분):", placeholder="ex. 1, 2, 3 or 1 2 3")

        # 입력 값이 비어 있는지 확분
        if user_input:
            x_coordinates = np.array([x_start + i * x_step for i in range(int((x_end - x_start) / x_step) + 1)])
            measurement_results = []
            for num_str in re.split(r'[, ]+', user_input):
                try:
                    num = float(num_str)
                    measurement_results.append(num)
                except ValueError:
                    st.error("숫자로 변환할 수 없습니다. , 또는 띄어쓰기로 데이터값을 구분해주세요.") 

            if len(x_coordinates) != len(measurement_results):
                st.error("x 좌표값 개수와 입력된 실험값 개수가 다릅니다.")
                st.write(f"x 좌표 개수 : {len(x_coordinates)}, y좌표 개수 : {len(measurement_results)}")
            else: 
                st.markdown("##### 입력된 실험값")
                measurement_results = np.array(measurement_results)

                st.write(x_coordinates)
                st.write(measurement_results)

                slope, intercept = get_line_with_lsm(x_coordinates, measurement_results)
                line_values = np.array(slope*x_coordinates + intercept)
                st.write(f"최소 자승법으로 구한 직선 방정식: y = {slope:.2f}x + {intercept:.2f}")

                mse = calculate_mse(line_values, measurement_results)
                st.write(f"mse: {mse}")

                st.pyplot(plot_st(measurement_results, line_values, x=x_coordinates, title="Measurement Data vs Approximate Line"))









