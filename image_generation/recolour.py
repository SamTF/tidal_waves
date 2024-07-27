# recolouring an image using numpy
### Re-colouring an image using PIL and NumPy
# from : https://stackoverflow.com/questions/3752476/python-pil-replace-a-single-rgba-color

from PIL import Image
import numpy as np

# re-colour SVG: https://stackoverflow.com/questions/61824128/python-change-color-in-svg-and-export-to-svg-png-pdf



def recolour(image:Image, old_colour:tuple, new_colour:tuple) -> Image:
    '''
    Re-colours an image by replacing all occurrences of a specified RGB colour with a new RGB colour.

    Args:
    - image (PIL.Image): The image to be re-coloured.
    - old_colour (tuple): A tuple of (R, G, B) integers representing the RGB colour to be replaced.
    - new_colour (tuple): A tuple of (R, G, B) integers representing the new RGB colour.

    Returns:
    - PIL.Image: The re-coloured image.
    '''
    data = np.array(image)                                                                              # "data" is a height x width 4-dimensional numpy array
    r, g, b, a = data.T                                                                                 # temporarily unpack the colour channels for readability

    replace = (r == old_colour[0]) & (g == old_colour[1]) & (b == old_colour[2])                        # replace current colour with desired colour, leaving alpha values alone
    data[..., :-1][replace.T] = new_colour                                                              # replacing the values that match the current colour with the new desired colour

    image_coloured = Image.fromarray(data)                                                              # converts the numpy array back into image format

    return image_coloured
