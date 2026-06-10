# Quick Reference - Mahadi's Code Style

## THE NON-NEGOTIABLES (Always Present)

| Pattern | Example | Where |
|---------|---------|-------|
| Space before `(` | `print ("hello")` | Every file |
| Space before `:` | `if (x) :` | Assignment files |
| `== True/False` | `if valid == True:` | Every file |
| Lowercase section comments | `#loading from file` | Every file |
| Header block | `#Name: / #Programmer: / #Date: / #Description:` | Every file |
| `?: ` input prompt ending | `input("Enter value?: ")` | Every file |
| Manual file open/close | `f = open(); ...; f.close()` | Every file |
| `input ()` at end | `input ()` | Every assignment file |

## NAMING CONVENTIONS

```
Variables:    snake_case          (player_name, item_line)
Constants:    UPPER_CASE          (TEA_PRICE, DELAY_SECONDS)
Functions:    snake_case          (add_items, validate_item)
Booleans:     yes prefix OR is_   (yestea, is_valid)
Files:        snake_case          (mahadi_inventory.py)
```

## STRUCTURE TEMPLATE

```python
#Name: Program Name
#Programmer: Syed (Mahadi) Masuduzzaman
#Date: Month Day, Year
#Description: What the program does
#             Wrapped description line

#Section Header
code_here

#Another Section
more_code

def function_name() :

    #comment about what this does
    code_here

def main() :

    print ("Title")
    print ("Description\n")

    #do stuff

main()

input ()
```

## VALIDATION TEMPLATE

```python
def validate_something(input_val):
    is_valid = True

    if is_valid:
        if some_condition:
            print("Error: message")
            is_valid = False

    if is_valid:
        if another_condition:
            print("Error: message")
            is_valid = False

    return is_valid
```

## LOOP TEMPLATE

```python
i = 0
while i < len(list):
    # do stuff
    i = i + 1
```

## FILE READ TEMPLATE

```python
file = open("name.txt", "r")
line = file.readline().strip()
while line != "":
    # process line
    line = file.readline().strip()
file.close()
```

## GUI WINDOW TEMPLATE

```python
window = tkinter.Tk()
window.geometry("700x700")
window.title("Title")
window.attributes("-topmost", True)
window.update_idletasks()
window.attributes("-topmost", False)
window.focus_force()

canvas = tkinter.Canvas(window, width=700, height=700, bg="white")
# ... drawing code ...
window.mainloop()
```
