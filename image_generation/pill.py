### Generates images displaying the tidal information

### IMPORTS
from PIL import Image, ImageDraw, ImageFont     # Importing PIL to generate and manipulate  images
from PIL import ImageColor                      # To convert #Hex colour to R,G,B

# Font and Text helper class
from fonts import Font, FontStyle, FontSize
from text import TextAnchor, Text

# Date and time
from datetime import datetime, timedelta

### CONSTANTS for creating the image canvas and formatting other elements
CANVAS_SIZE = (842, 596)
BG_COLOUR   = (255, 255, 255)
MODE        = 'RGB'

### Image templates and assets file paths
TEMPLATE = 'templates/template.png'
TIME_MARKER = 'templates/time_marker.png'
HI_TIDE_MARKER = 'templates/hi_tide_marker.png'
LO_TIDE_MARKER = 'templates/lo_tide_marker.png'
TIDE_GRAPH = 'templates/tide_graph.png'

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

# test constants
high_tide = { 'time' : '17:35', 'height' : '3.5' }
low_tide = { 'time' : '11:08', 'height' : '0.9' }


def create_image() -> Image:
    # CREATING CANVAS
    # canvas = Image.new(MODE, CANVAS_SIZE, BG_COLOUR)

    # Load the starting canvas from disk (for now)
    canvas = Image.open(TEMPLATE).copy()

    # Enable editing the image
    draw = ImageDraw.Draw(canvas)

    # Create Text objects
    spot = Text(
        'São Pedro de Moel',
        (30, 127),
        Font(FontStyle.BOLD_CONDENSED, FontSize.LARGE),
        "#FDC017",
        TextAnchor.LEFT
    )
    weekday = Text(
        'TODAY | July 8',
        (30, 59),
        Font(FontStyle.CONDENSED, FontSize.MEDIUM),
        "#FDC017",
        TextAnchor.LEFT
    )
    temperature = Text(
        '22º',
        (810, 120),
        Font(FontStyle.BOLD, FontSize.XL),
        "#FDC017",
        TextAnchor.RIGHT
    )

    # Add Text objects to list
    texts = [spot, weekday, temperature]

    # Add text to the canvas
    for t in texts:
        draw.text(t.position, t.text, fill=t.colour, font=t.font, anchor=t.anchor)
    
    # Adding tide graph
    x = tide_graph_x_position(11, 8)
    canvas.paste(TIDE_GRAPH_IMG, (x, 442), mask=TIDE_GRAPH_IMG)
    
    # Adding day progress marker
    time_marker = TIME_MARKER_IMG.copy()
    canvas.paste(time_marker, (get_progress_position(), TIME_MARKER_POS_Y), mask=time_marker)

    # Adding tide markers
    hi_tide_marker = HI_TIDE_MARKER_IMG.copy()
    canvas.paste(hi_tide_marker, (get_progress_position(datetime.strptime(high_tide['time'], "%H:%M").time()), TIDE_MARKER_POS_Y), mask=hi_tide_marker)

    lo_tide_marker = LO_TIDE_MARKER_IMG.copy()
    canvas.paste(lo_tide_marker, (get_progress_position(datetime.strptime(low_tide['time'], "%H:%M").time()), TIDE_MARKER_POS_Y), mask=lo_tide_marker)

    # Adding tide information
    hi_tide_height = Text(
        high_tide['height'],
        (get_progress_position(datetime.strptime(high_tide['time'], "%H:%M").time()) + 14, 444),
        Font(FontStyle.BOLD_CONDENSED, FontSize.XS),
        HI_TIDE_COLOUR,
        TextAnchor.CENTER   
    )

    lo_tide_height = Text(
        low_tide['height'],
        (get_progress_position(datetime.strptime(low_tide['time'], "%H:%M").time()) + 14, 520),
        Font(FontStyle.BOLD_CONDENSED, FontSize.XS),
        LO_TIDE_COLOUR,
        TextAnchor.CENTER
    )

    # Add Text objects to list
    tides = [hi_tide_height, lo_tide_height]

    # Add text to the canvas
    for t in tides:
        draw.text(t.position, t.text, fill=t.colour, font=t.font, anchor=t.anchor)
    
    # DEBUGGING
    canvas.save("test.png", "PNG", quality=100)
    print(canvas)



def get_progress_position(time: datetime.time = None) -> int:
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
    create_image()
    # x = calculate_x_position(12, 00)
    # print(x)