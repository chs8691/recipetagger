# Recipe fields. EXIF and Recipies import will campared by this attributes

NAME  = 'Name'                            # Recipe Name (recipe only)
PUBLISHER  = 'Publisher'                  # Publisher, String.  Empty if private recipe (recipe only)
FILMSIMULATION   = 'Filmsimulation'       # String Fujifilm's Simulation Name. See FS....
BW_COLOR_WC   = 'BW Color WC'             # Signed Integer: -18 .. 18
BW_COLOR_MC   = 'BW Color MC'             # Signed Integer: -18 .. 18
GRAIN_EFFECT   = 'Grain Effect'           # String: Off, Weak/Small, Weak/Large, Strong/Small or Strong/Large
CCR_EFFECT   = 'CCR Effect'               # String: Off, Weak or Strong
CCRFX_BLUE   = 'CCR FX Blue'              # String: Off, Weak or Strong
WHITE_BALANCE   = 'White Balance'         # String: White Priority, Auto, Ambience Priority, Kelvin, Daylight, Shade
KELVIN   = 'Kelvin'                       # Unsigned integer 2500 .. 10000
WHITE_BALANCE_R   = 'White Balance R'     # Signed Integer: -9 .. 9
WHITE_BALANCE_B   = 'White Balance B'     # Signed Integer: -9 .. 9
DYNAMIC_RANGE   = 'Dynamic Range'         # String: Auto, 100, 200, 400,  or Empty
DYNAMIC_RANGE_PRIORITY = 'Dynamic Range Priority'  # String: Off, Weak, Strong                                   
HIGHLIGHTS   = 'Highlights'               # Signed Decimal: -2 .. 4                  
SHADOWS   = 'Shadows'                     # Signed Decimal: -2 .. 4               
SHARPNESS   = 'Sharpness'                 # Signed Integer: -4 .. 4
COLOR   = 'Color'                         # Signed Integer: -4 .. 4
HIGH_ISONR   = 'High ISO NR'              # Signed Integer: -4 .. 4
CLARITY   = 'Clarity'                     # Signed Integer: -5 .. 5
ISO_MIN   = 'ISO min'                     # Unsigned Integer: 0 .. 51200 (recipe only)
ISO_MAX   = 'ISO max'                     # Unsigned Integer: 0 .. 51200 (recipe only)
ISO       = 'ISO'                         # Unsigned Integer: 0 .. 51200 (image only)
XTRANS_VERSION   = 'X-Trans Version'      # String: 5, 4, 3, ...

