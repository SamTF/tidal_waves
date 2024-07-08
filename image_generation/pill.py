### Generates images displaying the tidal information

### IMPORTS
from PIL import Image, ImageDraw, ImageFont     # Importing PIL to generate and manipulate  images
from PIL import ImageColor                      # To convert #Hex colour to R,G,B

# Font and Text helper class
from fonts import Font, FontStyle, FontSize
from text import TextAnchor, Text

# Date and time
from datetime import datetime

### CONSTANTS for creating the image canvas and formatting other elements
CANVAS_SIZE = (842, 596)
BG_COLOUR   = (255, 255, 255)
MODE        = 'RGB'

### Image templates and assets file paths
TEMPLATE = 'templates/blueprint.png'
TIME_MARKER = 'templates/time_marker.png'
HI_TIDE_MARKER = 'templates/hi_tide_marker.png'
LO_TIDE_MARKER = 'templates/lo_tide_marker.png'

### Open template and asset images
TEMPLATE_IMG = Image.open(TEMPLATE)
TIME_MARKER_IMG = Image.open(TIME_MARKER).convert('RGBA')
HI_TIDE_MARKER_IMG = Image.open(HI_TIDE_MARKER).convert('RGBA')
LO_TIDE_MARKER_IMG = Image.open(LO_TIDE_MARKER).convert('RGBA')

### Constant positions
TIME_MARKER_POS_Y = 490
MARKER_MAX_X = 800
MARKER_MIN_X = 17


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
        'TODAY | July 5',
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
    
    # Adding day progress marker
    x = 1
    time_marker = TIME_MARKER_IMG.copy()
    canvas.paste(time_marker, (get_progress_position(), TIME_MARKER_POS_Y), mask=time_marker)
    
    # DEBUGGING
    canvas.show()
    canvas.save("test.png", "PNG", quality=100)
    print(canvas)



def get_progress_position():
    now = (datetime.now().time())                                                       # Get current time
    minutes_passed = (now.hour - 9) * 60 + now.minute                                   # Calculate the minutes passed since 9 AM
    percentage = (minutes_passed / (12 * 60))                                           # Calculate the percentage of time passed between 9 AM and 9 PM
    position = int(MARKER_MIN_X + (MARKER_MAX_X - MARKER_MIN_X) * percentage)           # Calculate position between X = 17 and X = 800

    print(f"The current time is {now}. The percentage of time passed between 9 AM and 9 PM is {percentage}%.")
    print(f'Marker position: X {position}')

    return position


# Debugging
if __name__ == "__main__":
    create_image()