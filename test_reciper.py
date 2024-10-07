import exifing as ex
import reciping as rp
import constants.recipefields as R
import constants.filmsimulations as FS
import constants.grain as G
import constants.dynamicrange as DR
import constants.drangepriority as DP
import constants.whitebalance as WB
import constants.sensor as SR
import constants.colorchrome as CC
import constants.bwfilter as BWF
import constants.csvfields as CSV

import logging

LOGGER = logging.getLogger(__name__)

        
def test_map_drange_priority():
    assert ex.map_drange_priority(None) == None
    assert ex.map_drange_priority(1) == DP.WEAK
    assert ex.map_drange_priority(2) == DP.STRONG
    assert ex.map_drange_priority(3) == None


def test_map_dynamic_range():
    assert ex.map_dynamic_range(0) == DR.AUTO
    assert ex.map_dynamic_range(100) == DR.DR100
    assert ex.map_dynamic_range(200) == DR.DR200
    assert ex.map_dynamic_range(400) == DR.DR400
    

def test_exif_map_wb_finetune():
    assert ex.map_wb_finetune("0 0") == (0, 0)
    assert ex.map_wb_finetune("-1 2") == (-1, 2)
    assert ex.map_wb_finetune("19 -18") == (19, -18)
    assert ex.map_wb_finetune("20 -40") == (1, -2)

def test_exif_sharpness():
    assert ex.map_sharpness(0) == -4
    assert ex.map_sharpness(1) == -3
    assert ex.map_sharpness(2) == -2
    assert ex.map_sharpness(3) == 0
    assert ex.map_sharpness(4) == 2
    assert ex.map_sharpness(5) == 3
    assert ex.map_sharpness(6) == 4
    assert ex.map_sharpness(130) == -1 
    assert ex.map_sharpness(132) == 1

def test_exif_map_clarity():
    assert ex.map_clarity(0) == 0
    assert ex.map_clarity(-1000) == -1
    assert ex.map_clarity(-5000) == -5
    assert ex.map_clarity(1000) == 1
    assert ex.map_clarity(5000) == 5

def test_exif_map_noisereduction():
    assert ex.map_noisereduction(0) == 0
    assert ex.map_noisereduction(256) == 2
    assert ex.map_noisereduction(384) == 1
    assert ex.map_noisereduction(448) == 3
    assert ex.map_noisereduction(480) == 4
    assert ex.map_noisereduction(512) == -2
    assert ex.map_noisereduction(640) == -1
    assert ex.map_noisereduction(704) == -3
    assert ex.map_noisereduction(736) == -4


def test_exif_map_saturation():
    assert ex.map_saturation(0) == 0
    assert ex.map_saturation(128) == 1
    assert ex.map_saturation(256) == 2
    assert ex.map_saturation(192) == 3
    assert ex.map_saturation(224) == 4
    assert ex.map_saturation(384) == -1
    assert ex.map_saturation(1024) == -2
    assert ex.map_saturation(1216) == -3
    assert ex.map_saturation(1248) == -4
    assert ex.map_saturation(768) == (FS.MONOCHROME, None)
    assert ex.map_saturation(769) == (FS.MONOCHROME, BWF.RED)
    assert ex.map_saturation(770) == (FS.MONOCHROME, BWF.YELLOW)
    assert ex.map_saturation(771) == (FS.MONOCHROME, BWF.GREEN)
    assert ex.map_saturation(784) == (FS.SEPIA, None)
    assert ex.map_saturation(1280) == (FS.ACROS, None)
    assert ex.map_saturation(1281) == (FS.ACROS, BWF.RED)
    assert ex.map_saturation(1282) == (FS.ACROS, BWF.YELLOW)
    assert ex.map_saturation(1283) == (FS.ACROS, BWF.GREEN)


def test_exif_map_color_chrome():
    assert ex.map_color_chrome(0) == CC.OFF
    assert ex.map_color_chrome(1) == None
    assert ex.map_color_chrome(32) == CC.WEAK
    assert ex.map_color_chrome(64) == CC.STRONG


def test_exif_map_grain():
    assert ex.map_grain(0, 0) == G.OFF
    assert ex.map_grain(1, 1) == None
    assert ex.map_grain(32, 16) == G.WEAK_SMALL
    assert ex.map_grain(32, 32) == G.WEAK_LARGE
    assert ex.map_grain(64, 16) == G.STRONG_SMALL
    assert ex.map_grain(64, 32) == G.STRONG_LARGE


def test_exif_map_white_balance():
    
    assert ex.map_whitebalance(0) == WB.AUTO
    assert ex.map_whitebalance(1) == WB.WHITE_PRIORITY
    assert ex.map_whitebalance(2) == WB.AMBIENCE_PRIORITY
    assert ex.map_whitebalance(256) == WB.DAYLIGHT
    assert ex.map_whitebalance(512) == WB.SHADE
    assert ex.map_whitebalance(768) == WB.FLUORESCENT1
    assert ex.map_whitebalance(769) == WB.FLUORESCENT2
    assert ex.map_whitebalance(770) == WB.FLUORESCENT3
    assert ex.map_whitebalance(771) == None
    assert ex.map_whitebalance(772) == None
    assert ex.map_whitebalance(1024) == WB.INCANDESENT
    assert ex.map_whitebalance(1280) == WB.UNKNOWN
    assert ex.map_whitebalance(1536) == WB.UNDERWATER
    assert ex.map_whitebalance(3840) == WB.UNKNOWN
    assert ex.map_whitebalance(3841) == WB.UNKNOWN
    assert ex.map_whitebalance(3842) == WB.UNKNOWN
    assert ex.map_whitebalance(3843) == WB.UNKNOWN
    assert ex.map_whitebalance(3844) == WB.UNKNOWN
    assert ex.map_whitebalance(4080) == WB.KELVIN

def test_extract_recipe_data():
    
    row = {CSV.NAME             :"Recipe Nr. 1",
           CSV.PUBLISHER        :"Max Morytz",
           CSV.FILMSIMULATION   :"Astia",
           CSV.BW_COLOR_MC      :"",
           CSV.BW_COLOR_WC      :"",
           CSV.GRAIN_EFFECT     :"weak/small",
           CSV.CCR_EFFECT       :"strong",
           CSV.CCRFX_BLUE       :"off",
           CSV.WHITE_BALANCE    :"Auto",
           CSV.KELVIN           :"",
           CSV.WHITE_BALANCE_B  :"+1",
           CSV.WHITE_BALANCE_R  :"-1",
           CSV.DYNAMIC_RANGE    :"Auto",
           CSV.DRANGE_PRIORITY  :"off",
           CSV.HIGHLIGHTS       :"-1",
           CSV.SHADOWS          :"+1",
           CSV.SHARPNESS        :"-2",
           CSV.COLOR            :"0",
           CSV.HIGH_ISONR       :"+2",
           CSV.CLARITY          :"-3",
           CSV.ISO_MIN          :"",
           CSV.ISO_MAX          :"3200",
           CSV.XTRANS_VERSION   :"V",
           }
    
    
    r = rp.extract_data(row)

    assert r[R.NAME] == 'Recipe Nr. 1'
    assert r[R.PUBLISHER] == 'Max Morytz'
    assert r[R.XTRANS_VERSION] == 'V'
    assert r[R.FILMSIMULATION] == FS.ASTIA
    assert R.BW_COLOR_WC not in r 
    assert R.BW_COLOR_MC not in r
    assert r[R.GRAIN_EFFECT] == G.WEAK_SMALL
    assert r[R.WHITE_BALANCE] == WB.AUTO
    assert R.KELVIN not in r 
    assert r[R.WHITE_BALANCE_R] == -1
    assert r[R.WHITE_BALANCE_B] == 1
    assert r[R.DYNAMIC_RANGE] == DR.AUTO
    assert R.DRANGE_PRIORITY not in r 
    assert r[R.HIGHLIGHTS] == -1
    assert r[R.SHADOWS] == 1
    assert r[R.COLOR] == 0 
    assert r[R.SHARPNESS] == -2
    assert r[R.HIGH_ISONR] == 2
    assert r[R.CLARITY] == -3
    assert r[R.ISO_MIN] == 0
    assert r[R.ISO_MAX] == 3200

def test_extract_recipe_data2():

    row = {CSV.NAME              :"Recipe Nr. 2",
           CSV.PUBLISHER         :"Max Morytz",
           CSV.FILMSIMULATION    :"ACROS",
           CSV.BW_COLOR_MC       :"+1",
           CSV.BW_COLOR_WC       :"-1",
           CSV.GRAIN_EFFECT      :"",
           CSV.CCR_EFFECT        :"weak",
           CSV.CCRFX_BLUE        :"strong",
           CSV.WHITE_BALANCE     :"Kelvin",
           CSV.KELVIN            :"10000",
           CSV.WHITE_BALANCE_B   :"0",
           CSV.WHITE_BALANCE_R   :"0",
           CSV.DYNAMIC_RANGE     :"",
           CSV.DRANGE_PRIORITY   :"Strong",
           CSV.HIGHLIGHTS        :"0",
           CSV.SHADOWS           :"0",
           CSV.SHARPNESS         :"0",
           CSV.COLOR             :"",
           CSV.HIGH_ISONR        :"-4",
           CSV.CLARITY           :"1",
           CSV.ISO_MIN           :"1200",
           CSV.ISO_MAX           :"1600",
           CSV.XTRANS_VERSION    :"IV",
           }
    
    r = rp.extract_data(row)

    assert r[R.NAME] == 'Recipe Nr. 2'
    assert r[R.PUBLISHER] == 'Max Morytz'
    assert r[R.XTRANS_VERSION] == 'IV'
    assert r[R.FILMSIMULATION] == FS.ACROS
    assert r[R.BW_COLOR_WC] == -1
    assert r[R.BW_COLOR_MC] == 1
    assert r[R.GRAIN_EFFECT] == G.OFF
    assert r[R.WHITE_BALANCE] == WB.KELVIN
    assert r[R.KELVIN] == 10000
    assert r[R.WHITE_BALANCE_R] == 0
    assert r[R.WHITE_BALANCE_B] == 0
    assert R.DYNAMIC_RANGE not in r    
    assert r[R.DRANGE_PRIORITY] == DP.STRONG
    assert R.HIGHLIGHTS not in r
    assert R.SHADOWS not in r
    assert R.COLOR not in r
    assert r[R.SHARPNESS] == 0
    assert r[R.HIGH_ISONR] == -4
    assert r[R.CLARITY] == 1
    assert r[R.ISO_MIN] == 1200
    assert r[R.ISO_MAX] == 1600


# def test_read_file_nostalgic_neg():
#     act = read_file('testdata/x-t50-nostalgic_neg.JPG')
    
#     assert act[R.FILMSIMULATION] == FS.NOSTALGIC_NEG

def test_exif_map_filmsimulation():
    
    assert ex.map_filmsimulation(0) == FS.PROVIA
    assert ex.map_filmsimulation(288) == FS.ASTIA
    assert ex.map_filmsimulation(512) == FS.VELVIA
    assert ex.map_filmsimulation(1024) == FS.VELVIA
    assert ex.map_filmsimulation(1280) == FS.PRO_NEG_STD
    assert ex.map_filmsimulation(1281) == FS.PRO_NEG_HI
    assert ex.map_filmsimulation(1536) == FS.CLASSIC_CHROME
    assert ex.map_filmsimulation(1792) == FS.ETERNA
    assert ex.map_filmsimulation(2048) == FS.CLASSIC_NEG
    assert ex.map_filmsimulation(2304) == FS.ETERNA_BLEACH_BYPASS
    assert ex.map_filmsimulation(2560) == FS.NOSTALGIC_NEG
    assert ex.map_filmsimulation(2816) == FS.REALA_ACE
    assert ex.map_filmsimulation(9999) == None


def test_recipe_map_filmsimulation():

    exp=FS.CLASSIC_CHROME

    assert rp.map_filmsimulation('classic  chrome') == exp
    assert rp.map_filmsimulation('CLASSiC  CHROMe') == exp

    exp=None

    assert rp.map_filmsimulation('classic  chrom') == exp
    assert rp.map_filmsimulation('CLASSIC_CHROME') == exp

    exp=FS.PRO_NEG_STD

    assert rp.map_filmsimulation('pro neg std') == exp
    assert rp.map_filmsimulation('pro neg std.') == exp
    assert rp.map_filmsimulation('PRO NEG STD.') == exp
    assert rp.map_filmsimulation('PRO NEG. STD.') == exp

    exp=FS.ASTIA

    assert rp.map_filmsimulation('astia') == exp