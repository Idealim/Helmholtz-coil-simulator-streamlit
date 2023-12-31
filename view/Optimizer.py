import streamlit as st
from model.Calculator import optimize
import io

def Optimizer_page():

    col1, col2, col3 = st.columns(3, gap='large')

    with col1:
        st.subheader("하이퍼 파리미터 설정")
        st.markdown("##### 첫번째 코일의 반지름(a1)")
        r1_fixed = st.checkbox("a1 고정하기")

        if r1_fixed:
            r1_value = st.number_input("a1의 고정값을 입력해주세요. 단위:[cm]", value=5.0, min_value=0.01)
        else:
            r1_step = st.number_input(
                "a1의 단위 입니다. 최적의 a1 단위의 배수 값을 찾습니다. "
                "ex. 0.5인 경우 a1 = 5 or 5.5 or 6 ... 단위:[cm]",
                value=0.5, min_value=0.01)
            r1_range = st.slider(
                "첫번째 코일의 반지름 범위입니다. 해당 범위 안에서 최적의 a1 값을 찾습니다. 단위: [cm]",
                min_value=0.,
                max_value=30.,
                value=(5., 10.),
                step=float(r1_step)
            )
        
        st.markdown("##### 두번째 코일의 반지름(a2)")
        
        r2_fixed = st.checkbox("a2 고정하기")
        if r2_fixed:
            r2_value = st.number_input("a2의 고정값을 입력해주세요. 단위:[cm]", value=5.0, min_value=0.01)
        else:
            r2_step = st.number_input(
                "a2의 단위 입니다. 최적의 a2 단위의 배수 값을 찾습니다. "
                "ex. 0.5인 경우 a2 = 5 or 5.5 or 6 ... 단위:[cm]",
                value=0.5, min_value=0.01
            )
            r2_range = st.slider(
                "두번째 코일의 반지름 범위입니다. 해당 범위 안에서 최적의 a2 값을 찾습니다. 단위: [cm]",
                min_value=0.,
                max_value=30.,
                value=(5., 10.),
                step=float(r2_step)
            )
        
        st.markdown("##### 두 코일 사이의 거리(d)")
        d_fixed = st.checkbox("d값 고정하기")
        if d_fixed:
            d_value = st.number_input("d의 고정값을 입력해주세요. 단위:[cm]", value=5.0, min_value=0.01)
        else:
            d_step = st.number_input("d의 단위입니다. 최적의 d 단위 배수 값을 찾습니다. 단위:[cm]", value=0.5, min_value=0.01)
            d_range = st.slider(
                "두 코일 사이의 거리의 범위입니다. [cm]",
                min_value=0.,
                max_value=30.,
                value=(5., 10.),
                step=float(d_step)
            )

        st.markdown("##### 첫번째 코일의 x축 방향으로 감은 횟수(n_x1)")

        mf_fixed = st.checkbox("n_x1 고정하기")
        if mf_fixed:
            mf_value = st.number_input("n_x1의 고정값을 입력해주세요.", value=5, min_value=0)
        else:
            mf = st.slider(
                "n_x1의 범위입니다.",
                value=(5,20),
                min_value=1,
                max_value=100,
                step=1
            ) 
        
        st.markdown("##### 찻번째 코일의 y축 방향으로 감은 횟수(n_y1)")
        
        nf_fixed = st.checkbox("n_y1 고정하기")
        if nf_fixed:
            nf_value = st.number_input("n_y1의 고정값을 입력해주세요.", value=5, min_value=0)
        else:
            nf = st.slider(
                "n_y1의 범위입니다.",
                value=(5,20),
                min_value=1,
                max_value=100,
                step=1
            ) 

        st.markdown("##### 두번째 코일의 x축 방향으로 감은 횟수(n_x2)")
        ms_fixed = st.checkbox("n_x2 고정하기")
        if ms_fixed:
            ms_value = st.number_input("n_x2의 고정값을 입력해주세요.", value=5, min_value=0)
        else:
            ms = st.slider(
                "n_x2의 범위입니다.",
                value=(1,20),
                min_value=1,
                max_value=100,
                step=1
            ) 
            
        st.markdown("##### 두번째 코일의 y축 방향으로 감은 횟수(n_y2)")
        ns_fixed = st.checkbox("n_y2 고정하기")
        if ns_fixed:
            ns_value = st.number_input("n_y2의 고정값을 입력해주세요.", value=5, min_value=0)
        else:    
            ns = st.slider(
                "n_y2의 범위입니다.",
                value=(1,20),
                min_value=1,
                max_value=100,
                step=1
            ) 
        
        st.markdown("##### Wire Radius(R)")
        R = st.number_input(
            "초기값은 0.025cm입니다. (주의)0.001 단위는 반올림으로 표시됩니다. 단위: [cm]",
            value=0.025,
            min_value=0.005, 
            max_value=1.,
            step=0.005
        )

    with col2:
        st.subheader("베이지안 최적화")
        st.write("하이퍼파라미터 최적화 도구입니다.")
        step = st.number_input(
            "첫 번째 코일에서 두 번째 코일로 이동하는 길이입니다. 값이 작을수록 데이터가 많아집니다. 단위: [cm]",
            value=0.1,
            min_value=0.025, 
            max_value=20.
        )
        
        n_iter = st.number_input(
            "반복 횟수입니다. 반복 횟수를 증가시킬수록 정확도가 높아집니다. (단, 시간 소요 증가)",
            value = 500,
            min_value=1,
            max_value =5000
        )

        st.markdown("##### 목표값 설정")
        #plot_error = st.toggle("Plot Error Function")
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
        
        params = {
            'r1': {'min': r1_range[0], 'max': r1_range[1], 'step': r1_step} if not r1_fixed else r1_value,
            'r2': {'min': r2_range[0], 'max': r2_range[1], 'step': r2_step} if not r2_fixed else r2_value,
            'd': {'min': d_range[0], 'max': d_range[1], 'step': d_step} if not d_fixed else d_value,
            'mf': {'min': mf[0], 'max': mf[1]} if not mf_fixed else mf_value,
            'nf': {'min': nf[0], 'max': nf[1]} if not nf_fixed else nf_value,
            'ms': {'min': ms[0], 'max': ms[1]} if not ms_fixed else ms_value,
            'ns': {'min': ns[0], 'max': ns[1]} if not ns_fixed else ns_value,
            'R': R,
            'step': step,
            'n_iter': n_iter,
            'target_value1': target_value1,
            'target_value2': target_value2
        }
        st.markdown("##### 설정한 하이퍼파라미터 값")
        st.write(params)

    with col3:
        st.subheader('결과')

        btn_run = st.button("실행")

        if btn_run:
            with st.status("최적화 진행중...") as status:
                best_params, best_loss, fig, predicted_value = optimize(params)
                status.update(label="최적화 완료!", state="complete", expanded=False)
            st.markdown("##### 시각화")
            st.pyplot(fig)
            buffer = io.BytesIO()
            fig.savefig(buffer, format="png", bbox_inches="tight")
            buffer.seek(0)
            st.download_button(label='Download Graph', data=buffer, file_name=f'{best_params}.png',mime='image/png')
            st.markdown('##### 모델의 예측값')
            st.write(f"{predicted_value}")
            st.markdown("##### 최적의 하이퍼 파라미터값")
            st.write(f"{best_params}")
            st.markdown("##### 최적의 손실값")
            st.write(best_loss)
            st.session_state.best_params = best_params
            