from PIL import Image
import numpy as np
import argparse
from colorama import init, Fore  # , Back, Style


MAX_SIZE = (320, 240)  # Thumbnail imgs to this max size
BACKGROUND = "black"   # background color for the ascii text

COLORNAME_TO_COLORAMA_FORE_MAP = {"red": Fore.RED, 
                                  "blue": Fore.BLUE, 
                                  "green": Fore.GREEN}  # could add some more

ASCIIS = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

def open_and_resize_img(img_path, max_size=MAX_SIZE):
    im = Image.open(img_path).convert("RGB")
    im.thumbnail(max_size)
    return im

def get_ascii_charmap(background_color="black"):
    if background_color == "black":
        return ASCIIS
    elif background_color == "white":
        # if background is instead white, "invert"
        return ASCIIS[::-1]

def rgb_to_brightness(pixel, method="average", invert_brightness=False):
    if method == "average":
        bri = sum(pixel) / 3.
    elif method == "lightness":
        bri =  (max(pixel) + min(pixel)) / 2.
    elif method == "luminosity":
        bri = 0.21*pixel[0] + 0.72*pixel[1] + 0.07*pixel[2]
    else:
        raise ValueError("Unknown method")
    
    if invert_brightness:  # we could instead just reverse the charset...
        bri = abs(bri - 255)

    return bri

def brightness_to_ascii(bri, ascii_charset=ASCIIS, min_bri=0., max_bri=255.):
    bri_range = max_bri - min_bri 
    bri_levels_per_char = bri_range / (len(ascii_charset) - 1)
    return ascii_charset[int(round(bri/bri_levels_per_char))]

def get_brightness_and_ascii(img_arr, method, num_chars_per_pixel, invert_brightness):
    """Returns 
        - brightness values in numpy array
        - list of strings (rows) with the brightness-based characters
    """
    brightness_arr = np.empty(shape=img_arr.shape[:2])
    ascii_list = []

    # vectorize this part?
    for row in range(brightness_arr.shape[0]):
        row_str = ""
        for col in range(brightness_arr.shape[1]):
            brightness_arr[row, col] = rgb_to_brightness(img_arr[row, col], 
                                                         method=method,
                                                         invert_brightness=invert_brightness)
            row_str += brightness_to_ascii(brightness_arr[row, col]) * num_chars_per_pixel
        ascii_list.append(row_str)

    return brightness_arr, ascii_list


def img_to_ascii_str(img_path, max_size, brightness_method, background_color,
                    num_chars_per_pixel, invert_brightness):
    im = open_and_resize_img(img_path, max_size=max_size)
    img_arr = np.array(im)
    ascii_charmap = get_ascii_charmap(background_color=background_color)

    brightness_arr, ascii_list = get_brightness_and_ascii(img_arr, 
                                                          brightness_method, 
                                                          num_chars_per_pixel,
                                                          invert_brightness)

    return "\n".join(ascii_list)


if __name__ == "__main__":
    # init colorama
    init()

    parser = argparse.ArgumentParser(description='Turn an image to ascii version.')
    
    # Add long and short argument
    parser.add_argument("--img_file", "-f", help="image path", required=True)
    parser.add_argument("--max_size", "-s", nargs=2, metavar=("width", "height"), 
                        help="max img size", default=MAX_SIZE, type=int)
    parser.add_argument("--brightness_method", "-m", 
                        help="Brightness method (average, ligthness or luminosity",
                        default="average")
    parser.add_argument("--output_file", "-o", 
                        help="Where to write the string")
    parser.add_argument("--background_color", "-b", 
                help="Background color (black / white",
                default="black")
    parser.add_argument("--num_chars_per_pixel", "-n", type=int,
            help="How many times to repeat each character",
            default=2)  # 2 seemed to look quite okay
    parser.add_argument("--invert_brightness", "-i", action="store_true",
            help="Invert brightness")
    parser.add_argument("--write_to_console", "-w", action="store_true",
            help="Write to console")
    parser.add_argument("--text_color", "-c", 
            help="Text color string (colorama) for console output")


    # Read arguments from the command line
    args = parser.parse_args()
    args.max_size = tuple(args.max_size)

    ascii_str = img_to_ascii_str(args.img_file, 
                                 args.max_size, 
                                 args.brightness_method,
                                 args.background_color,
                                 args.num_chars_per_pixel,
                                 args.invert_brightness)
    
    if args.write_to_console:
        if args.text_color is not None:
            colorama_fore_color = COLORNAME_TO_COLORAMA_FORE_MAP.get(args.text_color)
            if colorama_fore_color is not None:
                ascii_str = colorama_fore_color + ascii_str
        print(ascii_str)

    if args.output_file is not None:
        print("Writing result to file:", args.output_file)
        with open(args.output_file, "w") as ofile:
            ofile.write(ascii_str)
