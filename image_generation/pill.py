### Generates images displaying the tidal information

### IMPORTS
# File system
import os

from PIL import Image, ImageDraw, ImageFont     # Importing PIL to generate and manipulate  images
from PIL import ImageColor                      # To convert #Hex colour to R,G,B

# Font and Text helper class
from image_generation.fonts import Font, FontStyle, FontSize
from image_generation.text import TextAnchor, Text

# Date and time
from datetime import datetime, time

# Typing
from typing import Dict, Union

### CONSTANTS for creating the image canvas and formatting other elements
CANVAS_SIZE = (842, 596)
BG_COLOUR   = (255, 255, 255)
MODE        = 'RGB'

### Image templates and assets file paths
TEMPLATE        = os.path.join(os.path.dirname(__file__), 'templates/template.png')
TIME_MARKER     = os.path.join(os.path.dirname(__file__), 'templates/time_marker.png')
HI_TIDE_MARKER  = os.path.join(os.path.dirname(__file__), 'templates/hi_tide_marker.png')
LO_TIDE_MARKER  = os.path.join(os.path.dirname(__file__), 'templates/lo_tide_marker.png')
TIDE_GRAPH      = os.path.join(os.path.dirname(__file__), 'templates/tide_graph.png')

### Open template and asset images
TEMPLATE_IMG = Image.open(TEMPLATE)
TIME_MARKER_IMG = Image.open(TIME_MARKER).convert('RGBA')
HI_TIDE_MARKER_IMG = Image.open(HI_TIDE_MARKER).convert('RGBA')
LO_TIDE_MARKER_IMG = Image.open(LO_TIDE_MARKER).convert('RGBA')
TIDE_GRAPH_IMG = Image.open(TIDE_GRAPH).convert('RGBA')

### Constant positions
TIME_MARKER_POS_Y = 490
TIDE_MARKER_POS_Y = 428
MARKER_MAX_X = 800
MARKER_MIN_X = 17
TIDE_GRAPH__POS_Y = 442

### Colours
HI_TIDE_COLOUR = '#D82E2A'
LO_TIDE_COLOUR = '#A1CC39'

### MAIN FUNCTION
def create_image(date: str, spot_name: str, temperature: int, high_tide: Dict[str, Union[time, str]], low_tide:  Dict[str, Union[time, str]], today: bool = False) -> Image:
    print('###' * 5)
    print(f'[pill.py] >>> Creating image for {spot_name} on {date}')
    print(f'High Tide: {high_tide}')
    print(f'Low Tide: {low_tide}')
    # CREATING CANVAS
    # canvas = Image.new(MODE, CANVAS_SIZE, BG_COLOUR)

    # Load the starting canvas from disk
    canvas = Image.open(TEMPLATE).copy()

    # Enable editing the image
    draw = ImageDraw.Draw(canvas)

    # Create Header Text objects
    spot = Text(
        spot_name,
        (30, 127),
        Font(FontStyle.BOLD_CONDENSED, FontSize.LARGE),
        "#FDC017",
        TextAnchor.LEFT
    )
    weekday = Text(
        date,
        (30, 59),
        Font(FontStyle.CONDENSED, FontSize.MEDIUM),
        "#FDC017",
        TextAnchor.LEFT
    )
    temp = Text(
        f'{temperature}º',
        (810, 120),
        Font(FontStyle.BOLD, FontSize.XL),
        "#FDC017",
        TextAnchor.RIGHT
    )

    # Add text to the canvas
    texts = [spot, weekday, temp]
    for t in texts:
        draw.text(t.position, t.text, fill=t.colour, font=t.font, anchor=t.anchor)
    
    # Adding the tide graph
    x = tide_graph_x_position(11, 8)
    canvas.paste(TIDE_GRAPH_IMG, (x, 442), mask=TIDE_GRAPH_IMG)
    
    # Adding day progress marker ONLY IF INFORMATION IS FOR TODAY
    if today:
        time_marker = TIME_MARKER_IMG.copy()
        canvas.paste(time_marker, ( get_progress_position(), TIME_MARKER_POS_Y ), mask=time_marker)

    # Adding tide markers
    hi_tide_marker = HI_TIDE_MARKER_IMG.copy()
    canvas.paste(
        hi_tide_marker,
        ( get_progress_position(high_tide['time']), TIDE_MARKER_POS_Y ),
        mask=hi_tide_marker
    )

    lo_tide_marker = LO_TIDE_MARKER_IMG.copy()
    canvas.paste(
        lo_tide_marker,
        ( get_progress_position(low_tide['time']), TIDE_MARKER_POS_Y ),
        mask=lo_tide_marker
    )

    # Adding tide information
    hi_tide_height = Text(
        high_tide['height'],
        (get_progress_position(high_tide['time']) + 14, 444),
        Font(FontStyle.BOLD_CONDENSED, FontSize.XS),
        HI_TIDE_COLOUR,
        TextAnchor.CENTER   
    )

    lo_tide_height = Text(
        low_tide['height'],
        (get_progress_position(low_tide['time']) + 14, 520),
        Font(FontStyle.BOLD_CONDENSED, FontSize.XS),
        LO_TIDE_COLOUR,
        TextAnchor.CENTER
    )

    # Add Text objects to list
    tides = [hi_tide_height, lo_tide_height]

    # Add text to the canvas
    for t in tides:
        draw.text(t.position, t.text, fill=t.colour, font=t.font, anchor=t.anchor)
    
    # Add tide times
    for t in [high_tide, low_tide]:
        # text_img = draw_tide_time(t['time'].strftime("%H:%M"))
        text_img = draw_tide_time(t['time'].strftime("%I:%M"))

        canvas.paste(text_img, (get_progress_position(t['time']) - 2, 448), mask=text_img)

    
    # DEBUGGING
    canvas.save("test.png", "PNG", quality=100)
    print(canvas)

    return canvas


def draw_tide_time(time: str) -> Image:
    '''
    Draws a text image rotated 90 degrees for the given time.

    Parameters:
    - time: str
        The time to draw in the format "HH:MM"

    Returns:
    - Image
        The image of the text
    '''
    # Create a new image for the rotated text
    f = Font(FontStyle.BOLD_CONDENSED, FontSize.XS)
    t = time

    # Create temp image
    rotated_text = Image.new('RGBA', (50, 50))
    rotated_draw = ImageDraw.Draw(rotated_text)

    # draw text and rotate the temp image
    rotated_draw.text((0, 0), t, fill='white', font=f.font)
    rotated_text = rotated_text.rotate(90, expand=True)

    # return the rotated text image
    return rotated_text


def get_progress_position(time: datetime.time = None) -> int:
    '''
    This calculates the X-position of the time and tide markers, so that it lines up perfectly with the day's progress.

    Parameters:
        time (datetime.time): The current time
    
    Returns:
        int: The X-position of the marker image to the nearest integer
    '''

    # Get current time if no time is given
    if not time:
        time = (datetime.now().time())

    minutes_passed = (time.hour - 9) * 60 + time.minute                                 # Calculate the minutes passed since 9 AM
    percentage = (minutes_passed / (12 * 60))                                           # Calculate the percentage of time passed between 9 AM and 9 PM
    position = int(MARKER_MIN_X + (MARKER_MAX_X - MARKER_MIN_X) * percentage)           # Calculate position between X = 17 and X = 800

    return position


def tide_graph_x_position(first_low_tide_hour: int, first_low_tide_minute: int) -> int:
    '''
    This calculates the X-position of the tide_graph.png overlay, so that it lines up perfectly with the day's tides.

    Parameters:
        first_low_tide_hour (int): The hour of the first low tide
        first_low_tide_minute (int): The minute of the first low tide
    
    Returns:
        int: The X-position of the tide_graph.png overlay to the nearest integer
    '''
    # Constants
    MAX_X = 30
    MIN_X = -778
    RANGE_X = MAX_X - MIN_X
    RATE_PER_HOUR = 66.5833
    HOURS_PER_DAY = 24
    REFERENCE_TIME = 3 # 3am as reference point

    # Convert time to hours since 3am
    time_in_hours = first_low_tide_hour + first_low_tide_minute / 60
    hours_passed = (time_in_hours - REFERENCE_TIME) % HOURS_PER_DAY
    
    # Calculate the change in X
    x_change = hours_passed * RATE_PER_HOUR
    
    # Calculate the new X position
    new_x = -769 + x_change  # Start from the X value at 3am
    
    # Adjust for wrapping around
    while new_x > MAX_X:
        new_x -= RANGE_X
    
    print(new_x)
    # return round(new_x, 2)
    return int(round(new_x, 0))

# Debugging
if __name__ == "__main__":
    create_image(
        'TODAY | July 8',
        'São Pedro de Moel',
        22,
        { 'time' : datetime.strptime('17:35', "%H:%M").time(), 'height' : '3.5' },
        { 'time' : datetime.strptime('11:08', "%H:%M").time(), 'height' : '0.9' },
        True
    )
    # x = tide_graph_x_position(12, 00)
    # print(x)