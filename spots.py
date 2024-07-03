# Data on all the beach spots supported by the bot

class Spot:
    def __init__(self, name: str, lat: float, lng: float, id: int, url: str) -> None:
        self.name = name
        self.lat = lat
        self.lng = lng
        self.id = id
        self.url = url

    def __repr__(self) -> str:
        return self.name

SPOTS = [
    Spot(name='São Pedro de Moel',  lat=39.759, lng=-9.033, id=0, url='https://pt.wisuki.com/tide/2450/sao-pedro-de-moel'),
    Spot(name='Nazaré',             lat=39.601, lng=-9.071, id=1, url='https://pt.wisuki.com/tide/2434/nazare'),
    Spot(name='Peniche',            lat=39.356, lng=-9.378, id=2, url='https://pt.wisuki.com/tide/9075/peniche'),
    Spot(name='Ericeira',           lat=38.963, lng=-9.417, id=3, url='https://pt.wisuki.com/tide/5949/ericeira'),
    Spot(name='Cascais',            lat=38.696, lng=-9.420, id=4, url='https://pt.wisuki.com/tide/2455/cascais'),
    Spot(name='Comporta',           lat=38.380, lng=-8.786, id=5, url='https://pt.wisuki.com/tide/2427/comporta')
]
    