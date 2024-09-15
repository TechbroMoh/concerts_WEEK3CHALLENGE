from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

Base = declarative_base()

class Band(Base):
    __tablename__ = 'bands'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)  
    hometown = Column(String)

    concerts = relationship('Concert', back_populates='band', cascade='all, delete-orphan')

    def get_concerts(self):
        return self.concerts

    def get_venues(self):
        return [concert.venue for concert in self.concerts]

    @classmethod
    def most_performances(cls, session):
        bands = session.query(cls).all()
        if not bands:
            return None
        return max(bands, key=lambda band: len(band.concerts))

    def play_in_venue(self, venue, date):
        return Concert(band=self, venue=venue, date=date)

    def all_introductions(self):
        return [concert.introduction() for concert in self.concerts]

class Venue(Base):
    __tablename__ = 'venues'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    city = Column(String)

    concerts = relationship('Concert', back_populates='venue', cascade='all, delete-orphan')

    def get_concerts(self):
        return self.concerts

    def get_bands(self):
        return [concert.band for concert in self.concerts]

    def concert_on(self, date):
        for concert in self.concerts:
            if concert.date == date:
                return concert
        return None

    def most_frequent_band(self):
        band_count = {}
        for concert in self.concerts:
            band_count[concert.band] = band_count.get(concert.band, 0) + 1
        if not band_count:
            return None
        return max(band_count, key=band_count.get)

class Concert(Base):
    __tablename__ = 'concerts'

    id = Column(Integer, primary_key=True)
    date = Column(String)
    band_id = Column(Integer, ForeignKey('bands.id'))
    venue_id = Column(Integer, ForeignKey('venues.id'))

    band = relationship('Band', back_populates='concerts')
    venue = relationship('Venue', back_populates='concerts')

    def get_band(self):
        return self.band

    def get_venue(self):
        return self.venue

    def hometown_show(self):
        return self.venue.city == self.band.hometown

    def introduction(self):
        return f"Hello {self.venue.city}!!!!! We are {self.band.name} and we're from {self.band.hometown}"

# Setup for testing
engine = create_engine('sqlite:///concerts.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
