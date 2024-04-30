# strings1.py


# We have a function called generate_lyrics, which takes a name
# and returns the lyrics with the name inserted in the lyrics.
# It does not work currently, can you fix it?

### I AM NOT DONE

def generate_lyrics(name: str):
    return """
Forgive me {name}
My lost fearless leader
In closets like cedar
Preserved from when we were just kids
Is it something I did
The goddess of timing
Once found us beguiling
She said she was trying
{name} was she lying
My ribs get the feeling she did
And I didn't want to come down
I thought it was just goodbye for now
"""

print(generate_lyrics("Peter"))


# Don't modify code below

def test_generate_lyrics():
    lyrics_peter = """
Forgive me Peter
My lost fearless leader
In closets like cedar
Preserved from when we were just kids
Is it something I did
The goddess of timing
Once found us beguiling
She said she was trying
Peter was she lying
My ribs get the feeling she did
And I didn't want to come down
I thought it was just goodbye for now
"""
    assert generate_lyrics("Peter") == lyrics_peter
    lyrics_wendy = """
Forgive me Wendy
My lost fearless leader
In closets like cedar
Preserved from when we were just kids
Is it something I did
The goddess of timing
Once found us beguiling
She said she was trying
Wendy was she lying
My ribs get the feeling she did
And I didn't want to come down
I thought it was just goodbye for now
"""
    assert generate_lyrics("Wendy") == lyrics_wendy

