import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from math import pi
import matplotlib.font_manager as fm
import matplotlib as mpl
import row as row
from matplotlib.path import Path
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D

mpl.rcParams['axes.unicode_minus'] = False

df = pd.read_csv('../backupdata/2020batterstat.csv', index_col=0)  # 타자 데이터 로드 index_col = 0 <- unnamed index 제거
df_dropteam = df.drop(['Team'], axis=1)
# print(df)

#진행상황 표시
from tqdm import tqdm, trange
from time import sleep

larger_categories = list(df_dropteam)[1:]

for i in tqdm(range(len(df)), mininterval=1): #진행상황 표시
    larger_categories = list(df_dropteam)[1:]
    larger_values = df_dropteam.loc[i].drop('NAME').values.flatten().tolist()
    larger_values += larger_values[:1]
    larger_angles = [n / float(len(larger_categories)) * 2 * pi for n in range(len(larger_categories))]
    larger_angles += larger_angles[:1]

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 10),
                           subplot_kw=dict(polar=True))
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    # 한글폰트 사용하는 방법
    path = 'C:/Windows/Fonts/HYPORM.ttf'
    fontprop = fm.FontProperties(fname=path, size=18)

    plt.xticks(larger_angles[:-1], larger_categories,
               color='grey', size=12)
    plt.yticks([0, 20, 40, 60, 80, 100], ['0', '20', '40', '60', '80', '100'],
               color='grey', size=12)
    plt.ylim(0, 100)
    ax.set_rlabel_position(50)

    ax.plot(larger_angles, larger_values, linewidth=1, linestyle='solid')
    ax.fill(larger_angles, larger_values, 'skyblue', alpha=0.4)
    plt.title(df_dropteam.loc[i][0], fontproperties=fontprop)  # fontproperties 로 한글 적용
    # plt.show()
    plt.savefig('./static/batter_stat_img/' + df.loc[i][1] + '_' + df.loc[i][0] + '.png')

