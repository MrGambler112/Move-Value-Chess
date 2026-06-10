#Name of Program: The Widgermidger Tester
#Name of Developer: Mahadi Masuduzzaman
#Date Finished: May 04, 2026
#Description: A tool to verify widget dimensions

#Libraries
import tkinter
import time
import random
import math

#constants
DELAY_SECONDS = 0.3

#Lists
measurements = []
qualitypass = []
qualityfail = []
convertedmeasures = []

#Boolean Variables
value = True

#Strings and Integer Variables
maxgood = 0
mingood = 0
check = 0
qualitypassamount = 0
qualityfailamount = 0
passsum = 0
user_input = 0
belt_shift = 0
live_passed = 0
live_failed = 0
total = 0
convertedaverage = 0
border_color = ""
loop = ""

#Title and Description
print ("The Widgermidger Tester")
print ("\nWelcome to the Widgermidger dimension tester;",
     "A tool to verify widget dimensions")

#setup
print ("-----------------------------------------------------")
print ("\nSet Up Stage Initialized")

#Get user input for the max and min dimensions
maxgood = float(input("\nWhat is the MAXIMUM good measure?: "))
mingood = float(input("\nWhat is the MINIMUM good measure?: "))

#Widget Measures
print ("-----------------------------------------------------")
print ("\nMeasurement Input Initialized")


#loop to continue getting user input for more measurements
while (user_input != -1) :
    user_input = float(input("\nWhat are the measurements? (decimals allowed | Press -1 to stop): "))
    
    #if user value is not -1 then add the input to the list
    if (user_input != -1) :
        measurements.append(user_input)


print ("-----------------------------------------------------")
print ("\n\nQuality Check Initialized")

print ("\nHere are all the measurements entered: \nMaximum Good Measure: ", maxgood,
       "\nMinimum Good Measure" ,mingood, "\n\nAll Measurements: \n")     

#measurement print without square brackets
for i in measurements :
    print (i)

#sorting passed and failed values of measurement
for i in measurements :

    check = i

    if (check >= mingood and check <= maxgood) :
        qualitypass.append (i)

    else :
        qualityfail.append (i)

#passed quality check print
print ("\nThese are all the measurements that have passed the quality check: \n")

#print qualitypass values without square brackets
for i in qualitypass :
    print (i)

#failed quality check print
print ("\nThese are all the measurements that have failed the quality check: \n")

#qualityfail values without square brackets
for i in qualityfail :
    print (i)

#numerical value of elements in each pass and fail lists
qualitypassamount = len(qualitypass)
qualityfailamount = len(qualityfail)


print ("\nTotal Number of Measurements Passed: ", qualitypassamount,
       "\nTotal Number of Measurements Failed: ", qualityfailamount)

#statistics
if (len(measurements) > 0) : #to prevent crash if there is no value entered
    
    #calculating percentage of how many values passed
    totalpasspercent = round(100*(qualitypassamount/(qualitypassamount + qualityfailamount)), 1)

    print ("\nHere is a percentage of all the measurements that have passed: ",
        totalpasspercent, "percent")

    #sum of passed values (required for average)
    for i in qualitypass :
        
        passsum += i

    #pass average
    if (qualitypassamount > 0) :
        passaverage = round(passsum/qualitypassamount, 1)

        print ("The average good measure is: ", passaverage)
    
    else :
        print ("No good measures were found to average")

#Central Tendency Analysis

#selecting a random value between 10 and 30 inclusive
p = random.randrange (10, 31)

#numerical value of the elements in measurements
totalmeasurements = len(measurements)

#number of elements based on p
actualmeasures = math.ceil((p/100) * totalmeasurements)

print (f"\n{p}% means {actualmeasures} measurements")

measurements.sort () #sort from lowest to largest values

#replicate parts of measurements in convertedmeasures
#without p lowest and p largest
convertedmeasures = measurements[actualmeasures:-(actualmeasures)]

print (f"\nThese are the remaining measures: ")

#print convertedmeasures without square brackets
for i in convertedmeasures :
    print (i)

#sum up all values in convertedmeasures
for k in convertedmeasures :
    total += k

#convertedmeasures average calculation
convertedaverage = round(total/len(convertedmeasures), 1)

print (f"The average converted measure is: {convertedaverage}")


#window config
window = tkinter.Tk ()
window.geometry ("700x700")  #Dimensions in pixels
window.title ("The Widgermidger Quality Control Visualizer")
window.attributes ("-topmost", True)
window.update_idletasks ()
window.attributes ("-topmost", False)
window.focus_force ()

#canvas widget in window
canvas = tkinter.Canvas (window, width = 700, height = 700, bg = "white")

#looping through each element in measurements
for m in measurements :

    widget_x1 = 0
    widget_y1 = 290
    widget_x2 = 50
    widget_y2 = 340
        
    # Check if this measurement is good or bad

    if (m >= mingood and m <= maxgood) :
        is_good = True

    else :
        is_good = False
        
    #animation illusion    
    for frame in range(70) :

        #create the canvas for each frame
        canvas = tkinter.Canvas(window, width=700, height=700, bg="white")
            
        #Conveyor belt image (static)
        canvas.create_rectangle(0, 340, 700, 360, fill="gray", outline="black")

        #Scanner image (static)
        canvas.create_rectangle(348, 250, 352, 340, fill="yellow", outline="black")

        #Scanner system to indicate if something passes or fails
        if (widget_x1 < 350) :
            border_color = "black"  #Basic package prior to scanner
        else :
            if (is_good == True) :
                border_color = "green"  #for things that pass
            else :
                border_color = "red"    #for things that fail

        #Packages with measurements
        canvas.create_rectangle (widget_x1, widget_y1, widget_x2, widget_y2, 
                                fill="blue", outline=border_color, width=4)
        
        #The measurement on the package
        canvas.create_text (widget_x1 + 25, widget_y1 + 25, text=str(m), fill="white")

        #Live Statistics on the bottom
        canvas.create_text (200, 600, text=f"Number of measurements passed: {live_passed}")
        canvas.create_text (200, 630, text=f"Number of measurements failed: {live_failed}")

        #title near top of the canvas
        canvas.create_text (350, 100, text="Package Quality Control Conveyor System")

        canvas.pack ()
        canvas.update ()
        time.sleep (0.03)
        canvas.destroy ()

        # Update position
        widget_x1 = widget_x1 + 10
        widget_x2 = widget_x2 + 10

    # 4. Update the live counts after the package finishes its trip
    if (is_good == True) :
        live_passed += 1
    else :
        live_failed += 1

# Final mainloop to keep the window open
window.mainloop ()

