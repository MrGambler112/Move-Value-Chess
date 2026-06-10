# Basica animation example - moving ball

import tkinter
import time

WINDOW_DIMEN = 500
#Each picture will display for 3/10 ths of a second
DELAY_SECONDS = .3
CUSTOM_COLOUR= "#DDC51F"

#Starting position of image
upper_left_x = 0
upper_left_y = 100
lower_right_x = 50
lower_right_y = 150


#Create the graphics bearing window
#Set a few important visual, static parameters
window = tkinter.Tk()
window.geometry ("500x500")  #Dimensions in pixels
window.title ("Moving Ball")

#Set an important behaviour - window appears on top of other windows
window.attributes ("-topmost", True)
window.update_idletasks ()
window.attributes ("-topmost", False)
window.focus_force ()
   

for i in range(20): #The animation will have 20 drawings

    canvas = tkinter.Canvas (window, width=WINDOW_DIMEN, height=WINDOW_DIMEN,
                        bg="blue")

    ball = canvas.create_oval (upper_left_x, upper_left_y,
                          lower_right_x, lower_right_y,
                          fill=CUSTOM_COLOUR)

    canvas.pack ()
    canvas.update ()

    #After the image displays, pause for a split second to allow the user
    #to register this image
    time.sleep (DELAY_SECONDS)
    
    #After the user has seen the image, clear the window for the next image
    canvas.destroy ()

    #Next image is drawn 10 pixels to the right
    upper_left_x = upper_left_x + 10
    lower_right_x = lower_right_x + 10
    
window.mainloop