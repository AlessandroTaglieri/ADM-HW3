import csv
import pandas as pd
import os.path
#define column of our dataframe
df=pd.DataFrame(columns=['title', 'intro', 'plot','film_name','producer','director','writer','starring','music','release date','runtime','country','language','budget'])


for index in range(totalMovies):
    print(index)
    title=''
    plot=''
    intro=''
    title_name='NA'
    producer='NA'
    director='NA'
    writer='NA'
    starring=['NA']
    music='NA'
    release_date='NA'
    runtime='NA'
    country='NA'
    language='NA'
    budget='NA'
    
    
    #define name of the file that we want to find (in my case: in the same directory)
    name="article_"
    extension=".html"
    file="{}{}{}".format(name,index ,extension)
    
    #check if this file exists
    if not os.path.isfile("HW3 ADM/"+file):
        continue
        
    #open file   
    response2 = open("HW3 ADM/"+file)
    soup = BeautifulSoup(response2)
    #take title.
    title=soup.title.text.rsplit(' ', 2)[0]
    
    #take all p in intro(firt section)
    #print(soup.find('span', attrs={'class': 'mw-headline'}))
    if soup.find('span', attrs={'class': 'mw-headline'}):
        heading = soup.find('span', attrs={'class': 'mw-headline'})
        paragraphs = heading.find_all_previous('p')
        for p in paragraphs: 
            intro = p.text + intro
            
     
        #take all p in 'plot'(second section)
        b=True
        #print(soup.find('span', attrs={'class': 'mw-headline'}))
        if soup.find('span', attrs={'class': 'mw-headline'}): 
            
            heading = soup.find('span', attrs={'class': 'mw-headline'})
            
            for item in heading.parent.nextSiblingGenerator():
                
                if item.name=='h2':
                    break
                if hasattr(item, "text"):
                    
                    plot+=item.text

        else:
            plot="NAN"
    
    else:
        intro="NAN"
        plot="NAN"
    
    
    #Get info about infobox from every page and put them in respective sections in tsv file  
    if soup.find('table', attrs={'class': 'infobox vevent'}):
        
        table = soup.find('table', attrs={'class': 'infobox vevent'})  
    
        if table.find('th', attrs={'class': 'summary'}):
        
            x=table.find('th', attrs={'class': 'summary'})
            title_name=x.text.strip()
        
        for cell in table.find_all('th'):
        
            if cell.find_next_sibling('td'):
                a=cell.find_next_sibling('td')
                if cell.text.strip()=='Directed by':
                    director=a.text.strip()
                elif cell.text.strip()=='Produced by':
                
                    producer=a.text.strip()
                elif cell.text.strip()=='Written by':
                
                    writer=a.text.strip()
                elif cell.text.strip()=='Starring':
                    listStarring=[]
                    for link in a.select('a'):
                        
                        listStarring.append(link.text)
                    starring=listStarring
                    #print(starring)
                elif cell.text.strip()=='Music by':
                
                    music=a.text.strip()
                elif cell.text.strip()=='Release date':
                    release_date=a.text.strip()   
                elif cell.text.strip()=='Running time':
                
                    runtime=a.text.strip()
                elif cell.text.strip()=='Country':
              
                    country=a.text.strip()
                elif cell.text.strip()=='Language':
              
                    language=a.text.strip()
                elif cell.text.strip()=='Budget':
              
                    budget=a.text.strip()
            else:
                continue
            
    
    #put all infos in movie list
    movie=[title,intro,plot,title_name,producer,director,writer,starring,music,release_date,runtime,country,language,budget]
    #update dataframe with this list
    extension2=".tsv"
    file="{}{}{}".format(name,index,extension2)
   
    movieTitle=["title","intro","plot","title_name","producer","director","writer","starring","music","release_date","runtime","country","language","budget"]
    with open("HW3 ADM/tsv_new/"+file, 'w', newline='') as f_output:
        tsv_output = csv.writer(f_output, delimiter='\t')
        tsv_output.writerow(movieTitle)
        tsv_output.writerow(movie)
    df.loc[index] = movie