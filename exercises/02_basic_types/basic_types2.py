# basic_types2.py

# We are given a time in hours and want to know what that time is in seconds.
# Can you finish the code for us?
# Let python do the math for you.
# After you're done, you can also change the number of hours and see what happens to the 
# time in minutes.


### I AM NOT DONE


time_in_hours = 33

time_in_minutes = time_in_hours


# Don't modify code below
# You can take a look at it, if you want to get a preview of if statements.

if(time_in_minutes != time_in_hours*60):
    raise ValueError(f"{time_in_minutes} is not {time_in_hours} hours in seconds.")
else:
    print(f"{time_in_minutes} is {time_in_hours} hours in seconds.")