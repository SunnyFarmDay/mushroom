
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm, mm, inch
from PIL import Image

# Set up the canvas and page size
c = canvas.Canvas("output.pdf", pagesize=(4*inch, 6*inch))

# Load the image and get its size
img = Image.open("input.jpg")
img_width, img_height = img.size

# Calculate the position and size of the image on the page
img_x = 8*mm
img_y = 6*mm
img_width_cm = 8.2*cm
img_height_cm = 11.2*cm

# Draw the image on the canvas
c.drawImage("input.jpg", img_x, img_y, img_width_cm, img_height_cm)

# Save the PDF
c.save()