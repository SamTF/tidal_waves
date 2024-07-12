### IMPORTS
from enum import Enum
from typing import Tuple
from image_generation.fonts import Font

# Enum for text anchor pivot
class TextAnchor(Enum):
    LEFT   = 'lm'
    CENTER = 'mm'
    RIGHT  = 'rm'

### TEXT FORMATTING CLASS ###
class Text:
    def __init__(self, text: str, position: Tuple[int, int], font: Font, colour: Tuple[int, int, int] | str = (0,0,0), anchor: TextAnchor = TextAnchor.LEFT) -> None:
        self.text       = text
        self.position   = position
        self.font       = font.font
        self.colour     = colour
        self.anchor     = anchor.value    # https://pillow.readthedocs.io/en/stable/handbook/text-anchors.html