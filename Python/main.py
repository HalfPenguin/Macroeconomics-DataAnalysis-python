import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fredapi import Fred

import mygraphs

# Initialize FRED client with your API key
fred = Fred(api_key='87f6c13666df13a96ad9dd8057abfc44')  # Replace with your actual API key

# Download monthly data
cpi = fred.get_series('CPIAUCSL')  # Consumer Price Index
m2 = fred.get_series('M2SL')       # M2 Money Stock

# Convert to DataFrame
data = pd.DataFrame({'CPI': cpi, 'M2': m2})

# Drop missing values
data.dropna(inplace=True)

# Convert monthly data to quarterly by taking the average
data_quarterly = data.resample('Q').mean()

# Calculate quarterly growth rates using log differences
data_quarterly['CPI_Growth'] = np.log(data_quarterly['CPI']).diff()
data_quarterly['M2_Growth'] = np.log(data_quarterly['M2']).diff()

# Drop the first row with NaN values due to differencing
data_quarterly.dropna(inplace=True)

# Convert growth rates to percentages
data_quarterly['CPI_Growth'] *= 100
data_quarterly['M2_Growth'] *= 100

# Plot the results
plt.figure(figsize=(12, 6))
plt.plot(data_quarterly.index, data_quarterly['CPI_Growth'], label='Inflation Rate (CPI)', color='red')
plt.plot(data_quarterly.index, data_quarterly['M2_Growth'], label='Money Growth Rate (M2)', color='blue')
plt.title('U.S. Inflation and Money Growth Rates (Quarterly) 1960-2025')
plt.xlabel('Date')
plt.ylabel('Growth Rate (%)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

data_quarterly.to_csv('processed_data.csv')

mygraphs.international_scatter_plot()
mygraphs.us_time_series_inflation_money_growth()
mygraphs.cpi_and_hourly_earnings()
mygraphs.saving_investment_trade_balance()
mygraphs.net_exports_and_federal_budget_deficit()
mygraphs.net_exports_and_real_exchange_rate()