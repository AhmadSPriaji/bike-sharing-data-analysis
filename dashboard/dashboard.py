import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

def get_total_count_by_hour_df(hour_df):
  hour_count_df =  hour_df.groupby(by="hours").agg({"count_cr": ["sum"]})
  return hour_count_df

def count_by_day_df(day_df):
    day_df_count_year = day_df.query(str('dateday >= "2011-01-01" and dateday < "2012-12-31"'))
    return day_df_count_year

def total_registered_df(day_df):
   reg_df =  day_df.groupby(by="dateday").agg({
      "registered": "sum"
    })
   reg_df = reg_df.reset_index()
   reg_df.rename(columns={
        "registered": "register_sum"
    }, inplace=True)
   return reg_df

def total_casual_df(day_df):
   cas_df =  day_df.groupby(by="dateday").agg({
      "casual": ["sum"]
    })
   cas_df = cas_df.reset_index()
   cas_df.rename(columns={
        "casual": "casual_sum"
    }, inplace=True)
   return cas_df

def sum_order(hour_df):
    sum_order_items_df = hour_df.groupby("hours").count_cr.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def kind_season(day_df): 
    season_df = day_df.groupby(by="season").count_cr.sum().reset_index() 
    return season_df

days_df = pd.read_csv("dashboard/day.csv")
hours_df = pd.read_csv("dashboard/hour.csv")

drop_col = ['instant']

for i in days_df.columns:
  if i in drop_col:
    days_df.drop(labels=i, axis=1, inplace=True)

for i in hours_df.columns:
  if i in drop_col:
    hours_df.drop(labels=i, axis=1, inplace=True)

# Mengganti nama kolom di dataset day_df
days_df.rename(columns={'dteday':'dateday','yr':'year','mnth':'month','weekday':'day_of_week', 'weathersit':'weather_situation', 'windspeed':'wind_speed','cnt':'count_cr','hum':'humidity', 'workingday':"category_days"},inplace=True)

# Mengganti nama kolom di dataset hour_df
hours_df.rename(columns={'dteday':'dateday','yr':'year','hr':'hours','mnth':'month','weekday':'day_of_week', 'weathersit':'weather_situation','windspeed':'wind_speed','cnt':'count_cr','hum':'humidity', 'workingday':"category_days"},inplace=True)

# konversi season menjadi: 1:Spring, 2:Summer, 3:Fall, 4:Winter
days_df.season.replace((1,2,3,4), ('Spring','Summer','Fall','Winter'), inplace=True)
hours_df.season.replace((1,2,3,4), ('Spring','Summer','Fall','Winter'), inplace=True)

# konversi month menjadi: 1:Jan, 2:Feb, 3:Mar, 4:Apr, 5:May, 6:Jun, 7:Jul, 8:Aug, 9:Sep, 10:Oct, 11:Nov, 12:Dec
days_df.month.replace((1,2,3,4,5,6,7,8,9,10,11,12),('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'), inplace=True)
hours_df.month.replace((1,2,3,4,5,6,7,8,9,10,11,12),('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'), inplace=True)

# konversi weather_situation menjadi: 1:Clear, 2:Misty, 3:Light_RainSnow 4:Heavy_RainSnow
days_df.weather_situation.replace((1,2,3,4), ('Clear','Misty','Light_rainsnow','Heavy_rainsnow'), inplace=True)
hours_df.weather_situation.replace((1,2,3,4), ('Clear','Misty','Light_rainsnow','Heavy_rainsnow'), inplace=True)

# konversi day_of_week menjadi: 0:Sun, 1:Mon, 2:Tue, 3:Wed, 4:Thu, 5:Fri, 6:Sat
days_df.day_of_week.replace((0,1,2,3,4,5,6), ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'), inplace=True)
hours_df.day_of_week.replace((0,1,2,3,4,5,6), ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'), inplace=True)

# konversi category_day menjadi: 0:weekend, 1:weekdays
days_df.category_days.replace((0,1), ('weekend','weekdays'), inplace=True)
hours_df.category_days.replace((0,1), ('weekend','weekdays'), inplace=True)

# konversi year menjadi: 0:2011, 1:2012
days_df.year.replace((0,1), ('2011','2012'), inplace=True)
hours_df.year.replace((0,1), ('2011','2012'), inplace=True)

# Mengubah tipe data ke datetime
days_df['dateday'] = pd.to_datetime(days_df.dateday)

# Mengubaha tipe data ke categorical
days_df['season'] = days_df.season.astype('category')
days_df['year'] = days_df.year.astype('category')
days_df['month'] = days_df.month.astype('category')
days_df['holiday'] = days_df.holiday.astype('category')
days_df['day_of_week'] = days_df.day_of_week.astype('category')
days_df['category_days'] = days_df.category_days.astype('category')
days_df['weather_situation'] = days_df.weather_situation.astype('category')


hours_df['dateday'] = pd.to_datetime(hours_df.dateday)

hours_df['season'] = hours_df.season.astype('category')
hours_df['year'] = hours_df.year.astype('category')
hours_df['month'] = hours_df.month.astype('category')
hours_df['hours'] =  hours_df.hours.astype("category")
hours_df['holiday'] = hours_df.holiday.astype('category')
hours_df['day_of_week'] = hours_df.day_of_week.astype('category')
hours_df['category_days'] = hours_df.category_days.astype('category')
hours_df['weather_situation'] = hours_df.weather_situation.astype('category')

datetime_columns = ["dateday"]
days_df.sort_values(by="dateday", inplace=True)
days_df.reset_index(inplace=True)   

hours_df.sort_values(by="dateday", inplace=True)
hours_df.reset_index(inplace=True)

min_date_days = days_df["dateday"].min()
max_date_days = days_df["dateday"].max()

min_date_hour = hours_df["dateday"].min()
max_date_hour = hours_df["dateday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://balicycling.com/wp-content/uploads/2019/06/bali-cycling-rent-1300x600.jpg")
    
        # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days])
  
main_df_days = days_df[(days_df["dateday"] >= str(start_date)) & 
                       (days_df["dateday"] <= str(end_date))]

main_df_hour = hours_df[(hours_df["dateday"] >= str(start_date)) & 
                        (hours_df["dateday"] <= str(end_date))]

hour_count_df = get_total_count_by_hour_df(main_df_hour)
day_df_count_year = count_by_day_df(main_df_days)
reg_df = total_registered_df(main_df_days)
cas_df = total_casual_df(main_df_days)
sum_order_items_df = sum_order(main_df_hour)
season_df = kind_season(main_df_hour)

#Melengkapi Dashboard dengan Berbagai Visualisasi Data
st.header('Bike Rent Dashboard 🚲')

st.subheader('Daily Rent')
col1, col2, col3 = st.columns(3)
 
with col1:
    total_rents = day_df_count_year.count_cr.sum()
    st.metric("Total Rent Bike", value=total_rents)

with col2:
    total_sum_red = reg_df.register_sum.sum()
    st.metric("Total Registered", value=total_sum_red)

with col3:
    total_sum_cas = cas_df.casual_sum.sum()
    st.metric("Total Casual", value=total_sum_cas)

# Pertanyaan 1
st.subheader("Perkembangan jumlah penyewa sepeda per bulan dalam beberapa tahun terakhir")

fig, ax = plt.subplots(figsize=(16, 8))

days_df['month'] = pd.Categorical(days_df['month'], categories=[
    'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
    ordered=True)

monthly_counts = days_df.groupby(by=["year", "month"], observed=False).agg({
    "count_cr": "sum"
}).reset_index()

monthly_counts['year_month'] = monthly_counts['year'].astype(str) + '-' + monthly_counts['month'].astype(str)

monthly_counts = monthly_counts.sort_values(by=['year', 'month'])

sns.lineplot(
    data=monthly_counts,
    x="year_month",
    y="count_cr",
    marker="o",
    color="blue",
    ax=ax 
)

ax.grid(True, linestyle='--', alpha=0.7)

ax.set_title("Jumlah Sepeda Disewakan Setiap Bulan pada Tahun 2011 - 2012", fontsize=16)
ax.set_xlabel("Tahun-Bulan" , fontsize=14)
ax.set_ylabel("Jumlah Sepeda Disewa", fontsize=14)

ax.set_xticklabels(monthly_counts['year_month'], rotation=45)
fig.tight_layout()

st.pyplot(fig)


# Pertanyaan 2
st.subheader("Korelasi antara suhu, kecepatan angin, dan kelembapan dengan jumlah penyewa sepeda")

fig, ax = plt.subplots(3, 1, figsize=(14, 12))

# Scatter plot untuk 'temp' vs 'count'
sns.scatterplot(
    x='temp',
    y='count_cr',
    data=days_df,
    alpha=0.5,
    ax=ax[0] 
)
ax[0].set_title('Temperature vs Count', fontsize=16)

# Scatter plot untuk 'wind_speed' vs 'count'
sns.scatterplot(
    x='wind_speed',
    y='count_cr',
    data=days_df,
    alpha=0.5,
    ax=ax[1] 
)
ax[1].set_title('Wind Speed vs Count', fontsize=16)

# Scatter plot untuk 'humidity' vs 'count'
sns.scatterplot(
    x='humidity',
    y='count_cr',
    data=days_df,
    alpha=0.5,
    ax=ax[2] 
)
ax[2].set_title('Humidity vs Count', fontsize=16)

fig.subplots_adjust(hspace=0.5)

fig.tight_layout()
st.pyplot(fig)


# Pertanyaan 3
st.subheader("Jumlah sepeda disewa berdasarkan perbedaan kondisi cuaca")

count_by_weather = days_df.groupby('weather_situation', observed=False)['count_cr'].sum().reset_index()

fig, ax = plt.subplots(figsize=(12, 6))

sns.barplot(x='weather_situation', y='count_cr', data=count_by_weather, 
            palette='viridis', ax=ax)

ax.set_title('Jumlah Sepeda Disewa Berdasarkan Kondisi Cuaca', fontsize=16)
ax.set_xlabel('Kondisi Cuaca', fontsize=12)
ax.set_ylabel('Jumlah Sepeda Disewa', fontsize=12)

plt.tight_layout()

st.pyplot(fig)


# Pertanyaan 4
st.subheader("Pengaruh musim terhadap jumlah penyewa sepeda berdasarkan kategori pelanggan Casual dan Registered")

seasonal_usage = days_df.groupby('season', observed=False)[['registered', 'casual']].sum().reset_index()

seasonal_usage_long = pd.melt(seasonal_usage, 
                              id_vars=['season'], 
                              value_vars=['registered', 'casual'],
                              var_name='user_type', 
                              value_name='count')

fig, ax = plt.subplots(figsize=(12, 6))

sns.barplot(x='season', y='count', hue='user_type', data=seasonal_usage_long, 
            palette='deep', ax=ax)

ax.set_title('Jumlah Sepeda Disewa oleh Registered dan Casual Berdasarkan Musim', fontsize=16)
ax.set_xlabel('Musim', fontsize=12)
ax.set_ylabel('Jumlah Sepeda Disewa', fontsize=12)

ax.legend(title='User Type', fontsize='10')

plt.tight_layout()

st.pyplot(fig)


# Pertanyaan 5
st.subheader("Pada jam berapa yang paling banyak dan paling sedikit jumlah sepeda disewa?")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

sum_count_hourly = hours_df.groupby("hours").count_cr.sum().reset_index()

max_count = sum_count_hourly["count_cr"].max()
min_count = sum_count_hourly["count_cr"].min()

fig, ax = plt.subplots(figsize=(15, 8)) 

colors = ["green" if count == max_count else "red" if count == min_count else "gray" 
          for count in sum_count_hourly["count_cr"]]

sns.barplot(x="hours", y="count_cr", data=sum_count_hourly, palette=colors, ax=ax)

ax.set_ylabel("Jumlah Sepeda Disewa", fontsize=14)
ax.set_xlabel("Jam", fontsize=14)
ax.set_title("Jumlah Sepeda Disewa Berdasarkan Jam", loc="center", fontsize=16)
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)

plt.tight_layout()
st.pyplot(fig)

st.caption('Copyright (c) Ahmad Siddiq Priaji 2024')