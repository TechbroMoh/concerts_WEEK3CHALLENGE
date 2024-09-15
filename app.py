from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Band, Venue, Concert
import sqlalchemy

def create_test_data(session):
    bands = {
        "Sautisol": "Nairobi",
        "Davido": "Lagos",
        "Psquare": "Nigeria"
    }
    
    venues = {
        "Feel My Love": "New York",
        "Square Arena": "New York"
    }

    concerts = [
        {"date": "2024-12-31", "band_name": "Sautisol", "venue_title": "Feel My Love"},
        {"date": "2025-02-10", "band_name": "Davido", "venue_title": "Square Arena"},
        {"date": "2025-01-15", "band_name": "Psquare", "venue_title": "Feel My Love"}
    ]

    for band_name, hometown in bands.items():
        band = session.query(Band).filter_by(name=band_name).first()
        if not band:
            band = Band(name=band_name, hometown=hometown)
            session.add(band)
        else:
            band.hometown = hometown  

    for venue_title, city in venues.items():
        venue = session.query(Venue).filter_by(title=venue_title).first()
        if not venue:
            venue = Venue(title=venue_title, city=city)
            session.add(venue)
        else:
            venue.city = city  

    for concert in concerts:
        band = session.query(Band).filter_by(name=concert["band_name"]).first()
        venue = session.query(Venue).filter_by(title=concert["venue_title"]).first()
        if band and venue:
            concert_instance = Concert(date=concert["date"], band=band, venue=venue)
            session.add(concert_instance)
    
    session.commit()

def test_methods(session):
    try:
        band = session.query(Band).filter_by(name="Sautisol").first()
        if band:
            print(f"Band found: {band}")
            venues = band.get_venues()
            print(f"Venues for {band.name}: {venues}")
        
        venue = session.query(Venue).filter_by(title="Feel My Love").first()
        if venue:
            print(f"Venue found: {venue}")
            bands_at_venue = venue.get_bands()
            print(f"Bands at {venue.title}: {bands_at_venue}")
        
        band = session.query(Band).filter_by(name="Sautisol").first()
        if band:
            introductions = band.all_introductions()
            print(f"Introductions for {band.name}: {introductions}")

    except sqlalchemy.exc.NoResultFound:
        print("No result found for the query.")
    except sqlalchemy.exc.MultipleResultsFound:
        print("Multiple results found for the query.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    engine = create_engine('sqlite:///concerts.db') 
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    print("Creating test data...")
    create_test_data(session)

    print("Testing methods...")
    test_methods(session)

if __name__ == "__main__":
    main()
