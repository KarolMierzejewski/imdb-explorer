from flask import Blueprint, jsonify, request, abort
from restapi.models import Names, Titles, Names_Titles
from peewee import SQL

views = Blueprint('views',__name__)

@views.route('/all_movies')
def all_movies():

    titles = Titles.select(Titles.originaltitle, Titles.tconst).where(Titles.startyear==2017).order_by(Titles.originaltitle.asc()).paginate(1,10).dicts()

    response = []

    for title in titles:
        response.append(title)

    return jsonify({'titles': response})
    
@views.route('/movies_and_names_by_startyear')
def movies_and_names_by_startyear():

    try:
        year = int(request.args.get('year'))
        page = int(request.args.get('page'))
    except ValueError:
        abort(400)

    titles = Titles.select(Titles.originaltitle, Titles.tconst).where(Titles.startyear==year).order_by(Titles.originaltitle.asc()).paginate(page,100).dicts()
    response = []

    for title in titles:
        names = Names.select(Names.primaryname).join(Names_Titles, on=(Names_Titles.tconst_id == title['tconst'])).where(Names_Titles.nconst_id==Names.nconst).dicts()
        title['names'] = [name['primaryname'] for name in names]
        del title['tconst']
        response.append(title)
        
    return jsonify({'titles': response})

@views.route('/movies_and_names_by_genre')
def movies_and_names_by_genre():

    try:
        genre = list()
        genre.append(str(request.args.get('genre')))
        page = int(request.args.get('page'))
    except ValueError:
        abort(400)

    titles = Titles.select(Titles.originaltitle, Titles.genres, Titles.tconst).where(SQL(" %s = ANY(genres)", (genre))).order_by(Titles.originaltitle.asc()).paginate(page,100).dicts()
    response = []

    for title in titles:
        names = Names.select(Names.primaryname).join(Names_Titles, on=(Names_Titles.tconst_id == title['tconst'])).where(Names_Titles.nconst_id==Names.nconst).dicts()
        title['names'] = [name['primaryname'] for name in names]
        del title['tconst']
        response.append(title)
        
    return jsonify({'titles': response})