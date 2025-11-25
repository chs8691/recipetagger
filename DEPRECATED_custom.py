from constants import filmsimulations as FS
from constants import whitebalance as WB
from constants import drangepriority as DP
from constants import dynamicrange as DR

def DEPRECATED_map_dynamicrange(recipe_value):
    """Returns custom settings value for the give recipe value"""

    match recipe_value:
        case DR.DR400:
            return '400'
        case DR.DR200:
            return '200'
        case DR.DR100:
            return '100'

    return '0'


def DEPRECATED_map_drpriority(recipe_value):
    """Returns custom settings value for the give recipe value"""

    match recipe_value:
        case DP.STRONG:
            return 'P2'
        case DP.WEAK:
            return 'P1'

    return '0'


def DEPRECATED_map_whitebalance(recipe_value):
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



def DEPRECATED_map_filmsimulation(recipe_value):
    """Returns custom settings value for the give recipe value"""


    print('cumstom.map_filmsimulation scheint doch noch in Verwendung. Doppelte Definition zu customs.')
    exit(1)

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

