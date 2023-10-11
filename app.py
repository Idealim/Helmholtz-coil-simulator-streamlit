import streamlit as st
from streamlit_option_menu import option_menu
from view import Optimizer_page, Analysis_page, About_page, Calculator_page


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
    selected = option_menu("Helmholtz Coil Simulator", ["About", "Calculator","Optimizer", "Data Analysis"],
                           icons=['house', 'calculator-fill','sliders2', 'graph-up'], menu_icon="magnet-fill"
                           )
if selected == "About":
    About_page()
elif selected == "Calculator":
    Calculator_page()
elif selected == "Optimizer":
    Optimizer_page()
elif selected == "Data Analysis":
    Analysis_page()


