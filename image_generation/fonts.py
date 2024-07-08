from enum import Enum
from PIL import ImageFont

class FontStyle(Enum):
    '''
    Styles available for the font. Basically just the font weight and wether it's condensed or not.
    '''
    BOLD            = "fonts/MyriadPro-Bold.otf"
    CONDENSED       = "fonts/MyriadPro-Cond.otf"
    BOLD_CONDENSED  = "fonts/MyriadPro-BoldCond.otf"
    # BOLD_SMALL      = ImageFont.truetype('MyriadPro-Bold.otf',       36)

class FontSize(Enum):
    '''
    Represents the different sizes available for text, in pixels.
    '''
    XS          = 16
    SMALL       = 18
    MEDIUM_SM   = 40
    MEDIUM      = 50
    LARGE       = 64
    XL          = 90

class Font:
    '''
    Represents a single font to be used with PIL.
    '''
    def __init__(self, style: FontStyle, size: FontSize):
        self.style = style
        self.size = size
        self.font = ImageFont.truetype(self.style.value, self.size.value)