# while_loops2.py


# We're trying to count till 13, but skip number 7
# Can you finish the code?
# Hint: try out the continue statement

### I AM NOT DONE


import time


counter = 13

while counter > 0:
    if counter == 7:
        counter = counter - 1
        raise ValueError("continue here")

    print(counter)

    time.sleep(1)
  
    counter = counter - 1
