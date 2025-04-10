import matplotlib.pyplot as plt
import numpy as np
import ephem
from astropy.coordinates import SkyCoord
from matplotlib.backends.backend_pdf import PdfPages
import argparse


# dimensions
OUTER_DISK_RADIUS = 4.5  # cm
MONTHS_TEXT_RADIUS = 4.05  # cm
MONTHS_DOTS_RADIUS = 4.35  # cm

LONGITUDE_TEXT_RADIUS = 3.7  # cm
LONGITUDE_DOTS_RADIUS = 3.5  # cm

INNER_DISK_RADIUS = 3.9  # cm
TIME_TEXT_RADIUS = 3.0  # cm
TIME_DOTS_RADIUS = 2.8  # cm

# Create the parser
parser = argparse.ArgumentParser(description="Generate the Nocturnal instrument in PDF format.")

# Add arguments with short and long forms
parser.add_argument('-l', '--lang', default='en', help='Language code (default: en)')
parser.add_argument('-o', '--output', default='nocturnal.pdf', help='Filename to save to (default: nocturnal.pdf)')

# Parse the arguments
args = parser.parse_args()
# set up the PDF file
pdf_filename = args.output
pdf = PdfPages(pdf_filename)

# DRAW OUTER DISK - MONTHS, LONGITUDES

# Define the figure and axis
fig, ax = plt.subplots()

# Draw a disk with diameter 9 cm (radius 4.5 cm)
circle = plt.Circle((0, 0), 4.5, color='black', fill=False)
ax.add_artist(circle)
# Mark the center of the disk with a cross
ax.plot(0, 0, '+', color='red', markersize=10, markeredgewidth=2)

# Add month abbreviations around the inside rim of the disk
months_en = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']
months_cz = ['LEDEN', 'ÚNOR', 'BŘEZEN', 'DUBEN', 'KVĚTEN', 'ČERVEN', 'ČERVENEC', 'SRPEN', 'ZÁŘÍ', 'ŘÍJEN', 'LISTOPAD', 'PROSINEC']
months = months_en if args.lang == 'en' else months_cz

radius = MONTHS_TEXT_RADIUS  # Slightly smaller than the disk radius
angles = np.linspace(0, -2 * np.pi, len(months), endpoint=False)

for month, angle in zip(months, angles):
    # Divide the two circles with perpendicular dashes into 12 segments
    for angle in angles:
        x_start = INNER_DISK_RADIUS * np.cos(angle)
        y_start = INNER_DISK_RADIUS * np.sin(angle)
        x_end = OUTER_DISK_RADIUS * np.cos(angle)
        y_end = OUTER_DISK_RADIUS * np.sin(angle)
        ax.plot([x_start, x_end], [y_start, y_end], color='black', linewidth=1)

    # Center month names in the segments
    for month, angle in zip(months, angles):
        offset_angle = angle - (np.pi / len(months))  # Offset by half the segment's width
        x = radius * np.cos(offset_angle)
        y = radius * np.sin(offset_angle)
        ax.text(x, y, month, ha='center', va='center', fontsize=12, fontweight='bold',
                rotation=np.degrees(offset_angle) - 90, rotation_mode='anchor')
    
    dot_radius = MONTHS_DOTS_RADIUS  # Slightly smaller than the disk radius
    for segment in angles:
        offset = np.pi / 6 /3
        for angle in [segment + offset, segment - offset]:
            x = dot_radius * np.cos(angle)
            y = dot_radius * np.sin(angle)
            ax.plot(x, y, 'o', color='black', markersize=3)

# Draw another disk just inside of the month names
inner_circle = plt.Circle((0, 0), INNER_DISK_RADIUS, color='black', fill=False)
ax.add_artist(inner_circle)

# Calculate the meridian passage of the star Dubhe on 2025/1/1
star = ephem.star('Dubhe')
observer = ephem.Observer()
observer.lat, observer.lon = '50', '0'  # Set observer's latitude and longitude
observer.date = ephem.Date('2025/1/1 00:00:00')  # Start with midnight on 1st January 2025
star.compute(observer)  # Compute the star's position for the observer

# Find the time of the next meridian passage
meridian_passage = observer.next_transit(star)

# Convert the meridian passage time to an angle where 24 hours equals 360 degrees
hours = meridian_passage.datetime().hour + meridian_passage.datetime().minute / 60 + meridian_passage.datetime().second / 3600
angle = (hours / 24) * 2 * np.pi  # Convert hours to radians
print(f"Meridian passage time: {meridian_passage}, Angle: {np.degrees(angle)} degrees")


# Calculate the time offset in radians, UTC timezone
tz_offset = -angle

# Draw dots for longitudes
dot_radius = LONGITUDE_DOTS_RADIUS
longitude_angles = np.linspace(0, 360, 180, endpoint=False)
for angle in longitude_angles:
    markersize = 3 if angle % 10 == 0 else 1.5
    angle = np.radians(angle) + tz_offset
    x = dot_radius * np.cos(angle)
    y = dot_radius * np.sin(angle)
    ax.plot(x, y, 'o', color='black', markersize=markersize)

# Add longitudes around the inner disk
longitudes = range(-180, 181, 10)  # Longitudes at 15-degree intervals for east
angles = np.radians(longitudes)
angles = -angles
# Adjust longitudes by adding the tz_offset
angles = angles + tz_offset
radius = LONGITUDE_TEXT_RADIUS  # Slightly smaller than the inner disk radius
for longitude, angle in zip(longitudes, angles):
    # Add longitude labels
    x_text = radius * np.cos(angle)
    y_text = radius * np.sin(angle)
    name = "W" if longitude >= 0 else "E"
    if abs(longitude) in [0, 180]:
        name = ""   
    ax.text(x_text, y_text, f"{abs(longitude)}{name}", ha='center', va='center', fontsize=10,
            rotation=np.degrees(angle) - 90, rotation_mode='anchor')


# Set the aspect of the plot to be equal
ax.set_aspect('equal')

# Set limits to ensure the disk is fully visible
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)

# Display the plot
plt.show()

# Page 1: Save the current plot
pdf.savefig(fig)
plt.close(fig)

# DRAW INNER DISK - MONTHS, LONGITUDES

fig, ax = plt.subplots()

# Add numbers from 0 to 23 inside the inner disk with an offset
hours = range(24)
hour_radius = TIME_TEXT_RADIUS  # Slightly smaller than the inner disk radius
hour_angles = np.linspace(0, 2 * np.pi, len(hours), endpoint=False)
for hour, angle in zip(hours, hour_angles):
    x = hour_radius * np.cos(angle)
    y = hour_radius * np.sin(angle)
    ax.text(x, y, str(hour), ha='center', va='center', fontsize=14, fontweight='bold',
            rotation=np.degrees(angle) - 90, rotation_mode='anchor')

# Draw 72 dots inside the numbers with an offset
dots_radius = TIME_DOTS_RADIUS  # Slightly smaller than the hour numbers radius
dots_angles = np.linspace(0, -2 * np.pi, 96, endpoint=False)
sharp_hour = 0
for angle in dots_angles:
    x = dots_radius * np.cos(angle)
    y = dots_radius * np.sin(angle)
    markersize = 4 if sharp_hour % 4 == 0 else 2
    sharp_hour += 1
    ax.plot(x, y, 'o', color='black', markersize=markersize)

# Add a small ▲ symbol pointing towards the 0 of longitude
triangle_angle = np.radians(0)  # Adjust for timezone offset
triangle_radius = LONGITUDE_DOTS_RADIUS - 0.2  # Position of the ▲ symbol
x = triangle_radius * np.cos(triangle_angle)
y = triangle_radius * np.sin(triangle_angle)
ax.text(x, y, '▲', ha='center', va='center', fontsize=14, fontweight='bold', rotation=np.degrees(triangle_angle) - 90)
triangle_radius = LONGITUDE_DOTS_RADIUS - 0.1  # Position of the triangle center

# Draw a line touching the tip of the ▲ symbol, perpendicular to the disk, 0.5 cm long
line_length = 1.0  # Length of the line
line_angle = triangle_angle + np.pi / 2  # Perpendicular to the ▲ symbol
x_start = triangle_radius * np.cos(triangle_angle)
y_start = triangle_radius * np.sin(triangle_angle)
x_end = x_start + (line_length / 2) * np.cos(line_angle)
y_end = y_start + (line_length / 2) * np.sin(line_angle)
x_start = x_start - (line_length / 2) * np.cos(line_angle)
y_start = y_start - (line_length / 2) * np.sin(line_angle)
ax.plot([x_start, x_end], [y_start, y_end], color='black', linewidth=1)

# Draw two short radial lines from the inner disk boundary towards the tips of the line above
short_line_length = INNER_DISK_RADIUS - triangle_radius  # Length of the short lines to reach the inner disk boundary
for direction in [-1, 1]:  # Two directions: one for each tip
    radial_angle = triangle_angle + direction * (np.pi / 6)  # Spread the lines by ±30 degrees
    x_tip = x_start if direction == -1 else x_end
    y_tip = y_start if direction == -1 else y_end
    x_start_radial = x_tip + short_line_length * np.cos(radial_angle)
    y_start_radial = y_tip + short_line_length * np.sin(radial_angle)
    ax.plot([x_start_radial, x_tip], [y_start_radial, y_tip], color='black', linewidth=1)

# Texts
name = "NOCTURNAL" if args.lang == 'en' else "NOKTURNÁL"
ax.text(0, 2.15, name, ha='center', va='center', fontsize=14, fontweight='bold')

text_lines_en = [
    "is an instrument to measure",
     "time at night. How to use it:",
     "",
    "1. Set local longitude in the time plate window",
    "2. Find Polaris through the hole in the middle",
    "3. Turn the nocturnal until current date is on top",
    "",
    "4. Align the alidade with the star Dubhe in Big Dipper",
    "5. Read the UTC time on the time plate",
    "",
    "www.chovanec.com"
]

text_lines_cz = [
    "je přístroj na měření času v noci",
    " Použití:",
    "",
    "1. Nastav místní zeměpisnou délku v okénku",
    "2. Najdi Polárku skrz otvor uprostřed nokturnálu",
    "3. Otoč nokturnál, aby aktuální datum bylo nahoře",
    "",
    "4. Zarovnej alhidádu s hvězdou Dubhe ve Velkém voze",
    "5. Odečti čas v UTC na časovém disku",
    "",
    "www.chovanec.com"
]
text_lines = text_lines_en if args.lang == 'en' else text_lines_cz

# Vertical spacing between lines
line_spacing = 0.3  # Adjust as needed

# Starting y-coordinate for the first line
start_y = (len(text_lines) - 1) * line_spacing / 2

for i, line in enumerate(text_lines):
    y = start_y - i * line_spacing + 0.28
    ax.text(0, y, line, ha='center', va='center', fontsize=10)



# Define the stars to plot

stars = [
    "Alkaid",  # Eta Ursae Majoris (Big Dipper)
    "Mizar",   # Zeta Ursae Majoris (Big Dipper)
    "Alioth",  # Epsilon Ursae Majoris (Big Dipper)
    "Dubhe",   # Alpha Ursae Majoris (Big Dipper)
    "Merak",   # Beta Ursae Majoris (Big Dipper)
    "Phecda",  # Gamma Ursae Majoris (Big Dipper)
    "Megrez",  # Delta Ursae Majoris (Big Dipper)
]


# Plot the stars on the disk

star_data = {}
for star in stars:
    star_coord = SkyCoord.from_name(star)
    
    # Get RA and Dec in radians
    ra = star_coord.ra.radian
    dec = star_coord.dec.radian

    print(f"Star: {star}, RA: {np.degrees(ra)}, Dec: {np.degrees(dec)}")

    # Convert RA and Dec to polar coordinates on the disk
    # Declination 90 degrees (π/2 radians) maps to the center of the disk
    # Declination 0 degrees maps to the edge of the disk
    radius = 1.2 * (90 - np.degrees(dec)) / 90 * OUTER_DISK_RADIUS 
    angle = -ra  + np.pi / 1.9 # RA increases counterclockwise, so negate it for the plot

    # Compute x and y coordinates
    x = radius * np.cos(angle)
    y = radius * np.sin(angle)

    # Plot the star
    markersize = 16 if star == "Dubhe" else 10
    ax.plot(x, y, marker='*', color='black', markersize=markersize)

    # Optionally, label the star
    #ax.text(x + 0.2, y + 0.2, star_name, fontsize=8, ha='center', va='center', color='blue')

# Draw another disk just inside of the month names
inner_circle = plt.Circle((0, 0), INNER_DISK_RADIUS, color='black', fill=False)
ax.add_artist(inner_circle)

# Mark the center of the disk with a cross
ax.plot(0, 0, '+', color='red', markersize=10, markeredgewidth=2)


# Set the aspect of the plot to be equal
ax.set_aspect('equal')

# Set limits to ensure the disk is fully visible
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)

# Display the plot
plt.show()

# Page 1: Save the current plot
pdf.savefig(fig)
plt.close(fig)

# Close the PDF file
pdf.close()