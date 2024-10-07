# All recipe specific stuff.

import constants.recipefields as R
import constants.filmsimulations as FS
import constants.grain as G
import constants.colorchrome as CC
import constants.drangepriority as DP
import constants.dynamicrange as DR
import constants.whitebalance as WB
import constants.sensor as SR
import constants.csvfields as CSV

def extract_data(row):
    """Extract relevant fields for the imported recipe row and convert them into recipe format. Returns dict with recipe."""
    
    field = ''

    # log(f'  {row}')
    recipe = dict()


    field = CSV.NAME
    value = row[field].strip()
    if len(value) == 0:
        print(f'Recipe: Missing field: "{field}" - recipe will be ignored')
        return None

    recipe[R.NAME] = value
    

    field = CSV.PUBLISHER
    value = row[field].strip()
    recipe[R.PUBLISHER] = value
    

    field = CSV.FILMSIMULATION
    value=row[field]
    
    recipe[R.FILMSIMULATION] = map_filmsimulation(value)

    if recipe[R.FILMSIMULATION] is None:
        print(f'Unknown film simulation: {row[field]} - recipe {recipe[R.NAME]} will be ignored')
        return None


    if recipe[R.FILMSIMULATION] == FS.ACROS or recipe[R.FILMSIMULATION] == FS.MONOCHROME:

        field = CSV.BW_COLOR_WC
        if len(row[field]) > 0:
            value=int(row[field])
        else:
            value = 0
        recipe[R.BW_COLOR_WC] = value

        field = CSV.BW_COLOR_MC
        if len(row[field]) > 0:
            value=int(row[field])
        else:
            value = 0
        recipe[R.BW_COLOR_MC] = value


    field = CSV.GRAIN_EFFECT
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


    field = CSV.CCR_EFFECT
    value=row[field].upper().strip()

    if value == 'WEAK':
        recipe[R.CCR_EFFECT] = CC.WEAK
    elif value == 'STRONG':
        recipe[R.CCR_EFFECT] = CC.STRONG
    else:
        recipe[R.CCR_EFFECT] = CC.OFF
    

    field = CSV.CCRFX_BLUE
    value=row[field].upper().strip()

    if value == 'WEAK':
        recipe[R.CCRFX_BLUE] = CC.WEAK
    elif value == 'STRONG':
        recipe[R.CCRFX_BLUE] = CC.STRONG
    else:
        recipe[R.CCRFX_BLUE] = CC.OFF


    field = CSV.WHITE_BALANCE           
    value=row[field].upper().replace('.','').replace(' ', '')
    if 'WHITEPRIORITY' in value:
        recipe[R.WHITE_BALANCE] = WB.WHITE_PRIORITY
    elif 'AMBIENCEPRIORITY' in value:
        recipe[R.WHITE_BALANCE] = WB.AMBIENCE_PRIORITY
    elif 'KELVIN' in value:
        recipe[R.WHITE_BALANCE] = WB.KELVIN
        recipe[R.KELVIN] = int(row['Kelvin'])
    elif 'DAYLIGHT' in value:
        recipe[R.WHITE_BALANCE] = WB.DAYLIGHT
    elif 'SHADE' in value:
        recipe[R.WHITE_BALANCE] = WB.SHADE
    else:
        recipe[R.WHITE_BALANCE] = WB.AUTO


    field = CSV.WHITE_BALANCE_R          
    if len(row[field]) > 0:
        value=int(row[field])
    else:
        value = 0
    recipe[R.WHITE_BALANCE_R] = value

    field = CSV.WHITE_BALANCE_B           
    if len(row[field]) > 0:
        value=int(row[field])
    else:
        value = 0
    recipe[R.WHITE_BALANCE_B] = value

    field = CSV.DRANGE_PRIORITY
    value=row[field].upper().strip()

    if value == 'WEAK':
        recipe[R.DRANGE_PRIORITY] = DP.WEAK
    elif value == 'STRONG':
        recipe[R.DRANGE_PRIORITY] = DP.STRONG
    
    if R.DRANGE_PRIORITY not in recipe:

        field = CSV.DYNAMIC_RANGE
        value=row[field].upper()

        if '100' in value:
            recipe[R.DYNAMIC_RANGE] = DR.DR100
        elif '200' in value:
            recipe[R.DYNAMIC_RANGE] = DR.DR200
        elif '400' in value:
            recipe[R.DYNAMIC_RANGE] = DR.DR400
        else:
            recipe[R.DYNAMIC_RANGE] = DR.AUTO
        
        field = CSV.HIGHLIGHTS
        if len(row[field]) > 0:
            value=float(row[field])
        else:
            value = 0
        recipe[R.HIGHLIGHTS] = value

        field = CSV.SHADOWS
        if len(row[field]) > 0:
            value=float(row[field])
        else:
            value = 0
        recipe[R.SHADOWS] = value

    field = CSV.SHARPNESS
    if len(row[field]) > 0:
        value=int(row[field])
    else:
        value = 0
    recipe[R.SHARPNESS] = value
    
    if recipe[R.FILMSIMULATION] != FS.ACROS and \
        recipe[R.FILMSIMULATION] != FS.MONOCHROME:
   
        field = CSV.COLOR
        if len(row[field]) > 0:
            value=int(row[field])
        else:
            value = 0
        recipe[R.COLOR] = value

    field = CSV.HIGH_ISONR
    if len(row[field]) > 0:
        value=int(row[field])
    else:
        value = 0
    recipe[R.HIGH_ISONR] = value

    field = CSV.CLARITY
    if len(row[field]) > 0:
        value=int(row[field])
    else:
        value = 0
    recipe[R.CLARITY] = value

    field = CSV.ISO_MIN
    if len(row[field]) > 0:
        value=int(row[field])
    else:
        value = 0
    recipe[R.ISO_MIN] = value

    field = CSV.ISO_MAX
    if len(row[field]) > 0:
        value=int(row[field])
    else:
        value = 0
    recipe[R.ISO_MAX] = value

    field = CSV.XTRANS_VERSION
    value=row[field].upper().strip()

    if 'III' == value:
        recipe[R.XTRANS_VERSION] = SR.X_III
    if 'IV' == value:
        recipe[R.XTRANS_VERSION] = SR.X_IV
    if 'V' == value:
        recipe[R.XTRANS_VERSION] = SR.X_V

    return recipe


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
    
