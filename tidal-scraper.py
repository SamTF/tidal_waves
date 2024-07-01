### IMPORTS
from bs4 import BeautifulSoup
import requests
import lxml
from typing import List
import pickle

from data import Tide, Day

### CONSTANTS
wisuki = 'https://wisuki.com/tide/2450/sao-pedro-de-moel'

### FUNCTIONS
def scrape_data() -> List[Day]:
    '''
    Scrapes all tidal data for the entire month, and saves into Day objects.

    Returns:
        List of Day objects
    '''
    # getting the website source code
    source = requests.get(wisuki).text

    # creating html parser object
    soup = BeautifulSoup(source, 'lxml')

    # fetch main table containing all data
    main_table = soup.find('tbody')
    # fetch every table row (each row is a day) AND delete all empty rows that for reason exist???
    days = main_table.findAll('tr')
    days = [tag for tag in days if tag.get_text(strip=True)]

    # init list of days
    days_list = []

    # iterate through every day and extract info
    for day in days:
        rows = day.findAll('td')
        weekday_row = rows[0]
        weekday = ''
        date = ''

        # weekend rows begin with a strong tag
        is_weekend = rows[0].contents[1].name == 'strong'

        # extract weekday and date - weekend
        if is_weekend:
            strong = weekday_row.find('strong')
            weekday = strong.contents[-1].strip()
            date = strong.contents[-2].text.strip()
        # extract weekday and date - week day
        else:
            weekday = weekday_row.contents[-1].strip()
            date = weekday_row.contents[-2].text.strip()

        # extract tides and create Tide objects
        tides = []
        for i in range(1, 5):
            # break if content is empty
            if not (len(rows[i].contents) > 0):
                break

            # extract tide info
            tide, time, height, _ = [item.text.strip() for item in rows[i].contents[::2]]
            t = Tide(True if tide == '▲' else False, time, height)

            # add to list
            tides.append(t)

        # Create Day object with all the info extracted
        d = Day(date, weekday, tides)
        print(d)
        print('\n')

        days_list.append(d)
    
    # Save the data to disk
    with open('data.pkl', 'wb') as file:
        pickle.dump(days_list, file)

    # Return the data
    return days_list


### MAIN
if __name__ == '__main__':
    scrape_data()