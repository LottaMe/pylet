# lists6.py

# We have tried to create a tuple of artists, but needed
# to remove and add to it afterwards.
# Can you figure out why the code doesn't work?
# Should we use a list instead?

### I AM NOT DONE

# trying to add or remove to tuple
artists = (
    "Taylor Swift",
    "Billie Eilish",
    "Olivia Rodrigo"
)

icon = artists.pop(0)
artists.append("James Blunt")

print(icon)
print(artists)