# All exif specific processing stuff. 
# Most exif data are stored as integer values and have to be 
# interpreted to there semantic value.
# For his, there is a lookup table for Fuji specific tags dcumentented in 
# https://exiftool.org/TagNames/FujiFilm.html 
# 
# Exiftool: use '-n' to see the unconverted value

import constants.whitebalance as WB
import constants.grain as G
import constants.dynamicrange as DR
import constants.colorchrome as CC
import constants.filmsimulations as FS
import constants.drangepriority as DP

def map_wb_finetune(values):
    """Maps string with 2 integer  as finetune values. Returns integer duple.
       Works for 'newer cameras' and older ones, too. Don't know, what are not newer cams.

       Newer cams: the value will be divided by 20 (-60 --> -3), if greater than 19.
    """

    (r, b) = values.split(' ')

    if abs(int(r)) < 20:
        return (int(r), int(b))
    else:
        return (int(r) / 20, int(b) / 20)
    


def map_color_chrome(value):
    """For Color Chrome Effect and Color Chrome FX Blue.
    Returns OFF, WEAK or STRONG or, in error case, None.
    
    - ColorChromeEffect
    - ColorChromeFXBlue

        0 = Off
        32 = Weak
        64 = Strong
    """

    match value:
        case 0:
            return CC.OFF
        case 16:
            return CC.WEAK
        case 32:
            return CC.STRONG
        
    return None

def map_drange_priority(value):
    """ Returns the DR Priority value, either for auto or for fixed. 
    Returns None in error case.
    
    Supported values:
        1 = Weak
        2 = Strong
    """    
    if value == 1:
        return DP.WEAK
    if value == 2:
        return DP.STRONG
    
    return None


def map_dynamic_range(value):
    """Return constants from DR for the given integer, or,
    if not supported, None.
    
        0x0 = Auto
        0x1 = Manual                <<< Not supperted
        0x100 = Standard (100%)
        0x200 = Wide1 (230%)
        0x201 = Wide2 (400%)
        0x8000 = Film Simulation    <<< Not supperted
    """

    match value:
        case 0:
            return DR.AUTO
        case 100:
            return DR.DR100
        case 200:
            return DR.DR200
        case 400:
            return DR.DR400
        

    return None

def map_whitebalance(value):
    """Parse integer value and return value of constants.whitebalance or, if no match, UNKNOWN. 
    This interger is the value stored in EXIF information MakerNotes:WhiteBalance.
    Not all existing values are supported (returns None).

        0x0 = Auto <br>
        0x1 = Auto (white priority) <br>
        0x2 = Auto (ambiance priority) <br>
        0x100 = Daylight <br>
        0x200 = Cloudy <br>
        0x300 = Daylight Fluorescent <br>
        0x301 = Day White Fluorescent <br>
        0x302 = White Fluorescent <br>
        0x303 = Warm White Fluorescent <br>
        0x304 = Living Room Warm White Fluorescent <br>
        0x400 = Incandescent <br>
        0x500 = Flash <br>
        0x600 = Underwater <br>
        0xf00 = Custom <br>
        0xf01 = Custom2 <br>
        0xf02 = Custom3 <br>
        0xf03 = Custom4 <br>
        0xf04 = Custom5 <br>
        0xff0 = Kelvin <br>
    """
        
    match hex(value):
        case '0x0':
            return WB.AUTO
        case '0x1':
            return WB.WHITE_PRIORITY
        case '0x2':
            return WB.AMBIENCE_PRIORITY
        case '0x100':
            return WB.DAYLIGHT
        case '0x200':
            return WB.SHADE
        case '0x300':
            return WB.FLUORESCENT1
        case '0x301':
            return WB.FLUORESCENT1
        case '0x302':
            return WB.FLUORESCENT1
        case '0x303':
            return WB.FLUORESCENT2
        case '0x304':
            return WB.FLUORESCENT3
        case '0x400':
            return WB.INCANDESENT
        case '0x500':
            return WB.UNKNOWN
        case '0x600':
            return WB.UNDERWATER
        case '0xf00':
            return WB.UNKNOWN
        case '0xf01':
            return WB.UNKNOWN
        case '0xf02':
            return WB.UNKNOWN
        case '0xf03':
            return WB.UNKNOWN
        case '0xf04':
            return  WB.UNKNOWN
        case '0xff0':
            return WB.KELVIN
        
    return  WB.UNKNOWN

def map_grain(roughness, size):
    """Parse integer value and return value of constants.grain or, if no match, None. 
    This interger is the value stored in EXIF information MakerNotes:GrainEffectRoughness
    and MakerNotes:GrainEffectSize.

    Roughness:
        0 = Off
        32 = Weak
        64 = Strong
    Size:
        0 = Off
        16 = Small
        32 = Large
    """
   
    match roughness:
        case 0:
            return G.OFF
   
        case 16:
            if size == 16:
                return G.WEAK_SMALL
            elif size == 32:
                return G.WEAK_LARGE

        case 32:
            if size == 16:
                return G.STRONG_SMALL
            elif size == 32:
                return G.STRONG_LARGE
    
    return None


def map_filmsimulation(value):
    """Parse integer value and return value of constants.filmsimulations or, if no match, None. 
    This interger is the value stored in EXIF information MakerNotes:FilmMode.
    Not all existing values are supported (returns None).

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

