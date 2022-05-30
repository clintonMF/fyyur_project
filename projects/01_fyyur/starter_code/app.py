#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import sys
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from models import *
import collections
collections.Callable = collections.abc.Callable
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
   
      

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  
  data = []
  venues = Venue.query.all()
  several_venues = set()
  for venue in venues:
    several_venues.add((venue.city, venue.state))
  for each_venue in several_venues:
    data.append({
      "city":each_venue[0],
      "state": each_venue[1],
      "venues":[]
    })
  for venue in venues:
    for i in data:
      if i["city"] == venue.city and i["state"] == venue.state:
        upcoming_shows = Show.query.join(Venue).filter(venue.id==venue.id).filter(
          Show.start_time > datetime.utcnow()
          )
        venue_details = {
          "id":venue.id,
          "name": venue.name,
          "num_upcoming_shows": upcoming_shows.count()
        }
        i["venues"].append(venue_details)
  
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # search for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  
  search_term = request.form.get('search_term')
  print(search_term)
  search_for = f"%{search_term}%"
  print(search_for)
  venues = Venue.query.filter(Venue.name.ilike(search_for)).all()
  print(venues)
  data = []
  count = 0
  for venue in venues:
    upcoming_shows = Show.query.join(Venue).filter(venue.id==venue.id).filter(
          Show.start_time > datetime.utcnow())
    each_data = {
      "id" : venue.id,
      "name" : venue.name,
      "num_upcoming_shows": upcoming_shows.count()
    }
    data.append(each_data)
    count += 1
  
  response={
    "count": count,
    "data": data
  }
  
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id): 
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  print(venue_id)
  venue = Venue.query.get(venue_id)
  def convert(string):
    li = string.split(",")
    return li
  past_shows = []
  upcoming_shows = []
  p_shows = Show.query.filter(Show.venue_id==venue_id).filter(
          Show.start_time < datetime.utcnow()).all()
  for p_show in p_shows:
    artist_id = p_show.artist_id
    artist_past = Artist.query.get(artist_id)
    past_show = {
      "artist_id": artist_id,
      "artist_name": artist_past.name,
      "artist_link": artist_past.image_link,
      "start_time": str(p_show.start_time),
    }
    past_shows.append(past_show)
      
  u_shows = Show.query.filter(Show.venue_id==venue_id).filter(
          Show.start_time > datetime.utcnow()).all()
  for u_show in u_shows:
    artist_id = u_show.artist_id
    artist_up = Artist.query.get(artist_id)
    upcoming_show = {
      "artist_id": artist_id,
      "artist_name": artist_up.name,
      "artist_link": artist_up.image_link,
      "start_time": str(u_show.start_time),
    }
    upcoming_shows.append(upcoming_show)
  
  data = {
    "id":venue.id,
    "name":venue.name,
    "genres": convert(venue.genres),
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website_link,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link":venue.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": Show.query.filter(Show.venue_id==venue.id).filter(
          Show.start_time > datetime.utcnow()).count(),
    "upcoming_shows_count": Show.query.filter(Show.venue_id==venue.id).filter(
          Show.start_time > datetime.utcnow()).count(),
    }
  
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form=VenueForm(request.form)
  try:
    if form.validate():
      new_venue = Venue(
        name = form.name.data,
        city = form.city.data,
        state = form.state.data,
        address = form.address.data,
        phone  = form.phone.data,
        genres = ',' .join(form.genres.data),
        image_link = form.image_link.data,
        facebook_link = form.facebook_link.data,
        website_link = form.website_link.data,
        seeking_talent = form.seeking_talent.data,
        seeking_description = form.seeking_description.data,
      )
      db.session.add(new_venue)
      db.session.commit()
      print('daniel')
      flash('Venue ' + request.form['name'] + 
            ' was successfully listed!')
  except:
    db.session.rollback()
    print(sys.exc_info)
    print('here')
    flash('An error occurred. Venue ' + request.form['name'] 
          + ' could not be listed.')
  finally:
    db.session.close()
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., 
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit
  except:
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  artists = Artist.query.all()
  data = []
  for artist in artists:
    each_data = {
      "id": artist.id,
      "name" : artist.name
    }
    data.append(each_data)
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # search for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  
  
  search_term = request.form.get('search_term')
  search_for = f"%{search_term}%"
  artists = Artist.query.filter(Artist.name.ilike(search_for))
  count = 0
  data = []
  for artist in artists:
    upcoming_shows = Show.query.join(Artist).filter(
      artist.id==artist.id).filter(Show.start_time > datetime.utcnow())
    each_data = {
      "id": artist.id,
      "name": artist.name,
      "num_upcoming_shows": upcoming_shows.count()
    }
    data.append(each_data)
    count += 1
    
  response={
    "count": count,
    "data": data
  }
  

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  artist = Artist.query.get(artist_id)
  def convert(string):
    li = string.split(",")
    return li
  past_shows = []
  upcoming_shows = []
  p_shows = Show.query.filter(Show.artist_id==artist_id).filter(
    Show.start_time < datetime.utcnow()).all()
  for p_show in p_shows:
    venue_id = p_show.venue_id
    venue_past = Venue.query.get(venue_id)
    past_show = {
      "venue_id": venue_id,
      "venue_name": venue_past.name,
      "venue_link": venue_past.image_link,
      "start_time": str(p_show.start_time),
    }
    past_shows.append(past_show)
      
  u_shows = Show.query.filter(Show.artist_id==artist_id).filter(
    Show.start_time > datetime.utcnow()).all()
  for u_show in u_shows:
    venue_id = u_show.venue_id
    venue_up = Venue.query.get(venue_id)
    upcoming_show = {
      "venue_id": venue_id,
      "venue_name": venue_up.name,
      "venue_link": venue_up.image_link,
      "start_time": str(u_show.start_time),
    }
    upcoming_shows.append(upcoming_show)
  
  data = {
    "id":artist.id,
    "name":artist.name,
    "genres": convert(artist.genres),
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website_link,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link":artist.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": Show.query.filter(Show.artist_id==artist.id).filter(
          Show.start_time < datetime.utcnow()).count(),
    "upcoming_shows_count": Show.query.filter(Show.artist_id==artist.id).filter(
      Show.start_time > datetime.utcnow()).count(),
    }
  
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist_req = Artist.query.get(artist_id)
  artist={
    "id": artist_id,
    "name": artist_req.name,
    "genres": artist_req.genres, #ask if this is the right way
    "city": artist_req.city,
    "state": artist_req.state,
    "phone": artist_req.phone,
    "website": artist_req.website_link,
    "facebook_link": artist_req.facebook_link,
    "seeking_venue": artist_req.seeking_venue,
    "seeking_description": artist_req.seeking_description,
    "image_link": artist_req.image_link,
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  artist = Artist.query.get(artist_id)
  try:
    form = ArtistForm(request.form)
    if form.validate():
      artist.city = form.city.data
      artist.state = form.state.data
      artist.genres = ','.join(form.genres.data)
      artist.phone = form.phone.data
      artist.website_link = form.website_link.data
      artist.facebook_link = form.facebook_link.data
      artist.seeking_venue = form.seeking_venue.data
      artist.seeking_description = form.seeking_description.data
      artist.image_link = form.image_link.data
      artist.name = form.name.data
      db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue_req = Venue.query.get(venue_id)
  venue={
    "id": venue_id,
    "name": venue_req.name,
    "genres": venue_req.genres,
    "address": venue_req.address,
    "city": venue_req.city,
    "state": venue_req.state,
    "phone": venue_req.phone,
    "website": venue_req.website_link,
    "facebook_link": venue_req.facebook_link,
    "seeking_talent": venue_req.seeking_talent,
    "seeking_description": venue_req.seeking_description,
    "image_link": venue_req.image_link
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  venue = Venue.query.get(venue_id)
  try:
    form = VenueForm(request.form)
    if form.validate():
      venue.name = form.name.data
      venue.genres = ','.join(form.genres.data)
      venue.address = form.address.data
      venue.city = form.city.data
      venue.state = form.state.data
      venue.phone = form.phone.data
      venue.website_link = form.website_link.data
      venue.facebook_link = form.facebook_link.data
      venue.seeking_talent = form.seeking_talent.data
      venue.seeking_description = form.seeking_description.data
      venue.image_link = form.image_link.data
      db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  form = ArtistForm(request.form)
  try:
    if form.validate():
      new_artist = Artist(
        name = form.name.data,
        city = form.city.data,
        state = form.state.data,
        phone = form.phone.data,
        image_link = form.image_link.data,
        genres = ",".join(form.genres.data),
        facebook_link = form.facebook_link.data,
        website_link = form.website_link.data,
        seeking_venue = form.seeking_venue.data,
        seeking_description = form.seeking_description.data,
        
      )
      db.session.add(new_artist)
      db.session.commit()
      flash('Artist ' + request.form['name'] + 
            ' was successfully listed!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred. Artist ' + request.form['name'] 
          +' could not be listed.')
  finally:
    db.session.close()
    
    
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., 
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  shows = Show.query.all()
  data = []
  for show in shows:
    display_show = {
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "artist_id" : show.artist_id,
      "artist_name" : show.artist.name,
      "artist_image_link" : show.artist.image_link,
      "start_time" :str(show.start_time),
    }
    data.append(display_show)
 
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  # on successful db insert, flash success
  
  try:
    form = ShowForm(request.form)
    if form.validate():
      new_show = Show(
        artist_id = form.artist_id.data,
        venue_id = form.venue_id.data,
        start_time = form.start_time.data
      )
      db.session.add(new_show)
      db.session.commit()
      flash('Show was successfully listed!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred. Show could not be listed.')
  finally:
    db.session.close()
    
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

  
  

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
