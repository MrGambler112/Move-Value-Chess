# MAHADI CODE IDENTITY CARD

## If you see these, it's Mahadi's code:

### IMMEDIATELY IDENTIFIABLE
```
print ("text")        <- space before (
input ("prompt?: ")   <- space before ( and ?: ending
if (condition) :      <- space before ( and before :
== True               <- always explicit
== False              <- never just `if x:`
```

### STRUCTURAL
```
#section header       <- lowercase comment as divider
def func() :          <- space before colon (early code)
i = i + 1             <- manual increment
x = x + 1             <- explicit self-assignment
```

### VALIDATION
```python
is_valid = True
if is_valid :
    if some_check :
        print ("Error: message")
        is_valid = False
if is_valid :
    if another_check :
        print ("Error: message")
        is_valid = False
return is_valid
```

### FILE HEADER
```python
#Name: Program Name
#Programmer: Syed (Mahadi) Masuduzzaman
#Date: Month Day, Year
#Description: Description text
#             wrapped line
```

### FILE ENDING
```python
main()

input ()
```

### GUI WINDOW
```python
window = tkinter.Tk ()
window.geometry ("700x700")
window.title ("Title")
window.attributes ("-topmost", True)
window.update_idletasks ()
window.attributes ("-topmost", False)
window.focus_force ()
```

### LOOP PATTERN
```python
i = 0
while i < len(list) :
    # stuff
    i = i + 1
```

### FILE READ
```python
f = open("file.txt", "r")
line = f.readline().strip()
while line != "":
    # process
    line = f.readline().strip()
f.close()
```

### RETURN PATTERN
```python
result = -1  # or False, or 0, or ""
# search/check logic
return result
```

### THE ELIF CHAIN
```python
if x == 0:
    return "A"
elif x == 1:
    return "B"
elif x == 2:
    return "C"
# ... continues for every possible value
else:
    return "?"
```

### STRING BUILDING
```python
result = "prefix " + str(value) + " suffix " + str(other)
```

### BOOLEAN NAMING
```python
yestea = True       # early: yes prefix
is_valid = False    # later: is_ prefix
```

### COMMENT STYLE
```python
#description of next section (lowercase, no period)
code
```

### INPUT VALIDATION
```python
if not input_string.isdigit() :
    print ("Error: Must be a whole number.")
```

### THE MAHADI FINGERPRINT IN ONE LINE:
`print ("Hello")` with space before paren, `== True` in condition, `#lowercase` comment above, `input ()` at file end.
