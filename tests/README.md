#Tests

###To run a test by the package:
```
$ python -m unittest -v tests.PacbioToSRA.cell_analysis.test_abstract_format
```
###To run a test by the class:
```
$ python -m unittest -v tests.PacbioToSRA.cell_analysis.test_abstract_formatTest.AbstractFormat
```
###To run a specific test:
```
$ python -m unittest -v tests.PacbioToSRA.cell_analysis.test_abstract_formatTest.AbstractFormat.test__init__directory_does_not_exist
```

###To run all tests:
```
$ python -m unittest discover -v
```
