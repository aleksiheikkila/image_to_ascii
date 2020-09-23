# image_to_ascii
Turns an image to corresponding ascii text version.

Dependencies:
  * Tested on python 3.7.7
  * Pillow (PIL)
  * numpy
  * colorama

Command line arguments:
  * --img_file", "-f": source image filepath
  * --max_size", "-s": max dimension of the output, default (320, 240). Image will be scaled down if needed, retaining the aspect ratio.
  * "--brightness_method", "-m": Method used to calculate the pixel brightness (average, ligthness or luminosity). Will change a little bit how the output looks
  * "--output_file", "-o": Filepath, where to write the string
  * "--background_color", "-b": Background color (either black / white. Others not directly supported). The background on which the ascii text will appear
  * --num_chars_per_pixel", "-n": How many times to repeat each character in the horizontal dimension (due to character maps being tall rectangles vs. square pixels). Default: 2
  * "--invert_brightness", "-i": Flag to invert brightness (so that dark pixel become bright and vice versa)
  * "--write_to_console", "-w": USe this flag if you want to output to (also) console (the other option being the output file)
  * --text_color", "-c": Text color string (red|blue|green) for console output.
  
  Usage example:
  python ./img_to_ascii.py -f C:/TEMP/test_image.jpg --brightness_method luminosity -s 150 300 -o C:/TEMP/img_as_ascii.txt -w -c green
