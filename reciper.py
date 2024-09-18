import argparse
import csv
import exifing as ex
import reciping as rp
import constants.recipefields as R
import constants.whitebalance as WB
import constants.filmsimulations as FS
import constants.grain as GR
import constants.colorchrome as CC

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
    parser.add_argument('-r', '--recipies', type=str, nargs=1, default='reipies.csv',
                        help='Update recipies from CSV file (Default: %(default)s) and store them in the internal Storage. See example file for columns names. ')
    parser.add_argument('-p', '--print', action='store_true',
                        help='Print result to console')
    parser.add_argument('filename', metavar='FILENAME', type=str, nargs=1,
                    help='Image file name')
    
    args = parser.parse_args()


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
            recipe = rp.extract_data(row)

            vvlog(recipe)
            recipies.append(recipe)


    print(f'{len(recipies)}/{row_count} recipies imported.')

    return recipies




def read_file(filename):
    """Works for Fujifilm X-T50. Returns dictionary with all recipe fields.
    Returns None in error case. """
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
                    print(f'Unknown value for {field}: {d[field]}')
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


def find_recipe(exif, recipies):
    
    res = []
    for r in recipies:
        res.append(check_recipe(exif, r))

    log(res)


def check_recipe(exif, recipe):
    """ Compare image exifs data wth recipe's data to find differences and calculate a
        total score percentage value.
        Returns tupel with two values:
        - score pertance value (0..100)
        - list with field names that doesn't match 100 %
        Example: ( 90, [R.COLOR, R.SHARPNESS] )
        Every single score will be weightend between 0..10. For instance FILMSIMULATION
        is very important: weight=10
    """
    failed = []
    total = 0
    max_total = 0
    MAX = 100

    field = R.FILMSIMULATION
    weight = 10
    act = rate_fs(exif[field], recipe[field])
    total += act * weight
    max_total += MAX * weight
    if act < MAX:
        failed.append(field)

    field = R.GRAIN_EFFECT
    weight = 3
    act =  rate_range(0, 4, grain_as_int(exif[field]), grain_as_int(recipe[field]))
    total += act * weight
    max_total += MAX * weight
    if act < MAX:
        failed.append(field)

    field = R.CCR_EFFECT
    weight = 2
    act =  rate_range(0, 2, cc_as_int(exif[field]), cc_as_int(recipe[field]))
    total += act * weight
    max_total += MAX * weight
    if act < MAX:
        failed.append(field)

    field = R.CCRFX_BLUE
    weight = 2
    act =  rate_range(0, 2, cc_as_int(exif[field]), cc_as_int(recipe[field]))
    total += act * weight
    max_total += MAX * weight
    if act < MAX:
        failed.append(field)

    field = R.SHARPNESS
    weight = 1
    act = rate_range(-4, +4, exif[field], recipe[field])
    total += act * weight
    max_total += MAX * weight
    if act < MAX:
        failed.append(field)

    field = R.HIGH_ISONR
    weight = 2
    act = rate_range(-4, +3, exif[field], recipe[field])
    total += act * weight
    max_total += MAX * weight
    if act < MAX:
        failed.append(field)

    field = R.CLARITY
    weight = 5
    act = rate_range(-4, 5, exif[field], recipe[field])
    total += act * weight
    max_total += MAX * weight
    if act < MAX:
        failed.append(field)


    bws=[FS.ACROS, FS.MONOCHROME]
    if exif[R.FILMSIMULATION] in bws and recipe in bws:

        field = R.BW_COLOR_WC
        weight = 1
        act = rate_range(-18, +18, exif[field], recipe[field])
        total += act * weight
        max_total += MAX * weight
        if act < MAX:
            failed.append(field)

        field = R.BW_COLOR_MC
        weight = 1
        act = rate_range(-18, +18, exif[field], recipe[field])
        total += act * weight
        max_total += MAX * weight
        if act < MAX:
            failed.append(field)

    elif exif[R.FILMSIMULATION] not in bws and recipe not in bws:

        field = R.COLOR
        weight = 1
        act = rate_range(-4, +4, exif[field], recipe[field])
        total += act * weight
        max_total += MAX * weight
        if act < MAX:
            failed.append(field)

    # else
    #  Was soll mit BW/Farbe passieren? 


    return (100 / max_total * total, failed)


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

def process():
    
    global recipies

    recipies = import_recipies(args.recipies[0])

    exif=read_file(args.filename[0])

    find_recipe(exif, recipies)

    

def main():

    log('Verbose mode')
    parse_args()
    process()



if __name__ == '__main__':
    main()
