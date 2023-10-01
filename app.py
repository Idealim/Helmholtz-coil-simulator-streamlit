import streamlit as st
from streamlit_option_menu import option_menu
from view import Optimizer_page, Analysis_page


if 'best_params' not in st.session_state:
    st.session_state.best_params = None


st.set_page_config(layout="wide")
# st.header('Helmholtz Coil Simulator', divider='gray')

st.markdown(f'''
    <style>
        section[data-testid="stSidebar"] .css-ng1t4o {{width: 13rem;}}
        section[data-testid="stSidebar"] .css-1d391kg {{width: 13rem;}}
    </style>
''',unsafe_allow_html=True)

with st.sidebar: 
    selected = option_menu("Helmholtz Coil Simulator", ["About", "Optimizer", "Data Analysis"],
                           icons=['house', 'sliders2', 'graph-up'], menu_icon="magnet-fill"
                           )
if selected == "About":
    st.latex(r'''H=\frac{I}{2}[\sum\limits_{n_2=0}^{nf-1}\sum\limits_{n_1=0}^{mf-1}(\frac {(r_1+R+n_1D)^2}{[(x+R+n_1D)^2+(r_1+R+n_2D)^2]^{3/2}})+ \sum\limits_{n_2=0}^{ns-1}\sum\limits_{n_1=0}^{ms-1}(\frac {(r_2+R+n_1D)^2}{[(d-x+R+n_1D)^2+(r_2+R+n_2D)^2]^{3/2}})]''')
    st.latex(r'''H=\frac{I}{2}[\sum\limits_{n_2=0}^{nf-2}\sum\limits_{n_1=0}^{mf-1}(\frac {(r_1+R+n_1D)^2}{[(x+R+n_1D)^2+(r_1+R+n_2D)^2]^{3/2}})+ \sum\limits_{n_1=0}^{\alpha_1-1}\frac {(r_1+R+n_1D)^2}{[(x+R+n_1D)^2+[r_1+R+(nf-1)D]^2]^{3/2}}+ \sum\limits_{n_2=0}^{ns-2}\sum\limits_{n_1=0}^{ms-1}(\frac {(r_2+R+n_1D)^2}{[(d-x+R+n_1D)^2+(r_2+R+n_2D)^2]^{3/2}})+ \sum\limits_{n_1=0}^{\alpha_2-1}\frac {(r_1+R+n_1D)^2}{[(x+R+n_1D)^2+[r_1+R+(ns-1)D]^2]^{3/2}}]''')
elif selected == "Optimizer":
    Optimizer_page()
elif selected == "Data Analysis":
    Analysis_page()


