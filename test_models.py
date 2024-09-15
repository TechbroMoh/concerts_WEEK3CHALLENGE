import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Band, Venue, Concert

@pytest.fixture(scope='module')
def test_session():
    engine = create_engine('sqlite:///test_concerts.db')

    
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()


    band1 = Band(name='Sautisol', hometown='Nairobi')
    band2 = Band(name='Davido', hometown='Lagos')
    band3 = Band(name='Psquare', hometown='Nigeria')
    
    venue1 = Venue(title='Feel My Love', city='New York')
    venue2 = Venue(title='Square Arena', city='New York')

    concert1 = Concert(date='2024-12-31', band=band1, venue=venue1)
    concert2 = Concert(date='2025-02-10', band=band3, venue=venue2)
    
    session.add_all([band1, band2, band3, venue1, venue2, concert1, concert2])
    session.commit()

    yield session

    session.close()
    engine.dispose()

def test_band_concerts(test_session):
    band = test_session.query(Band).filter_by(name='Sautisol').one()
    assert len(band.get_concerts()) == 1

def test_band_venues(test_session):
    band = test_session.query(Band).filter_by(name='Sautisol').one()
    venues = band.get_venues()
    assert len(venues) == 1
    assert venues[0].title == 'Feel My Love'

def test_venue_concerts(test_session):
    venue = test_session.query(Venue).filter_by(title='Square Arena').one()
    concerts = venue.get_concerts()
    assert len(concerts) == 1

def test_venue_bands(test_session):
    venue = test_session.query(Venue).filter_by(title='Square Arena').one()
    bands = venue.get_bands()
    assert len(bands) == 1
    assert bands[0].name == 'Psquare'

def test_concert_hometown_show(test_session):
    concert = test_session.query(Concert).filter_by(date='2025-02-10').one()
    assert not concert.hometown_show()

def test_concert_introduction(test_session):
    concert = test_session.query(Concert).filter_by(date='2025-02-10').one()
    assert concert.introduction() == 'Hello New York!!!!! We are Psquare and we\'re from Nigeria'

def test_band_all_introductions(test_session):
    band = test_session.query(Band).filter_by(name='Psquare').one()
    introductions = band.all_introductions()
    assert len(introductions) == 1
    assert introductions[0] == 'Hello New York!!!!! We are Psquare and we\'re from Nigeria'

def test_band_most_performances(test_session):
    band = Band.most_performances(test_session)
    assert band.name == 'Sautisol'

def test_venue_concert_on(test_session):
    venue = test_session.query(Venue).filter_by(title='Square Arena').one()
    concert = venue.concert_on('2025-02-10')
    assert concert is not None
    assert concert.band.name == 'Psquare'

def test_venue_most_frequent_band(test_session):
    venue = test_session.query(Venue).filter_by(title='Square Arena').one()
    band = venue.most_frequent_band()
    assert band.name == 'Psquare'
