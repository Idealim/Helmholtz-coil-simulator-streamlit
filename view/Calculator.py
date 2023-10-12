import streamlit as st
import io
from model.Calculator import optimize

def Calculator_page():
    st.subheader("Model Calculator")
    st.markdown("##### 모델로 예측값을 계산합니다.")
    col1, col2, col3 = st.columns(3, gap='large')

    with col1:
        st.markdown("#### 실험 변수 입력")

        st.markdown("##### 첫번째 코일의 반지름(a1)")
        r1_value = st.number_input("a1의 값을 입력해주세요. 단위:[cm]", value=5.0, min_value=0.01)

        st.markdown("##### 두번째 코일의 반지름(a2)")
        r2_value = st.number_input("a2의 값을 입력해주세요. 단위:[cm]", value=5.0, min_value=0.01)

        st.markdown("##### 두 코일 사이의 거리(d)")
        d_value = st.number_input("d의 고정값을 입력해주세요. 단위:[cm]", value=5.0, min_value=0.01)


        st.markdown("##### 첫번째 코일의 x축 방향으로 감은 횟수(n_x1)")
        mf_value = st.number_input("n_x1의 값을 입력해주세요.", value=5, min_value=0)

        
        st.markdown("##### 찻번째 코일의 y축 방향으로 감은 횟수(n_y1)")
        nf_value = st.number_input("n_y1의 값을 입력해주세요.", value=5, min_value=0)


    with col2:
        st.markdown("#### Helmholtz Coil 추가하기 ")
        st.write("아래 두 변수를 0 으로 설정 시 단일 코일로 계산됩니다.")
        st.markdown("##### 두번째 코일의 x축 방향으로 감은 횟수(n_x2)")
        ms_value = st.number_input("n_x2의 값을 입력해주세요.", value=5, min_value=0)
            
        st.markdown("##### 두번째 코일의 y축 방향으로 감은 횟수(n_y2)")
        ns_value = st.number_input("n_y2의 고정값을 입력해주세요.", value=5, min_value=0)
        st.markdown("#### 시뮬레이션 변수")
        st.markdown("##### Wire Radius(R)")
        R = st.number_input(
            "초기값은 0.025cm입니다. (주의)0.001 단위는 반올림으로 표시됩니다. 단위: [cm]",
            value=0.025,
            min_value=0.005, 
            max_value=1.,
            step=0.005
        )
        step = st.number_input(
            "첫 번째 코일에서 두 번째 코일로 이동하는 길이입니다. 값이 작을수록 데이터가 많아집니다. 단위: [cm]",
            value=0.1,
            min_value=0.025, 
            max_value=20.
        )
        params = {
            'r1': r1_value,
            'r2': r2_value,
            'd': d_value,
            'mf': mf_value,
            'nf': nf_value,
            'ms': ms_value,
            'ns': ns_value,
            'R': R,
            'step': step,
            'n_iter': 1,
            'target_value1': 0,
            'target_value2': 0
        }


    with col3:
        st.subheader('결과')

        btn_run = st.button("실행")

        if btn_run:
            with st.status("모델(예측)값 계산중...") as status:
                best_params, _, fig, predicted_value = optimize(params)
                status.update(label="모델(예측)값 계산 완료!", state="complete", expanded=False)
            st.markdown("##### 시각화")
            st.pyplot(fig)
            buffer = io.BytesIO()
            fig.savefig(buffer, format="png", bbox_inches="tight")
            buffer.seek(0)
            st.download_button(label='Download Graph', data=buffer, file_name=f'{best_params}.png',mime='image/png')
            st.markdown('##### 모델의 예측값')
            st.write(f"{predicted_value}")
            st.markdown("##### 입력된 변수값")
            st.write(f"{best_params}")


            