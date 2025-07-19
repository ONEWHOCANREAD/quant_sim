import streamlit as st
from utils.data_loader import get_historical_data
from utils.monte_carlo import run_simulation, plot_simulations
import plotly.io as pio

st.set_page_config(page_title="QuantSim v0.1", layout="wide")

st.title("Monte Carlo Asset Forecaster")

# Sidebar inputs
st.sidebar.header("Simulation Settings")
ticker = st.sidebar.text_input("Asset Ticker", value="AAPL")
days = st.sidebar.slider("Forecast Days", min_value=10, max_value=365, value=30)
num_simulations = st.sidebar.slider("Number of Simulations", 100, 5000, 500, step=100)

# Load data
st.subheader(f"Historical Data for {ticker}")
data = get_historical_data(ticker)

if data is not None:
    st.line_chart(data['Close'])

    st.subheader(f"Monte Carlo Simulations for {days} Days")

    simulations, final_prices = run_simulation(data, days, num_simulations)
    fig = plot_simulations(simulations)
    st.plotly_chart(fig, use_container_width=True)

    
    # Summary stats
    
    last_price = float(data['Close'].iloc[-1])
    mean_final_price = final_prices.mean()
    print("final_prices:", type(final_prices), final_prices.shape)
    print("last_price:", type(last_price), getattr(last_price, 'shape', 'scalar'))
    prob_loss = (final_prices < last_price).mean() * 100

    # Display expected price and loss probability
    st.markdown("""
                    <style>
                        .metric-box {
                            background-color: #ffffff;
                            padding: 10px 20px;
                            border-radius: 12px;
                            display: inline-block;
                            margin: 10px 10px 10px 0;
                            font-size: 16px;
                            color: #003366;
                            box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
                        }
                    </style>
                """, unsafe_allow_html=True)
    st.markdown(f'<div class="metric-box">Expected Price after 30 days: ${mean_final_price:.2f}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-box">Probability of Loss: {prob_loss:.2f}%</div>', unsafe_allow_html=True)


    
    if prob_loss > 60:
        st.error("[-] High risk. Asset is likely to lose value.")
    elif prob_loss < 30:
        st.success("[+] Good potential. Upside likely.")
    else:
        st.warning("[!] Uncertain. Moderate risk.")

else:
    st.error("Failed to fetch historical data. Please check the ticker.")
