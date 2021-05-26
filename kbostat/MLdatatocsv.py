import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.stats import norm

# kbo pitcher standard stat read csv
df1 = pd.read_csv('./data/2020kbopitcherstandard.csv')
print(df1)

# kbo pitcher advanced stat read csv
df2 = pd.read_csv('./data/2020kbopitcheradvanced.csv')
print(df2)

#df1 df2 열 선택

df1 = df1[['Name', 'ERA']]
df2 = df2[['Name', 'K/9', 'BB/9', 'HR/9']]

#두 데이터 프레임 합병

kbo_df2 = pd.merge(df1,df2, how='outer',on='Name') #투수는 kbo_df2
#print(kbo_df2)


# 영어 이름 제거
kbo_df2['Name'] = kbo_df2['Name'].str.replace(pat=r'[^가-힣]', repl= r'', regex=True)

print(kbo_df2)

kbo_df2.to_csv('./data/2020KBOPML.csv', encoding='utf-8') #kbo pitcher ML