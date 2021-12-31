# Generate an ascii representation from a given image

Turns an image to a corresponding ascii text version.

The basic approach is to map pixel values to ascii character(s). Different characters have different level of lightness/darkness based on how the character rectangle is divided into actual character and the background, which are typically of opposite color (e.g. black characters on white background). For example, character "." has a lot of background and character "$" has a lot of character itself. When looked from a distance, exact characters are no longer that much distinguishable, and the image is formed by just the lightness/darkness levels.


### Dependencies:

Tested on python 3.7.7 with the following package versions:
  * colorama==0.4.1
  * numpy==1.16.5
  * Pillow==6.2.0

### Command line arguments:

  * **--img_file", "-f"**: 
  
    source image filepath

  * **--max_size", "-s"**: 
  
    First, the input image will be scaled down (thumbnailed) to this size if needed, retaining the aspect ratio. Default (320, 240).

  * **"--brightness_method", "-m"**: 
  
    Method used to calculate the pixel brightness (options: average|lightness|luminosity). Will change a little bit how the output looks.

  * **"--output_file", "-o"**: 
  
    Filepath, where to write the generated text file.

  * **"--background_color", "-b"**: 
  
    NOT CURRENTLY IMPLEMENTED.

    Background color (either black|white. Others not directly supported). The background on which the ascii text will appear on the console.

  * **--num_chars_per_pixel"**, "-n": 
  
    How many times to repeat each character in the horizontal dimension (to retain the aspect ratio, repeat is often necessary due to character maps being tall rectangles instead of square pixels). Default: 2

  * **"--invert_brightness"**, "-i": 
  
    Flag to invert brightness (so that dark pixel become bright and vice versa)

  * **"--write_to_console"**, "-w": 
  
    Use this flag if you want to output to (also) console (the other option being the output txt file)

  * **--text_color", "-c"**: 
  
    Text color string (red|blue|green) for console output.

  
  ### Usage example:

  Convert test_image.jpg (not provided) into test_image_as_ascii.txt

    python ./img_to_ascii.py -f test_image.jpg --brightness_method luminosity -s 150 300 -o test_image_as_ascii.txt -w -c green

Inspect the generated txt file. Make sure to use an editor where you can zoom out to see the whole file at once (e.g. notepad++)