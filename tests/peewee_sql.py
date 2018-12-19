from peewee import PostgresqlDatabase, Model, TextField, IntegerField, BooleanField, ForeignKeyField
from playhouse.postgres_ext import ArrayField

db = PostgresqlDatabase(None)

class BaseModel(Model):
    class Meta:
        database = db
        
class Titles(BaseModel):
    tconst = TextField(primary_key=True)
    titletype = TextField()
    primarytitle = TextField()
    originaltitle = TextField()
    isadult = BooleanField()
    startyear = IntegerField()
    endyear = IntegerField()
    runtimemins = IntegerField()
    genres = ArrayField(TextField)
    
        
db.init('imdb',
            host='localhost',
            user='postgres',
            password='karol12345'
    )

db.connect()
