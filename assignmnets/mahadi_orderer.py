#Name of Program: Digital Bubble Tea Shop
#Name of Developer: Mahadi Masuduzzaman
#Date Finished: April 15, 2026
#Description: A digital store for purchasing bubble tea.

#import libraries
import tkinter
import random

#initialize variables and constants
grand_total_orders = 0
grand_total_revenue = 0
grand_total_hst = 0
grand_total_days = 0
grand_total_teas = 0
grand_total_slushies = 0
order_placement = 0
teas_placement = 0
slushies_placement = 0
teas = 0
numslushies = 0
numteapearls = 0
numslushiepearls = 0
teacost = 0
teapearlcost = 0
slushiecost = 0
slushiepearlcost = 0
subtotal = 0

#Boolean Variables
yestea = False
yesslushie = False
yesteapearls = False
yesslushiepearls = False

#Constants
TEA_PRICE = 1.50
SLUSHIE_PRICE = 3.25
PEARL_PRICE = 0.60
TAX_RATE = 0.13

#Serving employee name
server_name = input ("What is the server name?: ")
print (f"\nHi, im {server_name}, I will be taking your order today.")


#multiple day loop to allow the business to operate for days
another_day = "y"
while (another_day == "y") :

    total_orders = 0
    total_teas = 0
    total_slushies = 0
    total_pearls = 0
    total_revenue = 0
    total_hst = 0

    #welcome message for the user
    print ("Welcome to the Bubble Tea Digital Shop")
    print ("\nA place where bubble tea and slushies get ordered, but never delivered") 


    #ask if user wants to order or not
    orderornot = input("\nDo you want to make an order? (y/n): ")

    #if they do not want to order
    if (orderornot == "n") :
        print ("Thank you for visiting")

    #to keep the processing logic continue looping if user wants to order again
    while (orderornot == "y") :

        #resetting variable values for each new day
        teas = 0
        numslushies = 0
        numteapearls = 0
        numslushiepearls = 0
        teacost = 0
        teapearlcost = 0
        slushiecost = 0
        slushiepearlcost = 0
        yestea = False
        yesslushie = False
        yesteapearls = False
        yesslushiepearls = False


        #if they want to order
        if (orderornot == "y") :

            #asking all quesitons to determine the order
            #number of teas
            teas = int (input ("\nHow many teas do you want?: "))

            #number of slushies
            numslushies = int (input ("\nHow many slushies do you want?: "))

            #how many pearls
            teapearls = input ("\nDo you want pearls with the teas? (y/n): ")

            #slushies with pearls
            slushiepearls = input ("\nDo you want pearls with the slushies? (y/n): ")

            #tea calculations
            if (teas > 0) :
                yestea = True

                #determine if they want pearls
                if (teapearls == "y") :
                    numteapearls = int (input (f"\nHow many of the {teas} teas do you want pearls with?: "))

                #initial tea cost
                teacost = teas * TEA_PRICE

                #extra pearl cost
                if (teapearls == "y" and numteapearls > 0) :
                    yesteapearls = True
                    teapearlcost = numteapearls * PEARL_PRICE
                    
            #slushie calculations
            if (numslushies > 0) :
                yesslushie = True

                #determine if they want pearls
                if (slushiepearls == "y") :
                    numslushiepearls = int (input (f"\nHow many of the {numslushies} slushies do you want pearls with?: "))

                #initial slushie cost
                slushiecost = numslushies * SLUSHIE_PRICE

                #extra pearl cost
                if (slushiepearls == "y" and numslushiepearls > 0) :
                    yesslushiepearls = True
                    slushiepearlcost = numslushiepearls * PEARL_PRICE

        #grand total final calculation
        subtotal = teacost + teapearlcost + slushiecost + slushiepearlcost 

        #Tax calculation
        hst = subtotal * TAX_RATE

        #grand total
        grandtotal = round(subtotal * (1 + TAX_RATE), 2)

        #Receipt random number

        receiptnumber = random.randrange (10, 1000)

        #Receipt
        print ("\n----------------------------------------\n",
                f"\nReceipt",
                f"\nServer name: {server_name}",
                f"\nReceipt number: {receiptnumber:04d}",
                "\n\nOrder: ")

        #receipt but conditional based on users order
        if (yestea) :
            print (f"\n {teas} teas: {teacost:.2f} dollars")
        if (yesteapearls) :
            print (f"\n {numteapearls} teas with pearls: {teapearlcost:.2f} dollars")
        if (yesslushie) :
            print (f"\n {numslushies} slushies: {slushiecost:.2f} dollars")
        if (yesslushiepearls) :
            print (f"\n {numslushiepearls} slushies with pearls: {slushiepearlcost:.2f} dollars")

        print (f"\nSubtotal: {subtotal:.2f} dollars")

        print (f"\nHST: {hst:.2f} dollars")

        print (f"\nFinal total: {grandtotal:.2f} dollars")

        print ("\n----------------------------------------")

        #accumulate the total order for final printed statement
        total_orders += 1
        total_teas += teas
        total_slushies += numslushies
        total_pearls += (numteapearls + numslushiepearls)
        total_revenue += subtotal
        total_hst += hst

        #cause a repeat to the cycle, or end
        orderornot = input ("\nDo you want to make an order? (y/n): ")

    #end of day report
    print ("\n----------------------------------------")
    print (f"\nTotal Orders: {total_orders}")
    print (f"\nTotal teas: {total_teas}")
    print (f"\nTotal slushies: {total_slushies}")
    print (f"\nTotal drinks with pearls: {total_pearls}")
    print (f"\nTotal revenue: {total_revenue:.2f}")
    print (f"\nTotal HST tax: {total_hst:.2f}")
    print ("\n----------------------------------------")

    #add to grand total of the days worked
    grand_total_days += 1
    grand_total_teas += total_teas
    grand_total_slushies += total_slushies
    grand_total_orders += total_orders
    grand_total_revenue += total_revenue
    grand_total_hst += total_hst

    #to continue the cycle for another day, or end
    another_day = input ("\nDo you want to start another day?(y/n): ")


#window config
window = tkinter.Tk ()
window.geometry ("700x700")  #Dimensions in pixels
window.title ("Total Orders VS. Total Tea VS. Total Smoothies")
window.attributes ("-topmost", True)
window.update_idletasks ()
window.attributes ("-topmost", False)
window.focus_force ()

canvas = tkinter.Canvas (window, width = 700, height = 700, bg = "white")
canvas.pack()

#Text placement
ordertext = canvas.create_text (120, 190, text = "Orders")
teastext = canvas.create_text (320, 190, text = "Teas")
slushiestext = canvas.create_text (520, 190, text = "Slushies")

#create the box for graphic
graphbox = canvas.create_rectangle (60, 200, 600, 600)


#proportional scaling for bar graph sizes
if total_orders != 0 and total_teas != 0 and total_slushies != 0:
        
        if (total_orders >= total_teas and total_orders >= total_slushies) :
                
            order_placement = 3

            if (total_teas >= total_slushies) :
                    
                teas_placement = 2
                slushies_placement = 1


            else :
                    
                teas_placement = 1
                slushies_placement = 2

        elif (total_teas >= total_slushies and total_teas >= total_orders) :
                
            teas_placement = 3

            if (total_orders >= total_slushies) :
                    
                order_placement = 2
                slushies_placement = 1
                    

            else :
                    
                slushies_placement = 2
                order_placement = 1

        elif (total_slushies >= total_teas and total_slushies >= total_orders) :
                
            slushies_placement = 3

            if (total_teas >= total_orders) :
                    
                teas_placement = 2
                order_placement = 1


            else :
                    
                order_placement = 2
                teas_placement = 1


#actually creating the bars
if (order_placement == 3) :
        
    ordercolumn = canvas.create_rectangle (75, 200, 175, 600, fill = "cyan")
        
elif (order_placement == 2) :
        
    ordercolumn = canvas.create_rectangle (75, 400, 175, 600, fill = "cyan")
        
elif (order_placement == 1) :
        
    ordercolumn = canvas.create_rectangle (75, 500, 175, 600, fill = "cyan")

if (teas_placement == 3) :
        
    teacolumn = canvas.create_rectangle (270, 200, 370, 600, fill = "red")
        
elif (teas_placement == 2) :
        
    teacolumn = canvas.create_rectangle (270, 400, 370, 600, fill = "red")
        
elif (teas_placement == 1) :
        
    teacolumn = canvas.create_rectangle (270, 500, 370, 600, fill = "red")

if (slushies_placement == 3) :
        
    slushiecolumn = canvas.create_rectangle (470, 200, 570, 600, fill = "green")
        
elif (slushies_placement == 2) :
        
    slushiecolumn = canvas.create_rectangle (470, 400, 570, 600, fill = "green")
        
elif (slushies_placement == 1) :
        
    slushiecolumn = canvas.create_rectangle (470, 500, 570, 600, fill = "green")

canvas.pack ()

window.mainloop ()

#final message with regard to grand total day metrics
if (grand_total_days > 1) :
    print (f"\n{grand_total_days} days of consecutive business",
        f"\nTotal Orders: {grand_total_orders}",
        f"\nTotal Teas sold: {grand_total_teas}",
        f"\nTotal Slushies sold: {grand_total_slushies}",
        f"\nTotal Revenue: {grand_total_revenue:.2f}",
        f"\nTotal HST: {grand_total_hst:.2f}")

elif (grand_total_days == 1 and total_orders == 0) :
    print ("No Business at all :( gotta shutdown and claim bankruptcy")

elif (grand_total_days == 1) :
    print ("\nOne day of successful business")

if (total_orders > 0) :
    if (grand_total_teas <= 10 or grand_total_slushies <= 10) : 
        print ("\nBusiness is slow :(")

    else :
        print ("\nBusiness is booming :)")

input ()