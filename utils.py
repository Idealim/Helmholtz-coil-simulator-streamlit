import matplotlib.pyplot as plt
import numpy as np


def plot(predicted_values, actual_values, step, best_params=None):
    num_of_data = len(predicted_values)
    x = np.arange(0, step * num_of_data, step)
    if len(x) > num_of_data:
        x = np.delete(x, -1)
        
    plt.figure(figsize=(10,5))
    plt.plot(x, predicted_values, label='predicted_value', marker='o', linestyle='-', color='blue')
    plt.plot(x, actual_values, label='target_value', marker='', color='black')
    
    if best_params is not None:
        plt.title(f'{best_params}', fontsize=16, fontweight='bold')
    else:
        plt.title(f'Predicted_value vs Target_value', fontsize=16, fontweight='bold')
    plt.xlabel('x [cm]')
    plt.xticks(np.arange(0, step * num_of_data, 0.5))
    plt.ylabel('H [Oe]')
    plt.legend()
    plt.show()
    
    
def plot_st(predicted_values, target_values, x=None, x1=None, x2=None, step=None, title=None, description=None):
    """
    plot on streamlit app
    """
    fig, ax = plt.subplots(figsize=(10,5))  # Figure와 Axes 객체 생성

    # x축 값 생성
    num_of_data1 = len(predicted_values)
    num_of_data2 = len(target_values)

    # x축 data 생성
    if x is not None:
        x1 = x
        x2 = x
    else:
        if x1 is None:
            x1 = np.arange(0, step * num_of_data1, step)
            if len(x1) > num_of_data1:
                x1 = np.delete(x1, -1)

        if x2 is None:
            x2 = np.arange(0, step * num_of_data2, step)
            if len(x2) > num_of_data2:
                x2 = np.delete(x2, -1)


    if num_of_data1 < 20: 
        ax.scatter(x1, predicted_values, label='predicted_value', marker='x', color='red')
    else:
        ax.plot(x1, predicted_values, label='predicted_value', marker='o', linestyle='-', color='blue')
    
    if num_of_data2 < 20:
        ax.plot(x2, target_values, label='predicted_value', linestyle='-', color='black')
    else:  
        ax.plot(x2, target_values, label='target_value', marker='', color='black')
    
    if title is not None:
        ax.set_title(f'{title}', fontsize=12, fontweight='bold')
    else:
        ax.set_title(f'Predicted_value vs Target_value', fontsize=16, fontweight='bold')
   
    ax.set_xlabel('x [cm]')
    ax.set_ylabel('H [Oe]')
    
    # x축 눈금 그리기
    if step is not None: 
        if num_of_data1 > num_of_data2:
            ax.set_xticks(np.arange(0, step * num_of_data1, 0.5)) # x축 눈금 단위 0.5
        else:
            ax.set_xticks(np.arange(0, step * num_of_data2, 0.5)) # x축 눈금 단위 0.5

    if description is not None:
        ax.annotate(f"{description}", (0, 0), xycoords="axes fraction",
            xytext=(0.5, -0.3), textcoords="axes fraction",
            fontsize=11, color="black", horizontalalignment="center")
    
    # ax.legend()

    return fig  # Matplotlib Figure 객체 반환

def plot_error(predicted_values, actual_values, step):
    # 새로운 창에 그래프 그리기
    num_of_data = len(predicted_values)
    x = np.arange(0, step * num_of_data, step)
    if len(x) > num_of_data:
        x = np.delete(x, -1)
        
    diff = np.abs(actual_values-predicted_values)
    
    plt.figure()
    plt.plot(x, diff, linestyle='-', color='red')
    plt.title('Error', fontsize =16, fontweight='bold')
    plt.xlabel('x')
    plt.ylabel('|y1 - y2|')
    plt.grid(True)
    plt.show()


def plot_error_st(values, x=None, step=None, title=None, description=None):
    """
    plot on streamlit app
    """
    fig, ax = plt.subplots(figsize=(10,5))  # Figure와 Axes 객체 생성

    # x축 값 생성
    num_of_data = len(values)

    # x축 data 생성
    if x is None:
        x = np.arange(0, step * num_of_data, step)
        if len(x1) > num_of_data:
            x1 = np.delete(x1, -1)


    ax.plot(x, values, marker='o', linestyle='-', color='blue')
    
    
    if title is not None:
        ax.set_title(f'{title}', fontsize=12, fontweight='bold')
    else:
        ax.set_title(f' ', fontsize=16, fontweight='bold')
   
    ax.set_xlabel('x [cm]')
    ax.set_ylabel('Error Percentage [%]')
    
    # x축 눈금 그리기
    if step is not None: 
        ax.set_xticks(np.arange(0, step * num_of_data, 0.5)) # x축 눈금 단위 0.5

    if description is not None:
        ax.annotate(f"{description}", (0, 0), xycoords="axes fraction",
            xytext=(0.5, -0.3), textcoords="axes fraction",
            fontsize=11, color="black", horizontalalignment="center")
    

    return fig  # Matplotlib Figure 객체 반환