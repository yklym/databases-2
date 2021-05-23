import datetime
from math import fabs, ceil

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from storage.repository import lot_repository


def fix_region_str(region):
    region_code = 'область'
    if region.startswith(region_code):
        return f"{region.split(' ')[1]} {region_code}"
    elif region.endswith('обл.'):
        return f"{region.split(' ')[0]} {region_code}"
    elif region == 'м. Київ' or region == 'м.Київ':
        return 'м.Київ'
    elif region.endswith('обасть') or region.endswith('облась'):
        return f"{region.split(' ')[0]} {region_code}"
    elif not region.endswith(region_code):
        return f"{region} {region_code}"

    return region


def get_month_by_index(idx):
    monthinteger = idx

    return datetime.date(1900, monthinteger, 1).strftime('%B')


if __name__ == '__main__':
    lots = lot_repository.find_document({})

    df = pd.DataFrame(lots)

    # FORMAT DATA

    # 27.03.2020 11:00 ----> 27.03.2020
    df['auction_date'] = df['auction_date'].apply(lambda date_time: date_time.split(' ')[0])

    # add month of auction as separate date
    df['auction_month'] = df['auction_date'].apply(
        lambda date_time: get_month_by_index(int(date_time.split('.')[1]) if len(date_time.split('.')) > 1 else None))

    # add year of auction as separate date
    df['auction_year'] = df['auction_date'].apply(
        lambda date_time: int(date_time.split('.')[-1]) if len(date_time.split('.')) > 1 else None)

    # remove zeroes and empty strings from price
    df['region'] = df['place'].apply(
        lambda place: fix_region_str(place.split(',')[0].strip() if len(place.split(',')) >= 1 else ''))

    # remove mongo id from DF
    del df['_id']
    print(df.columns)
    print(len(df))

    print('\n0-----------------------\n')
    #
    print("Загальні інформація за 2021 рік")

    curr_year_df = df.loc[df['auction_year'] == 2021]
    max_curr_year_month = curr_year_df['auction_month'].max()
    prev_year_compatible = df.loc[(df['auction_year'] == 2020) & (df['auction_month'] <= max_curr_year_month)]

    lots_addition = len(curr_year_df) - len(prev_year_compatible)
    lots_addition_sign = '(+)' if lots_addition > 0 else '(-)'

    start_price_sum = curr_year_df['start_price'].sum() + curr_year_df['sell_price'].sum()
    minimal_income = ceil(start_price_sum + min(start_price_sum * 0.5, 40000) + len(curr_year_df) * 5000)

    print(f'Період: поч. 2021 - {max_curr_year_month} місяць 2021')
    print(f'Кількість лотів виставлено: {len(curr_year_df)}')
    print(f'Мінімальна стартова ціна: {curr_year_df["start_price"].min(skipna=True)}')
    print(f'Максимальна стартова ціна: {curr_year_df["start_price"].max(skipna=True)}')
    print(f'Очікуваний мінімальний прибуток до місцевих органів: {minimal_income}')
    print(f'Кількість лотів за відповідний період минулого року: {len(prev_year_compatible)}')
    print(
        'Приріст кількості лотів порівняно з відповідним періодом минулого року: '
        f'{lots_addition_sign}{int(fabs(lots_addition))}')

    print('\n1-----------------------\n')
    # 1. Які місяці найбільш підходять для участі в аукціонах?
    # Аукціони організовуються місцевими органами тому в теорії в них можуть бути певні звички щодо реєстрації лотів
    # на аукціони

    print('частота місяців:')
    print(df['auction_month'].value_counts())
    # висновок - частота місяців 3-12 приблизно наближаються до рівномірнго розподілу, в той час як 1 та 2 місяць
    # зустрічаються на порядок рідше. Отже цей період року є найгіршим для пошуку підходящого лоту

    df['auction_month'].value_counts().plot.bar()
    plt.show()
    print("\nСередня площа розігруваних ділянок та стартова ціна за місяцем")
    for i in range(1, 13):
        tmp_df = df.loc[df['auction_month'] == get_month_by_index(i)]
        print(f'{i}: mean square {ceil(tmp_df["square"].mean())}, mean start rent {ceil(tmp_df["start_price"].mean())}')

    # pie chart, won't be needed
    # df['auction_month'].value_counts().plot.pie(figsize=(10, 10), autopct='%1.1f%%')
    # plt.show()

    # Можемо підтвердити попередній висновок, адже крім того що на продаж виставляється менше ділянок, середня площа цих
    # ділянок теж є нижчою відносно подальших місяців

    print('\n2-----------------------\n')
    # 2. Дослідимо кореляцію між змінними
    pd.set_option('display.max_columns', 5)
    corr_df = pd.DataFrame({
        'square': df['square'],
        'guarantee_contribution': df['guarantee_contribution'],
        'start_price': df['start_price'],
        'evaluation': df['evaluation'],
        'auction_year': df['auction_year']
    })

    print(corr_df.corr(method='pearson'))
    corr_koeff = corr_df.corr(method='pearson')
    sns.heatmap(corr_koeff)
    plt.show()

    # між гарантійним внеском та початковою ціною є відносно висока кореляція (0,75), але в той же час початкова ціна
    # практично не залежить від площі ділянки, отже її в більшому степені визначають інші фактори

    print('\n3-----------------------\n')

    # 3 Переглянемо кількість лотів за регіоном. Використовувати для вибірки назви окермих населенних пункітв недоцільн
    # оскільки в них замало записів
    print('По регіонам:\n')
    print(df['region'].value_counts())
    # title_type = df.groupby('region'
    # ).count()
    # % matplotlib inline
    # ipython notebook --matplotlib inline
    df['region'].value_counts().plot.pie(figsize=(10, 10), autopct='%1.1f%%')
    plt.show()

    print('\n4-----------------------\n')
    # 4
    start_year = df['auction_year'].min()
    years_list = []
    values_list = []
    for i in range(start_year, 2021):
        count = len(df.loc[df['auction_year'] == i])
        years_list.append(i)
        values_list.append(count)

        print(f"{i}: {count}")

    years_df = pd.DataFrame({
        'y': values_list,
        'x': years_list,
    })

    years_df.plot(x="x", y="y")
    plt.show()
