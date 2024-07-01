# this file contains the data classes used in this project

# IMPORTS
from typing import List
from datetime import datetime
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
        self.datetime = timezone.localize(datetime.strptime(date, "%d/%m/%Y"))
    
    def __repr__(self) -> str:
        tides = "\n".join([str(tide) for tide in self.tides])

        return f"{self.date} {self.weekday}\n------------------------\n{tides}"
