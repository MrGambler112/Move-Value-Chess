#Name: Canadian Resource Calculator
#Programmer: Syed (Mahadi) Masuduzzaman
#Date: March 8, 2026
#Description: To calculate the amount of resources required for
#             Canada to have a place on the Global Leaderboard

print ("Canadian Resource Global Placement\n")
print ("This program will calculate the amount of resources required for Canada to "
        "have a place on the Global Leaderboard\n")

#Production amounts
china = 270000
usa = 45000
burma = 31000
australia = 13000
thailand = 13000
other = 18000

#input from user of how many tonnes (metric ton) Canada should mine in year

canada = float(input("How many tonnes of rare earth metals should Canada mine in a year?: "))

#sum of all resources
total = canada + china + usa + burma + australia + thailand + other

#worlds supply percentage
canada_percentage = (canada / total) * 100
china_percentage = (china / total) * 100
usa_percentage = (usa / total) * 100
burma_percentage = (burma / total) * 100
australia_percentage = (australia / total) * 100
thailand_percentage = (thailand / total) * 100
other_percentage = (other / total) * 100

#canada rounded
canada_rounded = round(canada_percentage, 1)

#canada's rank (global placement)
if canada_percentage > china_percentage:
    print ("Canada is ranked #1 with", canada_rounded, "percent of the world supply\n")

elif canada_percentage > usa_percentage:
    print ("Canada is ranked #2 with", canada_rounded, "percent of the world supply\n")

elif canada_percentage > burma_percentage:
    print ("Canada is ranked #3 with", canada_rounded, "percent of the world supply\n")

elif canada_percentage > australia_percentage:
    print ("Canada is ranked #4 with", canada_rounded, "percent of the world supply\n")

elif canada_percentage > thailand_percentage:
    print ("Canada is ranked #5 with", canada_rounded, "percent of the world supply\n")

else:
    print ("Canada is ranked #6 with", canada_rounded, "percent of the world supply\n")

#inquire if user wants to calculate how many tonnes of rare earth metals Canada should
#mine for a specific percentage

question = input("Would you like to calculate how many tonnes of rare "
                "earth metals Canada should mine for a specific percentage? (y/n): ")

if question == "y":
    percentage = float(input("What percentage would you like to calculate?: "))
    final_percentage = percentage / 100 
    tonnes = round((final_percentage * 390000) / (1 - final_percentage), 1)
    print ("\nTo have", percentage, "percent of the worlds supply, Canada would have to mine",
            tonnes, "tonnes of rare earth metals\n")

else:
    print ("")

#rare earth metal calculations

print ("Here are a couple of rare earth metals:\n")
print ("Neodymium for $221,000 per tonne\n")
print ("Dysprosium for $930,700 per tonne\n")
print ("Terbium for $4,500,000 per tonne\n")

print ("Select one of the following rare earth metal for calculation:\n For Neodymium (type Nd)"
       "\n For Dysprosium (type Dy)\n For Terbium (type Tb)\n")

#user choice of rare earth metal
choice = input ("Type the letter of the rare earth metal you want to calculate the price for: ")

#rare earth metal calculations
if choice == "Nd":
    ndvalue = float(input("\nHow many tonnes (metric ton) of Neodymium do you "
                            "want to calculate the price for?: "))
    price1 = round(ndvalue * 221100, 1)
    print ("\nTo purchase", ndvalue, "tonnes of Neodymium, it will cost approximately: ", price1, "dollars\n")

elif choice == "Dy":
    dyvalue = float(input("\nHow many tonnes (metric ton) of Dysprosium do you "
                            "want to calculate the price for?: "))
    price2 = round(dyvalue * 930700, 1)
    print ("\nTo purchase", dyvalue, "tonnes of Dysprosium, it will cost approximately: ", price2, "dollars\n")

elif choice == "Tb":
    tbvalue = float(input("\nHow many tonnes (metric ton) of Terbium do you "
                            "want to calculate the price for?: "))
    price3 = round(tbvalue * 4500000, 1)
    print ("\nTo purchase", tbvalue, "tonnes of Terbium, it will cost approximately: ", price3, "dollars\n")

else:
    print ("Invalid choice")

input ()