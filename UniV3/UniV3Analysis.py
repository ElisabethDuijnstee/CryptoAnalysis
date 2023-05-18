import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def calculate_pnl(spot, x, lower, upper):
    spot_range = max(min(spot,upper),lower)
    price_range = np.clip(x, lower, upper)
    y = ((np.sqrt(price_range)) + x/np.sqrt(price_range) - (x/np.sqrt(spot_range)) - np.sqrt(spot_range)) / ((spot_range/np.sqrt(spot_range)) - np.sqrt(lower) + (np.sqrt(spot_range)) - (spot/np.sqrt(upper)))
    y_hold = ((x/np.sqrt(price_range)) - (x/np.sqrt(upper)) + np.sqrt(price_range) - np.sqrt(lower))/((spot/(np.sqrt(spot))) - (spot/np.sqrt(upper)) + np.sqrt(spot)-np.sqrt(lower)) -1 
    return y, y_hold

def plot_pnl(x, y, y_hold, lower, upper):
    fig, ax = plt.subplots()
    ax.plot(x, y, label = 'y')
    ax.plot(x, y_hold, label = 'y_hold')
    ax.set_xlabel('Price of Ethereum ($)')
    ax.set_ylabel('IL Rate')
    ax.set_xlim(0, 5000)
    ax.set_ylim(-1.2, 1.2)
    ax.legend()
    ax.grid()
    st.pyplot(fig)

# Define the range of values for x
x = np.linspace(0, 5000, 100)

# Create a Streamlit app
st.title('Ethereum Price vs Impermanent Loss')
spot = st.slider('Select the spot price of Ethereum', min_value=0.0, max_value=5000.0, value=1500.0, step=0.01)
lower = st.slider('Select the lower price range', min_value=0.0, max_value=5000.0, value=1000.0, step=0.01)
upper = st.slider('Select the upper price range', min_value=0.0, max_value=5000.0, value=2000.0, step=0.01)
y, y_hold = calculate_pnl(spot, x, lower, upper)
plot_pnl(x, y, y_hold, lower, upper)
