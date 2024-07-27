### Generates images displaying the tidal information

### IMPORTS
# File system
import os
from io import BytesIO                          # Used to store the output images in memory instead of saving them to disk

# Pillow
from PIL import Image, ImageDraw, ImageFont     # Importing PIL to generate and manipulate  images
from PIL import ImageColor                      # To convert #Hex colour to R,G,B

# Font and Text helper class
from image_generation.fonts import Font, FontStyle, FontSize
from image_generation.text import TextAnchor, Text
from image_generation import recolour

# Date and time
from datetime import datetime, time

# Weather codes
from weather import weather_codes

# Typing
from typing import Dict, Union

### CONSTANTS for creating the image canvas and formatting other elements
CANVAS_SIZE = (842, 596)
BG_COLOUR   = (255, 255, 255)
MODE        = 'RGB'

### Image templates and assets file paths
TEMPLATE            = os.path.join(os.path.dirname(__file__), 'templates/template.png')
TEMPLATE_COMPACT    = os.path.join(os.path.dirname(__file__), 'templates/template_compact.png')
TIME_MARKER         = os.path.join(os.path.dirname(__file__), 'templates/time_marker.png')
HI_TIDE_MARKER      = os.path.join(os.path.dirname(__file__), 'templates/hi_tide_marker.png')
LO_TIDE_MARKER      = os.path.join(os.path.dirname(__file__), 'templates/lo_tide_marker.png')
TIDE_GRAPH          = os.path.join(os.path.dirname(__file__), 'templates/tide_graph.png')
ICONS_DIR           = os.path.join(os.path.dirname(__file__), 'icons/')

### Open template and asset images
TEMPLATE_IMG = Image.open(TEMPLATE)
TEMPLATE_COMPACT_IMG = Image.open(TEMPLATE_COMPACT)
TIME_MARKER_IMG = Image.open(TIME_MARKER).convert('RGBA')
HI_TIDE_MARKER_IMG = Image.open(HI_TIDE_MARKER).convert('RGBA')
LO_TIDE_MARKER_IMG = Image.open(LO_TIDE_MARKER).convert('RGBA')
TIDE_GRAPH_IMG = Image.open(TIDE_GRAPH).convert('RGBA')

### Constant positions - FULL
TIME_MARKER_POS_Y = 490
TIDE_MARKER_POS_Y = 428
MARKER_MAX_X = 800
MARKER_MIN_X = 17
TIDE_GRAPH__POS_Y = 442
HIGH_TIDE_INFO_POS_Y = 444
LOW_TIDE_INFO_POS_Y = 520
TIDE_TIME_POS_Y = 448

### Constant positions - COMPACT
TIME_MARKER_POS_Y_COMPACT = 239
TIDE_MARKER_POS_Y_COMPACT = 177
MARKER_MAX_X_COMPACT = 800
MARKER_MIN_X_COMPACT = 17
TIDE_GRAPH__POS_Y_COMPACT = 191
HIGH_TIDE_INFO_POS_Y_COMPACT = 193
LOW_TIDE_INFO_POS_Y_COMPACT = 269
TIDE_TIME_POS_Y_COMPACT = 200

### Colours
HI_TIDE_COLOUR = '#D82E2A'
LO_TIDE_COLOUR = '#A1CC39'

### MAIN FUNCTION
def create_image(date: str, spot_name: str, high_tide: Dict[str, Union[time, str]], low_tide:  Dict[str, Union[time, str]], temperature: int = 0, wwo_code: int = 0, today: bool = False, compact: bool = False) -> BytesIO:
    '''
    Creates an image with information about the tides at a beach on a specific date.

    Args:
        - date (str): The date for which the tides should be displayed.
        - spot_name (str): The name of the beach.
        - high_tide: A dictionary containing the time and height of the high tide.
        - low_tide: A dictionary containing the time and height of the low tide.
        - temperature (int): The air temperature at the beach.
        - wwo_code (int): The WWO code for the weather conditions.
        - today (bool, optional): Whether the information is for today. Defaults to False.
        - compact (bool, optional): Whether the image should be compact or full-sized. Defaults to False.

    Returns:
        - BytesIO: The generated image as a bytes object
    '''
    print(f'[pill.py] >>> Creating image for {spot_name} on {date}')
    # CREATING CANVAS
    # canvas = Image.new(MODE, CANVAS_SIZE, BG_COLOUR)

    # Load the starting canvas from disk - Full Size or Compact
    canvas = Image.open(TEMPLATE).copy() if not compact else Image.open(TEMPLATE_COMPACT).copy()

    # Init vars for element positions depending on size requested
    if not compact:
        time_marker_pos_y   =   TIME_MARKER_POS_Y
        tide_marker_pos_y   =   TIDE_MARKER_POS_Y
        tide_graph_pos_y    =   TIDE_GRAPH__POS_Y
        high_tide_pos_y     =   HIGH_TIDE_INFO_POS_Y
        low_tide_pos_y      =   LOW_TIDE_INFO_POS_Y
        tide_time_pos_y     =   TIDE_TIME_POS_Y
    else:
        time_marker_pos_y   =   TIME_MARKER_POS_Y_COMPACT
        tide_marker_pos_y   =   TIDE_MARKER_POS_Y_COMPACT
        tide_graph_pos_y    =   TIDE_GRAPH__POS_Y_COMPACT
        high_tide_pos_y     =   HIGH_TIDE_INFO_POS_Y_COMPACT
        low_tide_pos_y      =   LOW_TIDE_INFO_POS_Y_COMPACT
        tide_time_pos_y     =   TIDE_TIME_POS_Y_COMPACT

    # Enable editing the image
    draw = ImageDraw.Draw(canvas)

    # Getting accent colour
    accent = weather_codes.ACCENT_COLOUR[weather_codes.WWO_CODE[wwo_code]]
    accent_rgb = ImageColor.getcolor(accent, 'RGB') # converting it to RGB for the recolour script

    # Create Header Text objects
    spot = Text(
        spot_name,
        (30, 127),
        Font(FontStyle.BOLD_CONDENSED, FontSize.LARGE),
        accent,
        TextAnchor.LEFT
    )
    weekday = Text(
        date,
        (30, 59),
        Font(FontStyle.CONDENSED, FontSize.MEDIUM),
        accent,
        TextAnchor.LEFT
    )
    header_texts = [spot, weekday]
    
    if temperature:
        temp = Text(
            f'{temperature}º',
            (810, 120),
            Font(FontStyle.BOLD, FontSize.XL),
            accent,
            TextAnchor.RIGHT
        )
        header_texts.append(temp)

    # Add text to the canvas
    for t in header_texts:
        draw.text(t.position, t.text, fill=t.colour, font=t.font, anchor=t.anchor)
    
    # Adding the tide graph
    hour, minute = low_tide['time'].hour, low_tide['time'].minute
    tide_graph_x = tide_graph_x_position(hour, minute)
    canvas.paste(TIDE_GRAPH_IMG, (tide_graph_x, tide_graph_pos_y), mask=TIDE_GRAPH_IMG)
    
    # Adding day progress marker ONLY IF INFORMATION IS FOR TODAY
    if today:
        time_marker = TIME_MARKER_IMG.copy()
        canvas.paste(time_marker, ( get_progress_position(), time_marker_pos_y ), mask=time_marker)

    # Adding tide markers
    hi_tide_marker = HI_TIDE_MARKER_IMG.copy()
    canvas.paste(
        hi_tide_marker,
        ( get_progress_position(high_tide['time']), tide_marker_pos_y ),
        mask=hi_tide_marker
    )

    lo_tide_marker = LO_TIDE_MARKER_IMG.copy()
    canvas.paste(
        lo_tide_marker,
        ( get_progress_position(low_tide['time']), tide_marker_pos_y ),
        mask=lo_tide_marker
    )

    # Adding tide information
    hi_tide_height = Text(
        high_tide['height'],
        (get_progress_position(high_tide['time']) + 14, high_tide_pos_y),
        Font(FontStyle.BOLD_CONDENSED, FontSize.XS),
        HI_TIDE_COLOUR,
        TextAnchor.CENTER   
    )

    lo_tide_height = Text(
        low_tide['height'],
        (get_progress_position(low_tide['time']) + 14, low_tide_pos_y),
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

        canvas.paste(text_img, (get_progress_position(t['time']) - 2, tide_time_pos_y), mask=text_img)

    # Loading the corresponding weather condition icon
    icon_name =  weather_codes.WWO_CODE[wwo_code]
    icon_path = f'{ICONS_DIR}{icon_name}.png'
    icon = Image.open(icon_path)

    # formatting and pasting weather icon
    icon_coloured = recolour.recolour(icon, (250, 253, 255), accent_rgb)
    canvas.paste(icon_coloured, (610, 85), mask=icon_coloured)

    
    # DEBUGGING
    # canvas.save("test.png", "PNG", quality=100)
    # print(canvas)

    # Saving the created image to memory in BytesIO as a "file-like object" -> https://stackoverflow.com/questions/60006794/send-image-from-memory
    tide_card = BytesIO()
    canvas.save(tide_card, format='PNG')

    return tide_card


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