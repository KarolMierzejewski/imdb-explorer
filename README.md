# imdb-explorer
Download and decompressed .TSV file from IMDb and prepare database to explore them in simple REST-API.

# How to install
Clone repository
```
$ git clone https://github.com/Luqqk/imdb-import.git
```
Create virtualenv for this project
```
$ mkvirtualenv imdb
```
Switch to the created environment
```
$ workon imdb
```
Install requirements
```
$ pip install -r requirements.txt
```
Enter Your DB credential into database.ini file (if you don't know how to create Posgresql Database check [this](http://www.postgresqltutorial.com/install-postgresql/))
```
[postgresql]
host=localhost
database=imdb
user=postgres
password=pass
```
Download IMDb data and save it to the database
```
$ python imdb_importer.py
```
Run REST-API to interact with IMDb data
```
$ python start_restapi.py
```

# How to use
Get list (in alphabetical order) with all movies in indicated year and corresponding actor names. This method supports pagination, you can add page param.
```
GET /movies_and_names_by_startyear?year=2017&page=1
```
Get list (in alphabetical order) with all movies in indicated genre and corresponding actor names. This method supports pagination, you can add page param.
```
GET /movies_and_names_by_genre?genre=Drama&page=1
```

# Useful links
- more about IMDb datasets https://www.imdb.com/interfaces/
