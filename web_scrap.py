#======= Important Libraries
from bs4 import BeautifulSoup
import pandas as pd
import  requests

#======= collect data from internet
url='https://www.worldometers.info/coronavirus/?utm_campaign=homeAdvegas1?#countries'
response=requests.get(url)

html=response.text
soup=BeautifulSoup(html,'html.parser')
#print(soup.title)

data=soup.find(id='main_table_countries_today')
tbody=data.find('tbody')

title_list=['#','country','total cases','new cases','total deaths','new deaths','total recovered','col 1','active cases','serious, critical','tot cases/1M pop','deaths/1M pop','total tests','tests/1M pop','population','continent','col 2','col 3','col 4']

tr=tbody.find_all('tr')
ld=[]
count=0
for item in tr:
    count+=1
    i=k=0
    dict1={}
    td=item.find_all('td')
    for one_td in td:
        l=len(one_td.contents)
        if l<1:
            dict1[str(i)]=None
        elif l==1:
            if count>8:
                k+=1
                if k==2:
                    dict1[str(i)]=one_td.contents[0].text
                else:
                    dict1[str(i)]=one_td.contents[0]
            else:
                dict1[str(i)]=one_td.contents[0]
        else:
                if count>7:
                    dict1[str(i)]=one_td.contents[0].text
                else:
                    dict1[str(i)]=one_td.contents[1].text
        i+=1
    ld.append(dict1)

#====== Create DataFrame   & csv
df=pd.DataFrame(ld)
df.to_csv('covid.csv')
                
#====== clean the data
def remove_comma(n):
    try:
        return int(n.replace(',',''))
    except:
        return 0

information=pd.read_csv('covid.csv', names=title_list)
df=information.iloc[1:]
df=df.fillna('0')
df['total cases']=df['total cases']. apply(lambda x: remove_comma(x))
df['total deaths']=df['total deaths']. apply(lambda x: remove_comma(x))
df['total recovered']=df['total recovered']. apply(lambda x: remove_comma(x))
df['active cases']=df['active cases']. apply(lambda x: remove_comma(x))
df['new cases']=df['new cases']. apply(lambda x: remove_comma(x))
df.to_csv('covid1.csv')