import streamlit as st
import pandas as pd 
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import requests
import matplotlib.dates as mdates


def calculate_pnl(spot, x, lower_percent, upper_percent):
    lower = spot * (1 - lower_percent/100)
    upper = spot * (1 + upper_percent/100)
    spot_range = max(min(spot,upper),lower)
    price_range = np.clip(x, lower, upper)
    y = (((x/np.sqrt(price_range)) - (x/np.sqrt(upper)) + np.sqrt(price_range) - (np.sqrt(lower)))/((spot/(np.sqrt(spot_range))) - (spot/np.sqrt(upper)) + np.sqrt(spot_range)-np.sqrt(lower))) -1
    y2 = (np.sqrt(x/spot)) -1
    #y2 = usdc_investment*()
    return y, y2

def plot_pnl(x, y, y2, spot, lower, upper, xlim, ylim):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, name='y', line=dict(color='#b2a2cf')))
    fig.add_trace(go.Scatter(x=x, y=y2, name='yV2', line=dict(color='#8367c7')))
    #fig.add_trace(go.Scatter(x=[spot, spot], y=[0, max(max(y), max(y2))], mode='lines', name='Spot', line=dict(color='black', width=2, dash='dash')))
    fig.update_layout(xaxis_title="Price of Ethereum ($)", yaxis_title="Asset value (USDC)", xaxis_range=xlim, yaxis_range=ylim, title="Ethereum Price vs Impermanent Loss")

    # Get y value at that index
    fig.add_trace(go.Scatter(
        x= x[(x>=lower)&(x<=upper)],
        y = y[(x>=lower)&(x<=upper)],
        fill='tozeroy',
        fillcolor='rgba(128, 0, 128, 0.2)',
        line=dict(color='rgba(255, 255, 255, 0)'),
        hoverinfo='skip',
        showlegend=False
    ))
   
    shape_dict = {
        'type': 'line', 
        'x0': spot, 
        'y0': 0, 
        'x1': spot, 
        'y1': max(max(y), max(y2)),
        'line': dict(color='black', width=1, dash='dot'), 
        'editable': True
    }
    #fig.update_layout(shapes=[shape_dict])

    fig.update_layout(
        shapes=[shape_dict],
        xaxis_title='Price of Ethereum ($)',
        yaxis_title='Asset value (USDC)',
        xaxis_range=xlim,
        yaxis_range=ylim,
        plot_bgcolor='white'
    )
    
    st.plotly_chart(fig)

x = np.linspace(0, 5000, 100)

st.sidebar.header("Select strategy")
spot = st.sidebar.slider('Ethereum spot price', min_value=0.0, max_value=5000.0, value=1500.0, step=0.01)
lower_percent = st.sidebar.slider('Lower bound %', min_value=0.0, max_value=100.0, value=10.0, step=0.1)
upper_percent = st.sidebar.slider('Upper bound %', min_value=0.0, max_value=100.0, value=10.0, step=0.1)
#usdc_investment = st.sidebar.slider('Investment USDC', min_value=0.0, max_value=100000.0, value=1000.0, step=0.01)
y, y2 = calculate_pnl(spot, x, lower_percent, upper_percent)
plot_pnl(x, y, y2, spot, spot*(1-lower_percent/100), spot*(1+upper_percent/100), xlim=(spot-1000,spot+2000), ylim = (-0.5, 0.5))


#create columns
# Create three columns below the plot
col1, col2 = st.columns(2)



# Set the UniswapV3 API endpoint
api_endpoint = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"

# Define the pool address
pool_address = "0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8"

start_date = "2023-01-01T00:00:00Z"
end_date = "2023-02-01T00:00:00Z"

query = """
    query {
        pool(id: "0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8") {
            id
            token0 {
                symbol
            }
            token1 {
                symbol
            }
            poolDayData(last: 100, orderBy: date, orderDirection: desc) {
                date
                liquidity
                volumeUSD
                feesUSD
                tvlUSD
            }
        }
    }
"""

# Send the query to the API endpoint
response = requests.post(api_endpoint, json={'query': query})

# Parse the JSON response into a Pandas DataFrame
data = response.json()['data']['pool']['poolDayData']
df = pd.DataFrame(data)

# Convert the date column to a datetime object and set it as the index
df['date'] = pd.to_datetime(df['date'], unit='s')
df.set_index('date', inplace=True)

df['volumeUSD'] = pd.to_numeric(df["volumeUSD"])
df['feesUSD'] = pd.to_numeric(df["feesUSD"])
df['tvlUSD'] = pd.to_numeric(df["tvlUSD"])

# Method 1: Plot daily volume over time
def plot_daily_volume(df):
    colors = ['#a6bddb','#67a9cf','#1c9099', "ffb6c1"]
    
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(df.index, df['volumeUSD'], width=1, color=colors[1], alpha=0.8)
    ax.axhline(y=df['volumeUSD'].mean(), color='purple', linestyle='--', label='Mean')
    ax.set_ylabel('Volume (USD)')

    # Format the x-axis tick labels as month/day
    date_fmt = '%m/%y'
    date_formatter = plt.matplotlib.dates.DateFormatter(date_fmt)
    ax.xaxis.set_major_formatter(date_formatter)
    
    st.pyplot(fig)

# Method 2: Plot daily fees over time
def plot_daily_fees(df):
    colors = ['#a6bddb','#67a9cf','#1c9099', "ffb6c1"]
    
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(df.index, df['feesUSD'], width=1, color=colors[1], alpha=0.8)
    ax.axhline(y=df['feesUSD'].mean(), color='purple', linestyle='--', label='Mean')
    ax.set_ylabel('Fees (USD)')

    # Format the x-axis tick labels as month/day
    date_fmt = '%m/%y'
    date_formatter = plt.matplotlib.dates.DateFormatter(date_fmt)
    ax.xaxis.set_major_formatter(date_formatter)
    
    st.pyplot(fig)

# Add content to the first column
with col1:
    plot_daily_volume(df)

# Add content to the second column
with col2:
    plot_daily_fees(df)

#create columns
# Create three columns below the plot
col3, col4 = st.columns(2)

def plot_tvl(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(df.index, df['tvlUSD'], color='purple')
    ax.fill_between(df.index, df['tvlUSD'], color='purple', alpha=0.3)
    ax.set_ylabel('TVL (USD)')
    ax.set_xlabel("Date")

    # Format the x-axis tick labels as month/day
    date_fmt = '%m/%y'
    date_formatter = plt.matplotlib.dates.DateFormatter(date_fmt)
    ax.xaxis.set_major_formatter(date_formatter)
    
    st.pyplot(fig)

with col3:
    plot_tvl(df)
