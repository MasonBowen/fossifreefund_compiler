# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#%%
import requests
import pandas as pd
import os
import re

#%%

#url = "https://api.fossilfreefunds.org/api/v1/shareclasses?filter%5Bskip%5D=0&filter%5Border%5D%5B0%5D=ussif%20DESC&filter%5Border%5D%5B1%5D=fund_share_class_net_assets%20DESC&filter%5Bwhere%5D%5Bor%5D%5B0%5D%5Bname%5D%5Bregexp%5D=%2F.*morgan%20stanley.*%2Fi&filter%5Bwhere%5D%5Bor%5D%5B0%5D%5Bversion%5D=53.3&filter%5Bwhere%5D%5Band%5D%5B0%5D%5Bportfolio_carbon_relative_carbon_footprint%5D%5Bgt%5D=0&filter%5Bwhere%5D%5Bor%5D%5B1%5D%5Bfund_legal_name%5D%5Bregexp%5D=%2F.*morgan%20stanley.*%2Fi&filter%5Bwhere%5D%5Bor%5D%5B1%5D%5Bversion%5D=53.3&filter%5Bwhere%5D%5Band%5D%5B1%5D%5Bportfolio_carbon_relative_carbon_footprint%5D%5Bgt%5D=0&filter%5Bwhere%5D%5Bor%5D%5B2%5D%5Bfund_family_name%5D%5Bregexp%5D=%2F.*morgan%20stanley.*%2Fi&filter%5Bwhere%5D%5Bor%5D%5B2%5D%5Bversion%5D=53.3&filter%5Bwhere%5D%5Band%5D%5B2%5D%5Bportfolio_carbon_relative_carbon_footprint%5D%5Bgt%5D=0&filter%5Bwhere%5D%5Bor%5D%5B3%5D%5Bticker%5D%5Bregexp%5D=%2F.*morgan%20stanley.*%2Fi&filter%5Bwhere%5D%5Bor%5D%5B3%5D%5Bversion%5D=53.3&filter%5Bwhere%5D%5Band%5D%5B3%5D%5Bportfolio_carbon_relative_carbon_footprint%5D%5Bgt%5D=0"
#url = "https://api.fossilfreefunds.org/api/v1/shareclasses?filter%5Blimit%5D=10000&filter%5Bskip%5D=0&filter%5Border%5D%5B0%5D=ussif%20DESC&filter%5Border%5D%5B1%5D=fund_share_class_net_assets%20DESC&filter%5Bwhere%5D%5Bversion%5D=53.3&filter%5Bwhere%5D%5Bportfolio_carbon_relative_carbon_footprint%5D%5Bgt%5D=0"
url = "https://api.fossilfreefunds.org/api/v1/shareclasses?filter%5Blimit%5D=10000&filter%5Bskip%5D=0"

dir_file_base = os.path.dirname(os.path.realpath(__file__))

#%%

r = requests.get(url)
j = r.json()

#%%
df = pd.DataFrame(j)

df.to_csv(os.path.join(dir_file_base, "stocks_total.csv"), index=False)

#%%
colkeep = ['ticker', 'name', # tracking id info
           'percent_rated', # percent of fund total holdings which fossilfreefunds ('fff') could evaluate
           'fund_family_name','fund_legal_name', 'fund_id', # tracking id info
           'category_group', # type of fund
           'socially_responsible_fund', # is it SRI?
           'inception_date', # date created
           'number_of_holding', # total number of holdings
           'portfolio_carbon_relative_carbon_footprint', # want low, carbon intensity
           'trailing_return_m3', 'trailing_return_y1', 'trailing_return_y3', 'trailing_return_y5', 'trailing_return_y10', 'trailing_return_y15', # performance at different scales (YTD and lifetime also available)
           'badge_count', # fossilfreefunds awards up to 5 badges for different 'achievements'
           'gef_score', # unsure need to look up, could be useful metric
           'grade_fossil', 'grade_deforestation', # fff awards grades (1 == best, 5 == worst) in a variety of categories (tobacco, weapons and gender equality also possible)
           'morningstar_url', # for more information
           'cl_weight', 'cl_count', 'cl_asset', # want high clean 200 count (see fossilfreefunds.org for more info, clean 200 are best 200 companies for fossil free)
           'c2f5coogutweight', 'c2f5coogutasset', # want low, fossil fuel holdings
           'c2weight', # % holdings in top 200 owners of carbon reserves
           'ogweight', # % holdings in oil and gas
           'f5weight', # % holdings in top 30 coal-fired utilities
           'utweight', # % holdings in fossil-fired utilities
           'c2f5coogutcount', # holdings (#) fossil fuels comapnies
           'ussif' # sustainability mandate; 0, 1, 1.5 options
           ] 

df_slim = df.loc[:,colkeep]

convert_numeric_dict = {'percent_rated': float, 
                        'number_of_holding': int,
                        'portfolio_carbon_relative_carbon_footprint': float,
                        'trailing_return_m3': float,
                        'trailing_return_y1': float,
                        'trailing_return_y3': float,
                        'trailing_return_y5': float,
                        'trailing_return_y10': float,
                        'trailing_return_y15': float,
                        'badge_count': int, 
                        'gef_score': float, 
                        'grade_fossil': int, 
                        'grade_deforestation':int,
                        'cl_weight': float, 
                        'cl_count': int, 
                        'cl_asset': float,
                        'c2f5coogutweight': float, 
                        'c2f5coogutasset': float,
                        'c2weight': float,
                        'ogweight': float,
                        'f5weight': float,
                        'utweight': float,
                        'c2f5coogutcount': int,
                        'ussif': float}
                        
df_slim = df_slim.astype(convert_numeric_dict) 

#%%

df_slim = df_slim.loc[(df_slim.grade_fossil==1) & 
                      (df_slim.grade_deforestation==1)&
                      (df_slim.badge_count==5) &
                      (df_slim.percent_rated > .9) &
                      (df_slim.socially_responsible_fund == "true") &
                      (df_slim.ussif >= 1)]

# not interested in real estate and healthcare, keeping aside to track separately (otherwise they take over)
df_health = df_slim.copy().loc[(df_slim['name'].str.contains(re.compile('Healthcare|Health'))) | (df_slim['fund_legal_name'].str.contains(re.compile('Healthcare|Health')))]
df_real_est = df_slim.copy().loc[(df_slim['name'].str.contains(re.compile('Rl Est|Rl Estt|Real Est|Real Estate'))) | (df_slim['fund_legal_name'].str.contains(re.compile('Rl Est|Rl Estt|Real Est|Real Estate')))]

df_slim = df_slim.loc[(~df_slim['name'].str.contains(re.compile('Healthcare|Health|Rl Est|Rl Estt|Real Est|Real Estate'))) & (~df_slim['fund_legal_name'].str.contains(re.compile('Healthcare|Health')))]


#%%

df_final = df_slim.copy()

# clean 200 companies metric best 30% (would it be better to set as separate variable elsewhere and hide most of code?)
df_final = df_final.loc[(df_final.cl_weight >= df_slim.cl_weight.quantile(q=.3))]

# fossil fuel related metrics, best 10% (mostly already super low by this point)
df_final = df_final.loc[(df_final.c2f5coogutweight <= df_slim.c2f5coogutweight.quantile(q=.1))]
df_final = df_final.loc[(df_final.c2weight <= df_slim.c2weight.quantile(q=.1))]
df_final = df_final.loc[(df_final.ogweight <= df_slim.ogweight.quantile(q=.1))]
df_final = df_final.loc[(df_final.f5weight <= df_slim.f5weight.quantile(q=.1))]
df_final = df_final.loc[(df_final.utweight <= df_slim.utweight.quantile(q=.1))]

#%%
# carbon intensity metric, best 30% 
df_final = df_final.loc[(df_final.portfolio_carbon_relative_carbon_footprint <= 
                         df_final.portfolio_carbon_relative_carbon_footprint.quantile(q=.7))]
#%%

# many funds are minor variations on a very similar family of funds
# only want one fund from each 'family'
# grabbing top performing funds by family based on 5 year trailing returns
temp = df_final.copy()[['fund_legal_name', 'trailing_return_y5', 'trailing_return_y3', 'trailing_return_y1']].sort_values(['fund_legal_name', 'trailing_return_y5'], ascending=False)
df_final = df_final.loc[temp.groupby(['fund_legal_name']).head(1).index][:]

df_final.to_csv(os.path.join(dir_file_base, "stocks_filtered.csv"), index=False)

#%%

#df_slim.sort_values(['fund_id', 'fund_legal_name', 'ticker'],  ascending=True, inplace=True)
# want a separate condensed cleaned up csv that I could potentially share with others or fund managers
colkeeptwo = ['ticker', 'fund_legal_name', 'fund_id', 'category_group', 'inception_date', 'number_of_holding',
              'trailing_return_y1', 'trailing_return_y3', 'trailing_return_y5', 'trailing_return_y10', 'trailing_return_y15',
              'morningstar_url']

df_final = df_final.loc[:, colkeeptwo]

df_final['inception_date'] = df_final['inception_date'].map(lambda x: x.split('T', 1)[0])

df_final.rename(columns={'ticker': 'Ticker', 
                        'fund_legal_name': 'Name',
                        'fund_id': 'Fund ID',
                        'category_group': 'Category',
                        'inception_date': 'Inception Date',
                        'number_of_holding': 'No. Holdings',
                        'trailing_return_y1': 'Trailing 1-Yr Returns',
                        'trailing_return_y3': 'Trailing 3-Yr Returns',
                        'trailing_return_y5': 'Trailing 5-Yr Returns',
                        'trailing_return_y10': 'Trailing 10-Yr Returns',
                        'trailing_return_y15': 'Trailing 15-Yr Returns',
                        'morningstar_url': 'Morningstar Website'}, inplace=True)

#%%

df_final.to_csv(os.path.join(dir_file_base, "stocks_filtered_clean.csv"), index=False)