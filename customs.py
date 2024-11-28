# Recipes to custom settings for Fujifilm X Ras Studio. 
import argparse
from os import path
import re
from reciper import import_recipes
from reciper import err
from reciper import set_log_mode
from reciper import LOG_V
from reciper import LOG_VV
from reciper import log
from reciper import vvlog
from reciping import split_grain_effect
from constants import recipefields as R
from constants import grain as GR
from constants import colorchrome as CC
from constants import whitebalance as WB
from constants import filmsimulations as FS
from constants import drangepriority as DP
from constants import dynamicrange as DR
from constants import customfields as C

args = None

def get_null_value(tag):
    """Returns the value for a not set <MonochromaticColor_RG/> or an empty string 
    for unknown tags.    
    Hint: For every tag that can be an non-set tag, there must be an entry here. 
    """
    match tag:
        case C.MONOCHROMATIC_COLOR_RG:
            return '0'
        
    return ''

def search_tag(tag, lines):
    """Returns tuple with three values count, line number an value.  
    Count: number of occurances
    Line Number: Index of (last) occurances or, if count is 0, None. Starts with 0.
    Value: value at line number. Is None, of tag without value or if count is 0 
    """

    count = 0
    value = None
    line_number = None

    # Search for tag pair   
    p = re.compile(f'.*<{tag}>(.+?)</{tag}>.*') 
    cnt = 0   
    for l in lines:
        # vvlog(l)
        m = p.match(l)
        if m is not None and m.lastindex > 0:
            vvlog(f'Found {tag}={m.group(1)} in line {cnt}')
            value = m.group(1)
            line_number = cnt
            count += 1
        cnt += 1
      
    #  Search for single tag (non value)
    if count == 0:
        p = re.compile(f'.*<{tag}/>.*') 
        cnt = 0   
        for l in lines:
            # vvlog(l)
            m = p.match(l)
            if m is not None:
                vvlog(f'Found non value {tag} in line {cnt}')
                line_number = cnt
                count += 1
                value = get_null_value(tag)
            cnt += 1

    if count == 0:
        log(f'tag {tag} not found')
    
    return (count, line_number, value)
    

def search_propertyGroup(tag, lines):
    """Returns tuple with three values count, line number an value.  
    Count: number of occurances
    Line Number: Index of (last) occurances or, if count is 0, None. Starts with 0.
    Value: value at line number. Is None, of tag without value or if count is 0 
    """
    count = 0
    value = None
    line_number = None

    p = re.compile(f'.*<PropertyGroup.* {tag}="(.+?)".*>.*') 
    cnt = 0   
    found = False
    for l in lines:
        # vvlog(l)
        m = p.match(l)
        if m is not None and m.lastindex > 0:
            vvlog(f'Found {tag}={m.group(1)}')
            value = m.group(1)
            line_number = cnt
            count += 1
        cnt += 1            
      
    if not found:
        log(f'tag {tag} not found')
    
    return (count, line_number, value)


def update_tag(tag, value, lines):
    """Returns updated lines if the give tag was found."""

    (count, line_number, old_value) = search_tag(tag, lines)

    if count == 0:
        log(f'tag {tag} not found. Skipping.')
        return lines

    if count > 1:
        log(f'tag {tag} not unique. Skipping.')
        return lines

    # Found tag exactly once  
    ret = lines
    # Tag can be a single Tag or enclosed tag
    ret[line_number]=re.sub(f'<{tag}.*>', f'<{tag}>{value}</{tag}>', lines[line_number])
    return ret


def update_propertyGroup(tag, value, lines):
    """Returns updated lines if the give property was found."""

    (count, line_number, old_value) = search_propertyGroup(tag, lines)

    if count == 0:
        log(f'tag {tag} not found. Skipping.')
        return lines

    if count > 1:
        log(f'tag {tag} not unique. Skipping.')
        return lines

    # Found tag exactly once  
    ret = lines
    # Tag can be a single Tag or enclosed tag
    ret[line_number]=re.sub(f' {tag}="(.+?)"', f' {tag}="{value}"', lines[line_number])
    return ret


def create_custom(recipe, lines):
    """Create custom setting data for the give recipe by using the template string. 
    Returns string list with custom settings."""
    ret = lines

    update_propertyGroup(C.LABEL, recipe[R.NAME], ret)

    tag = C.DYNAMIC_RANGE
    value = 'OFF'
    field = R.DYNAMIC_RANGE
    if field in recipe: value = map_dynamicrange(recipe[field])
    ret = update_tag(tag, value, ret)

    tag = C.WIDE_D_RANGE
    value = '0'
    field = R.DRANGE_PRIORITY
    if field in recipe: value = map_drpriority(recipe[field])
    ret = update_tag(tag, value, ret)

    field = R.FILMSIMULATION
    value = FS.PROVIA
    if field in recipe: 
        value = map_filmsimulation(recipe[field])
    tag = C.FILM_SIMULATION
    ret = update_tag(tag, value, ret)

    field = R.BW_COLOR_WC
    value = '0'
    if field in recipe: 
        value = recipe[field]
    tag = C.BLACK_IMAGE_TONE
    ret = update_tag(tag, value, ret)

    field = R.BW_COLOR_MC
    value = '0'
    if field in recipe: 
        value = recipe[field]
    tag = C.MONOCHROMATIC_COLOR_RG
    ret = update_tag(tag, value, ret)

    field = R.GRAIN_EFFECT
    (value, value2) = split_grain_effect(GR.OFF)
    if field in recipe: 
        (value, value2) = split_grain_effect(recipe[field])

    tag = C.GRAIN_EFFECT
    ret = update_tag(tag, value, ret)
    tag = C.GRAIN_EFFECT_SIZE
    ret = update_tag(tag, value2, ret)

    field = R.CCR_EFFECT
    value = CC.OFF
    if field in recipe: 
        value = recipe[field]
    tag = C.CHROME_EFFECT
    ret = update_tag(tag, value, ret)

    field = R.CCRFX_BLUE
    value = CC.OFF
    if field in recipe: 
        value = recipe[field]
    tag = C.COLOR_CHROME_BLUE
    ret = update_tag(tag, value, ret)

    field = R.WHITE_BALANCE
    value = WB.AUTO
    if field in recipe: 
        value = map_whitebalance(recipe[field])
    tag = C.WHITE_BALANCE
    ret = update_tag(tag, value, ret)

    field = R.WHITE_BALANCE_R
    value = '0'
    if field in recipe: 
        value = recipe[field]
    tag = C.WB_SHIFT_R
    ret = update_tag(tag, value, ret)
      
    field = R.WHITE_BALANCE_B
    value = '0'
    if field in recipe: 
        value = recipe[field]
    tag = C.WB_SHIFT_B
    ret = update_tag(tag, value, ret)
      
    field = R.KELVIN
    # Temperature with '0' makes the custom settings unusable
    value = map_kelvin('5500')
    if field in recipe: 
        value = map_kelvin(recipe[field])
    tag = 'WBColorTemp'
    ret = update_tag(tag, value, ret)     
    
    field = R.HIGHLIGHTS
    value = '0'
    if field in recipe: 
        value = recipe[field]
    tag = C.HIGHLIGHT_TONE
    ret = update_tag(tag, value, ret)
          
    field = R.SHADOWS
    value = '0'
    if field in recipe: 
        value = recipe[field]
    tag = C.SHADOW_TONE
    ret = update_tag(tag, value, ret)
      
    field = R.COLOR
    value = '0'
    if field in recipe: 
        value = recipe[field]
    tag = C.COLOR
    ret = update_tag(tag, value, ret)
      
    field = R.SHARPNESS
    value = '0'
    if field in recipe: 
        value = recipe[field]
    tag = C.SHARPNESS
    ret = update_tag(tag, value, ret)
      
    field = R.HIGH_ISONR
    value = '0'
    if field in recipe: 
        value = recipe[field]
    tag = C.NOIS_REDUCTION
    ret = update_tag(tag, value, ret)
      
    field = R.CLARITY
    value = '0'
    if field in recipe: 
        value = recipe[field]
    tag = C.CLARITY
    ret = update_tag(tag, value, ret)
    
    return ret 


def read_template(template):
    """Returns tuple with device and data as list of string. Or None in error case."""

    tdata=[]
    camera=None
    with open(template, newline='') as tf:
        tdata = tf.readlines()
 
    if tdata is None or len(tdata) == 0:
        exit('Invalid template file')

    # print(tdata)
    p = re.compile('.+ device="(.+?)".*')
    for l in tdata:
        m = p.match(l)
        if m is not None and m.lastindex > 0:
            camera = m.group(1)
            break

    return (camera, tdata)


def write_custom(custom, outdir, name):

    filenname = f'{name.replace(' ', '_').replace("’", '')}.FP1'

    with(open(path.join(outdir,filenname), mode="w")) as f:
        f.writelines(custom)   
        vvlog(f'Created {filenname}')
        return 1
    
    return 0


def map_kelvin(recipe_value):
    """Returns custom settings value for the give recipe value"""

    return f'{recipe_value}K'


def map_dynamicrange(recipe_value):
    """Returns custom settings value for the give recipe value"""

    match recipe_value:
        case DR.DR400:
            return '400'
        case DR.DR200:
            return '200'
        case DR.DR100:
            return '100'

    return '0'


def map_drpriority(recipe_value):
    """Returns custom settings value for the give recipe value"""

    match recipe_value:
        case DP.STRONG:
            return 'P2'
        case DP.WEAK:
            return 'P1'

    return '0'


def map_whitebalance(recipe_value):
    """Returns custom settings value for the give recipe value"""

    match recipe_value:
        case WB.WHITE_PRIORITY:
            return 'Auto_White'
        # case WB.AUTO:
            # return 'Auto'
        case WB.AMBIENCE_PRIORITY:
            return 'Auto_Ambience'
        case WB.KELVIN:
            return 'Temperature'
        case WB.DAYLIGHT:
            return 'Daylight'
        case WB.SHADE:
            return 'Shade'
        case WB.FLUORESCENT1:
            return 'FLight1'
        case WB.FLUORESCENT2:
            return 'FLight2'
        case WB.FLUORESCENT3:
            return 'FLight3'
        case WB.INCANDESENT:
            return 'Incand'
        case WB.UNDERWATER:
            return 'UWater'
        
    return 'Auto'



def map_filmsimulation(recipe_value):
    """Returns custom settings value for the give recipe value"""

    match recipe_value:
        # case FS.PROVIA:
        #     return 'Provia'
        case FS.VELVIA:
            return 'Velvia'
        case FS.ASTIA:
            return 'Astia'
        case FS.CLASSIC_CHROME:
            return 'Classic'
        case FS.REALA_ACE:
            return 'Reala'
        case FS.CLASSIC_NEG:
            return 'ClassicNEGA'
        case FS.NOSTALGIC_NEG:
            return 'NostalgicNEGA'
        case FS.PRO_NEG_HI:
            return 'NEGAhi'
        case FS.PRO_NEG_STD:
            return 'NEGAStd'
        case FS.ETERNA:
            return 'Eterna'
        case FS.ETERNA_BLEACH_BYPASS:
            return 'BleachBypass'
        case FS.ACROS:
            # AcrosR, AcrosG, AcrosYe
            return 'Acros'
        case FS.MONOCHROME:
            # BR, BG, BYe
            return 'BW'
        case FS.SEPIA:
            return 'Sepia'

    return 'Provia'



def main():

    outdir = args.outdir
    input = args.input
    template = args.template
    
    if not path.exists(outdir) or not path.isdir(outdir):
        err(f'Invalid outdir: {outdir}')

    if not path.exists(input) or not path.isfile(input):
        err(f'Invalid input file: {input}')

    if not path.exists(input) or not path.isfile(input):
        err(f'Invalid input file: {input}')

    if not path.exists(template) or not path.isfile(template):
        err(f'Invalid template file: {template}')

    (camera, lines) = read_template(template)

    print(f'Camera: {camera}')

    recipes = import_recipes(input)

    cnt = 0
    ok = 0
    for r in recipes:
        cnt += 1
        log(f'{cnt:3}. recipe \'{r[R.NAME]}\'')
        custom = create_custom(r, lines)
        # print(custom)
        ok += write_custom(custom, outdir, r[R.NAME])

    print(f'{ok} files written.')

def parse_args():

    global args
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input', type=str, default='recipes.csv',
                        help='Input CSV file with recipes (default: %(default)s).')

    parser.add_argument('-t', '--template', type=str, default='template.FP1',
                        help='Template file, creating based on. Only recpipe fields will be changed.')

    parser.add_argument('-o', '--outdir', type=str, default='customs',
                        help='Output directory')

    parser.add_argument('-v', '--verbose', help='Increase output verbosity.', action="store_true")
    parser.add_argument('-vv', '--vverbose', help='Increase output very verbosity.', action="store_true")

    args = parser.parse_args()

    if args.verbose:
        set_log_mode(LOG_V)
    elif args.vverbose:
        set_log_mode(LOG_VV)

if __name__ == '__main__':
    parse_args()
    main()
