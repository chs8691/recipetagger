import argparse
import csv
import constants.recipefields as R
import constants.filmsimulations as FS
import constants.grain as G
import constants.colorchrome as CC
import constants.dynamicrangepriority as DP
import constants.dynamicrange as DR
import constants.whitebalance as WB
import constants.sensor as SR

# exiftool must be installed on the system
from exiftool import ExifToolHelper

args=None

recipies = [] 

def log(message):
    """Logs to console in verbose mode"""

    # In unit tests args is None
    if(args is None or args.verbose):
        print(message)
 
def vvlog(message):
    """Logs to console in very verbose mode"""

    # In unit tests args is None
    if(args is None or args.vverbose):
        print(message)

def err(message):
    """Print message an exit with '1'"""
    print(f"ERROR {message}")
    exit(1)

def parse_args():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', help='Increase output verbosity.', action="store_true")
    parser.add_argument('-vv', '--vverbose', help='Increase output very verbosity.', action="store_true")
    parser.add_argument('-r', '--recipies', type=str, nargs=1, default='X-Recipies.csv',
                        help='Update recipies from CSV file (Default: %(default)s) and store them in the internal Storage. See example file for columns names. ')
    parser.add_argument('filename', metavar='FILENAME', type=str, nargs=1,
                    help='Image file name')
    
    args = parser.parse_args()


def map_exif_filmsimulation(value):
    """Parse integer value and return value of constants.filmsimulations or, if no match, None. 
    This interger is the value stored in EXIF information MakerNotes:FilmMode.
    Not all existing values are supported (returns None).

    Exiftool: use '-n' to see the unconverted value<br>
    There is a lookup table dcumentented in https://exiftool.org/TagNames/FujiFilm.html  <br>
        0x0   = F0/Standard (Provia) <br>
        0x100 = F1/Studio Portrait <br>
        0x110 = F1a/Studio Portrait Enhanced Saturation <br>
        0x120 = F1b/Studio Portrait Smooth Skin Tone (Astia) <br>
        0x130 = F1c/Studio Portrait Increased Sharpness <br>
        0x200 = F2/Fujichrome (Velvia) <br>
        0x300 = F3/Studio Portrait Ex <br>
        0x400 = F4/Velvia <br>
        0x500 = Pro Neg. Std <br>
        0x501 = Pro Neg. Hi <br>
        0x600 = Classic Chrome <br>
        0x700 = Eterna <br>
        0x800 = Classic Negative <br>
        0x900 = Bleach Bypass <br>
        0xa00 = Nostalgic Neg <br>
        0xb00 = Reala ACE <br>
    """

    match hex(value):
        case '0x0':
            return FS.PROVIA
        case '0x100':
            return None #"Studio Portrait"
        case 'v110':
            return None #"Studio Portrait Enhanced Saturation"
        case '0x120':
            return FS.ASTIA
        case '0x130':
            return None #"Studio Portrait Increased Sharpness"
        case '0x200':
            return None #"F2/Fujichrome (Velvia)"
        case '0x300':
            return None #"Studio Portrait Ex"
        case '0x400':
            return FS.VELVIA
        case '0x500':
            return FS.PRO_NEG_STD
        case '0x501':
            return FS.PRO_NEG_HI
        case '0x600':
            return FS.CLASSIC_CHROME
        case '0x700':
            return FS.ETERNA
        case '0x800':
            return FS.CLASSIC_NEG
        case '0x900':
            return FS.ETERNA_BLEACH_BYPASS
        case '0xa00':
            return FS.NOSTALGIC_NEG
        case '0xb00':
            return FS.REALA_ACE
        
    return None




def map_filmsimulation(value):
    """Parse String value from recipe and return value of constants.filmsimulations or, if no match, None. """

    value=value.upper().replace('.','').replace(' ', '')

    if 'PROVIA' in value:
        return FS.PROVIA
    elif 'VELVIA' in value:
        return FS.VELVIA
    elif 'ASTIA' in value:
        return FS.ASTIA
    elif 'CLASSICCHROME' in value:
        return FS.CLASSIC_CHROME
    elif 'REALAACE' in value:
        return FS.REALA_ACE
    elif 'PRONEGHI' in value:
        return FS.PRO_NEG_HI
    elif 'PRONEGSTD' in value:
        return FS.PRO_NEG_STD
    elif 'CLASSICNEG' in value:
        return FS.CLASSIC_NEG
    elif 'NOSTALGICNEG' in value:
        return FS.NOSTALGIC_NEG
    elif 'ETERNABLEACHBYPASS' in value:
        return FS.ETERNA_BLEACH_BYPASS
    elif 'ETERNA' in value:
        return FS.ETERNA
    elif 'ACROS' in value:
        return FS.ACROS
    elif 'MONOCHROME' in value:
        return FS.MONOCHROME
    elif 'SEPIA' in value:
        return FS.SEPIA
    else:
        return None
    

def import_recipies(filename):
    """CSV file import from CSV file. Returns list with recipies"""
    
    log(f'Importing recipies from {filename}')

    recipies = []

    with open(filename, newline='') as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')


        row_count = 0
        for row in spamreader:
            row_count += 1
            # log(f'  {row}')
            recipe = extract_recipe_data(row)

            vvlog(recipe)
            recipies.append(recipe)


    print(f'{len(recipies)}/{row_count} recipies imported.')

    return recipies


def extract_recipe_data(row):
    """Extract relevant fields for the imported recipe row and convert them into recipe format. Returns dict with recipe."""
    
    field=''

    # log(f'  {row}')
    recipe = dict()


    field='Name'
    value = row[field].strip()
    if len(value) == 0:
        print(f'Recipe: Missing field: "{field}" - recipe will be ignored')
        return None

    recipe[R.NAME] = value
    

    field = 'Publisher'
    value = row[field].strip()
    recipe[R.PUBLISHER] = value
    

    field='Film Simulation'
    value=row[field]
    
    recipe[R.FILMSIMULATION] = map_filmsimulation(value)

    if recipe[R.FILMSIMULATION] is None:
        print(f'Unknown film simulation: {row[field]} - recipe {recipe[R.NAME]} will be ignored')
        return None


    if recipe[R.FILMSIMULATION] == FS.ACROS or recipe[R.FILMSIMULATION] == FS.MONOCHROME:

        field = 'BW Color WC'
        if len(row[field]) > 0:
            value=int(row[field])
        else:
            value = 0
        recipe[R.BW_COLOR_WC] = value

        field = 'BW Color MC'
        if len(row[field]) > 0:
            value=int(row[field])
        else:
            value = 0
        recipe[R.BW_COLOR_MC] = value


    field = 'Grain Effect'
    value=row[field].upper().strip()

    if 'WEAK' in value and 'SMALL' in value:
        recipe[R.GRAIN_EFFECT] = G.WEAK_SMALL
    elif 'WEAK' in value and 'LARGE' in value:
        recipe[R.GRAIN_EFFECT] = G.WEAK_LARGE
    elif 'STRONG' in value and 'SMALL' in value:
        recipe[R.GRAIN_EFFECT] = G.STRONG_SMALL
    elif 'STRONG' in value and 'LARGE' in value:
        recipe[R.GRAIN_EFFECT] = G.STRONG_LARGE
    else:
        recipe[R.GRAIN_EFFECT] = G.OFF


    field = 'CCR Effect'
    value=row[field].upper().strip()

    if value == 'WEAK':
        recipe[R.CCR_EFFECT] = CC.WEAK
    elif value == 'STRONG':
        recipe[R.CCR_EFFECT] = CC.STRONG
    else:
        recipe[R.CCR_EFFECT] = CC.OFF
    

    field = 'CCR FX Blue'
    value=row[field].upper().strip()

    if value == 'WEAK':
        recipe[R.CCRFX_BLUE] = CC.WEAK
    elif value == 'STRONG':
        recipe[R.CCRFX_BLUE] = CC.STRONG
    else:
        recipe[R.CCRFX_BLUE] = CC.OFF


    field='White Balance'            
    value=row[field].upper().replace('.','').replace(' ', '')
    if 'WHITEPRIORITY' in value:
        recipe[R.WHITE_BALANCE] = WB.WHITE_PRIORITY
    elif 'AMBIENCEPRIORITY' in value:
        recipe[R.WHITE_BALANCE] = WB.AMBIENCE_PRIORITY
    elif 'KELVIN' in value:
        recipe[R.WHITE_BALANCE] = WB.KELVIN
    elif 'DAYLIGHT' in value:
        recipe[R.WHITE_BALANCE] = WB.DAYLIGHT
    elif 'SHADE' in value:
        recipe[R.WHITE_BALANCE] = WB.SHADE
    else:
        recipe[R.WHITE_BALANCE] = WB.AUTO


    field='White Balance R'            
    if len(row[field]) > 0:
        value=int(row[field])
    else:
        value = 0
    recipe[R.WHITE_BALANCE_R] = value

    field='White Balance B'            
    if len(row[field]) > 0:
        value=int(row[field])
    else:
        value = 0
    recipe[R.WHITE_BALANCE_B] = value

    field = 'Dynamic Range Priority'
    value=row[field].upper().strip()

    if value == 'WEAK':
        recipe[R.DYNAMIC_RANGE_PRIORITY] = DP.WEAK
    elif value == 'STRONG':
        recipe[R.DYNAMIC_RANGE_PRIORITY] = DP.STRONG
    else:
        recipe[R.DYNAMIC_RANGE_PRIORITY] = DP.OFF
    
    if recipe[R.DYNAMIC_RANGE_PRIORITY] == DP.OFF:

        field = 'Dynamic Range'
        value=row[field].upper()

        if '100' in value:
            recipe[R.DYNAMIC_RANGE] = DR.DR100
        elif '200' in value:
            recipe[R.DYNAMIC_RANGE] = DR.DR200
        elif '400' in value:
            recipe[R.DYNAMIC_RANGE] = DR.DR400
        else:
            recipe[R.DYNAMIC_RANGE] = DR.AUTO
        
        field = 'Highlights'
        if len(row[field]) > 0:
            value=float(row[field])
        else:
            value = 0
        recipe[R.HIGHLIGHTS] = value

        field = 'Shadows'
        if len(row[field]) > 0:
            value=float(row[field])
        else:
            value = 0
        recipe[R.SHADOWS] = value

    field = 'Sharpness'
    if len(row[field]) > 0:
        value=int(row[field])
    else:
        value = 0
    recipe[R.SHARPNESS] = value
    
    field = 'Color'
    if len(row[field]) > 0:
        value=int(row[field])
    else:
        value = 0
    recipe[R.COLOR] = value

    field = 'High ISO NR'
    if len(row[field]) > 0:
        value=int(row[field])
    else:
        value = 0
    recipe[R.HIGH_ISONR] = value

    field = 'Clarity'
    if len(row[field]) > 0:
        value=int(row[field])
    else:
        value = 0
    recipe[R.CLARITY] = value

    field = 'ISO min'
    if len(row[field]) > 0:
        value=int(row[field])
    else:
        value = 0
    recipe[R.ISO_MIN] = value

    field = 'ISO max'
    if len(row[field]) > 0:
        value=int(row[field])
    else:
        value = 0
    recipe[R.ISO_MAX] = value

    field = 'X-Trans'
    value=row[field].upper().strip()

    if 'III' == value:
        recipe[R.XTRANS_VERSION] = SR.X_III
    if 'IV' == value:
        recipe[R.XTRANS_VERSION] = SR.X_IV
    if 'V' == value:
        recipe[R.XTRANS_VERSION] = SR.X_V

    return recipe

def read_file(filename):
    """Works for Fujifilm X-T50. Returns dictionary with all recipe fields."""
    log(f'Readin Image file {filename}')

    exif = dict()

    with ExifToolHelper() as et:
        for d in et.get_metadata(filename):

            for k, v in d.items():
                print(f"Dict: {k} = {v}")   
        
            field='MakerNotes:FilmMode'
            value=d[field]
            print(f'{field}={value}')
            # Color film only; not existing for monochromatic films
            if(field in d):   
                exif[R.FILMSIMULATION] = map_exif_filmsimulation(d[field])
            
            # Monochromatic film only (ACROS, MONOCHROMATIC)
            else:
                field='MakerNotes:BWAdjustment'                # Monochromatic Color warm/cool
                exif[field.removeprefix('MakerNotes')]=d[field]
                field='MakerNotes:BWMagentaGreen'              # Monochromatic Color magenta/green
                exif[field.removeprefix('MakerNotes')]=d[field]
            
            field='MakerNotes:Sharpness'
            exif[field.removeprefix('MakerNotes')]=d[field]
            
            field='MakerNotes:GrainEffectRoughness'           
            exif[field.removeprefix('MakerNotes')]=d[field]
            field='MakerNotes:GrainEffectSize'           
            exif[field.removeprefix('MakerNotes')]=d[field]
            field='MakerNotes:ColorChromeEffect'             
            exif[field.removeprefix('MakerNotes')]=d[field]
            field='MakerNotes:ColorChromeFXBlue'            
            exif[field.removeprefix('MakerNotes')]=d[field]
            field='MakerNotes:WhiteBalance'          
            exif[field.removeprefix('MakerNotes')]=d[field]

            field='MakerNotes:ColorTemperature'      
            if(field in d):           
                exif[field.removeprefix('MakerNotes')]=d[field]
    
            field='MakerNotes:WhiteBalanceFineTune'        
            exif[field.removeprefix('MakerNotes')]=d[field]
            field='MakerNotes:DynamicRange'          
            exif[field.removeprefix('MakerNotes')]=d[field]
            field='MakerNotes:DynamicRangeSetting' 
            exif[field.removeprefix('MakerNotes')]=d[field]
            field='MakerNotes:HighlightTone'             
            exif[field.removeprefix('MakerNotes')]=d[field]
            field='MakerNotes:ShadowTone'                
            exif[field.removeprefix('MakerNotes')]=d[field]
            field='MakerNotes:Sharpness'              
            exif[field.removeprefix('MakerNotes')]=d[field]
            field='MakerNotes:Saturation'                    # Color value or ACROS etc.   
            exif[field.removeprefix('MakerNotes')]=d[field]
            field='MakerNotes:NoiseReduction'            
            exif[field.removeprefix('MakerNotes')]=d[field]
            field='MakerNotes:Clarity'
            exif[field.removeprefix('MakerNotes')]=d[field]

    # img = Image(filename)
    # img.read_exif()
    # img.close()
    # vvlog(exif)
    return exif


def process():
    
    global recipies

    recipies = import_recipies(args.recipies[0])

    exif_dict=read_file(args.filename[0])

    

def main():

    log('Verbose mode')
    parse_args()
    process()



if __name__ == '__main__':
    main()
