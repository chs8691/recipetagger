import argparse
import csv
import exifing as ex
import reciping as rp
import constants.recipefields as R
import constants.whitebalance as WB
import constants.filmsimulations as FS
import constants.grain as GR
import constants.colorchrome as CC
from os import path
from os import listdir

# exiftool must be installed on the system
from exiftool import ExifToolHelper

args=None

recipes = [] 

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
    parser.add_argument('-r', '--recipes', type=str, nargs=1, default='recipes.csv',
                        help='Update recipes from CSV file (Default: %(default)s) and store them in the internal Storage. See example file for columns names. ')
    parser.add_argument('-p', '--print', action='store_true',
                        help='Print result to console')
    parser.add_argument('path', metavar='PATH', type=str, nargs=1,
                    help='Path to image file(s). Only JPG files will be processed. Can be a directory or a single file name. Wildcards are not supported.')
    
    args = parser.parse_args()


def import_recipes(filename):
    """CSV file import from CSV file. Returns list with recipes"""
    
    log(f'Importing recipes from {filename}')

    recipes = []

    with open(filename, newline='') as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')

        row_count = 0
        for row in spamreader:
            row_count += 1
            # log(f'import_recipes:  {row}')
            recipe = rp.extract_data(row)

            vvlog(recipe)
            recipes.append(recipe)


    print(f'{len(recipes)}/{row_count} recipes imported.')

    return recipes




def read_file(filename):
    """Works for Fujifilm X-T50. Returns dictionary with all recipe fields.
    Returns None in error case. 
    """
    log(f'Readin Image file {filename}')

    exif = dict()
    exif[R.NAME] = filename

    with ExifToolHelper() as et:
        for d in et.get_metadata(filename):

            for k, v in d.items():
                vvlog(f"Dict: {k} = {v}")   
        
            field='MakerNotes:FilmMode'
            # Color film; not existing for monochromatic films
            if(field in d):   
        
                value=d[field]
                vvlog(f'{field}={value}')
        
                exif[R.FILMSIMULATION] = ex.map_filmsimulation(d[field])

                field='MakerNotes:Saturation'         
                exif[R.COLOR]=ex.map_saturation(d[field])
            
            # Monochromatic film (ACROS, MONOCHROME, SEPIA)
            else:

                field='MakerNotes:Saturation'         # Color value or ACROS etc.  
                value = None 
                (exif[R.FILMSIMULATION], value)=ex.map_saturation(d[field])
                
                if value is not None:
                    exif[R.BW_FILTER] = value

                if exif[R.FILMSIMULATION] != FS.SEPIA:
                    field='MakerNotes:BWAdjustment'    # Monochromatic Color warm/cool
                    exif[R.BW_COLOR_WC] = d[field]
                    field='MakerNotes:BWMagentaGreen'  # Monochromatic Color magenta/green
                    exif[R.BW_COLOR_MC] = d[field]
            
            field='MakerNotes:Sharpness'
            exif[R.SHARPNESS] = ex.map_sharpness(d[field])
            
            exif[R.GRAIN_EFFECT] = ex.map_grain(
                d['MakerNotes:GrainEffectRoughness'],
                d['MakerNotes:GrainEffectSize']
            )

            field='MakerNotes:ColorChromeEffect'             
            exif[R.CCR_EFFECT] = ex.map_color_chrome(d[field])

            field='MakerNotes:ColorChromeFXBlue'             
            exif[R.CCRFX_BLUE] = ex.map_color_chrome(d[field])

            field='MakerNotes:WhiteBalance'          
            exif[R.WHITE_BALANCE] = ex.map_whitebalance(d[field])

            field='MakerNotes:ColorTemperature'      
            if(exif[R.WHITE_BALANCE] == WB.KELVIN):           
                exif[R.KELVIN] = d[field]
    
            field='MakerNotes:WhiteBalanceFineTune'
            if field not in d:
                log(f'ERROR Field {field} not found.')
                return None
            (value, value2) = ex.map_wb_finetune(d[field])
            exif[R.WHITE_BALANCE_R] = value
            exif[R.WHITE_BALANCE_B] = value2

            field='MakerNotes:DRangePriority' # Auto (0) or Fixed (1)

            # DRange Proirity
            if field in d:
                field='MakerNotes:DRangePriorityAuto' 
                field2='MakerNotes:DRangePriorityFixed' 
                if field in d:
                    exif[R.DRANGE_PRIORITY]=ex.map_drange_priority(d[field])
                elif field2 in d:
                    exif[R.DRANGE_PRIORITY]=ex.map_drange_priority(d[field2])
    
            # No DRange Priority
            else:
                field='MakerNotes:DynamicRangeSetting'
                if  d[field] == 0: # Auto
                    field2='MakerNotes:AutoDynamicRange'
                    exif[R.DYNAMIC_RANGE] = ex.map_dynamic_range(d[field2])
                elif d[field] == 1: # Manuel
                    field2='MakerNotes:DevelopmentDynamicRange'
                    exif[R.DYNAMIC_RANGE] = ex.map_dynamic_range(d[field2])
                else:
                    print(f'ERROR Unknown value for {field}: {d[field]}')
                    return None
                
                field='MakerNotes:HighlightTone'
                exif[R.HIGHLIGHTS] = d[field]
                field='MakerNotes:ShadowTone'
                exif[R.SHADOWS] = d[field]
              
            field='MakerNotes:NoiseReduction'            
            exif[R.HIGH_ISONR]=ex.map_noisereduction(d[field])

            field='MakerNotes:Clarity'
            exif[R.CLARITY]=ex.map_clarity(d[field])

            field='EXIF:ISO'
            exif[R.ISO]=d[field]

        log(exif)
    return exif


def find_recipe(exif, recipes):
    """"Create sorted result list. Return None in error case."""

    results = []
    for r in recipes:
        res = check_recipe(exif, r)
        if res is not None:
            results.append(res)
        else:
            log('ERROR check_recipe() returned \'None\'.')
            return None

    results.sort(key=lambda a: a[0], reverse=True)
    log('find_recipe()')
    log(results)

    return results


def check_recipe(exif, recipe):
    """ Compare image exifs data wth recipe's data to find differences and calculate a
        total score percentage value.
        Returns tuple with three values:
        - score pertance value (0..100)
        - Name of the recipe
        - list with four value tuple:
          - score (0..99)
          - Field name
          - exif value
          - recipe value
        Example: ( 90, [R.COLOR, R.SHARPNESS] )
        Every single score will be weightend between 0..10. For instance FILMSIMULATION
        is very important: weight=10
    """
    failed = []
    total = 0
    max_total = 0
    MAX = 100

    if exif is None:
        log('ERROR exif is \'None\'.')
        return None

    field = R.FILMSIMULATION
    weight = 10
    act = rate_fs(exif[field], recipe[field])
    total += act * weight
    max_total += MAX * weight
    if act < MAX:
        failed.append((act, field, exif[field], recipe[field]))

    field = R.GRAIN_EFFECT
    weight = 3
    act =  rate_range(0, 4, grain_as_int(exif[field]), grain_as_int(recipe[field]))
    total += act * weight
    max_total += MAX * weight
    if act < MAX:
        failed.append((act, field, exif[field], recipe[field]))

    field = R.CCR_EFFECT
    weight = 2
    act =  rate_range(0, 2, cc_as_int(exif[field]), cc_as_int(recipe[field]))
    total += act * weight
    max_total += MAX * weight
    if act < MAX:
        failed.append((act, field, exif[field], recipe[field]))

    field = R.CCRFX_BLUE
    weight = 2
    act =  rate_range(0, 2, cc_as_int(exif[field]), cc_as_int(recipe[field]))
    total += act * weight
    max_total += MAX * weight
    if act < MAX:
        failed.append((act, field, exif[field], recipe[field]))

    field = R.SHARPNESS
    weight = 1
    act = rate_range(-4, +4, exif[field], recipe[field])
    total += act * weight
    max_total += MAX * weight
    if act < MAX:
        failed.append((act, field, exif[field], recipe[field]))

    field = R.HIGH_ISONR
    weight = 2
    act = rate_range(-4, +3, exif[field], recipe[field])
    total += act * weight
    max_total += MAX * weight
    if act < MAX:
        failed.append((act, field, exif[field], recipe[field]))

    field = R.CLARITY
    weight = 5
    act = rate_range(-4, 5, exif[field], recipe[field])
    total += act * weight
    max_total += MAX * weight
    if act < MAX:
        failed.append((act, field, exif[field], recipe[field]))


    bws=[FS.ACROS, FS.MONOCHROME]
    if exif[R.FILMSIMULATION] in bws and recipe in bws:

        field = R.BW_COLOR_WC
        weight = 1
        act = rate_range(-18, +18, exif[field], recipe[field])
        total += act * weight
        max_total += MAX * weight
        if act < MAX:
            failed.append((act, field, exif[field], recipe[field]))

        field = R.BW_COLOR_MC
        weight = 1
        act = rate_range(-18, +18, exif[field], recipe[field])
        total += act * weight
        max_total += MAX * weight
        if act < MAX:
            failed.append((act, field, exif[field], recipe[field]))

    elif exif[R.FILMSIMULATION] not in bws and recipe[R.FILMSIMULATION] not in bws:
        # print(f'CHECKER exif:{exif[R.FILMSIMULATION]}, recipe:{recipe[R.FILMSIMULATION]}')
        field = R.COLOR
        weight = 1
        act = rate_range(-4, +4, exif[field], recipe[field])
        total += act * weight
        max_total += MAX * weight
        if act < MAX:
            failed.append((act, field, exif[field], recipe[field]))

    # No points for film mismatch of Color and B/W comparison
    else:
        weight = 1
        act = 0

        exifval = None
        recipeval = None
        if field in exif:
            exifval = exif[field]
        if field in recipe:
            recipeval = recipe[field]

        field = R.COLOR
        total += act * weight
        max_total += MAX * weight
        if act < MAX:
            failed.append((act, field, exifval, recipeval))

        field = R.BW_COLOR_WC
        total += act * weight
        max_total += MAX * weight
        if act < MAX:
            failed.append((act, field, exifval, recipeval))

        field = R.BW_COLOR_MC
        total += act * weight
        max_total += MAX * weight
        if act < MAX:
            failed.append((act, field, exifval, recipeval))


    failed.sort(key=lambda a: a[0])

    return (int(100 / max_total * total), recipe[R.NAME], failed)



def grain_as_int(value):
    """Interprates GRAIN value as integer for better compareness.
    Return interger 0 (OFF) ... 4 (STRONG/LARGE)"""
        
    if value == GR.WEAK_SMALL:
        return 1
    
    elif value == GR.WEAK_LARGE:
        return 2

    elif value == GR.STRONG_SMALL:
        return 3
    
    elif value == GR.STRONG_LARGE:
        return 4

    return 0


def cc_as_int(value):
    """Interprates Color Chrome Effect/Blue value as integer for better compareness.
    Return interger 0 (OFF) .. 2 (STRONG)"""
        
    if value == CC.WEAK:
        return 1
    
    elif value == CC.STRONG:
        return 2

    return 0


def rate_range(min, max, evalue, rvalue):
    """Returns integer 0 (no match) .. 100 (total match) 
        Range: min .. max. Can include 0 as valid value, e.g. -4..5
        min: can be < 0
        max: must be > 0
    """

    # Include 0 as value
    max = abs(min) + max + 1 

    diff = abs(evalue - rvalue)

    return int(100 / max * (max - diff))


def rate_fs(evalue, rvalue):
    """Returns integer 0 (no match) .. 100 (total match) """
    
    if evalue == rvalue:
        return 100
    
    fs = [FS.ACROS, FS.MONOCHROME]
    if evalue in [fs] and rvalue in [fs]:
        return 80
    
    fs = [FS.ASTIA, FS.PROVIA]
    if evalue in [fs] and rvalue in [fs]:
        return 80

    fs = [FS.PRO_NEG_HI, FS.REALA_ACE, FS.CLASSIC_CHROME]
    if evalue in [fs] and rvalue in [fs]:
        return 70
    
    fs = [FS.CLASSIC_NEG, FS.NOSTALGIC_NEG, FS.ETERNA]
    if evalue in [fs] and rvalue in [fs]:
        return 30
    
    return 0


def report(filename, res):
    """Print result to the console.
    res: Ascending list of rated recipes.
    """
    
    print(f'\n{path.basename(filename)}')

    if len(res) == 0:
        print('  No match found :o(')
        return

    item = res[0]

    if item[0] == 100:
        print(f'   Complete fitting recipe: {item[1]}')
        return

    print('   Best fitting recipe ({:2d}%) and the image\'s deviation settings:'.format(item[0]))
    print('   {}'.format(item[1]))
    for v in item[2]:
        print('    {:18s}: {:18s} {:18s} {:2d}%'.format(str(v[1]), str(v[2]), f'({str(v[3])})', v[0]))


def get_image_files(pathto):
    """ Returns list with all JPG file names for the given path (without subdirectories).
    """

    if path.isdir(pathto):
        log(f'Directory found: {pathto}')
        files = [path.join(pathto, each) for each in listdir(pathto) if each.upper().endswith('.JPG')]
        if len(files) > 0:
            log(f'Found JPG files: {len(files)}')
            return files
        else:
            exit(f'No JPG files found in: {pathto}')
        
    elif path.isfile(pathto) and pathto.upper().endswith('.JPG'):
        log(f'Found single JPG file: {pathto}')
        return [pathto]
    
    else:
        exit(f'Neither an image file nor a path: {pathto}')

def process():
    
    global recipes

    total = 0
    err = 0

    recipes = import_recipes(args.recipes)

    files = get_image_files(args.path[0])

    for f in files:
        total += 1
        log(f'Processing {f}')
        exif=read_file(f)

        res = find_recipe(exif, recipes)
        if res == None:
            err += 1
            print(f'\nERROR Skipping image, maybe of insufficient exif data: {path.basename(f)}')
            continue

        report(f, res)

    if err == 0:
        print(f'\nProcessed all {total} image(s) successfully.')
    else:
        print(f'\nProcessed {total} image(s), but skipped {err} with error!')


def main():

    log('Verbose mode')
    parse_args()
    process()



if __name__ == '__main__':
    main()
