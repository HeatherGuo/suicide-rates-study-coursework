# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 14:35:21 2019

@author: maple
"""

def fillmiss(dframe,missdata,whdata):
    #dframe--dataset;country--the conditions;c--the conditions should keep same;
    #y--the conditions sould keep differ; v--the value
    for index,row in missdata.iterrows():
        sc=whdata['country']==row['country']#same codition
        ss=whdata['sex']==row['sex']
        sa=whdata['age']==row['age']
        yra=whdata['year']==row['year']+1
        yrb=whdata['year']==row['year']-1
        no1=whdata[sc & ss & sa & yra].suicides_no
        no2=whdata[sc & ss & sa & yrb].suicides_no
        no0=(no1+no2)/2
        row.suicides_no=no0
        dframe.loc[index]=row
    return print(index)
suifil[(suifil[c]==suifil.iloc[0][c]) & (suifil[y]==suifil.iloc[0][y]+1)]
suifil.query("(year==1987) & (sex=='female')")

c=['country','sex','age']
y=['year']
v=['suicides_no']
fillmiss(suifil,missdata,suicide)
print(suifil.suicides_no.isnull())

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


clt2=['Bosnia and Herzegovina','Israel','United Kingdom'\
      ,'TFYR Macedonia','Mongolia','Kiribati','Brunei Darussalam','United States of America']
s=suicide[suicide.country.isin(clt2)]#suicide filter with counry list
g=s.groupby(['country','year'])['year'].count()
g.groupby(['country']).count()

m=suifil[suifil.suicides_no.isnull()]
m.groupby(['country']).count()

for index,row in genders.iterrows():
    allpop=whole[(whole['country']==row['country']) & (whole['year']==row['year'])]['population'].values
    sexrate=row.population/allpop
    genders.loc[index,'sexrate']=sexrate
sexcor=pd.DataFrame(columns=['country','cor','p','no'])
for c in cntys:
    data=whole[whole.country==c]
    sexratio=data['sexratio'].values
    suirate=data['suirate'].values
    cor, p = pearsonr(sexratio, suirate)
    sexcor=sexcor.append({'country': c,'cor':cor,'p':p,'no':len(data)}, ignore_index=True)
for index,row in whole.iterrows():
    female=genders[(genders['country']==row['country']) & (genders['year']==row['year']) & (genders['sex']=='female')]['suirate'].values
    male=genders[(genders['country']==row['country']) & (genders['year']==row['year']) & (genders['sex']=='male')]['suirate'].values
    ssdiff=male-female#number of male per 100 female
    whole.loc[index,'ssdiff']=ssdiff
for index,row in sexcor.iterrows():
    c=row['country']
    data=whole[whole.country==c]
    sexratio=data['sexratio'].values
    fmlr=genders[(genders.country==c) & (genders.sex=='female')]['suirate'].values
    cor, p = pearsonr(sexratio, fmlr)
    sexcor.loc[index,'femalecor']=cor
    sexcor.loc[index,'femalep']=p
sexcorjoin=pd.concat([sexcor,whole],axis=1, join_axes=[sexcor.country])

plt.plot(genders[(genders.country=='Argentina')&(genders.sex=='female')]['year'].values,\
                 genders[(genders.country=='Argentina')&(genders.sex=='female')]['suirate'].values,'r--')
plt.plot(genders[(genders.country=='Argentina')&(genders.sex=='male')]['year'].values,\
                 genders[(genders.country=='Argentina')&(genders.sex=='male')]['suirate'].values,'b--')
plt.plot(whole[whole.country=='Argentina']['year'].values,\
                 whole[whole.country=='Argentina']['sexratio'].values)
plt.plot(whole[whole.country=='Argentina']['sexratio'].values,\
                 genders[(genders.country=='Argentina')&(genders.sex=='female')]['suirate'].values)