# strings3.py


# We want to write a function that takes a text (we've given you an example text)
# and a word and returns how many times a version of that word is in the text.
# Capitalization of the word should not matter.
# Hint: Look up the string methods count and lower


### I AM NOT DONE

example_text = """
I need to forget, so take me to Florida
I've got some regrets, I'll bury them in florida
Tell me I'm despicable, say it's unforgivable
At least the dolls are beautiful, fuck me up, florida
I need to forget, so take me to Florida
I've got some regrets, I'll bury them in Florida
Tell me I'm despicable, say it's unforgivable
What a crash, what a rush, fuck me up, Florida
"""

def count_word(text: str, word: str) -> int:
    return


# Don't modify code below

def test_count_word():
    assert count_word(example_text, "florida") == 6
    assert count_word(example_text, "bury") == 2
