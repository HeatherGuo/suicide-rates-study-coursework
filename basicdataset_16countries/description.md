description:
choose 16 countries from dataset 'who_suicide_statistics.csv', time range is from 1980 to 2016.

country:
choose 16 countries with 8 countries have increased suicide number and 8 countries have decreased suicide number
8 increase countries:
'Austria','Azerbaijan','Belgium','Brazil','Bulgaria','Canada','Chile','Colombia'
8 decrease countries:
'Mexico','Paraguay','Republic of Korea','Serbia','Slovenia','Uruguay','Kyrgyzstan','Hungary'

fill missing data:
suicides_no(suicide number) that is missing is 
country=Azerbaijan; year=1983,2005 
country=Kyrgzstan; year=1983
coungtry=paraguay; year=1988
method:
fill missing data use the average number of the data from a year before and a year after.

add new attribute: suicide_no per 100000
new attribute suicide_no per 100000 calculate by: suicides_no/populaiton*100000
