# Film Simulations
PROVIA = 'PROVIA'
VELVIA  = 'VELVIA'
ASTIA  = 'ASTIA'
CLASSIC_CHROME  = 'CLASSIC_CHROME'
REALA_ACE  = 'REALA_ACE'
PRO_NEG_HI  = 'PRO_NEG_HI'
PRO_NEG_STD  = 'PRO_NEG_STD'
CLASSIC_NEG  = 'CLASSIC_NEG'
NOSTALGIC_NEG = 'NOSTALGIC_NEG'
ETERNA  = 'ETERNA'
ETERNA_BLEACH_BYPASS  = 'ETERNA_BLEACH_BYPASS'
ACROS  = 'ACROS'
MONOCHROME  = 'MONOCHROME'
SEPIA  = 'SEPIA'

def name(fs):
    """Returns human readable name for the given film simulation"""
    return fs.replace('_', ' ').capitalize