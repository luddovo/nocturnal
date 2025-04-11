# Nocturnal - A Nighttime Sundial

Nocturnal is an instrument for measuring time at night. You can think of it as a nighttime sundial.
Time is measured from rotation of circumpolar stars around Polaris.

## Description

This project generates an SVG file that represents the components of the Nocturnal time-measuring device. The generated SVG can be easily converted to other formats, such as PDF.

## Usage

### Command-Line Arguments

- `-l` or `--lang`: Specifies the language code. The default is `en` (English).
- `-o` or `--output`: Specifies the filename to save the generated SVG file. The default is `nocturnal.svg`.

### Example Commands

To generate the SVG file with the default settings:

`python nocturnal.py

### PDF to print

You can convert the SVG to a PDF using Inkscape:

`inkscape nocturnal.svg --export-filename=nocturnal.svg.pdf
