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
    plt.ylabel('y [Oe]')
    plt.legend()
    plt.show()
    
    
def plot_st(predicted_values, target_values, x=None, step=None, title=None, description=None):
    """
    plot on streamlit app
    """
    num_of_data = len(predicted_values)

    if x is None:
        x = np.arange(0, step * num_of_data, step)
        if len(x) > num_of_data:
            x = np.delete(x, -1)
        
    fig, ax = plt.subplots(figsize=(10,5))  # Figure와 Axes 객체 생성

    if num_of_data < 10: 
        ax.scatter(x, predicted_values, label='predicted_value', marker='x', color='red')
    else:
        ax.plot(x, predicted_values, label='predicted_value', marker='o', linestyle='-', color='blue')
    
    ax.plot(x, target_values, label='target_value', marker='', color='black')
    
    if title is not None:
        ax.set_title(f'{title}', fontsize=12, fontweight='bold')
    else:
        ax.set_title(f'Predicted_value vs Target_value', fontsize=16, fontweight='bold')
    
    ax.set_xlabel('x [cm]')
    ax.set_ylabel('y [Oe]')
    
    if step is not None:
        ax.set_xticks(np.arange(0, step * num_of_data, 0.5))

    if description is not None:
        ax.annotate(f"{description}", (0, 0), xycoords="axes fraction",
            xytext=(0.5, -0.3), textcoords="axes fraction",
            fontsize=11, color="black", horizontalalignment="center")
    
    ax.legend()

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


