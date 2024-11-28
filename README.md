# recipetagger
A small set of tools to manage recipes for Fujfilm X cameras:

* Search best matching recipe for a Fujifilm X image. Optional update image's description and keyword.
* Create customer settings files from recipes.

Recipes are stored as csv file. See example file `recipes.csv`. There are great sources for recipes, like the marvellous [Fuji X Weekly](https://fujixweekly.com). 

> [!NOTE]
> This software uses recipes published on the website 'Fuji X Weekly' by Ritchie Roesch and other sources. The name of the recipe and its settings have been carefully copied into this project. However, no responsibility is taken for the correctness, completeness and up-to-dateness.


The script compares the exif data of one or more images with the recipes from the CSV file. The best matching recipe will be searched. If a recipe is found, that matchs better than the given threshold, the result can be written into the image description. You can also tag the image the recipe as keyword. 

In addition, the image can be tagged with the film simulation name.

### man

#### reciper
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

#### customs

Recipes to custom settings for Fujifilm X Ras Studio. 

```text
usage: customs.py [-h] [-i INPUT] [-t TEMPLATE] [-o OUTDIR] [-v] [-vv]

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input CSV file with recipes (default: recipes.csv).
  -t TEMPLATE, --template TEMPLATE
                        Template file, creating based on. Only recpipe fields will be changed.
  -o OUTDIR, --outdir OUTDIR
                        Output directory
  -v, --verbose         Increase output verbosity.
  -vv, --vverbose       Increase output very verbosity.
  ```

#### converter

Simple tool to convert recipes file from a properitary csv to the reciper's csv file format. Can be used as template for other converter.
The created csv file is ready to import in recipes.py
Import CSV may not have spaces before or after the column values.

```text
(venv) ➜  recipetagger git:(main) ✗ python converter.py -h
usage: converter.py [-h] [-i INPUT] [-o OUTPUT]

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input CSV file (Default: import/X-Recipes.csv).
  -o OUTPUT, --output OUTPUT
                        Output CSV file (Default: recipes.csv).
```

### Camera Compatibility

Tested for cameras X-T50 and X-S10. But every Fujifilm cameras with a X-sensor of generation V and IV should be working, too. But older camera models can have different setting/tag ranges and some settings/tags may not exists at all. For instance, the X-T30 doesn't have the exif tag `MakerNotes:BWMagentaGreen`. And the tag `MakerNotes:BlackImageTone` has a smaller range from -9..9 the X-T50 (-18..18).

### Matching Qualitiy 

Comparing EXIF data of an specific image with settings of an recipe is not easy and not clear-cut.

The finding logic for the best matching recipe is based only on comparing values. To find the best matching recipe attributes are **weighted**. For instance the film simulation is more relevant than the sharpness value. The weighting is a subjective assessment. Future adjustments cannot be ruled out. 

The value **deviation** is a percentage value of the setting range. The setting range may vary for different models. For instance _BW Tone_ on X-T30 has a range from -9 to +9 (B & W Adjustment), on X-T50 the range is from -18 to +18 (Monochromatic Color warm/cool). 

The **recipes** can vary in precision. Not all setting values are always specified. They may or may not relate to a specific sensor generation.


## Installation

exiftool must be installed on your system.


### Examples

#### reciper

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

> [!NOTE]
> Both tag values are hierarchical. Existing values in this hierarchy are deleted.

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

> [!NOTE]
> An existing description will not be overwritten. But all after `--- Recipe info ---` will be replaced.

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

No matching result updates the description, too:
```console
$ python reciper.py -t=100 -d 1188-X-T50.jpg 
44/44 recipes imported.
Found 1 file(s).
    1 image files updated

Processed all 1 image(s) successfully.
```

Result:
```console
$ exiftool -b  -imagedescription  1188-X-T50.jpg
Me an my dog.

--- Recipe info ---
Filmsimulation: NOSTALGIC_NEG
Grain Effect: STRONG/SMALL
CCR Effect: STRONG
White Balance: AUTO
White Balance R: -2.0
White Balance B: -4.0
Dynamic Range: 200
Shadows: 3
Sharpness: -2
High ISO NR: -4
Clarity: -3.0
ISO: 640%    
```

#### customs

Example on MacOS for camera X-T50.

Create FP1 files for X-T50 camera. For this, an FP1 file has been exported from Fujifilm X Raw Studio.

Check template file for the correct camera name:
```console
$ head -n 3 template.FP1 
<?xml version="1.0" encoding="utf-8"?>
<ConversionProfile application="XRFC" version="1.12.0.0">
    <PropertyGroup device="X-T50" version="X-T50_0100" label="Kodachrome 64">
```

Create FP1 files into new directory `customs`:
```console
$ mkdir customs
$ python customs.py -i recipes.csv -t template.FP1 -o customs/
```

Backup existing Fujifilm X Raw Studio settings (the name of the subdirectory may vary):
```console
$ mv ~/Library/Application\ Support/com.fujifilm.denji/X\ RAW\ STUDIO/X-T50/X-T50_0100 ~/Library/Application\ Support/com.fujifilm.denji/X\ RAW\ STUDIO/X-T50/X-T50_0100_bak
```

Activate new settings:
```console
$ mv customs/ ~/Library/Application\ Support/com.fujifilm.denji/X\ RAW\ STUDIO/X-T50/X-T50_0100/
```

After re-opening the Fujifilm X-Raw Studio, the custom seettings for X-T50 are ready to use.
