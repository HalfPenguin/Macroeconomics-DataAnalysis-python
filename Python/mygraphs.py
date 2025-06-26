import pandas as pd
import matplotlib.pyplot as plt
import io
import matplotlib.ticker as mticker
from datetime import datetime

def international_scatter_plot():
    # Load Inflation Data (inflation, consumer prices)
    inflation_df = pd.read_csv('Data/API_FP/API_FP.CPI.TOTL.ZG_DS2_en_csv_v2_132014.csv', skiprows=4)

    # Load Money Growth Data (broad money growth)
    money_df = pd.read_csv('Data/API_FM/API_FM.LBL.BMNY.ZG_DS2_en_csv_v2_91461.csv', skiprows=4)

    # Identify year columns (all digit columns)
    year_columns_inflation = [col for col in inflation_df.columns if col.isdigit()]
    year_columns_money = [col for col in money_df.columns if col.isdigit()]

    # Melt both dataframes to long format
    inflation_long = inflation_df.melt(
        id_vars=['Country Name'], 
        value_vars=year_columns_inflation, 
        var_name='Year', 
        value_name='Inflation'
    )

    money_long = money_df.melt(
        id_vars=['Country Name'], 
        value_vars=year_columns_money, 
        var_name='Year', 
        value_name='Money Growth'
    )

    # Merge dataframes on 'Country Name' and 'Year'
    merged_df = pd.merge(inflation_long, money_long, on=['Country Name', 'Year'])

    # Convert values to numeric, handling non-numeric gracefully
    merged_df['Inflation'] = pd.to_numeric(merged_df['Inflation'], errors='coerce')
    merged_df['Money Growth'] = pd.to_numeric(merged_df['Money Growth'], errors='coerce')
    merged_df['Year'] = pd.to_numeric(merged_df['Year'], errors='coerce')

    # Drop missing values
    merged_df.dropna(subset=['Inflation', 'Money Growth'], inplace=True)

    # Group by Country and calculate averages
    country_avg = merged_df.groupby('Country Name').agg({
        'Inflation': 'mean',
        'Money Growth': 'mean'
    }).reset_index()

    # Plot
    plt.figure(figsize=(12, 8))
    plt.scatter(country_avg['Money Growth'], country_avg['Inflation'], color='skyblue', edgecolor='k')

    # Annotate points
    for i, row in country_avg.iterrows():
        plt.text(row['Money Growth'], row['Inflation'], row['Country Name'], fontsize=8)

    # Labels and title
    plt.xlabel('Average Money Supply Growth Rate (%)')
    plt.ylabel('Average Inflation Rate (%)')
    plt.title('International data on inflation and money growth')
    plt.grid(True)
    plt.show()

def us_time_series_inflation_money_growth():
     # Load Inflation Data
    inflation_df = pd.read_csv('Data/API_FP/API_FP.CPI.TOTL.ZG_DS2_en_csv_v2_132014.csv', skiprows=4)
    
    # Load Money Growth Data
    money_df = pd.read_csv('Data/API_FM/API_FM.LBL.BMNY.ZG_DS2_en_csv_v2_91461.csv', skiprows=4)
    
    # Filter for United States and relevant columns
    inflation_df = inflation_df[inflation_df['Country Name'] == 'United States']
    money_df = money_df[money_df['Country Name'] == 'United States']
    
    # Keep year columns
    inflation_df = inflation_df[[col for col in inflation_df.columns if col.isdigit()]]
    money_df = money_df[[col for col in money_df.columns if col.isdigit()]]
    
    # Convert to long format
    inflation_long = inflation_df.melt(var_name='Year', value_name='Inflation')
    money_long = money_df.melt(var_name='Year', value_name='Money Growth')
    
    # Convert data types
    inflation_long['Year'] = inflation_long['Year'].astype(int)
    money_long['Year'] = money_long['Year'].astype(int)
    inflation_long['Inflation'] = pd.to_numeric(inflation_long['Inflation'], errors='coerce')
    money_long['Money Growth'] = pd.to_numeric(money_long['Money Growth'], errors='coerce')
    
    # Merge dataframes on Year
    merged_df = pd.merge(inflation_long, money_long, on='Year')
    
    # Drop missing values
    merged_df.dropna(inplace=True)
    
    # Plot line diagram
    plt.figure(figsize=(12, 6))
    plt.plot(merged_df['Year'], merged_df['Inflation'], label='Inflation (%)', color='red', linewidth=2)
    plt.plot(merged_df['Year'], merged_df['Money Growth'], label='Money Growth Rate (%)', color='blue', linewidth=2)
    
    plt.xlabel('Year')
    plt.ylabel('%' + 'Change from 12 months earlier (quarterly)')
    plt.title('US Inflation and Money Growth Rate 1960-2024')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def cpi_and_hourly_earnings():
        # --- Load Data ---
    nominal_df = pd.read_csv('Data/CES0500000003.csv')  # Nominal Hourly Earnings
    cpi_df = pd.read_csv('Data/CPIAUCSL_NBD19470101.csv')  # CPI

    # --- Rename columns ---
    nominal_df.rename(columns={'observation_date': 'Date', 'CES0500000003': 'Nominal_Hourly_Earnings'}, inplace=True)
    cpi_df.rename(columns={'observation_date': 'Date', 'CPIAUCSL_NBD19470101': 'CPI'}, inplace=True)

    # Convert 'Date' to datetime
    nominal_df['Date'] = pd.to_datetime(nominal_df['Date'])
    cpi_df['Date'] = pd.to_datetime(cpi_df['Date'])

    # Filter for 2006-2025
    start_date = datetime(2006, 1, 1)
    end_date = datetime(2025, 12, 31)
    nominal_df = nominal_df[(nominal_df['Date'] >= start_date) & (nominal_df['Date'] <= end_date)]
    cpi_df = cpi_df[(cpi_df['Date'] >= start_date) & (cpi_df['Date'] <= end_date)]

    # Merge on Date
    merged_df = pd.merge(nominal_df, cpi_df, on='Date', how='inner')

    # Resample quarterly for smoothness (optional)
    merged_df.set_index('Date', inplace=True)
    merged_df = merged_df.resample('Q').mean().reset_index()

    # Calculate Real Average Hourly Earnings
    base_cpi = merged_df[merged_df['Date'].dt.year == 2006]['CPI'].iloc[0]
    merged_df['Real_Hourly_Earnings'] = (merged_df['Nominal_Hourly_Earnings'] / merged_df['CPI']) * base_cpi

    # --- Plot ---
    fig, ax1 = plt.subplots(figsize=(12, 7))

    # CPI on left Y-axis
    ax1.plot(merged_df['Date'], merged_df['CPI'], color='red', label='CPI')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('CPI (Index)', color='red')
    ax1.tick_params(axis='y', labelcolor='red')
    ax1.grid(True, linestyle='--', alpha=0.7)

    # Nominal & Real Earnings on right Y-axis
    ax2 = ax1.twinx()
    ax2.plot(merged_df['Date'], merged_df['Nominal_Hourly_Earnings'], color='blue', label='Nominal Hourly Earnings')
    ax2.plot(merged_df['Date'], merged_df['Real_Hourly_Earnings'], color='green', linestyle='--', label='Real Hourly Earnings')
    ax2.set_ylabel('Hourly Earnings ($)', color='blue')
    ax2.tick_params(axis='y', labelcolor='blue')

    # X-axis formatting
    ax1.set_xlim(start_date, end_date)
    ax1.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y'))
    ax1.xaxis.set_major_locator(plt.matplotlib.dates.YearLocator(1))

    # Combine legends from both axes
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

    plt.title('The CPI and average hourly earnings (2006-2025)')
    plt.tight_layout()
    plt.show()


def saving_investment_trade_balance():  
    # --- Load main data (Saving, Investment) ---
    df = pd.read_csv('Data/fredgraph.csv')
    df['Date'] = pd.to_datetime(df['observation_date'])

    # --- Load GDP data ---
    gdp_df = pd.read_csv('Data/GDP.csv')
    gdp_df.rename(columns={'observation_date': 'Date', 'GDP': 'GDP_Billions'}, inplace=True)
    gdp_df['Date'] = pd.to_datetime(gdp_df['Date'])

    # --- Load Net Exports data (billions) ---
    netexp_df = pd.read_csv('Data/NETEXP.csv')
    netexp_df.rename(columns={'observation_date': 'Date', 'NETEXP': 'NetExports_Billions'}, inplace=True)
    netexp_df['Date'] = pd.to_datetime(netexp_df['Date'])

    # --- Calculate Net Exports as % of GDP ---
    netexp_gdp_df = pd.merge(netexp_df, gdp_df, on='Date', how='inner')
    netexp_gdp_df['NetExports_PctGDP'] = (netexp_gdp_df['NetExports_Billions'] / netexp_gdp_df['GDP_Billions']) * 100

    # --- Merge Saving and Investment with GDP ---
    merged_df = pd.merge(df, gdp_df, on='Date', how='inner')
    merged_df['Saving_PctGDP'] = (merged_df['GSAVE'] / merged_df['GDP_Billions']) * 100
    merged_df['Investment_PctGDP'] = (merged_df['GPDI'] / merged_df['GDP_Billions']) * 100

    # --- Filter Saving and Investment from 1990 ---
    saving_investment_df = merged_df[merged_df['Date'].dt.year >= 1990]

    # --- Filter Net Exports from 1990 ---
    netexp_gdp_df_filtered = netexp_gdp_df[netexp_gdp_df['Date'].dt.year >= 1990]

    # --- Plot ---
    plt.figure(figsize=(12, 6))
    plt.plot(saving_investment_df['Date'], saving_investment_df['Saving_PctGDP'],
            label='Saving (% of GDP)', color='blue')
    plt.plot(saving_investment_df['Date'], saving_investment_df['Investment_PctGDP'],
            label='Investment (% of GDP)', color='green')

    # Net Exports as % GDP on right y-axis (filtered from 1990)
    ax = plt.gca()
    ax2 = ax.twinx()
    ax2.plot(netexp_gdp_df_filtered['Date'], netexp_gdp_df_filtered['NetExports_PctGDP'],
            label='Net Exports (% of GDP)', color='red')

    # --- Format ---
    ax.set_xlabel('Year')
    ax.set_ylabel('Saving / Investment (% of GDP)')
    ax.set_ylim(0, 25)            # Left y-axis limits

    ax2.set_ylabel('Trade Balance (% of GDP)', color='red')
    ax2.set_ylim(-10, 20)         # Right y-axis limits
    ax2.tick_params(axis='y', labelcolor='red')

    # Combine legends
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

    plt.title('Saving, Investment, and Trade Balance (% of GDP) Starting from 1990-2024')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


def net_exports_and_federal_budget_deficit():
    # --- Load Data ---
    budget_df = pd.read_csv('Data/FYFSGDA188S.csv')  # Budget deficit (% of GDP)
    netexp_df = pd.read_csv('Data/NETEXP.csv')       # Net exports in billions
    gdp_df = pd.read_csv('Data/GDP.csv')             # GDP in billions

    # --- Rename columns for consistency ---
    budget_df.rename(columns={'observation_date': 'Date', 'FYFSGDA188S': 'Budget_Deficit_PctGDP'}, inplace=True)
    netexp_df.rename(columns={'observation_date': 'Date', 'NETEXP': 'Net_Exports'}, inplace=True)
    gdp_df.rename(columns={'observation_date': 'Date', 'GDP': 'GDP'}, inplace=True)

    # Convert 'Date' columns to datetime
    budget_df['Date'] = pd.to_datetime(budget_df['Date'])
    netexp_df['Date'] = pd.to_datetime(netexp_df['Date'])
    gdp_df['Date'] = pd.to_datetime(gdp_df['Date'])

    # Merge net exports and GDP on Date to calculate Net Exports as % of GDP
    netexp_gdp_df = pd.merge(netexp_df, gdp_df, on='Date', how='inner')
    netexp_gdp_df['Net_Exports_PctGDP'] = (netexp_gdp_df['Net_Exports'] / netexp_gdp_df['GDP']) * 100

    # Now merge budget deficit and net exports % GDP on Date
    combined_df = pd.merge(budget_df, netexp_gdp_df[['Date', 'Net_Exports_PctGDP']], on='Date', how='inner')

    # Extract year for x-axis
    combined_df['Year'] = combined_df['Date'].dt.year

    # --- Plot ---
    plt.figure(figsize=(12, 7))
    plt.plot(combined_df['Year'], combined_df['Budget_Deficit_PctGDP'], label='Budget Deficit (% of GDP)')
    plt.plot(combined_df['Year'], combined_df['Net_Exports_PctGDP'], label='Net Exports (% of GDP)')

    plt.xlabel('Year')
    plt.ylabel('Percentage of GDP (%)')
    plt.title('NX and the federal budget deficit (% of GDP) 1947-2023')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()

    # Set x-axis ticks with steps of 5 years
    min_year = combined_df['Year'].min()
    max_year = combined_df['Year'].max()
    plt.xticks(range(min_year, max_year + 1, 5), rotation=45)

    plt.tight_layout()
    plt.show()



def net_exports_and_real_exchange_rate():
    # --- Load net exports and GDP data ---
    netexp_df = pd.read_csv('Data/NETEXP.csv')
    gdp_df = pd.read_csv('Data/GDP.csv')

    netexp_df.rename(columns={'observation_date': 'Date', 'NETEXP': 'Net_Exports'}, inplace=True)
    gdp_df.rename(columns={'observation_date': 'Date', 'GDP': 'GDP'}, inplace=True)

    netexp_df['Date'] = pd.to_datetime(netexp_df['Date'])
    gdp_df['Date'] = pd.to_datetime(gdp_df['Date'])

    # Merge and compute Net Exports divided by GDP (both in billions)
    netexp_gdp_df = pd.merge(netexp_df, gdp_df, on='Date', how='inner')
    netexp_gdp_df['Net_Exports_to_GDP'] = netexp_gdp_df['Net_Exports'] / netexp_gdp_df['GDP'] * 100

    # --- Load real exchange rate ---
    reer_df = pd.read_csv('Data/RBUSBIS.csv')
    reer_df.rename(columns={'observation_date': 'Date', 'RBUSBIS': 'Real_Exchange_Rate'}, inplace=True)
    reer_df['Date'] = pd.to_datetime(reer_df['Date'])

    # Resample monthly data to quarterly averages and align to quarter end dates
    reer_df.set_index('Date', inplace=True)
    reer_quarterly = reer_df.resample('Q').mean().reset_index()
    reer_quarterly['Date'] = reer_quarterly['Date'] + pd.offsets.QuarterEnd(0)  # Align to quarter end dates

    # Now align netexp_gdp_df['Date'] to quarter end for consistency
    netexp_gdp_df['Date'] = netexp_gdp_df['Date'] + pd.offsets.QuarterEnd(0)

    # Merge on aligned Date column
    combined_df = pd.merge(netexp_gdp_df[['Date', 'Net_Exports_to_GDP']], reer_quarterly, on='Date', how='inner')

    # --- Plot ---
    fig, ax1 = plt.subplots(figsize=(12, 7))

    # Net Exports / GDP on left y-axis
    ax1.plot(combined_df['Date'], combined_df['Net_Exports_to_GDP'], color='blue', label='Net Exports / GDP')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Net Exports / GDP', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y'))
    ax1.xaxis.set_major_locator(plt.matplotlib.dates.YearLocator(base=1))  # Show every year
    plt.xticks(rotation=45)

    # Real Exchange Rate on right y-axis
    ax2 = ax1.twinx()
    ax2.plot(combined_df['Date'], combined_df['Real_Exchange_Rate'], color='red', label='Real Exchange Rate')
    ax2.set_ylabel('Real Exchange Rate (Index)', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    # Combine legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

    plt.title('U.S. net exports and the real exchange rate 1994-2025')
    plt.tight_layout()
    plt.show()

