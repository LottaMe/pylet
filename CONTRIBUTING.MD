## Test the application

To test the application enter:

```
pytest
```

## Keep code formatting consistent

I am using black to keep the code formatting consistent.
The exercise folder should be excluded from formatting.
To do this run:

```
black . --extend-exclude exercises
isort pylet
```
