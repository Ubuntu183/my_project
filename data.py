import pandas as pd

df = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vQrgeKp732xnhbWDqyYVxOasvWl8grlLE0bmMXRPqGEz0qzUH9iBtyPF9OJyC6iaZbAH070ecBySiKN/pub?output=csv',
                sep=',')
platforms_list = df['Platform'].unique()
genre_list = df['Genre'].unique()
region_list = ['Америка' , 'NA_Sales'], ['Европа', 'EU_Sales'], ['Япония', 'JP_Sales'], ['Остальные', 'Other_Sales']
count_grouped = df.groupby('Year')['Name'].count().reset_index(name='Count')