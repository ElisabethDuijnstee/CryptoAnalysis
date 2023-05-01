import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def calculate_pnl(spot, x, n_range):
    pnl_data = []
    for n in n_range:
        lower = spot / n
        upper = spot * n
        spot_range = max(min(spot,upper),lower)
        price_range = np.clip(x, lower, upper)
        y = ((np.sqrt(price_range)) + x/np.sqrt(price_range) - (x/np.sqrt(spot_range)) - np.sqrt(spot_range)) / ((spot_range/np.sqrt(spot_range)) - np.sqrt(lower) + (np.sqrt(spot_range)) - (spot/np.sqrt(upper)))
        pnl_data.append({'n': n, 'pnl': y})
    return pnl_data

def plot_pnl(pnl_data):
    fig, ax = plt.subplots()
    for pnl in pnl_data:
        ax.plot(x, pnl['pnl'], label=f'n: {pnl["n"]:.2f}')
    ax.set_xlabel('Price of Ethereum ($)')
    ax.set_ylabel('IL Rate')
    ax.set_xlim(0, 5000)
    ax.set_ylim(-1.2, 0.2)
    ax.legend()
    ax.grid()
    st.pyplot(fig)

# Define the range of values for x
x = np.linspace(0, 5000, 100)

# Define the range of values for n
n_range = [1.01, 1.10, 1.20, 1.50, 2.00, 10.00, np.inf]

# Create a Streamlit app
st.title('Ethereum Price vs Impermanent Loss')
spot = st.slider('Select the spot price of Ethereum', min_value=0, max_value=5000, value=1500)
pnl_data = calculate_pnl(spot, x, n_range)
plot_pnl(pnl_data)