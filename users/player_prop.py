from sqlalchemy import Column, DateTime, Float, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base= declarative_base()

class PlayerProp(Base):
    __tablename__ = 'player_props'

    id = Column(Integer, primary_key=True, index=True)
    time = Column(DateTime, nullable=False )
    team = Column(String, nullable=False)
    player = Column(String, nullable=False)
    position = Column(String, nullable=False)
    prop = Column(String, nullable=False)
    h2h = Column(String)  # Assuming Head-to-Head data as a string; adjust type as needed
    l10_avg = Column(Float)  # Last 10 games average; using Float for decimal values
    l5_avg = Column(Float)   # Last 5 games average; using Float for decimal values

    def __init__(self, time, team, player, position, prop, h2h=None, l10_avg=None, l5_avg=None):
        self.time = time
        self.team = team
        self.player = player
        self.position = position
        self.prop = prop
        self.h2h = h2h
        self.l10_avg = l10_avg
        self.l5_avg = l5_avg