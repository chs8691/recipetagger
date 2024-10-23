# recipetagger
Mapping from Fujifilm X image settings to recipes. Optional tag it to the image metadata.

Recipes can be imported by csv file. See example file `recipes.csv`. There are great sources for recipes, like the marvellous [Fuji X Weekly](https://fujixweekly.com). 

THe script compares the exif data of one or more images with every recipe of the imported recipes to find the best matching recipe. If a recipe is found, that matchs better than the given threshold, the result can be written into the image description. You can also tag the image the recipe as keyword. 

In addition, the image can be tagged with the film simulation name.

### man

```text
usage: reciper.py [-h] [-v] [-vv] [-r RECIPES] [-t THRESHOLD] [-p] [-d] [-k] FILE [FILE ...]

positional arguments:
  FILE                  Image file(s), support glob syntax. Use Wildcards to select mltiples files or pass mulptiple file names.

options:
  -h, --help            show this help message and exit
  -v, --verbose         Increase output verbosity.
  -vv, --vverbose       Increase output very verbosity.
  -r RECIPES, --recipes RECIPES
                        Update recipes from CSV file (Default: recipes.csv) and store them in the internal Storage. See example file for columns names.
  -t THRESHOLD, --threshold THRESHOLD
                        Threshold value for the match of percent of EXIF data and recipe (default: 85)
  -p, --print           Print result to console
  -d, --description     Insert result into image description
  -k, --keywords        Update image keywords with recipe and filmsimulation
```

### Supported cameras

Tested for X-T50 and X-S10. But every Fujifilm cameras with a X-sensor of generation V and IV should be working, too. 

## Installation

exiftool must be installed on your system.


### Examples

For the ricipes, the given file 'recipes.csv' is used (default name).

Print infos to console:
```console
$ python reciper.py  -p 770-X-T50.JPG
44/44 recipes imported.
Found 1 file(s).

770-X-T50.JPG
   Best fitting recipe (89%) and the image's deviation settings:
     Vibrant Arizona by Fuji X Weekly
       https://fujixweekly.com/2023/04/25/getting-a-wes-anderson-look-from-your-fujifilm-camera-4-new-film-simulation-recipes/
       ISO max           : 12800              (6400)              0%
       DRange Priority   : OFF                (STRONG)           33%
       Dynamic Range     : 100                (OFF)              66%
       Color             : 3                  (4)                88%

Processed all 1 image(s) successfully.
```

Write tags:
```console
$ python reciper.py  -k import/770-X-T50.JPG
44/44 recipes imported.
Found 1 file(s).

Processed all 1 image(s) successfully.
```
Result:
```console
$ exiftool -tagslist import/770-X-T50.JPG 
Tags List : Fuji-X/Color/Classic Chrome, Recipe/Fuji X Weekly/Vibrant Arizona
```

[!NOTE]
Both tag values use the hierarchy option. Existing values in this hierchy will be deleted.

Write descripion:
```console
$ python reciper.py -d import/1188-X-T50.jpg            
44/44 recipes imported.
Found 1 file(s).
    1 image files updated
Done.

Processed all 1 image(s) successfully.
```

Result:
```console
$ exiftool -b  -imagedescription  import/1188-X-T50.jpg            
Me an my dog.

--- Recipe info ---
1976 Kodak by Fuji X Weekly
https://fujixweekly.com/2023/08/03/1976-kodak-fujifilm-x-t5-x-trans-v-film-simulation-recipe/
Divergent settings:
- Highlights: 0 (1.5)
```

[!NOTE]
An existing description will not be overwritten. But all after `--- Recipe info ---` will be replaced.

Using wildcard...:
```console
$ python reciper.py -d import/*.jpg
```

...or multiple files:
```console
python reciper.py -d import/1188.jpg import/1139.jpg
```

Same result in both cases:
```console
44/44 recipes imported.
Found 2 file(s).
    1 image files updated
    1 image files updated

Processed all 2 image(s) successfully.
```


## Helpers

The script `converter.py` can be used as template to convert your own source of recipe data into the required input format.

