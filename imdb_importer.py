import urllib.request
import io
import gzip
import psycopg2
from configparser import ConfigParser

class IMDB_importer(object):

    def download_and_decompressed_File(self, fileName):
        response = urllib.request.urlopen('https://datasets.imdbws.com/' + fileName)
        compressed_file = io.BytesIO(response.read())
        decompressed_file = gzip.GzipFile(fileobj=compressed_file)
        return decompressed_file

    def write_file(self):
        title = self.download_and_decompressed_File('title.basics.tsv.gz')
        with open('title.tsv','wb') as f:
            f.write(title.read())
        return print('true')

    def read_database_config(self, filename='database.ini', section='postgresql'):
        parser = ConfigParser()
        parser.read(filename)
    
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Not found section {0} in {1} file'.format(section, filename))
    
        return db

    def connect_to_database_and_write_data(self, dropTablesIfExists=True):
        connection = None

        try:   
            params = self.read_database_config()
            print('Connecting to the database.')
            connection = psycopg2.connect(**params)

            cursor = connection.cursor()

            if dropTablesIfExists == True:
                print('Drop tables if exists in database.')
                cursor.execute('DROP TABLE IF EXISTS titles')
                cursor.execute('DROP TABLE IF EXISTS names')
                cursor.execute('DROP TABLE IF EXISTS names_titles')
                connection.commit()

            print('Create tables if not exists.')
            cursor.execute(
                '''CREATE TABLE IF NOT EXISTS names
                (
                    nconst text PRIMARY KEY,
                    primaryName text,
                    birthYear integer,
                    deathYear integer,
                    primaryProfession text,
                    knownForTitles text
                )'''
            )

            cursor.execute(
                '''CREATE TABLE IF NOT EXISTS titles
                (   
                    tconst text PRIMARY KEY,
                    titleType text,
                    primaryTitle text,
                    originalTitle text,
                    isAdult bool,
                    startYear integer,
                    endYear integer,
                    runtimeMinutes integer,
                    genres text
                )'''
            )

            cursor.execute(
                '''CREATE TABLE IF NOT EXISTS names_titles
                (   
                    PRIMARY KEY(nconst_id, tconst_id),
                    nconst_id text,
                    tconst_id text
                )'''
            )
            connection.commit()

            print('Download and write data into Titles table.')
            titles = self.download_and_decompressed_File('title.basics.tsv.gz')
            with titles as titles_lines:
                titles_lines.readline()
                cursor.copy_from(titles_lines,'titles')

            cursor.execute('ALTER TABLE titles ALTER COLUMN genres TYPE text[] USING string_to_array(genres, \',\')')
            connection.commit()

            print('Download and write data into Names table.')
            names = self.download_and_decompressed_File('name.basics.tsv.gz')
            with names as names_lines:
                names_lines.readline()
                cursor.copy_from(names_lines,'names')

            cursor.execute('ALTER TABLE names ALTER COLUMN knownForTitles TYPE text[] USING string_to_array(knownForTitles, \',\')')
            connection.commit()

            cursor.execute('ALTER TABLE names ALTER COLUMN primaryProfession TYPE text[] USING string_to_array(primaryProfession, \',\')')
            connection.commit()

            print('Write data into names_titles table.')
            cursor.execute('INSERT INTO names_titles SELECT nconst as ncost_id,UNNEST(knownForTitles) as tconst_id FROM Names')
            connection.commit()

            print('Create indexes.')
            #cursor.execute('CREATE INDEX idx_knownForTitles ON Names USING GIN(knownForTitles)')
            cursor.execute('CREATE INDEX idx_nconst_id ON names_titles (nconst_id)')
            cursor.execute('CREATE INDEX idx_tconst_id ON names_titles (tconst_id)')
            connection.commit()

            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()
                print('Database connection closed.')

#test = IMDB_importer()
#test.write_file()
test = IMDB_importer()
test.connect_to_database_and_write_data()