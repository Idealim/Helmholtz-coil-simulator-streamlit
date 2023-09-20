import streamlit as st
from Calcaulator import optimize


st.set_page_config(layout="wide")
st.header('Helmholtz Coil Simulator', divider='gray')


col1, col2, col3 = st.columns(3, gap='medium')

with col1: 
    st.subheader("Parameters of Helmholtz Coil")
    st.markdown("#### R1")
    r1_step = st.number_input("r1_step [cm]", value=0.1, min_value=0.01)
    
    r1_range = st.slider(
        "Range of Radius of Coil1(r1) [cm]",
        min_value=0.,
        max_value=30.,
        value=(5., 10.),
        step=float(r1_step)
    )
    
    st.markdown("#### R2")
    r2_step = st.number_input("r2_step [cm]", value=0.1, min_value=0.01)
    r2_range = st.slider(
        "Range of Radius of Coil2(r2) [cm]",
        min_value=0.,
        max_value=30.,
        value=(5., 10.),
        step=float(r2_step)
    )
    
    st.markdown("#### d")
    d_step = st.number_input("d_step [cm]", value=0.1, min_value=0.01)
    
    d_range = st.slider(
        "Distance between Coil1 and Coil2 [cm]",
        min_value=0.,
        max_value=30.,
        value=(5., 10.),
        step=float(r2_step)
    )

    st.markdown("#### mf")
    mf = st.slider(
        "# of Coil1 x",
        value=(5,20),
        min_value=1,
        max_value=100,
        step=1
    ) 
    
    st.markdown("#### nf")
    nf = st.slider(
        "# of Coil1 y",
        value=(5,20),
        min_value=1,
        max_value=100,
        step=1
    ) 
    
    st.markdown("#### ms")
    ms = st.slider(
        "# of Coil2 x",
        value=(1,20),
        min_value=1,
        max_value=100,
        step=1
    ) 
    
    st.markdown("#### ns")
    ns = st.slider(
        "# of Coil2 y",
        value=(1,20),
        min_value=1,
        max_value=100,
        step=1
    ) 
    
    st.markdown("####   Parameters of Wire")
    R = st.number_input(
        "Wire Radius [m]",
        value=0.04,
        min_value=0.005, 
        max_value=1.
    )

with col2:
    st.subheader("Parameters of Bayesian-Optimizer")
    step = st.number_input(
        "Step [cm]", 
        value=0.1,
        min_value=0.025, 
        max_value=20.
    )
    
    n_iter = st.number_input(
        "# of iteration",
        value = 100,
        min_value=1,
        max_value =10000
    )
    
    #plot_error = st.toggle("Plot Error Function")
    conpensation = st.toggle("set Start Point 26 Oe & set End Point 11 Oe")
    
    params = {
        'r1': {'min': r1_range[0], 'max': r1_range[1], 'step': r1_step},
        'r2': {'min': r2_range[0], 'max': r2_range[1], 'step': r2_step},
        'd': {'min': d_range[0], 'max': d_range[1], 'step': d_step},
        'mf': {'min': mf[0], 'max': mf[1]},
        'nf': {'min': nf[0], 'max': nf[1]},
        'ms': {'min': ms[0], 'max': ms[1]},
        'ns': {'min': ns[0], 'max': ns[1]},
        'R': R,
        'step': step,
        'n_iter': n_iter,
        'conpensation': conpensation
    }
    st.markdown("#### Parameters")
    st.write(params)
    
with col3: 
    st.subheader('Optimize')
    
    btn_run = st.button("Run")
    
    if btn_run:    
        with st.status("Optimizing"):
            best_params, best_loss, fig, predicted_value = optimize(params)
        st.markdown("#### Plot")
        fig = st.pyplot(fig)
        st.markdown('#### Predicted value')
        st.write(predicted_value)
        st.markdown("#### Best Parameters")
        st.write(best_params)
        st.markdown("#### Best Loss")       
        st.write(best_loss)            
    
    
    
