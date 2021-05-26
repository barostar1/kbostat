
# 모듈 없을 시 설치

import re
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np 
import seaborn as sns
from scipy.stats import norm


# kbo batter standard stat read csv
df1 = pd.read_csv('./data/2020kbobatstandard.csv')
#print(df1)

# kbo batter advanced stat read csv
df2 = pd.read_csv('./data/2020kbobatadvanced.csv')
#print(df2)

#df1 df2 중복열 제거

df2 = df2.drop(['Team', 'Age', 'PA' ,'AVG','PlayerId'],axis=1)
print(df2)

#두 데이터 프레임 합병

kbo_df = pd.merge(df1,df2, how='outer',on='Name')
#print(kbo_df)

# 와이번스 소속 선수들의 팀명을 랜더스로 변경, KBO 이름제거, () 제거
kbo_df['Team'] = kbo_df['Team'].replace('(.*)Wyverns(.*)', r'\1Landers\2', regex=True) #와이번스 >> 랜더스 변경
kbo_df['Team'] = kbo_df['Team'].replace('(.*)KBO', r'\1', regex=True) #KBO제거
kbo_df['Team'] = kbo_df['Team'].replace(r'[^\w]', r'', regex=True) #괄호제거
print(kbo_df)

# 영어 이름 제거
kbo_df['Name'] = kbo_df['Name'].str.replace(pat=r'[^가-힣]', repl= r'', regex=True)

# ISO 스탯의 평균 구하기 (ISO 는 장타율에 비하여 순수한 파워력을 보여줄수있는 지표) SLG가 아닌 iso로 하는 이유는 4할치는 단타유형의 타자는 거포가 아니기 때문
print(kbo_df['Name'])

pow_mean = kbo_df['ISO'].mean()
print(pow_mean)

# ISO 스탯의 표준편차 구하기

pow_std = kbo_df['ISO'].std()
print(pow_std)

# Box Plot

#print(sns.boxplot(kbo_df['ISO']))

#이상치 한계선
pow_q1 = np.percentile(kbo_df['ISO'], 25) 
pow_q3 = np.percentile(kbo_df['ISO'], 75)
pow_iqr = pow_q3 - pow_q1
pow_lc = pow_q1 - 1.5 * pow_iqr # 아래 울타리
pow_uc = pow_q3 + 1.5 * pow_iqr # 위 울타리

#이상치 변환
kbo_df['ISO'] = np.clip(kbo_df['ISO'],pow_lc,pow_uc) #박스플랏에서 아웃라이어 경계인 0.1과 0.6 이상인 선수들을 0.1, 0.6으로 변환
#print(kbo_df['ISO'])
#print(sns.boxplot(kbo_df['ISO'])) #이상치 변환 후 박스플롯

pow_mean = kbo_df['ISO'].mean()
#print(pow_mean)

# ISO 스탯의 표준편차 구하기

pow_std = kbo_df['ISO'].std()
#print(pow_std)


 #정규확률분포 그리기
'''
rv = norm(loc = pow_mean, scale = pow_std) #평균이 리그평균장타율이고 표준편차가 리그평균장타율 표준편차인 정규분포 객체 만들기
x = kbo_df['ISO'] #X 확률변수 범위
y = rv.pdf(x) #X 범위에 따른 정규확률밀도값
fig, ax = plt.subplots(1,1) 
ax.plot(x, y,'bo', ms=8, label = 'normal pdf')
ax.vlines(x, 0, y, colors='b', lw =5, alpha =0.5) #결과는
ax.set_ylim([0,10]) #y축 범위
'''
# 장타력을 기반으로한 파워스탯 (하지만 장타력=힘 자체는 아니다. 따라서 2루타와 홈런의 가중치 변경할 고민도 해봐야함, 스탯캐스트 데이터를 알수있다면 더 좋을텐데)

x = (100/3)/pow_mean #리그평균의 장타율을 가진 선수의 파워 (100/3)으로 정했을때
kbopowerstat = kbo_df['ISO']*x
print(kbopowerstat)

# 같은 방식으로 컨택능력도 구한다

# AVG(Contact) 스탯의 평균 구하기

avg_mean = kbo_df['AVG'].mean()
#print(avg_mean)

# AVG 스탯의 표준편차 구하기

avg_std = kbo_df['AVG'].std()
#print(avg_std)

# Box Plot

#print(sns.boxplot(kbo_df['AVG']))

avg_q1 = np.percentile(kbo_df['AVG'], 25) 
avg_q3 = np.percentile(kbo_df['AVG'], 75)
avg_iqr = avg_q3 - avg_q1
avg_lc = avg_q1 - 1.5 * avg_iqr # 아래 울타리
avg_uc = avg_q3 + 1.5 * avg_iqr # 위 울타리

print(avg_lc)
print(avg_uc)


#이상치 변환
kbo_df['AVG'] = np.clip(kbo_df['AVG'],avg_lc,avg_uc) #박스플랏에서 아웃라이어 경계를 변환
#print(kbo_df['AVG'])
#print(sns.boxplot(kbo_df['AVG'])) #이상치 변환 후 박스플롯

avg_mean = kbo_df['AVG'].mean()
print(avg_mean)

# avg 스탯의 표준편차 구하기

avg_std = kbo_df['AVG'].std()
print(avg_std)


 #정규확률분포 그리기
'''
rv = norm(loc = avg_mean, scale = avg_std) #평균이 리그평균타율이고 표준편차가 리그평균타율 표준편차인 정규분포 객체 만들기
x = kbo_df['AVG'] #X 확률변수 범위
y = rv.pdf(x) #X 범위에 따른 정규확률밀도값
fig, ax = plt.subplots(1,1) 
ax.plot(x, y,'bo', ms=8, label = 'normal pdf')
ax.vlines(x, 0, y, colors='b', lw =5, alpha =0.5) #결과는
ax.set_ylim([0,10]) #y축 범위
'''
# 타율을 기반으로한 컨택스탯

x = 50/avg_mean #리그평균의 장타율을 가진 선수의 컨택능력을 50으로 정했을때
kbocontactstat = kbo_df['AVG']*x
print(kbocontactstat)

# 같은 방식으로 선구안 능력도 구한다 bb% 이용

# BB(Vision) 스탯의 평균 구하기

bb_mean = kbo_df['BB%'].mean()
#print(bb_mean)

# BB 스탯의 표준편차 구하기

bb_std = kbo_df['BB%'].std()
#print(bb_std)

# Box Plot

#print(sns.boxplot(kbo_df['BB%']))

bb_q1 = np.percentile(kbo_df['BB%'], 25) 
bb_q3 = np.percentile(kbo_df['BB%'], 75)
bb_iqr = bb_q3 - bb_q1
bb_lc = bb_q1 - 1.5 * bb_iqr # 아래 울타리
bb_uc = bb_q3 + 1.5 * bb_iqr # 위 울타리

print(bb_lc)
print(bb_uc)


#이상치 변환
kbo_df['BB%'] = np.clip(kbo_df['BB%'],bb_lc,bb_uc) #박스플랏에서 아웃라이어 경계를 변환
#print(kbo_df['BB%'])
#print(sns.boxplot(kbo_df['BB%'])) #이상치 변환 후 박스플롯

bb_mean = kbo_df['BB%'].mean()
#print(bb_mean)

# BB 스탯의 표준편차 구하기

bb_std = kbo_df['BB%'].std()
#print(bb_std)


 #정규확률분포 그리기
'''
rv = norm(loc = bb_mean, scale = bb_std) #평균이 리그평균타율이고 표준편차가 리그평균타율 표준편차인 정규분포 객체 만들기
x = kbo_df['BB%'] #X 확률변수 범위
y = rv.pdf(x) #X 범위에 따른 정규확률밀도값
fig, ax = plt.subplots(1,1) 
ax.plot(x, y,'bo', ms=8, label = 'normal pdf')
ax.vlines(x, 0, y, colors='b', lw =5, alpha =0.5) #결과는
ax.set_ylim([0,10]) #y축 범위
'''
# 타율을 기반으로한 선구안스탯 

x = 50/bb_mean #리그평균의 볼넷률을 가진 선수의 선구안능력을 50으로 정했을때
kbovisionstat = kbo_df['BB%']*x
print(kbovisionstat)

#
kbo_df['wSB']=kbo_df['wSB']+2 #음수인 부분을 제거하기위해 분포를 균등하게 +2만큼 우측으로 이동시킨다/

# 같은 방식으로 베이스러닝 능력도 구한다 wSB 이용

# br(wSB) 스탯의 평균 구하기

br_mean = kbo_df['wSB'].mean()
#print(br_mean)

# wSB 스탯의 표준편차 구하기

br_std = kbo_df['wSB'].std()
#print(br_std)

# Box Plot

#print(sns.boxplot(kbo_df['wSB']))

br_q1 = np.percentile(kbo_df['wSB'], 25) 
br_q3 = np.percentile(kbo_df['wSB'], 75)
br_iqr = br_q3 - br_q1
br_lc = br_q1 - 1.5 * br_iqr # 아래 울타리
br_uc = br_q3 + 1.5 * br_iqr # 위 울타리

print(br_lc)
print(br_uc)


#이상치 변환
kbo_df['wSB'] = np.clip(kbo_df['wSB'],br_lc,br_uc) #박스플랏에서 아웃라이어 경계를 변환
#print(kbo_df['wSB'])
#print(sns.boxplot(kbo_df['wSB'])) #이상치 변환 후 박스플롯

#br 스탯의 평균 구하기

br_mean = kbo_df['wSB'].mean()
#print(br_mean)

# br 스탯의 표준편차 구하기

br_std = kbo_df['wSB'].std()
#print(br_std)


 #정규확률분포 그리기
'''
rv = norm(loc = br_mean, scale = br_std) #평균이 리그평균주루능력이고 표준편차가 리그평균주루능력 표준편차인 정규분포 객체 만들기
x = kbo_df['wSB'] #X 확률변수 범위
y = rv.pdf(x) #X 범위에 따른 정규확률밀도값
fig, ax = plt.subplots(1,1) 
ax.plot(x, y,'bo', ms=8, label = 'normal pdf')
ax.vlines(x, 0, y, colors='b', lw =5, alpha =0.5) #결과는
ax.set_ylim([0,10]) #y축 범위
'''
# wSB를 기반으로한 베이스러닝 능력 

x = 50/br_mean #리그평균의 베이스러닝실력을 가진 선수의 능력치를 50으로 정했을때
kbobrstat = kbo_df['wSB']*x
#print(kbobrstat)

#print(sns.boxplot(kbo_df['wSB']))

# 같은 방식으로 베이스러닝 능력도 구한다 wSB 이용

# Spd(Spd) 스탯의 평균 구하기

spd_mean = kbo_df['Spd'].mean()
#print(spd_mean)

# Spd 스탯의 표준편차 구하기

spd_std = kbo_df['Spd'].std()
print(spd_std)

# Box Plot

#print(sns.boxplot(kbo_df['Spd']))

spd_q1 = np.percentile(kbo_df['Spd'], 25) 
spd_q3 = np.percentile(kbo_df['Spd'], 75)
spd_iqr = spd_q3 - spd_q1
spd_lc = spd_q1 - 1.5 * spd_iqr # 아래 울타리
spd_uc = spd_q3 + 1.5 * spd_iqr # 위 울타리

print(spd_lc)
print(spd_uc)


#이상치 변환
kbo_df['Spd'] = np.clip(kbo_df['Spd'],spd_lc,spd_uc) #박스플랏에서 아웃라이어 경계를 변환
print(kbo_df['Spd'])
print(sns.boxplot(kbo_df['Spd'])) #이상치 변환 후 박스플롯

#Spd 스탯의 평균 구하기

spd_mean = kbo_df['Spd'].mean()
#print(spd_mean)

# br 스탯의 표준편차 구하기

spd_std = kbo_df['Spd'].std()
#print(spd_std)


 #정규확률분포 그리기
'''
rv = norm(loc = spd_mean, scale = spd_std) #평균이 리그평균주루능력이고 표준편차가 리그평균주루능력 표준편차인 정규분포 객체 만들기
x = kbo_df['Spd'] #X 확률변수 범위
y = rv.pdf(x) #X 범위에 따른 정규확률밀도값
fig, ax = plt.subplots(1,1) 
ax.plot(x, y,'bo', ms=8, label = 'normal pdf')
ax.vlines(x, 0, y, colors='b', lw =5, alpha =0.5) #결과는
ax.set_ylim([0,10]) #y축 범위
'''
# Spd를 기반으로한 스피드 능력 

x = 50/spd_mean #리그평균의 베이스러닝실력을 가진 선수의 능력치를 50으로 정했을때
kbospdstat = kbo_df['Spd']*x*(4/5)
print(kbobrstat)

batterstat_df = pd.concat([kbo_df['Name'],kbo_df['Team'],kbopowerstat,kbocontactstat,kbovisionstat,kbospdstat,kbobrstat],axis=1)
print(batterstat_df)

batterstat_df = batterstat_df.rename( {"Name": "NAME",
                       "Team": "Team",
                       "ISO": "POWER",
                       "AVG": "CONTACT",
                       "BB%": "VISION",
                       "Spd": "SPEED",
                       "wSB": "BASERUNNING"}, axis='columns')
batterstat_df = batterstat_df.round()
batterstat_df = batterstat_df.astype({'POWER':int,
                                      'CONTACT':int,
                                      'VISION':int,
                                      'SPEED':int,
                                      'BASERUNNING':int})
print(batterstat_df)

batterstat_df.to_csv('./data/2020batterstat.csv', encoding='utf-8')


