# Script to use tkinter to simulate the lifting of a platform using a taut chain-elevator
import tkinter as tk

import math

# Function to convert degree angle into radians
def toRad(angle):
    return angle / 360 * 2 * math.pi

def toDegree(angle):
    """Converts radians to degrees"""
    return angle / 2 / math.pi * 360


class Label:

    def __init__(self, canvas, x, y, text, anchor = tk.W):
        """Creates a text label on canvas"""

        # Reference parameters
        self.canvas = canvas
        self.x, self.y = x, y
        self.text = text
        self.anchor = anchor

        # Create drawing
        self.drawing = self.canvas.create_text(self.x, self.y,
                                               text = self.text, anchor = self.anchor)

    def update(self):
        """Updates label based on new parameters"""

        self.canvas.coords(self.drawing, self.x, self.y)
        self.canvas.itemconfig(self.drawing, text = self.text, anchor = self.anchor)

# Class to simulate angled lifter
class LiftSimulator:

    def __init__(self, distance, chain, angle, size = 400):
        
        # Initialize lenght of lifter
        self.distance = distance
        # Initialize length of chain
        self.chain = chain
        # Initial angle
        self.angle = angle

        # Create tk root
        self.root = tk.Tk()

        # Create canvas
        self.display = tk.Canvas(self.root, width = size, height = size)
        self.display.pack()

        # Create center references for future use
        self.centerX = size / 2
        self.centerY = size / 2

        # Determine height
        self.height = self.calculateHeight()

        # Create initial drawing
        self.drawing = self.display.create_line(self.centerX, self.centerY,

                                           self.centerX - self.distance*math.sin(toRad(self.angle)), 
                                           self.centerY - self.distance*math.cos(toRad(self.angle)),

                                           self.centerX, self.centerY - self.height,
                                           self.centerX, self.centerY)

        # Create initial height label
        # self.heightLabel = Label(self.display, self.centerX + 5, self.centerY - self.calculateHeight()/2,
        #                          round(self.calculateHeight(), 2))

        self.text = self.display.create_text(self.centerX + 5, 
                                             self.centerY - self.height/2, 
                                             text = round(self.height, 2), anchor = tk.W)

        # Bind events
        self.root.bind("<Up>", self.decreaseAngle)
        self.root.bind("<Down>", self.increaseAngle)
        self.root.bind("<Left>", self.decreaseHeight)
        self.root.bind("<Right>", self.increaseHeight)

        # Start the tk mainloop
        tk.mainloop()

    def increaseAngle(self, event):
        """Increases the angle and redraws"""
        self.angle += 1
        self.height = self.calculateHeight()
        self.draw()

    def decreaseAngle(self, event):
        """Decreases the angle and redraws"""
        self.angle -= 1
        self.height = self.calculateHeight()
        self.draw()

    def increaseHeight(self, event):
        """Increases height and redraws"""
        self.height += 1
        self.angle = self.calculateAngle()
        self.draw()

    def decreaseHeight(self, event):
        """Decreases height and redraws"""
        self.height -= 1
        self.angle = self.calculateAngle()
        self.draw()

    def calculateHeight(self):
        """Calculates heigh based on chain, distance, and angle"""

        return (math.sqrt( self.chain**2 
                         - self.distance**2 
                         + (self.distance * math.cos(toRad(self.angle)))**2
                         )
               + self.distance*math.cos(toRad(self.angle))
               )

    def calculateAngle(self):
        """Calculate angle based on chain, distance, and height"""
        """
        c^2 = d^2 + h^2 - 2dhcosC
        2dhcosC = d^2 + h^2 - c^2
        cosC = (d^2 + h^2 - c^2)/(2dh)
        """
        return toDegree(math.acos( (self.distance**2 + self.height**2 - self.chain**2)
                          /(2 * self.distance * self.height) )
        )
    
    def draw(self):
        """Redraws the triangle"""

        # Redraw the triangle position
        self.display.coords(self.drawing, self.centerX, self.centerY,

                                           self.centerX - self.distance*math.sin(toRad(self.angle)), 
                                           self.centerY - self.distance*math.cos(toRad(self.angle)),

                                           self.centerX, self.centerY - self.height,
                                           self.centerX, self.centerY)

        # Redraw the label position
        self.display.coords(self.text, self.centerX + 5, 
                                       self.centerY - self.height/2,)

        # Reset the label content
        self.display.itemconfig(self.text, text = round(self.height, 2))


prog = LiftSimulator(50, 100, 90)



