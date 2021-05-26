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

#df1 df2 중복열 제거
df2 = df2.drop(['Team', 'IP' ,'Age', 'ERA', 'PlayerId'],axis=1)
print(df2)

#두 데이터 프레임 합병

kbo_df2 = pd.merge(df1,df2, how='outer',on='Name') #투수는 kbo_df2
#print(kbo_df2)

# 와이번스 소속 선수들의 팀명을 랜더스로 변경, KBO 이름제거, () 제거
kbo_df2['Team'] = kbo_df2['Team'].replace('(.*)Wyverns(.*)', r'\1Landers\2', regex=True) #와이번스 >> 랜더스 변경
kbo_df2['Team'] = kbo_df2['Team'].replace('(.*)KBO', r'\1', regex=True) #KBO제거
kbo_df2['Team'] = kbo_df2['Team'].replace(r'[^\w]', r'', regex=True) #괄호제거
print(kbo_df2)



# 영어 이름 제거
kbo_df2['Name'] = kbo_df2['Name'].str.replace(pat=r'[^가-힣]', repl= r'', regex=True)


#K/9 피안타율 BB/9 HR/9 LOB%(잔루처리율 : 클러치능력)

# 같은 방식으로 삼진잡는 능력도 구한다

# k/9() 스탯의 평균 구하기

k9_mean = kbo_df2['K/9'].mean()
#print(k9_mean)

# K/9 스탯의 표준편차 구하기

k9_std = kbo_df2['K/9'].std()
#print(k9_std)

# Box Plot

#print(sns.boxplot(kbo_df2['K/9']))

k9_q1 = np.percentile(kbo_df2['K/9'], 25)
k9_q3 = np.percentile(kbo_df2['K/9'], 75)
k9_iqr = k9_q3 - k9_q1
k9_lc = k9_q1 - 1.5 * k9_iqr # 아래 울타리
k9_uc = k9_q3 + 1.5 * k9_iqr # 위 울타리

print(k9_lc)
print(k9_uc)


#이상치 변환
kbo_df2['K/9'] = np.clip(kbo_df2['K/9'],k9_lc,k9_uc) #박스플랏에서 아웃라이어 경계를 변환
#print(kbo_df2['K/9'])
#print(sns.boxplot(kbo_df2['K/9'])) #이상치 변환 후 박스플롯

k9_mean = kbo_df2['K/9'].mean()
#print(k9_mean)

# K/9 스탯의 표준편차 구하기

k9_std = kbo_df2['K/9'].std()
#print(k9_std)


 #정규확률분포 그리기
'''
rv = norm(loc = k9_mean, scale = k9_std) #평균이 리그평균타율이고 표준편차가 리그평균타율 표준편차인 정규분포 객체 만들기
x = kbo_df2['K/9'] #X 확률변수 범위
y = rv.pdf(x) #X 범위에 따른 정규확률밀도값
fig, ax = plt.subplots(1,1)
ax.plot(x, y,'bo', ms=8, label = 'normal pdf')
ax.vlines(x, 0, y, colors='b', lw =5, alpha =0.5) #결과는
ax.set_ylim([0,1]) #y축 범위
'''


x = 50/k9_mean #리그평균의 삼진율을 가진 선수의 삼진능력을 50으로 정했을때
kbokstat = kbo_df2['K/9']*x
#print(kbokstat)

#범타처리율 구하기위한 데이터프레임 사전작업
kbo_df2['AVG']=1 - kbo_df2['AVG'] #범타처리율을 알기위해 1 - 피안타율을 한다

#print(kbo_df2['AVG'])

#K/9 피안타율 BB/9 HR/9 LOB%(잔루처리율 : 클러치능력)

# 같은 방식으로 범타처리율 능력도 구한다

# 1-oba(AVG) 스탯의 평균 구하기

avg2_mean = kbo_df2['AVG'].mean()
#print(avg2_mean)

# K/9 스탯의 표준편차 구하기

avg2_std = kbo_df2['AVG'].std()
#print(avg2_std)

# Box Plot

#print(sns.boxplot(kbo_df2['AVG']))

avg2_q1 = np.percentile(kbo_df2['AVG'], 25)
avg2_q3 = np.percentile(kbo_df2['AVG'], 75)
avg2_iqr = avg2_q3 - avg2_q1
avg2_lc = avg2_q1 - 1.5 * avg2_iqr # 아래 울타리
avg2_uc = avg2_q3 + 1.5 * avg2_iqr # 위 울타리

print(avg2_lc)
print(avg2_uc)


#이상치 변
kbo_df2['AVG'] = np.clip(kbo_df2['AVG'],avg2_lc,avg2_uc) #박스플랏에서 아웃라이어 경계를 변환
#print(kbo_df2['AVG'])
#print(sns.boxplot(kbo_df2['AVG'])) #이상치 변환 후 박스플롯

avg2_mean = kbo_df2['AVG'].mean()
#print(avg2_mean)

# 1-범타처리율 스탯의 표준편차 구하기

avg2_std = kbo_df2['AVG'].std()
#print(avg2_std)


 #정규확률분포 그리기
'''
rv = norm(loc = avg2_mean, scale = avg2_std) #평균이 리그평균타율이고 표준편차가 리그평균타율 표준편차인 정규분포 객체 만들기
x = kbo_df2['AVG'] #X 확률변수 범위
y = rv.pdf(x) #X 범위에 따른 정규확률밀도값
fig, ax = plt.subplots(1,1)
ax.plot(x, y,'bo', ms=8, label = 'normal pdf')
ax.vlines(x, 0, y, colors='b', lw =5, alpha =0.5) #결과는
ax.set_ylim([0,10]) #y축 범위
'''


x = 50/avg2_mean #리그평균의 삼진율을 가진 선수의 삼진능력을 50으로 정했을때
kbohstat = kbo_df2['AVG']*x
#print(kbohstat)


# 같은 방식으로 bb9 능력도 구한다

# BB/9(control) 스탯의 평균 구하기

bb9_mean = kbo_df2['BB/9'].mean()
#print(bb9_mean)

# BB/9 스탯의 표준편차 구하기

bb9_std = kbo_df2['BB/9'].std()
#print(bb9_std)

# Box Plot

#sns.boxplot(kbo_df2['BB/9'])
#plt.show()


bb9_q1 = np.percentile(kbo_df2['BB/9'], 25)
bb9_q3 = np.percentile(kbo_df2['BB/9'], 75)
bb9_iqr = bb9_q3 - bb9_q1
bb9_lc = bb9_q1 - 1.5 * bb9_iqr # 아래 울타리
bb9_uc = bb9_q3 + 1.5 * bb9_iqr # 위 울타리

print(bb9_lc)
print(bb9_uc)


#이상치 변
kbo_df2['BB/9'] = np.clip(kbo_df2['BB/9'],bb9_lc,bb9_uc) #박스플랏에서 아웃라이어 경계를 변환
#print(kbo_df2['AVG'])
#print(sns.boxplot(kbo_df2['AVG'])) #이상치 변환 후 박스플롯

bb9_mean = kbo_df2['BB/9'].mean()
print(bb9_mean)

# bb/9 스탯의 표준편차 구하기

bb9_std = kbo_df2['BB/9'].std()
#print(bb9_std)

x = 50/bb9_mean #리그평균의 볼넷율을 가진 선수의 컨트롤능력을 정했을때 bb9는 낮을수록 좋기떄문에 한계 능력치 100에서 뺌
kbocontrolstat = 100 - kbo_df2['BB/9']*x
print(kbocontrolstat)


# 같은 방식으로 HR9 능력도 구한다

# HR/9(구위) 스탯의 평균 구하기

hr9_mean = kbo_df2['HR/9'].mean()
#print(bb9_mean)

# hr9 스탯의 표준편차 구하기

hr9_std = kbo_df2['HR/9'].std()
#print(bb9_std)

# Box Plot

#sns.boxplot(kbo_df2['HR/9'])
#plt.show()


hr9_q1 = np.percentile(kbo_df2['HR/9'], 25)
hr9_q3 = np.percentile(kbo_df2['HR/9'], 75)
hr9_iqr = hr9_q3 - hr9_q1
hr9_lc = hr9_q1 - 1.5 * hr9_iqr # 아래 울타리
hr9_uc = hr9_q3 + 1.5 * hr9_iqr # 위 울타리

print(hr9_lc)
print(hr9_uc)


#이상치 변
kbo_df2['HR/9'] = np.clip(kbo_df2['HR/9'],hr9_lc,hr9_uc) #박스플랏에서 아웃라이어 경계를 변환
#print(kbo_df2['HR/9'])
#print(sns.boxplot(kbo_df2['HR/9'])) #이상치 변환 후 박스플롯

hr9_mean = kbo_df2['HR/9'].mean()
print(hr9_mean)

# bb/9 스탯의 표준편차 구하기

hr9_std = kbo_df2['HR/9'].std()
#print(hr9_std)

x = 50/hr9_mean #리그평균의 홈런저지율을 가진 선수의 구위능력을 정했을때 HR9는 낮을수록 좋기떄문에 한계 능력치 100에서 뺌
kbobreakstat = 100 - kbo_df2['HR/9']*x
print(kbobreakstat)

# 같은 방식으로 클러치 (LOB%) 능력도 구한다

# clu(클러치상황극복) 스탯의 평균 구하기

clu_mean = kbo_df2['LOB%'].mean()
#print(clu_mean)

# clu 스탯의 표준편차 구하기

hr9_std = kbo_df2['LOB%'].std()
#print(clu_std)

# Box Plot

#sns.boxplot(kbo_df2['LOB%'])
#plt.show()


clu_q1 = np.percentile(kbo_df2['LOB%'], 25)
clu_q3 = np.percentile(kbo_df2['LOB%'], 75)
clu_iqr = clu_q3 - clu_q1
clu_lc = clu_q1 - 1.5 * clu_iqr # 아래 울타리
clu_uc = clu_q3 + 1.5 * clu_iqr # 위 울타리

print(clu_lc)
print(clu_uc)


#이상치 변
kbo_df2['LOB%'] = np.clip(kbo_df2['LOB%'],clu_lc,clu_uc) #박스플랏에서 아웃라이어 경계를 변환
#print(kbo_df2['LOB%'])
#print(sns.boxplot(kbo_df2['LOB%'])) #이상치 변환 후 박스플롯

clu_mean = kbo_df2['LOB%'].mean()
print(clu_mean)

# bb/9 스탯의 표준편차 구하기

clu_std = kbo_df2['LOB%'].std()
#print(clu_std)

x = 50/clu_mean #리그평균의 볼넷율을 가진 선수의 컨트롤능력을 50으로 정했을
kboclutchstat =  kbo_df2['LOB%']*x
print(kboclutchstat)


pitcherstat_df = pd.concat([kbo_df2['Name'],kbo_df2['Team'],kbokstat,kbohstat,kbocontrolstat,kbobreakstat,kboclutchstat],axis=1)
print(pitcherstat_df)

pitcherstat_df = pitcherstat_df.rename( {"Name": "NAME",
                       "Team": "Team",
                       "K/9": "K Ability",
                       "AVG": "H Ability",
                       "BB/9": "CONTROL",
                       "HR/9": "BREAK",
                       "LOB%": "CLUTCH"}, axis='columns')
pitcherstat_df = pitcherstat_df.round()
pitcherstat_df = pitcherstat_df.astype({'K Ability':int,
                                      'H Ability':int,
                                      'CONTROL':int,
                                      'BREAK':int,
                                      'CLUTCH':int})

print(pitcherstat_df)

pitcherstat_df.to_csv('./data/2020pitcherstat.csv', encoding='utf-8')


