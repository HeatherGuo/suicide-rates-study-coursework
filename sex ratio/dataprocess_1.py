import os
import csv
import pandas
import numpy as np
import matplotlib.pyplot as plt
os.chdir('E:\\02Data Science\\1S COMP6235 foundation of data science\\course work 3 group project')
clist=['Austria','Belgium','Bulgaria','Canada','Kyrgyzstan','Slovenia','Hungary'\
,'Brazil','Colombia','Chile','Mexico','Paraguay','Republic of Korea','Uruguay']#row1 decrese 7;row2 increase 7
with open('who_suicide_statistics.csv','r') as f:
    suicide=pandas.read_csv(f)
    suifil=suicide[suicide.country.isin(clist)]#suicide filter with counry list
    suifil=suifil[suifil.year>=1980]
missdata=suifil[suifil.suicides_no.isnull()]
#find countries which have missing data
miscountry=missdata.drop_duplicates('country',inplace=False).country
miscountry=np.array(miscountry)
#viewmiss=missdata.groupby(['country','year']).agg(['count'])
#print(viewmiss)
#print(suifil.groupby('country').agg(['count']))
def fillmiss(dframe,condition,c,y,v):
    #dframe--dataset;country--the conditions;c--the conditions should keep same;
    #y--the conditions sould keep differ; v--the value
    for index,row in dframe.iterrows():
        for cc in condition:
            if row.country==cc:
                no1=dframe[dframe[c]==row[c] & dframe[y]==row[y]+1].v
                no2=dframe[dframe[c]==row[c] & dframe[y]==row[y]-1].v
                no0=(no1+no2)/2
                row.v=no0
    return None

#fill missing data
c=['country','sex','age']
y=['year']
v=['suicides_no']
fillmiss(suifil,miscountry,c,y,v)
print(suifil.suicides_no.isnull())
#suifil.to_csv('processing1.csv')
###########--------------------------------------------#############################
with open('processing1.csv','r') as f:
    suicide=pandas.read_csv(f)
columns=suicide.columns
suicide.groupby(['country','year','sex']).sum()
#analyze gender
gender=suicide.groupby([suicide['country'],suicide['year'],suicide['sex']])[['suicides_no','population']].sum()
genders=gender.reset_index()
genders['suirate']=genders.suicides_no*100000/genders.population
genders.to_csv('processgender.csv')
#age
age=suicide.groupby([suicide['country'],suicide['year'],suicide['age']])[['suicides_no','population']].sum()
ages=age.reset_index()
ages['suirate']=ages.suicides_no*100000/genders.population
ages.to_csv('processage.csv')
#whole
whole=suicide.groupby([suicide['country'],suicide['year']])[['suicides_no','population']].sum()
whole=whole.reset_index()
whole['suirate']=whole.suicides_no*100000/whole.population
whole.to_csv('processwhole.csv')
#file
with open('processbackup\processgender.csv','r') as f:
    progender=pandas.read_csv(f)
with open('processbackup\processage.csv','r') as f:
    proage=pandas.read_csv(f)
progender.head()
gap1=progender.malrate/progender.felrate
gap1=np.array(gap1)
gap1.sum()
plt.hist(gap1)
plt.show()