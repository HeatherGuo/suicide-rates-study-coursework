import os
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
os.chdir('E:\\02Data Science\\1S COMP6235 foundation of data science\\course work 3 group project')
#clist=['Austria','Belgium','Bulgaria','Canada','Kyrgyzstan','Slovenia','Hungary'\
#,'Brazil','Colombia','Chile','Mexico','Paraguay','Republic of Korea','Uruguay']#row1 decrese 7;row2 increase 7
clist=['Albania','Denmark','Switzerland','Slovakia','Cuba','Belarus','Philippines'\
       ,'Mongolia','San Marino','Georgia','Romania','Portugal','Armenia','Egypt'\
       ,'Cyprus','Poland']#reduce country which missing value over 36, missing two consecutive year
with open('who_suicide_statistics.csv','r') as f:
    suicide=pd.read_csv(f)
    #suifil=suicide[suicide.country.isin(clist)]#suicide filter with counry list
    suifil=suicide.query("country not in @clist")
    suifil=suifil[suicide.year>=1987]
#missdata=suicide[suicide.suicides_no.isnull()]
missdata=suifil[suifil.suicides_no.isnull()]
#find countries which have missing data
missdata.groupby(['country','year'])['country'].count()
miscountry=missdata.drop_duplicates('country',inplace=False).country
miscountry=np.array(miscountry)
#viewmiss=missdata.groupby(['country','year']).agg(['count'])
#print(viewmiss)
#print(suifil.groupby('country').agg(['count']))
def fillmiss(dframe,missdata,suicide):#see file process 4
    #dframe--dataset;country--the conditions;c--the conditions should keep same;
    #y--the conditions sould keep differ; v--the value
    for index,row in missdata.iterrows():
        sc=suicide['country']==row['country']#same codition
        ss=suicide['sex']==row['sex']
        sa=suicide['age']==row['age']
        yra=suicide['year']==row['year']+1
        yrb=suicide['year']==row['year']-1
        ind1=suicide[sc & ss & sa & yra].index
        ind2=suicide[sc & ss & sa & yrb].index
        no1=suicide.at[ind1[0],'suicides_no']
        no2=suicide.at[ind2[0],'suicides_no']
        no0=(no1+no2)/2
        s.loc[index,'suicides_no']=no0
    return None

#fill missing data
for index,row in missdata.iterrows():
    sc=suicide['country']==row['country']#same codition
    ss=suicide['sex']==row['sex']
    sa=suicide['age']==row['age']
    if np.isin(row.country,['Bosnia and Herzegovina','Israel','United Kingdom'\
                            'Philippines','TFYR Macedonia','Mongolia','Kiribati','Brunei Darussalam','United States of America']):
        continue
    if row.year==2005:
        yra=suicide['year']==row['year']+2
    else:  yra=suicide['year']==row['year']+1
    yrb=suicide['year']==row['year']-1
    ind1=suicide[sc & ss & sa & yra].index    
    ind2=suicide[sc & ss & sa & yrb].index
    no1=suicide.at[ind1[0],'suicides_no']
    no2=suicide.at[ind2[0],'suicides_no']
    no0=(no1+no2)/2
    suifil.loc[index,'suicides_no']=no0
    print(row.country)
###
fillmiss(suifil,miscountry)
print(suifil[suifil.suicides_no.isnull()])
suifil.to_csv('suicidefillmissing.csv')
###########--------------------------------------------#############################
with open('suicidefillmissing.csv','r') as f:
    suicide=pd.read_csv(f)
suicide.reset_index(drop=True)
suicide=suicide.drop(['Unnamed: 0'],axis=1)
columns=suicide.columns
suicide.groupby(['country','year','sex']).sum()
misspop=suicide[suicide.population.isnull()]
misspop.groupby(['country'])['country'].count()
#no precessing missing population
suicide=suicide[suicide.population.notnull()]
#analyze gender
gender=suicide.groupby([suicide['country'],suicide['year'],suicide['sex']])[['suicides_no','population']].sum()
genders=gender.reset_index()
genders['suirate']=genders.suicides_no*100000/genders.population
#gender rate
for index,row in genders.iterrows():
    allpop=whole[(whole['country']==row['country']) & (whole['year']==row['year'])]['population'].values
    sexrate=row.population/allpop
    genders.loc[index,'sexrate']=sexrate
    
genders.to_csv('gender.csv')
#age
age=suicide.groupby([suicide['country'],suicide['year'],suicide['age']])[['suicides_no','population']].sum()
ages=age.reset_index()
ages['suirate']=ages.suicides_no*100000/ages.population
#age rate
for index,row in ages.iterrows():
    allpop=whole[(whole['country']==row['country']) & (whole['year']==row['year'])]['population'].values
    agerate=row.population/allpop
    ages.loc[index,'agerate']=agerate

ages.to_csv('age.csv')
#whole
whole=suicide.groupby([suicide['country'],suicide['year']])[['suicides_no','population']].sum()
whole=whole.reset_index()
whole['suirate']=whole.suicides_no*100000/whole.population
for index,row in whole.iterrows():
    female=genders[(genders['country']==row['country']) & (genders['year']==row['year']) & (genders['sex']=='female')]['population'].values
    male=genders[(genders['country']==row['country']) & (genders['year']==row['year']) & (genders['sex']=='male')]['population'].values
    sexratio=male*100/female#number of male per 100 female
    whole.loc[index,'sexratio']=sexratio
whole.to_csv('whole.csv')
#file
with open('gender.csv','r') as f:
    genders=pd.read_csv(f)
with open('age.csv','r') as f:
    ages=pd.read_csv(f)
with open('whole.csv','r') as f:
    whole=pd.read_csv(f)

###############--------------------------------------------####################
#how many countrys?
cntys=suicide.drop_duplicates('country',inplace=False).country
len(cntys)#100
#analysize
import matplotlib
import matplotlib.pyplot as plt
#####gender gap######
fm=genders[genders.sex=='female']['suirate'].values
ml=genders[genders.sex=='male']['suirate'].values
plt.figure(figsize=[10,8])
plt.boxplot([fm,ml],labels=['female','male'])
plt.ylabel('suicide rate')
plt.show
plt.savefig('box_sex_allcountry.eps')
plt.savefig('box_sex_allcountry.png')
plt.close()
#distribution of suicide rates
from scipy import stats
dist = stats.norm()
gg=genders.groupby(['country','sex'])['suirate'].mean()
gg=gg.unstack()#suicide rate
plt.figure(figsize=[10,8])
plt.plot(gg['female'].values,dist.pdf(gg['female'].values),'r.', lw=3,\
        alpha=0.5, label='female suicide')
plt.plot(gg['male'].values,dist.pdf(gg['male'].values),'b+', lw=3,\
        alpha=0.8, label='male suicide')
plt.legend()
#------------#
sexgrp=genders.groupby(['country','sex'])['suirate'].mean()#suicide rate gender group, year average
sexgrp=sexgrp.unstack()
sexgrp.to_csv('sexgroup.csv')
sexgrp[sexgrp.female>=sexgrp.male]
#correaltion of suicide rate and sex rate
plt.figure(figsize=[10,8])
fmlr=genders[genders.sex=='female']['sexrate'].values
sr=whole['suirate'].values
plt.scatter(fmlr,sr)
plt.xlabel('sex rate of female')
plt.ylabel('suicide rate')
plt.show
plt.close()
#sex ratio

#correlation between sexratio and suicide rate of each country
from scipy.stats.stats import pearsonr
sexcor=pd.DataFrame(columns=['country','cor','p','no'])
for c in cntys:
    data=whole[whole.country==c]
    sexratio=data['sexratio'].values
    suirate=data['suirate'].values
    cor, p = pearsonr(sexratio, suirate)
    sexcor=sexcor.append({'country': c,'cor':cor,'p':p,'no':len(data)}, ignore_index=True)
   
plt.plot(whole[whole.country=='Iran (Islamic Rep of)']['year'].values\
         ,whole[whole.country=='Iran (Islamic Rep of)']['ssdiff'].values,'bo')
plt.close()
sexcor.to_csv('sexcor.csv')

#countrys have positive correlation,cor>0.4
len(sexcor.query("p<0.05 &cor>0 & no>=5"))#20;number of countries that cor are positive
pcl=sexcor.query("p<0.05 &cor>0 & no>=5")['country']
#countrys have negative correlation,cor<=-0.4
len(sexcor.query("p<0.05 & cor<=0 & no>=5"))#27;number of countries that cor are negative
ncl=sexcor.query("p<0.05 & cor<=0 & no>=5")['country']
#correlation unsignificient
len(sexcor.query("p>=0.05 & no>=5"))#44;number of countries that cor are not significient
uncl=sexcor.query("p>=0.05 & no>=5")['country']

len(sexcor.query("p<0.05 &cor>-0.3&cor<0 & no>=5"))


with open('sexcor.csv','r') as f:
    sexcor=pd.read_csv(f)
#positive, developed
len(sexcor.query("cor<0 & no>=5 & sexrt_avg>100"))#14
len(sexcor.query("cor>=0 & no>=5 & sexrt_avg>100"))#6
len(sexcor.query("cor<0 & no>=5 & sexrt_avg<=100"))#41
len(sexcor.query("cor>=0 & no>=5 & sexrt_avg<=100"))#30

for index,row in sexcor.iterrows():
    c=row['country']
    sexcor.loc[index,'sexrt_avg']=np.mean(whole[whole.country==c]['sexratio'].values)
sexcor.to_csv('sexcor2.csv')

sexcor.query("country in @pcl & development=='HIGH-INCOME ECONOMIES'")['continent']
len(sexcor.query("no>=5 & development=='HIGH-INCOME ECONOMIES'"))#9
len(sexcor.query("cor>0 & p<0.05 & no>=5 & development=='HIGH-INCOME ECONOMIES'"))#9
len(sexcor.query("cor<=0 & p<0.05 & no>=5 & development=='HIGH-INCOME ECONOMIES'"))#20
#box plot of female cor and male cor
fmcor=sexcor[sexcor.femalecor.notnull()]['femalecor'].values
mlcor=sexcor[sexcor.malecor.notnull()]['malecor'].values
cor=sexcor[sexcor.cor.notnull()]['cor'].values
plt.figure(figsize=[10,8])
plt.boxplot([fmcor,mlcor],labels=['female correlation','male correlation'])

plt.show
plt.savefig('box_sex_correlation.eps')
plt.savefig('box_sex_correlation.png')
plt.close()

from scipy import stats
import seaborn as sns
ax=sns.kdeplot(mlcor,label='male correlation distribution',legend=True)
ax=sns.kdeplot(fmcor,label='female correlation distribution',legend=True,linestyle="--")
fig = ax.get_figure()
fig.savefig('distribution_sex_correlation.eps')
fig.savefig('distribution_sex_correlation.png')

dist = stats.norm()
plt.figure(figsize=[10,8])
plt.hist(fmcor,histtype='step',alpha=0.8, label='female correlation distribution')
plt.hist(mlcor,histtype='step',alpha=0.8, label='male correlation distribution')

#-----------------------#
plt.figure(figsize=[10,8])
plt.plot(fmcor,dist.pdf(fmcor),'r.', lw=3,\
        alpha=0.5, label='female correlation distribution')
plt.plot(mlcor,dist.pdf(mlcor),'b+', lw=3,\
        alpha=0.8, label='male correlation distribution')
plt.plot(cor,dist.pdf(cor),'go', lw=3,\
        alpha=0.8, label='total correlation distribution')
plt.legend()
plt.savefig('distribution_sex_correlation.eps')
plt.savefig('distribution_sex_correlation.png')
plt.close()
#------------#
#correlation between male suicide rate and sex ratio
for index,row in sexcor.iterrows():
    c=row['country']
    data=whole[whole.country==c]
    sexratio=data['sexratio'].values
    ssdiff=data['ssdiff'].values
    malr=genders[(genders.country==c) & (genders.sex=='male')]['suirate'].values
    cor, p = pearsonr(sexratio, malr)
    sexcor.loc[index,'malecor']=cor
    sexcor.loc[index,'malep']=p
    diffcor,diffp = pearsonr(sexratio, ssdiff)
    sexcor.loc[index,'diffcor']=diffcor
    sexcor.loc[index,'diffp']=diffp

for index,row in sexcor2.iterrows():
    c=row['country']
    fmlr=genders[(genders.country==c) & (genders.sex=='female')]['suirate'].values
    mlr=genders[(genders.country==c) & (genders.sex=='male')]['suirate'].values
    cor, p = pearsonr(mlr, fmlr)
    sexcor2.loc[index,'insexcor']=cor
sexcor2.to_csv('sexcor2.csv')
#######-------------##########
#difference correaltion
len(sexcor.query("no>=5 & diffp<0.05 & diffcor > 0"))#17 positive
len(sexcor.query("no>=5 & diffp<0.05 & diffcor < 0"))#27 engative
len(sexcor.query("no>=5 & diffp>=0.05"))#47 nocor

len(sexcor.query("no>=5 & diffp<0.05 & diffcor < 0 & diffcor>-0.3"))
###########------age---------#########
a514=ages[ages.age=='5-14 years']['suirate'].values
a1524=ages[ages.age=='15-24 years']['suirate'].values
a2534=ages[ages.age=='25-34 years']['suirate'].values
a3554=ages[ages.age=='35-54 years']['suirate'].values
a5574=ages[ages.age=='55-74 years']['suirate'].values
a75=ages[ages.age=='75+ years']['suirate'].values
plt.figure(figsize=[20,10])
plt.boxplot([a514,a1524,a2534,a3554,a5574,a75]\
            ,labels=['5-14 years','15-24 years','25-34 years'\
                     ,'35-54 years','55-74 years','75+ years'])
plt.show
plt.savefig('box_age_allcountry.eps')
plt.savefig('box_age_allcountry.png')
plt.close()
