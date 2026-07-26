# recipetagger
A small set of tools to manage recipes for Fujfilm X cameras:

* **reciper.py** - Search best matching recipe for a Fujifilm X image. Optional update image's description and keyword.
* **customs.py** - Copies the recipes to customer settings files (`FP1`) for FUJIFILM X RAW STUDIO. Tested with X RAW Studio 1.25.0.1.
* **converter.py** - Example script to convert recipes into the import CSV-format.  

Recipes must be stored in a csv file. See example file `recipes.csv`. There are great sources for recipes, like the marvellous [Fuji X Weekly](https://fujixweekly.com). 

> [!NOTE]
> This software uses recipes published on the website 'Fuji X Weekly' by Ritchie Roesch and other sources. The name of the recipe and its settings have been carefully copied into this project. However, no responsibility is taken for the correctness, completeness and up-to-dateness.


The **reciper** script compares the exif data of one or more images with the recipes from the CSV file. The best matching recipe will be searched. If a recipe is found, that matchs better than the given threshold, the result can be written into the image description. You can also tag the image the recipe as keyword. 

In addition, the image can be tagged with the film simulation name.

The **customs** script creates for every recipe in the CSV file a `FP1` file. For this an existing FP1 file for your camera is needed as template file. Copy this files into your camera's sub directory of your _FUJIFILM X RAW STUDIO_ installation. For instance, on MacOS the directory is for X-T50 camera

```text
~/Library/Application Support/com.fujifilm.denji/X RAW STUDIO/X-T50/X-T50_0100
```

The **converter** script is a simple tool to convert recipes file from a properitary csv to the reciper's csv file format. Can be used as template for your specific converter. The created csv file is ready to import in recipes.py. Import CSV may not have spaces before or after the column values.

### reciper


#### Camera Compatibility

Tested for cameras X-T50 and X-S10. But every Fujifilm cameras with a X-sensor of generation V and IV should be working, too. But older camera models can have different setting/tag ranges and some settings/tags may not exists at all. For instance, the X-T30 doesn't have the exif tag `MakerNotes:BWMagentaGreen`. And the tag `MakerNotes:BlackImageTone` has a smaller range from -9..9 the X-T50 (-18..18).

#### Matching Qualitiy 

Comparing EXIF data of an specific image with settings of an recipe is not easy and not clear-cut.

The finding logic for the best matching recipe is based only on comparing values. To find the best matching recipe attributes are **weighted**. For instance the film simulation is more relevant than the sharpness value. The weighting is a subjective assessment. Future adjustments cannot be ruled out. 

The value **deviation** is a percentage value of the setting range. The setting range may vary for different models. For instance _BW Tone_ on X-T30 has a range from -9 to +9 (B & W Adjustment), on X-T50 the range is from -18 to +18 (Monochromatic Color warm/cool). 

The **recipes** can vary in precision. Not all setting values are always specified. They may or may not relate to a specific sensor generation.

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

### customs

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

### converter

```text
usage: converter.py [-h] [-i INPUT] [-o OUTPUT]

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input CSV file (Default: import/X-Recipes.csv).
  -o OUTPUT, --output OUTPUT
                        Output CSV file (Default: recipes.csv).
```


## Installation

Exiftool and Python 3 must be installed on your system. 

### Examples

#### reciper.py

For the recipes, the given file 'recipes.csv' is used (default name).

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

Selecting multiple image files by using wildcards:
```console
$ python reciper.py -d import/*.jpg
```

Selecting multiple files is possible, too:
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
If you have changed an image file with _FUJIFILM X RAW STUDIO_ you can just update the last modified file. For instance:

```console
find ~/Pictures -iname "*.j*"  | head -n1 | xargs python reciper.py -d -k 
```


Matching no recipe will also update the description:
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

#### customs.py

Example on MacOS for camera X-T50.

The script creates FP1 files for X-T50 camera. For this, an existing FP1 file from _FUJIFILM X RAW STUDIO_ has to be used as template. For instance you have saved a custom settings with the name _my-custom-settings_:

```console
cp ~/Library/Application\ Support/com.fujifilm.denji/X\ RAW\ STUDIO/X-T50/X-T50_0100/my-custom-settings.FP1 template.FP1
```

Check template file for the correct camera name:
```console
$ head -n 3 template.FP1 
<?xml version="1.0" encoding="utf-8"?>
<ConversionProfile application="XRFC" version="1.12.0.0">
    <PropertyGroup device="X-T50" version="X-T50_0100" label="Kodachrome 64">
```

Create FP1 files into directory `customs` (must exists):
```console
$ python customs.py -i recipes.csv -t template.FP1 -o customs/
```

Backup existing _FUJIFILM X RAW STUDIO_ settings (the name of the subdirectory may vary):
```console
$ mkdir ~/Library/Application\ Support/com.fujifilm.denji/X\ RAW\ STUDIO/X-T50/X-T50_0100_bak 
$ mv ~/Library/Application\ Support/com.fujifilm.denji/X\ RAW\ STUDIO/X-T50/X-T50_0100/* ~/Library/Application\ Support/com.fujifilm.denji/X\ RAW\ STUDIO/X-T50/X-T50_0100_bak/
```

Activate new settings:
```console
$ mv customs/* ~/Library/Application\ Support/com.fujifilm.denji/X\ RAW\ STUDIO/X-T50/X-T50_0100/
```

After re-opening the Fujifilm X-Raw Studio, the custom seettings for X-T50 are ready to use. 

HINT: In _FUJIFILM X RAW STUDIO_ _DR Priority_ = `Auto` can not be set to an image. So it is not possible to store this recipe value as custom setting to your camera with FUJIFILM X RAW STUDIO. Instead, the value must be set in the camera directly.

#### converter.py

Update recipes from my local Tap Forms Pro formular _X-Rezepte_.

<a id="export_from_tap_forms_pro"></a>
##### Export from Tap Forms Pro

First export formular _X-Rezepte_ in Tap Forms Pro by calling Dialog _Datensätze exportieren_ from _Datei > Exportieren > Datensätze (CSV, Excel)..._ 
The settings are stored as Template `recipetagger` with this settings:

Parameter|Wert
---|---
Exportieren als | CSV
Dateikodierung  | Unicode (UTF-8)
Spaltentrenner  | Tabulator
Zeilenende      | Unix (LF)
Zahlenformat    | kein Stil
Datumsformat    | MM/dd/yyyy
Zeitformat      | h:mm a
Datensatz-ID exportieren         | nein
Feldtyp Schlagwörter             | nein
Verlinkte Datensätze exportieren | nein
Medien exportieren               | nein

And following fields (Felder):

| Exportieren|Type|Feldname
| :-:|---|---
|   | f(x)   | Name
| X | A      | Bezeichnung
| X | Bool   | Draft
| X | A      | Film Simulation
|   | Bild   | Bild
|   | A      | Film
| X | A      | X-Trans
| X | A      | Publisher
|   | Note   | Desciption
| X | URL    | Website
|   | Bool   | B/W
|   | A      | Filter
| X | A      | BW Color WC
| X | A      | BW Color MC
| X | A      | Grain Effect
| X | A      | CCR Effect
| X | A      | CCR FX Blue
| X | A      | White Balance
| X | 123    | Kelvin
|   | f(x)   | WB Info
| X | A      | White Balance R
| X | A      | White Balance B
| X | A      | Dynamic Range
| X | A      | Dynamic Range Priority
|   | f(x)   | Dynamic Range Info
| X | A      | Highlights
| X | A      | Shadows
| X | A      | Color
| X | A      | Sharpness
| X | A      | High ISI NR
| X | A      | Clarity
| X | 123    | ISO min
| X | 123    | ISO max
|   | A      | Exposure Compensation
|   | A      | Double Exposer
|   | A      | Double Exposer Hint

Press **[Exportieren]** and save it in file `~/dev/recipetagger/import/X-Rezepte.csv`. Existing file will be overwritten.

Now the recipetagger can be updated with it:

```text
python converter.py -i import/X-Rezepte.csv -o recipes.csv 
```

# Cheat Sheet

## Tag description and tags for the 10 newest "jpg"-images and check for 95% matching treshold

```zsh
find ~/pictures -type f -iname "*.jpg" -print0 | xargs -0 ls -t | head -n10 | xargs python reciper.py -t 95 -d -k 
```

## Tag description and tags jpeg-images with all possible suffixes (jpg, JPG, jpeg, JPEG)

```zsh
find ~/pictures -type f \( -iname "*.jpg" -or -iname "*.jpeg" \) -print0 | xargs -0 ls -t  | xargs python reciper.py  -d -k 
```

## All toghter

```zsh
find ~/pictures -type f \( -iname "*.jpg" -or -iname "*.jpeg" \) -print0 | xargs -0 ls -t | head -n10 | xargs python reciper.py -t 95 -d -k 
```


## Update recipes from Tap Forms Pro-Formular. 

### Short

```zsh
    cd /Users/chris/dev/recipetagger  
    source venv/bin/activate
```
```zsh
    x_root=~/Library/Application\ Support/com.fujifilm.denji/X\ RAW\ STUDIO/X-T50 && \
    x_camdir=$x_root/X-T50_0100 && \
    x_bak=${x_camdir}_bak && \
    python converter.py -i import/X-Rezepte.csv -o recipes.csv && \
rm -rf customs && mkdir customs && \
python customs.py -i recipes.csv -t template.FP1 -o customs/  && \
rm -rf $x_bak && \
mkdir $x_bak && \
mv $x_camdir/* $x_bak && \
mv customs/* $x_camdir/ 
```
 

### Step by step

Replace all _User Profiles_ from the recipes formular in Tap Forms Pro.

1. Prepare python environment and set your specific path variables: 
```zsh
    cd /Users/chris/dev/recipetagger  
    source venv/bin/activate
```
Set OS and camera dependend path variables:

```zsh
    x_root=~/Library/Application\ Support/com.fujifilm.denji/X\ RAW\ STUDIO/X-T50 && \
    x_camdir=$x_root/X-T50_0100 && \
    x_bak=${x_camdir}_bak 
```

All operations will be done here in the directory `recipetagger`.

2. Export from Tap Forms Pro

See [Export from Tap Forms Pro](#export_from_tap_forms_pro). The exported data will be saved into file `import/X-Rezepte.csv`. 

3. Convert into script's format:

```zsh
python converter.py -i import/X-Rezepte.csv -o recipes.csv 
```   
Now the data are in `recipes.csv`.

4. Prepare blank output directory for profile files:

```zsh
rm -rf customs && mkdir customs
```   
Now `customs/` exists and is empty.

5. Create user profile files

Create user profile file for every recipe:

```zsh
python customs.py -i recipes.csv -t template.FP1 -o customs/ 
``` 

Now in `customs\` are the `FP1` files.

6. Move profile files to FUJIFILM X RAW STUDIO

Delete all existing profiles and replace them with new ones.

```zsh
rm -rf $x_bak && \
mkdir $x_bak && \
mv $x_camdir/* $x_bak && \
mv customs/* $x_camdir/
```   
Now all `FP1` files are in the _FUJIFILM X RAW STUDIO_ directory and previous files are backed up.

Check result:

```zsh
ls -l $x_camdir
```
All `FP1` files should be listed here. 

Restart _FUJIFILM X RAW STUDIO_ to make them visible.
