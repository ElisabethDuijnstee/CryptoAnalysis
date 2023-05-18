import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import altair as alt 

def calculate_pnl(spot, x, lower_percent, upper_percent, usdc_investment):
    lower = spot * (1 - lower_percent/100)
    upper = spot * (1 + upper_percent/100)
    spot_range = max(min(spot,upper),lower)
    price_range = np.clip(x, lower, upper)
    y = usdc_investment*((x/np.sqrt(price_range)) - (x/np.sqrt(upper)) + np.sqrt(price_range) - np.sqrt(lower))/((spot/(np.sqrt(spot))) - (spot/np.sqrt(upper)) + np.sqrt(spot)-np.sqrt(lower)) -1
    #y_hold = ((x/np.sqrt(price_range)) - (x/np.sqrt(upper)) + np.sqrt(price_range) - np.sqrt(lower))/((spot/(np.sqrt(spot))) - (spot/np.sqrt(upper)) + np.sqrt(spot)-np.sqrt(lower)) -1 
    y2 = usdc_investment*(np.sqrt(x/spot)) -1
    return y, y2


def plot_pnl(x, y, y2, lower, upper, xlim, ylim):
    fig, ax = plt.subplots()
    colors = ['#8367c7', '#b2a2cf', '#cab2d6']
    ax.plot(x, y, label = 'y', color = colors[1] )
    ax.plot(x, y2, label = 'yV2', color = colors[0] )
    ax.fill_between(x, y, 0, where=(lower < x) & (x < upper), color=colors[0], alpha=0.5)
    ax.axvline(x=spot, linestyle='--', color='black', label='Spot')
    #ax.plot(x, y_hold, label = 'y_hold')
    ax.set_xlabel('Price of Ethereum ($)')
    ax.set_ylabel('Asset value (USDC)')
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.legend()
    ax.grid()
    st.pyplot(fig)

# Define the range of values for x
x = np.linspace(0, 5000, 100)

# Create a Streamlit app
st.title('Ethereum Price vs Impermanent Loss')
spot = st.slider('Select the spot price of Ethereum', min_value=0.0, max_value=5000.0, value=1500.0, step=0.01)
lower_percent = st.slider('Select the lower price range as a percentage of the spot price', min_value=0.0, max_value=100.0, value=10.0, step=0.1)
upper_percent = st.slider('Select the upper price range as a percentage of the spot price', min_value=0.0, max_value=100.0, value=10.0, step=0.1)
#lower = st.slider('Select the lower price range', min_value=0.0, max_value=5000.0, value=1000.0, step=0.01)
#upper = st.slider('Select the upper price range', min_value=0.0, max_value=5000.0, value=2000.0, step=0.01)
usdc_investment = st.slider('Select the USDC investment amount', min_value=0.0, max_value=100000.0, value=1000.0, step=0.01)
y, y2 = calculate_pnl(spot, x, lower_percent, upper_percent, usdc_investment)
plot_pnl(x, y, y2, spot*(1-lower_percent/100), spot*(1+upper_percent/100), xlim=(spot-1000,spot+2000), ylim = (usdc_investment-1000, usdc_investment+1000))
#((spot*(1-lower_percent/100))-1000, (spot*(1+upper_percent/100))+1000)


def plot_pnl_fill_between_y_y1(x, y, y2, spot, lower, upper, xlim, ylim):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=x, y=y, name='y', line=dict(color='royalblue')))
    fig.add_trace(go.Scatter(x=x, y=y2, name='yV2', line=dict(color='darkorange')))

    # Add filled area
    fig.add_trace(go.Scatter(
        x=np.concatenate([x, x[::-1]]),
        y=np.concatenate([np.clip(y, 0, np.inf), np.clip(y2[::-1], 0, np.inf)]),
        fill='toself',
        fillcolor='lightblue',
        line=dict(color='rgba(255, 255, 255, 0)'),
        hoverinfo='skip',
        showlegend=False
    ))