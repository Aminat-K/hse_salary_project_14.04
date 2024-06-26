# -*- coding: utf-8 -*-
"""анализ_зарплат_для_ВШЭ_Амирханова_А.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1KK5Cj2HRslAhtrv86aKKt23y5GYyjFoU

#Проект: анализ зарплат в России

Условные обозначения:
- year - год,
- mining_n - номинальная заработная плата в добыче полезных ископаемых (НЗП_иск), тыс.руб.
- education_n	- номинальная заработная плата в образовании (НЗП_обр), тыс.руб.
- health_n	- номинальная заработная плата в области здравоохранения и социальных услуг (НЗП_здр), тыс.руб.
- inflation	- инфляция, %.
- all_n	- номинальная заработная плата в среднем по всем видам экономической деятельности в целом (НЗП по всем отраслям), тыс. руб.
- mining_r	- реальная заработная плата в добыче полезных ископаемых (НЗП_иск), тыс.руб.
- education_r	- реальная заработная плата в образовании (РЗП_обр),
- health_r	- реальная заработная плата в области здравоохранения и социальных услуг (РЗП_здр), тыс.руб.
- all_r - реальная заработная плата в среднем по всем видам экономической деятельности в целом (РЗП по всем отраслям),

*   Новый пункт
*   Новый пункт

тыс. руб.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

!git clone https://github.com/Aminat-K/HSE_project.git

df = pd.read_excel('/content/HSE_project/salary.xlsx')
df.head(5)

df.info()

"""Построим график изменения номинальных зарплат по годам для следующих видов экономической деятельсноти:
- добыча полезных ископаемых (НЗП_иск),
- деятельность в области здравоохранения и социальных услуг (НЗП_здр),
- образование (НЗП_обр),
- все виды экономической деятельности в целом (НЗП по всем отраслям).

"""

sns.lineplot(data=df, x="year", y="all_n", label = 'НЗП по всем отраслям')
sns.lineplot(data=df, x="year", y="mining_n", label = 'НЗП_иск')
sns.lineplot(data=df, x="year", y="health_n", label = 'НЗП_здр')
sns.lineplot(data=df, x="year", y="education_n", label = 'НЗП_обр')

"""На основании данного графика мы можем сделать следующие выводы:
- за рассматриваемый период (2000 - 2023 гг) произошел рост номинальных заработных плат по каждому анализируемому направлению,
- абсолютные величины и темпы роста номинальных заработных плат в области добычи полезных ископаемых значительно превышают остальные рассмотренные виды экономической деятельности,
- наименее привлекательной отраслью с точки зрения размеров номинальных заработных плат является образование,
- интересен факт ярко  выраженного увеличения темпов роста номинальных зарплат в области здравоохранения за период с 2018 по 2020 гг. (индекс номинальных цен в 2018 году составил 1,25) . Что в свою очередь может быть связано с выполнением майских указов президента перед выборами 2018 года.

Затем добавляем в датафрейм столбцы с расчитанными значениями реальных зарплат по отраслям с учетом уровня инфляции.
"""

df = df.assign(mining_r = df.mining_n/(1+df.inflation/100))
df = df.assign(education_r = df.education_n/(1+df.inflation/100))
df = df.assign(health_r = df.health_n/(1+df.inflation/100))
df = df.assign(all_r = df.all_n/(1+df.inflation/100))
df.head(5)

df.describe()

"""Расчитаем и добавим в датафрейм темпы роста номинальных и реальных заработных плат про интересующим нас направлениям."""

df['index_m_n']=df['mining_n']/df['mining_n'].shift(1)
df['index_m_r']=df['mining_r']/df['mining_r'].shift(1)
df['index_e_n']=df['education_n']/df['education_n'].shift(1)
df['index_e_r']=df['education_r']/df['education_r'].shift(1)
df['index_h_n']=df['health_n']/df['health_n'].shift(1)
df['index_h_r']=df['health_r']/df['health_r'].shift(1)
df['index_all_n']=df['all_n']/df['all_n'].shift(1)
df['index_all_r']=df['all_r']/df['all_r'].shift(1)
df.fillna(1, inplace=True)
df

decrease = df[(df < 1).any(axis=1)]
decrease

"""На основании произведенных расчетов, мы можем сделать следующий вывод: инфляция приводит к снижению реальных зарплат по сравнению с номинальными, однако в связи с тем, что темпы роста заработных плат больше уровеня инфляции, реальные доходы текущего года превышают реальные доходы в предыдущем периоде.
Исключением в данном случае является реальная заработная плата в области здравоохранения в 2021, уровень которой понизился по сравнению с 2020 годом.

Визуализируем и отобразим динамику изменения реальных зарплат с учетом инфляции и их соотношение с номинальными заработными платами.
"""



sns.lineplot(data=df, x="year", y="all_r", label = 'РЗП по всем отраслям')
sns.lineplot(data=df, x="year", y="mining_r", label = 'РЗП_иск' )
sns.lineplot(data=df, x="year", y="health_r", label = 'РЗП_здр')
sns.lineplot(data=df, x="year", y="education_r", label = 'РЗП_обр')

fig, ax = plt.subplots(figsize = (8, 4))

ax = sns.barplot(data = df,
            x = 'year',
            y = 'all_n');

ax.set_xticklabels(df['year'],
                   rotation = 90,
                   fontsize = 7);

plt.title("Динамика номинальной и реальной заработной платы по всем отраслям", fontsize = 10) #заголовок рисунка
plt.ylabel('Номинальная и реальная заработная плата по всем отраслям', fontsize = 8) #подпись оси ординат
plt.xlabel("Год", fontsize = 8) #подпись оси абцисс
ax = sns.barplot(data = df,
            x = 'year',
            y = 'all_r');

fig, ax = plt.subplots(figsize = (8, 4))

ax = sns.barplot(data = df,
            x = 'year',
            y = 'health_n');

ax.set_xticklabels(df['year'],
                   rotation = 90,
                   fontsize = 7);

plt.title("Динамика номинальной и реальной заработной платы в области здравоохранения", fontsize = 10) #заголовок рисунка
plt.ylabel('Номинальная и реальная заработная плата в области здравоохранения', fontsize = 8) #подпись оси ординат
plt.xlabel("Год", fontsize = 8) #подпись оси абцисс
ax = sns.barplot(data = df,
            x = 'year',
            y = 'health_r');

sns.lineplot(data=df, x="year", y="health_r", label = 'РЗП_здр')
sns.lineplot(data=df, x="year", y="health_n", label = 'НЗП_здр')

fig, ax = plt.subplots(figsize = (8, 4))

ax = sns.barplot(data = df,
            x = 'year',
            y = 'education_n');

ax.set_xticklabels(df['year'],
                   rotation = 90,
                   fontsize = 7);

plt.title("Динамика номинальной и реальной заработной платы в области образования", fontsize = 10) #заголовок рисунка
plt.ylabel('Номинальная и реальная заработная плата в области образования', fontsize = 8) #подпись оси ординат
plt.xlabel("Год", fontsize = 8) #подпись оси абцисс
ax = sns.barplot(data = df,
            x = 'year',
            y = 'education_r');

fig, ax = plt.subplots(figsize = (8, 4))

ax = sns.barplot(data = df,
            x = 'year',
            y = 'mining_n');

ax.set_xticklabels(df['year'],
                   rotation = 90,
                   fontsize = 7);

plt.title("Динамика номинальной и реальной заработной платы в области добычи полезных ископаемых", fontsize = 10) #заголовок рисунка
plt.ylabel('Номинальная и реальная заработная плата в области добычи полезных ископаемых', fontsize = 8) #подпись оси ординат
plt.xlabel("Год", fontsize = 8) #подпись оси абцисс
ax = sns.barplot(data = df,
            x = 'year',
            y = 'mining_r');

"""Использование инструментов визуализация для отображения динамики изменения реальных зарплат с учетом инфляции наглядно подтверждает сделанные выше выводы, а именно:
-  инфляция приводит к снижению реальных зарплат по сравнению с номинальными, однако в связи с тем, что темпы роста заработных плат больше уровня инфляции, реальные доходы текущего года превышают реальные доходы в предыдущем периоде за сключением реальной заработной платы в области здравоохранения в 2021, уровень которой понизился по сравнению с 2020 годом.
- за рассматриваемый период (2000 - 2023 гг) произошел рост номинальных и реальных заработных плат по каждому анализируемому направлению,
- абсолютные величины номинальных и реальных заработных плат в области добычи полезных ископаемых значительно превышают уровень заработных плат в остальных рассмотренных видах экономической деятельности,
- наименее привлекательной отраслью с точки зрения размеров номинальных и реальных  заработных плат является образование.
"""

