import argparse
import csv
import exifing as ex
import reciping as rp
import constants.recipefields as R
import constants.whitebalance as WB

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

                field='MakerNotes:BWAdjustment'                # Monochromatic Color warm/cool
                exif[R.BW_COLOR_WC] = d[field]
                field='MakerNotes:BWMagentaGreen'              # Monochromatic Color magenta/green
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

            # field='MakerNotes:ColorTemperature'      
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
