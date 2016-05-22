__author__ = 'abhisheksingh29895'

'''
Url used for this
1) "http://trevor-smith.github.io/scraping-post/"
2) "https://stackoverflow.com/questions/12680754/split-pandas-dataframe-string-entry
-to-separate-rows/12681217#12681217?newreg=fbba4cb73a9f4c2c97a46fefffacdfa1"
3) "http://stackoverflow.com/questions/30230854/unable-to-access-tastekid-
s-api-it-says-error-403-request-forbidden"
4)  "http://stackoverflow.com/questions/11983049/python-read-and-validate-input-url"
'''

from  bs4  import  BeautifulSoup
from  mechanize  import Browser
import urllib,  urllib2,  json,  re,  random,  time
import  pandas  as  pd
from  urllib2  import  Request, urlopen, URLError
import numpy as np

#creating the Movie url's from the Box Office Mojo html page
mylist = []
page_number = range(0, 55)
for i in page_number:
    mylist.append("http://www.boxofficemojo.com/alltime/domestic.htm?page=" + str(page_number[i]) + "&p=.htm")

####Picking random 15 entries from this list of page.htms
best_15  =  [mylist[i]  for  i  in  sorted(random.sample(xrange(len(mylist)),  15))]

#Breaking page urls to list of movie url's
id_list  =  []  ;  movie_url_to_scrape  =  []
for  url  in  best_15:
    time.sleep(.2)
    page_domestic  =  urllib2.urlopen(url)
    soup_domestic  =  BeautifulSoup(page_domestic,"lxml")
    href_movie_tags  =  [(a.attrs.get('href')).encode('utf-8') for a in soup_domestic.select('a[href^/movies/?]')]
    href_movie_tags_split  =  [i.split('id', 1) for i in href_movie_tags]
    for  i  in  href_movie_tags_split[:-1]:
        id_list.append(i[1])
    for  id  in  id_list:
        movie_url_to_scrape.append("http://www.boxofficemojo.com/movies/?id"  +  id)
    movie_url_to_scrape_unique  =  set(movie_url_to_scrape)
    my_movies  =  list(movie_url_to_scrape_unique)

my_movies_new  =  [my_movies[i]  for  i  in  sorted(random.sample(xrange(len(my_movies)),  200))]

ja  =  np.array_split(my_movies_new,  50)
#Creating data objects
all_movie,  all_movie_path,  all_domestic,  all_international  =  [],  [],  [],  []
all_worldwide  =  []

headers = { 'User-Agent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36"}
#Converting from Movies_URL_LIST to Movies_list
for b  in  ja:
    time.sleep(2)
    for  a  in  b:
        time.sleep(1)
        req  =  urllib2.Request(a,  headers  =  headers)
        try:
            page = urllib2.urlopen(req)
        except URLError, e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server couldn\'t fulfill the request.'
                print 'Error code: ', e.code
        else:
            print 'URL is good!'
        if page:
            page  =  page.read()  ;  soup  =  BeautifulSoup(page,  "lxml")
            revenue_string  =  str((soup.find("div", {"class": "mp_box_content"}))).split('$')
            r_length  =  len(revenue_string)
            if  r_length  ==  4:
                domestic  =  revenue_string[1].split("<")[0]
                International  =  revenue_string[2].split("<")[0]
                worldwide  =  revenue_string[3].split("<")[0]
            else:
                domestic  =  revenue_string[1].split("<")[0]
                International  =  ""
                worldwide  =  ""
            movie_string  =  str(soup.title).split('(')[0]
            movie1  =  movie_string.split(">")[1]
            movie  =  movie1.strip()  ;  movie_path  =  movie.replace(" ", "+")
        else:
            movie,  movie_path,  domestic,  International,  worldwide  =  "",  "",  "",  "",  ""
        all_movie.append(movie)  ;  all_movie_path.append(movie_path)  ;  all_domestic.append(domestic)
        all_international.append(International)  ;  all_worldwide.append(worldwide)
my_data  =  zip(all_movie,all_movie_path,all_domestic,all_international,all_worldwide)
small_data  =  pd.DataFrame(my_data)
small_data.columns  =  ['Movie','Movie_path','US_revenue','Foreign_revenue','Worldwide_revenue']


#Creating data objects to store values
all_rated,  all_response,  all_metascore,  all_movie1,  all_run_time  =  [],  [],  [],  [],  []
all_votes,  all_speciality,  all_imdb_rating,  all_director,  all_If_movie  =  [],  [],  [],  [],  []
all_actors,  all_genre,  all_release_date,  all_language,  all_year,  all_a  =  [],  [],  [],  [],  [],  []
#Pulling data from the movie-urls and appending all information into a dataset
for  a  in  all_movie_path:
    time.sleep(2)
    url  =  'http://www.omdbapi.com/?t=%s=&plot=full&r=json'%a
    url1  =  urllib.urlopen(url)
    json_file  =  json.loads(url1.read())  ;  json_len  =  len(json_file.values())
    #Capturing the parameters
    if  json_len  >  10:
        movie  =  json_file.values()[4].encode('utf-8')
        run_time  =  json_file.values()[15].encode('utf-8')
        votes  =  json_file.values()[18].encode('utf-8')
        speciality  =  json_file.values()[14].encode('utf-8')
        rated  =  json_file.values()[1].encode('utf-8')
        response  =  json_file.values()[2].encode('utf-8')
        metascore  =  json_file.values()[7].encode('utf-8')
        imdb_rating  =  json_file.values()[8].encode('utf-8')
        director  =  json_file.values()[9].encode('utf-8')
        release_date  =  json_file.values()[10].encode('utf-8')
        actors =  json_file.values()[11].encode('utf-8')
        genre  =  json_file.values()[13].encode('utf-8')
        language  =  json_file.values()[3].encode('utf-8')
        year  =  json_file.values()[12].encode('utf-8')
        If_movie  =  json_file.values()[16].encode('utf-8')
    else:
        movie,  run_time,  votes,  speciality  =  "",  "",  "",  ""
        rated,  response,  metascore,  If_movie  =  "",  "",  "",  ""
        imdb_rating,  director,  release_date,  actors  =  "",  "",  "",  ""
        genre,  language,  year  =  "",  "",  ""
#appending to the big lists
    all_rated.append(rated) ; all_response.append(response) ; all_metascore.append(metascore)
    all_movie1.append(movie) ; all_run_time.append(run_time) ; all_votes.append(votes)  ;  all_a.append(a)
    all_speciality.append(speciality) ; all_imdb_rating.append(imdb_rating)  ;  all_If_movie.append(If_movie)
    all_director.append(director) ; all_actors.append(actors) ; all_genre.append(genre)
    all_release_date.append(release_date)  ;  all_language.append(language)  ;  all_year.append(year)

#Making dataframes
Full_data  =  zip(all_rated,all_response,all_metascore,all_movie1,all_run_time,all_votes,all_If_movie,all_language,
                  all_speciality,all_imdb_rating,all_director,all_actors,all_genre,all_release_date,all_year,all_a)
Data_df  =  pd.DataFrame(Full_data)
Data_df.columns  =  ['rated','response','metascore','Movie','run_time','votes','If_movie','language','all_speciality',
                     'imdb_rating','director','actors','genre','release_date','year','Movie_path']

#Merging the 2 datasets
my_data  =  pd.merge(left  =  small_data,  right  =  Data_df,  left_on  =  'Movie_path'
                     ,  right_on  =  'Movie_path')
del my_data['Movie_path']   ;  del my_data['Movie_y']
my_data.rename(columns  =  {'Movie_x'  :  'Movie'},  inplace  =  True)
my_data.to_csv('movies_everything.csv')

#Making more dataframes for list type variables
#Genre
genre_df  =  my_data[['Movie', 'genre']]
genre_df1  =  pd.concat([pd.Series(row['Movie'], row['genre'].split(','))
                    for _, row in genre_df.iterrows()]).reset_index()
genre_df1.columns  =  ['genre','Movie']  ;  genre_df1.to_csv('genre_movie.csv')
#Actor
actor_df  =  my_data[['Movie','actors']]
actor_df1  =  pd.concat([pd.Series(row['Movie'], row['actors'].split(','))
                    for _, row in actor_df.iterrows()]).reset_index()
actor_df1.columns  =  ['actors','Movie']  ;  actor_df1.to_csv('actor_movie.csv')
#langauge
language_df  =  my_data[['Movie','language']]
language_df1  =  pd.concat([pd.Series(row['Movie'], row['language'].split(','))
                    for _, row in language_df.iterrows()]).reset_index()
language_df1.columns  =  ['language','Movie']  ;  language_df1.to_csv('language_movie.csv')
