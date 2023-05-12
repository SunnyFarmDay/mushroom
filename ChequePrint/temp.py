
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm, mm, inch
from PIL import Image

# Set up the canvas and page size
c = canvas.Canvas("output.pdf", pagesize=(4*inch, 6*inch))

# Calculate the position and size of the image on the page
img_x = 5*mm
img_y = 3*mm
img_width_cm = 8.8*cm
img_height_cm = 11.8*cm

# Draw the image on the canvas
c.drawImage("/home/sunny/mushroom/ChequePrint/Input.png", img_x, img_y, img_width_cm, img_height_cm)

# Save the PDF
c.save()