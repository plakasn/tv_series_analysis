#%%
import pandas as pd
import matplotlib as plt
import plotly.express as px
import seaborn as sns

title_basics_df = pd.read_csv('C:/Users/user/tv-series analysis/Title_Basics.tsv', sep= '\t')
#unique_values = title_basics_df['titleType'].unique()
#print(unique_values)
title_basics_df= title_basics_df[(title_basics_df['titleType']=='tvSeries')]
title_basics_df= title_basics_df[(title_basics_df['titleType']=='tvSeries') | (title_basics_df['titleType']=='tvMiniSeries') ]

unique_values = title_basics_df['titleType'].unique()
title_ratings_df= pd.read_csv('C:/Users/user/tv-series analysis/Title_Ratings.tsv', sep= '\t')

dates_list= sorted(title_basics_df[('startYear')].unique())


#%%
'''Distribution of series by year from 1927-2024'''

distribution_df= title_basics_df['startYear'].value_counts().sort_values(ascending=False).to_frame()
distribution_df.reset_index(inplace=True)
distribution_df.columns.values[0]= 'Year'
distribution_df.columns.values[1]= 'Series#'
distribution_df=distribution_df[distribution_df['Year'] != '\\N']



distribution_list=sorted(distribution_df[('Series#')].unique())
'''Maybe for a more clear distribution its better to drop the years which have under a specific number series


'''
#distribution_df=distribution_df.drop(r"\\N")
distribution_df['Year']=distribution_df['Year'].astype(int)
distribution_df= distribution_df[(distribution_df['Year']>=1960) & (distribution_df['Year']<=2025)]

px.bar(distribution_df,x='Year', y='Series#',color='Series#',
       labels={'Year':'Release Year', 'Series#':'Number of Series'},
       title='Distribution of TV Series by Release Year', template='presentation')



#%%
'''Most popular Tv Series by genres over time'''

genres_df= title_basics_df.filter(items= ['genres'],axis=1)
genres_df=genres_df.groupby('genres').size().reset_index(name='genre_count')

genres_df.dropna(inplace=True)
genres_df.reset_index(drop=True,inplace=True)
genres_df.drop(1530,inplace=True,errors='ignore')
genres_df.dropna(inplace=True)
genres_df=genres_df.sort_values(by='genre_count',ascending=False).head()
genres_df.dropna(inplace=True)


px.bar(genres_df,x='genres', y='genre_count',color='genre_count',
labels={'genres':'Genres','genre_count':'Number of Genres'},
title='Most Popular Genres',template='presentation')

'''Genre pie distribution'''

px.pie(genres_df,
       names='genres',
       values='genre_count',
       title='Genre Distribution',
       template='presentation',
       color='genres')

#%%
'''Rating analysis'''


rating_df=title_basics_df.merge(title_ratings_df,on='tconst')

rating_df={
       'primaryTitle':rating_df['primaryTitle'],
       'genres':rating_df['genres'],
       'averageRating':rating_df['averageRating']
}
rating_df=pd.DataFrame(rating_df)
rating_df.dropna(inplace=True)
'''I am not sure I must split them as I didnt do it before for the distribution, I must decide if I should procced this way'''
rating_df['genres'] = rating_df['genres'].str.split(',')  
rating_df = rating_df.explode('genres') 

rating_genre_cc = rating_df[ 
    (rating_df['genres'] == 'Documentary') | 
    (rating_df['genres'] == 'Comedy') | 
    (rating_df['genres'] == 'Reality-TV') | 
    (rating_df['genres'] == 'Drama') | 
    (rating_df['genres'] == 'Talk-Show')
]

rating_genre_cc = rating_genre_cc.groupby(['genres'])['averageRating'].mean().to_frame()
rating_genre_cc = rating_genre_cc.sort_values(by='averageRating', ascending=False).reset_index()

px.bar(rating_genre_cc,x='genres',y='averageRating',color='averageRating',
       labels={'averageRating':'Average Rating','genres':'Genres'},
       title='Popular Genres by Average Rating', template='presentation')

'''Corellation also here i have to think about split'''

rating_df['genre_code']=rating_df['genres'].astype('category').cat.codes
correlation=rating_df[['genre_code','averageRating']].corr()
value=correlation.loc['genre_code','averageRating']
value = correlation.loc['genre_code', 'averageRating']
print(f"\nThe correlation coefficient between genre and average rating is {value:.2f}.")

if value > 0.5:
    print("There is a significant positive correlation, indicating that certain genres are associated with higher average ratings.")
elif value < -0.5:
    print("There is a substantial negative correlation, implying that some genres are generally linked to lower average ratings.")
else:
    print("There is a weak or negligible correlation, suggesting that average ratings are largely independent of genre.")

#%%
'''Year vs Rating Analysis'''
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression

year_rate_df=pd.DataFrame({
    'startYear':title_basics_df['startYear'],
    'average_rating': title_ratings_df['averageRating']
})


year_rate_df['startYear']=pd.to_numeric(year_rate_df['startYear'],errors='coerce')
year_rate_df['average_rating'] = pd.to_numeric(year_rate_df['average_rating'], errors='coerce') 


year_rate_df.dropna(subset=['startYear','average_rating'],inplace=True)

avg_year_rate_df=year_rate_df.groupby('startYear')['average_rating'].mean().reset_index()

px.line(avg_year_rate_df,x='startYear', y='average_rating',
        labels={'startYear':'Start Year','average_rating': 'Average Rating'},
       title='Average Tv Series Rating by Year',template='presentation')


correlation=year_rate_df['startYear'].corr(year_rate_df['average_rating'])

year_bins = [1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020]
year_labels = ['1920s', '1930s', '1940s', '1950s', '1960s', '1970s', '1980s', '1990s', '2000s', '2010s']

year_rate_df['year_group']=pd.cut(year_rate_df['startYear'],bins=year_bins,labels=year_labels,right=False)
group_rating_df=year_rate_df.groupby('year_group')['average_rating'].mean().reset_index()

fig = px.pie(group_rating_df, 
             names='year_group', 
             values='average_rating',
             title='Average Tv Series Rating Distribution by Year Group',
             template='plotly')

x=year_rate_df['startYear'].values.reshape(-1,1)
y=year_rate_df['average_rating'].values
model=LinearRegression()
model.fit(x,y)
predict_rating=model.predict(x)

print("\nRegression Analysis Insights:")
print(f"The regression line equation is: Average Rating = {model.intercept_:.3f} + {model.coef_[0]:.3f} * Year")
print(f"The model's slope is {model.coef_[0]:.3f}, meaning for each additional year, the average rating increases by this value.")
print(f"The intercept is {model.intercept_:.3f}, indicating the estimated average rating at the year 0 (though not realistic, it's part of the regression formula).")

print("\nConclusions:")
if correlation > 0:
    print("1. There is a positive correlation between the year of release and TV Series ratings, suggesting that newer TV Series tend to have higher ratings.")
elif correlation < 0:
    print("1. There is a negative correlation between the year of release and TV Series ratings, suggesting that newer TV Series tend to have lower ratings.")
else:
    print("1. There is no significant correlation between the year of release and TV Series ratings, indicating that ratings are not influenced by the year.")

if model.coef_ > 0:
    print("2. The regression line shows an increasing trend in ratings over time, suggesting that TV Series ratings have improved over the years.")
else:
    print("2. The regression line shows a decreasing trend in ratings over time, suggesting that newer TV Series may be receiving lower ratings.")


fig=px.scatter(year_rate_df,x='startYear',y='average_rating',
               title='Regression line for Tv Series Ratings by Year',
               labels={'startYear':'Start Year','average_rating':'Average Rating'})
fig.add_scatter(x=year_rate_df['startYear'],y=predict_rating,
                mode='lines',name='Regression Line',line=dict(color='red'))
