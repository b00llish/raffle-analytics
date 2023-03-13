import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from data import GetExistingFromDB

week_dict = dict({
    0:"Monday",
    1:"Tuesday",
    2:"Wednesday",
    3:"Thursday",
    4:"Friday",
    5:"Saturday",
    6:"Sunday"
}
)
at = GetExistingFromDB(query='''select * from fact_buys order by date_buy desc''')
#at.date_buy = at.date_buy.dt.tz_convert('America/Chicago')
max_at = max(at.date_buy)

tw_min = max_at - pd.DateOffset(days=14)
#tw_min = pw_min.normalize() + pd.DateOffset(days=1)
tw = at.loc[(at.date_buy > tw_min)] #inclusive
tw_day = tw.groupby(pd.Grouper( key='date_buy', freq='D')).agg(
    buy_sum=('amount_buy', 'sum'),
    max_time=('date_buy', 'max')
)
tw_day.max_time = tw_day.max_time.dt.hour
tw_day = tw_day.loc[(tw_day.max_time == 23)]
tw_min = max(tw_day.index) - pd.DateOffset(days=21)
tw_day = tw_day.loc[(tw_day.index > tw_min)] #inclusive

min_date = min(tw_day.index)
max_date = max(tw_day.index)
length = max_date - min_date

min_date = min_date.strftime('%m/%d')
max_date = max_date.strftime('%m/%d')
length = str(length.days + 1)

tw_grp = tw.groupby(pd.Grouper( key='date_buy', freq='H')).agg(
    buy_sum=('amount_buy', 'sum')
).reset_index()

tw_grp['week_day'] = tw_grp.date_buy.dt.day_of_week
tw_grp['hour (utc)'] = tw_grp.date_buy.dt.hour
# tw_grp = tw_grp.unstack()
tw_grp = tw_grp.groupby(['hour (utc)', 'week_day'])['buy_sum'].mean().unstack()
tw_grp = tw_grp.rename(columns=week_dict)

sns.heatmap(
    data= tw_grp,
    cmap= "Spectral_r",
    vmin= 0
).set(title= f'buying volume, past {length} days ({min_date} to {max_date})')
plt.subplots_adjust(bottom=0.26, right=0.96, top=0.92)
plt.show()




def renamer(agg_func,desired_name):
    def return_func(x):
        return agg_func(x)
    return_func.__name__ = desired_name
    return return_func

freq_dict = dict({
    'day':"D",
    'hour':"H",
    'past week':"7D",
    'past two weeks':"14D"
})

freq = freq_dict['day']

at_sub = at.groupby(pd.Grouper(key='date_buy', freq=freq)).agg({
    #'AMT_BUY': [('volume', 'sum'), ('number of purchases', 'count')],
    'amount_buy': [renamer(sum, 'buying volume (sol)'), renamer(pd.Series.count, 'number of purchases')],
    'raffle_id': [renamer(pd.Series.nunique, 'number of raffles')],
    'buyer_wallet': [renamer(pd.Series.nunique, 'unique buyers')],
    'date_buy': [renamer(max, 'max time')]
})
at_sub.columns = at_sub.columns.droplevel()
at_sub['max time'] = at_sub['max time'].dt.hour
at_sub = at_sub.loc[(at_sub['max time'] == 23)]
at_sub = at_sub.drop(columns='max time')
at_sub['buying volume (sol)'] = at_sub['buying volume (sol)'].round(0)
at_sub.index.name = 'date(utc)'
at_sub.sort_values('date(utc)')

min_date = min(at_sub.index)
min_date = min_date.strftime('%m/%d')
max_date = max(at_sub.index)
max_date = max_date.strftime('%m/%d')

at_sub.plot(
    kind='line',
    subplots=True,
    sharey=False,
    figsize=(10, 6)
)#.set(title= f'buying volume, past 3 weeks ({min_date} to {max_date})')
plt.tight_layout()
plt.subplots_adjust(wspace=0.5)
plt.show()
