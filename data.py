# this file contains the data classes used in this project

# IMPORTS
from typing import List, Tuple
from datetime import datetime, time
import pytz

# Timezone
timezone = pytz.timezone('Europe/Lisbon')

# TIDE
class Tide:
    """
    Represents an ocean tide in a day.
    """

    def __init__(self, tide: bool, time: str, height: str) -> None:
        '''
        Constructor method for the Tide class.

        Parameters:
        - tide: bool
            whether the tide is high or low

        - time: str
            the time of the tide

        - height: str
            the height of the tide

        '''
        self.tide = tide
        self.time = time
        self.height = height
    
    @property
    def datetime(self) -> time:
        return datetime.strptime(self.time, "%H:%M").time()
    
    def __repr__(self) -> str:
        '''
        Prints out tide information in the format "▲▼ / HH:MM / height"

        ex: ▲ / 12:42 / 3m)
        '''
        return f"{'▲' if self.tide == True else '▼'} / {self.time} / {self.height}"
    
# DAY
class Day:
    '''
    Represents a day of ocean tides.

    Attributes:
    - date: str
        the date

    - weekday: str
        the day of the week

    - tides: List[Tide]
        the tides in the day
    '''
    def __init__(self, date: str, weekday: str, tides: List[Tide]) -> None:
        self.date = date
        self.weekday = weekday
        self.tides = tides
        self.datetime = timezone.localize(datetime.strptime(date, "%d/%m/%Y")).date()
    
    def __repr__(self) -> str:
        tides = "\n".join([str(tide) for tide in self.tides])

        return f"{self.date} {self.weekday}\n------------------------\n{tides}"
    
    def daytime_tides(self) -> Tuple[Tide]:
        '''
        Returns the tides in the day that are in the daytime as a tuple of Tide objects.
        '''
        start_time = time(9,0)
        end_time = time(21,0)
        tides = []

        for t in self.tides:
            tide_time = datetime.strptime(t.time, "%H:%M").time()

            if start_time <= tide_time <= end_time:
                tides.append(t)
        
        high_tide = next((t for t in tides if t.tide), None)
        low_tide = next((t for t in tides if not t.tide), None)

        return (high_tide, low_tide)
