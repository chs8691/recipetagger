import reciping as rp
import constants.recipefields as R
import constants.filmsimulations as FS
import constants.grain as G
import constants.dynamicrange as DR
import constants.drangepriority as DP
import constants.whitebalance as WB
import constants.csvfields as CSV

import logging

LOGGER = logging.getLogger(__name__)


def test_extract_recipe_data():
    
    row = {CSV.NAME             :"Recipe Nr. 1",
           CSV.PUBLISHER        :"Max Morytz",
           CSV.FILMSIMULATION   :"Astia",
           CSV.WEBSITE          :"xy.com",
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
    assert r[R.WEBSITE] == 'xy.com'
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
           CSV.WEBSITE          :"xy.com",
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
    assert r[R.WEBSITE] == 'xy.com'
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