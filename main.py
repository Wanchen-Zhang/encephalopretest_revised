# Encephalo Investments Coding Pre-Test - Revised April 2020

import pandas as pd
import numpy as np
import math


def cleanse_data(df):
    # Your task here is to remove data from any ticker that isn't XXY, sort chronologically and return a dataframe
    # whose only column is 'Adj Close'
    for i in range(0,335):
        if(df.Ticker[i]!='XXY'):
            df=df.drop(index=i)
    dfclean = df
    return dfclean


def mc_sim(sims, days, df):
    # The code for a crude monte carlo simulation is given below. Your job is to extract the mean expected price
    # on the last day, as well as the 95% confidence interval.
    # Note that the z-score for a 95% confidence interval is 1.960
    
    returns = df.pct_change()
    last_price = df.iloc[-1]

    simulation_df = pd.DataFrame()

    for x in range(sims):
        count = 0
        daily_vol = returns.std()

        price_series = []

        price = last_price * (1 + np.random.normal(0, daily_vol))
        price_series.append(price)

        for y in range(days):
            price = price_series[count] * (1 + np.random.normal(0, daily_vol))
            price_series.append(price)
            count += 1

        simulation_df[x] = price_series
    sum=0
    sum_all=0
    mean=np.zeros(sims)
    for i in range(sims):
        for j in range(len(simulation_df[i])):
                       sum=sum+simulation_df[i][j]
        mean[i]=sum/len(simulation_df[i])
    for k in range(sims):
        sum_all=sum_all+mean[k]
    std=sum_all.std()
    mean_val=sum_all/sims
    ci_95_low=mean_val-1.960*std/np.sqrt(sims)
    ci_95_up=mean_val+1.960*std/np.sqrt(sims)
    ci_95=(ci_95_low,ci_95_up)
    # FILL OUT THE REST OF THE CODE. The above code has given you 'sims' of simulations run 'days' days into the future.
    # Your task is to return the expected price on the last day +/- the 95% confidence interval.
    return mean_val, ci_95

def main():
    filename = '20192020histdata.csv'
    rawdata = pd.read_csv(filename)
    cleansed = cleanse_data(rawdata)
    simnum = 1  # change this number to one that you deem appropriate
    days = 25
    mc_sim(simnum, days, cleansed)
    return


if __name__ == '__main__':
    main()
