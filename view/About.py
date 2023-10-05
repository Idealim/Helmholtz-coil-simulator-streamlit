import streamlit as st

def About_page():
    
    col1, col2 = st.columns(2, gap='large')
    with col1:
        st.markdown('''
#### Problem 1. 단일 코일 디자인 
- 코일 중심부의 자기력(Magnetic field Strength)이 `24~26Oe` 사이로 설계
- 코일의 끝부터 `거리에 따른 magnetic field Strength`  구하기
- 설계조건) 1A 이하, 지름 5cm 이상
#### Problem 2. Helmholtz Coil Design 
- `25~10 Oe 까지 선형`으로 변하는 최적의 Helmholtz Coil 설계
- 최적의 의미 = 분산(MSE) 최소화
''')
    with col2:
        st.markdown('''#### Simulator Purpose
- Helmholtz coil Model 설계
- Bayesian Optimizer를 이용한 하이퍼 파라미터 최적화
- 실험값과 모델값 비교''')
    st.markdown("---")
    st.markdown("#### Model of Problem 1")
    st.latex(r'''H=\frac{I}{2}\sum\limits_{n_2=0}^{n_{y}-1}\sum\limits_{n_1=0}^{n_{x}-1}(\frac {(a_1+R+n_2D)^2}{[(x+R+n_1D)^2+(a_1+R+n_2D)^2]^{3/2}})''')
    st.markdown("#### Model of Problem 2")
    st.latex(r''' H=\frac{I}{2}[\sum\limits_{n_2=0}^{n_{y1}-1}\sum\limits_{n_1=0}^{n_{x1}-1}(\frac {(a_1+R+n_2D)^2}{[(x+R+n_1D)^2+(a_1+R+n_2D)^2]^{3/2}})+ 
            \sum\limits_{n_2=0}^{n_{y2}-1}\sum\limits_{n_1=0}^{n_{x2}-1}(\frac {(a_2+R+n_2D)^2}{[(d-x+R+n_1D)^2+(a_2+R+n_2D)^2]^{3/2}})]''')
    st.markdown('''
- 코일 중심에서의 H 식
- Wire의 Diameter, Coil의 x축 y축 감은 개수를 고려한 모델
- 코일의 시작점을 코일의 반지름(r) + 와이어의 반지름(R)로 설정
- 솔레노이드 안 코일의 거리는 와이어의 지름(D)만큼 떨어짐
- 변수
    - a1, a2: 두 코일의 반지름
    - n_x, n_y: 코일의 x축 방향, y축 방향 감은 개수
    - d:코일 중심으로 부터의 거리''')

        
        