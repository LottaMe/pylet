# lists5.py

# We have an unordered list of the numbers 1 to 5.
# Use the list methods sort and reverse to change the order
# of the list items, so it is instead a sorted list where the numbers are in
# decreasing order.

### I AM NOT DONE

import time

my_list = [1, 4, 2, 3, 5]   # don't edit this line

# only edit the following two lines
my_list
my_list


# Don't modify code below,
# but feel free to read and understand :)

index = 0

while index < len(my_list):
  print(my_list[index])

  time.sleep(0.5)
  
  index +=1

if my_list != [5, 4, 3, 2, 1]:
  raise ValueError("my_list should be [5, 4, 3, 2, 1]")

print("Happy New Year!!")



# Don't modify code below, 
# but you can take a look and try to understand it
