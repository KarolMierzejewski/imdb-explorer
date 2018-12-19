from peewee import PostgresqlDatabase, Model, TextField, IntegerField, BooleanField, ForeignKeyField
from playhouse.postgres_ext import ArrayField

db = PostgresqlDatabase(None)

class BaseModel(Model):
    class Meta:
        database = db

class Names(BaseModel):
    nconst = TextField(primary_key=True)
    primaryname = TextField()
    birthyear = IntegerField()
    deathyear = IntegerField()
    primaryprofession = TextField()
    knownfortitles = ArrayField(TextField)

    class Meta:
        db_table = 'names'

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

    class Meta:
        db_table = 'titles'

class Names_Titles(BaseModel):
    tconst_id = ForeignKeyField(model=Titles)
    nconst_id = ForeignKeyField(model=Names)

    class Meta:
        db_table = 'names_titles'