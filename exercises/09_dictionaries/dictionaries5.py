# dictionaries5.py

# 

### I AM NOT DONE

complex_person_dict = {
    "firstname": "Taylor",
    "lastname": "Swift",
    "occupation": "Musician",
    "albums": [
        {
            "title": "Taylor Swift",
            "release_year": 2006,
            "album_of_the_year": False
        },
        {
            "title": "Fearless",
            "release_year": 2008,
            "album_of_the_year": True
        },
        {
            "title": "Speak Now",
            "release_year": 2010,
            "album_of_the_year": False
        },
        {
            "title": "Red",
            "release_year": 2012,
            "album_of_the_year": False
        },
        {
            "title": "1989",
            "release_year": 2014,
            "album_of_the_year": True
        },
        {
            "title": "Reputation",
            "release_year": 2017,
            "album_of_the_year": False
        },
        {
            "title": "Lover",
            "release_year": 2019,
            "album_of_the_year": False
        },
        {
            "title": "Folklore",
            "release_year": 2020,
            "album_of_the_year": True
        },
        {
            "title": "Evermore",
            "release_year": 2020,
            "album_of_the_year": False
        },
        {
            "title": "Midnights",
            "release_year": 2023,
            "album_of_the_year": True
        },
        {
            "title": "The Tortured Poets Department",
            "release_year": 2024
        }
    ]
}


def count_albums_of_the_year(albums: list) -> int:
    pass

print(
    complex_person_dict["firstname"],
    complex_person_dict["lastname"],
    "is a",
    complex_person_dict["occupation"],
    "with",
    count_albums_of_the_year(complex_person_dict["albums"]),
    "album(s) of the year."
)

# Don't modify code below

def test_count_albums_of_the_year_swift():
    albums = [
        {
            "title": "Taylor Swift",
            "release_year": 2006,
            "album_of_the_year": False
        },
        {
            "title": "Fearless",
            "release_year": 2008,
            "album_of_the_year": True
        },
        {
            "title": "Speak Now",
            "release_year": 2010,
            "album_of_the_year": False
        },
        {
            "title": "Red",
            "release_year": 2012,
            "album_of_the_year": False
        },
        {
            "title": "1989",
            "release_year": 2014,
            "album_of_the_year": True
        },
        {
            "title": "Reputation",
            "release_year": 2017,
            "album_of_the_year": False
        },
        {
            "title": "Lover",
            "release_year": 2019,
            "album_of_the_year": False
        },
        {
            "title": "Folklore",
            "release_year": 2020,
            "album_of_the_year": True
        },
        {
            "title": "Evermore",
            "release_year": 2020,
            "album_of_the_year": False
        },
        {
            "title": "Midnights",
            "release_year": 2023,
            "album_of_the_year": True
        },
        {
            "title": "The Tortured Poets Department",
            "release_year": 2024
        }
    ]
    assert count_albums_of_the_year(albums) == 3

def test_count_albums_of_the_year_2():
    albums = [
        {
            "title": "1",
            "release_year": 1,
            "album_of_the_year": False
        },
        {
            "title": "2",
            "release_year": 2,
            "album_of_the_year": True
        },
    ]
    assert count_albums_of_the_year(albums) == 2