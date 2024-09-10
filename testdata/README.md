There _can_ be an image for every camera for a test case but must not. The camera directory and the specifc camera prefix in the image file must match the defined names in the test suite. 

Missing images of a specific test case for a camera will be reported as WARNING. For this, `pytest.ini` must be set at least to level WARNING (30):

```txt
log_cli_level = 30 
```

The name for the film simulations must match exactly the values in `constants.filmsimulations`. For a B&W film simulation the  opional filter value must exactly match the value in `constants.bwfilter`, joined by `+`. 
