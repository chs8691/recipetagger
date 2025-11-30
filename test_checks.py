import reciper
import constants.recipefields as R
import constants.filmsimulations as FS
import constants.grain as GR
import constants.colorchrome as CC
import constants.sensor as SR
import constants.drangepriority as DRP
import constants.dynamicrange as DR
import constants.whitebalance as WB

import logging

LOGGER = logging.getLogger(__name__)


def test_check_recpipe_full_match_color_drp_mode():

    recipe = { 
        R.NAME:'RECIPE No. 1',
        R.PUBLISHER:'Publisher XY',
        R.WEBSITE:'xy.com',
        R.FILMSIMULATION:FS.REALA_ACE, 
        R.DRANGE_PRIORITY:DRP.WEAK,
        R.WHITE_BALANCE:WB.AUTO,
        R.WHITE_BALANCE_R:-1,
        R.WHITE_BALANCE_B:1,
        R.GRAIN_EFFECT:GR.OFF,
        R.CCR_EFFECT:CC.OFF,
        R.CCRFX_BLUE:CC.OFF,
        R.COLOR:-1,
        R.SHARPNESS:-1,
        R.HIGH_ISONR:-1,
        R.CLARITY:-1,
        R.ISO_MIN:0,
        R.ISO_MAX:6400,
        R.XTRANS_VERSION:SR.X_V,
        }
    
    exif = {
        R.FILMSIMULATION:FS.REALA_ACE,
        R.DRANGE_PRIORITY:DRP.WEAK,
        R.WHITE_BALANCE:WB.AUTO,
        R.WHITE_BALANCE_R:-1,
        R.WHITE_BALANCE_B:1,
        R.GRAIN_EFFECT:GR.OFF,
        R.CCR_EFFECT:CC.OFF,
        R.CCRFX_BLUE:CC.OFF,
        R.COLOR:-1,
        R.SHARPNESS:-1,
        R.HIGH_ISONR:-1,
        R.CLARITY:-1,
        R.ISO:3200,
        R.XTRANS_VERSION:SR.X_V,
        }

    (perc, name, publisher, website, result) = reciper.check_recipe(exif, recipe)
    fields = [i[1] for i in result]

    assert perc == 100
    assert name == 'RECIPE No. 1'
    assert publisher == 'Publisher XY'
    assert website == 'xy.com'
    assert len(result) == 0
    assert R.FILMSIMULATION not in fields
    assert R.DYNAMIC_RANGE not in fields
    assert R.WHITE_BALANCE not in fields
    assert R.WHITE_BALANCE_R not in fields
    assert R.WHITE_BALANCE_B not in fields
    assert R.HIGHLIGHTS not in fields
    assert R.SHADOWS not in fields
    assert R.GRAIN_EFFECT not in fields
    assert R.CCR_EFFECT not in fields
    assert R.CCRFX_BLUE not in fields
    assert R.COLOR not in fields
    assert R.SHARPNESS not in fields
    assert R.HIGH_ISONR not in fields
    assert R.CLARITY not in fields
    assert R.ISO_MIN not in fields
    assert R.ISO_MAX not in fields
    assert R.XTRANS_VERSION not in fields

def test_check_recpipe_full_match_color_dr_mode():

    recipe = { 
        R.NAME:'RECIPE No. 1',
        R.PUBLISHER:'Publisher XY',
        R.WEBSITE:'xy.com',
        R.FILMSIMULATION:FS.REALA_ACE, 
        R.WHITE_BALANCE:WB.AUTO,
        R.WHITE_BALANCE_R:-1,
        R.WHITE_BALANCE_B:1,
        R.DYNAMIC_RANGE:DR.DR100,
        R.SHADOWS:1,
        R.HIGHLIGHTS:-1,
        R.GRAIN_EFFECT:GR.OFF,
        R.CCR_EFFECT:CC.OFF,
        R.CCRFX_BLUE:CC.OFF,
        R.COLOR:-1,
        R.SHARPNESS:-1,
        R.HIGH_ISONR:-1,
        R.CLARITY:-1,
        R.ISO_MIN:0,
        R.ISO_MAX:6400,
        R.XTRANS_VERSION:SR.X_V,
        }
    
    exif = {
        R.FILMSIMULATION:FS.REALA_ACE,
        R.DYNAMIC_RANGE:DR.DR100,
        R.WHITE_BALANCE:WB.AUTO,
        R.WHITE_BALANCE_R:-1,
        R.WHITE_BALANCE_B:1,
        R.SHADOWS:1,
        R.HIGHLIGHTS:-1,
        R.GRAIN_EFFECT:GR.OFF,
        R.CCR_EFFECT:CC.OFF,
        R.CCRFX_BLUE:CC.OFF,
        R.COLOR:-1,
        R.SHARPNESS:-1,
        R.HIGH_ISONR:-1,
        R.CLARITY:-1,
        R.ISO:3200,
        R.XTRANS_VERSION:SR.X_V,
        }

    (perc, name, publisher, website, result) = reciper.check_recipe(exif, recipe)
    fields = [i[1] for i in result]

    assert perc == 100
    assert name == 'RECIPE No. 1'
    assert publisher == 'Publisher XY'
    assert website == 'xy.com'
    assert len(result) == 0
    assert R.FILMSIMULATION not in fields
    assert R.DYNAMIC_RANGE not in fields
    assert R.WHITE_BALANCE not in fields
    assert R.WHITE_BALANCE_R not in fields
    assert R.WHITE_BALANCE_B not in fields
    assert R.HIGHLIGHTS not in fields
    assert R.SHADOWS not in fields
    assert R.GRAIN_EFFECT not in fields
    assert R.CCR_EFFECT not in fields
    assert R.CCRFX_BLUE not in fields
    assert R.COLOR not in fields
    assert R.SHARPNESS not in fields
    assert R.HIGH_ISONR not in fields
    assert R.CLARITY not in fields
    assert R.ISO_MIN not in fields
    assert R.ISO_MAX not in fields
    assert R.XTRANS_VERSION not in fields


def test_check_recpipe_full_match_wb_kelvin():

    recipe = { 
        R.NAME:'RECIPE No. 1',
        R.PUBLISHER:'Publisher XY',
        R.WEBSITE:'xy.com',
        R.FILMSIMULATION:FS.REALA_ACE, 
        R.WHITE_BALANCE:WB.KELVIN,
        R.KELVIN:5000,
        R.WHITE_BALANCE_R:-1,
        R.WHITE_BALANCE_B:1,
        R.DYNAMIC_RANGE:DR.DR100,
        R.SHADOWS:1,
        R.HIGHLIGHTS:-1,
        R.GRAIN_EFFECT:GR.OFF,
        R.CCR_EFFECT:CC.OFF,
        R.CCRFX_BLUE:CC.OFF,
        R.COLOR:-1,
        R.SHARPNESS:-1,
        R.HIGH_ISONR:-1,
        R.CLARITY:-1,
        R.ISO_MIN:0,
        R.ISO_MAX:6400,
        R.XTRANS_VERSION:SR.X_V,
        }
    
    exif = {
        R.FILMSIMULATION:FS.REALA_ACE,
        R.DYNAMIC_RANGE:DR.DR100,
        R.WHITE_BALANCE:WB.KELVIN,
        R.KELVIN:5000,
        R.WHITE_BALANCE_R:-1,
        R.WHITE_BALANCE_B:1,
        R.SHADOWS:1,
        R.HIGHLIGHTS:-1,
        R.GRAIN_EFFECT:GR.OFF,
        R.CCR_EFFECT:CC.OFF,
        R.CCRFX_BLUE:CC.OFF,
        R.COLOR:-1,
        R.SHARPNESS:-1,
        R.HIGH_ISONR:-1,
        R.CLARITY:-1,
        R.ISO:3200,
        R.XTRANS_VERSION:SR.X_V,
        }

    (perc, name, publisher, website, result) = reciper.check_recipe(exif, recipe)
    fields = [i[1] for i in result]

    assert perc == 100
    assert name == 'RECIPE No. 1'
    assert publisher == 'Publisher XY'
    assert website == 'xy.com'
    assert len(result) == 0
    assert R.FILMSIMULATION not in fields
    assert R.DYNAMIC_RANGE not in fields
    assert R.WHITE_BALANCE not in fields
    assert R.KELVIN not in fields
    assert R.WHITE_BALANCE_R not in fields
    assert R.WHITE_BALANCE_B not in fields
    assert R.HIGHLIGHTS not in fields
    assert R.SHADOWS not in fields
    assert R.GRAIN_EFFECT not in fields
    assert R.CCR_EFFECT not in fields
    assert R.CCRFX_BLUE not in fields
    assert R.COLOR not in fields
    assert R.SHARPNESS not in fields
    assert R.HIGH_ISONR not in fields
    assert R.CLARITY not in fields
    assert R.ISO_MIN not in fields
    assert R.ISO_MAX not in fields
    assert R.XTRANS_VERSION not in fields


def test_check_recpipe_full_match_monochromatic():

    recipe = { 
        R.NAME:'RECIPE No. 2',
        R.PUBLISHER:'Publisher XY',
        R.WEBSITE:'xy.com',
        R.FILMSIMULATION:FS.ACROS, 
        R.WHITE_BALANCE:WB.AUTO,
        R.WHITE_BALANCE_R:-1,
        R.WHITE_BALANCE_B:1,
        R.DRANGE_PRIORITY:DRP.WEAK,
        R.GRAIN_EFFECT:GR.STRONG_LARGE,
        R.CCR_EFFECT:CC.OFF,
        R.CCRFX_BLUE:CC.OFF,
        R.BW_COLOR_MC:-1,
        R.BW_COLOR_WC:-1,
        R.SHARPNESS:-1,
        R.HIGH_ISONR:-1,
        R.CLARITY:-1,
        R.ISO_MIN:0,
        R.ISO_MAX:6400,
        R.XTRANS_VERSION:SR.X_V,
        }
    
    exif = {
        R.FILMSIMULATION:FS.ACROS,
        R.DRANGE_PRIORITY:DRP.WEAK,
        R.GRAIN_EFFECT:GR.STRONG_LARGE,
        R.WHITE_BALANCE:WB.AUTO,
        R.WHITE_BALANCE_R:-1,
        R.WHITE_BALANCE_B:1,
        R.CCR_EFFECT:CC.OFF,
        R.CCRFX_BLUE:CC.OFF,
        R.BW_COLOR_MC:-1,
        R.BW_COLOR_WC:-1,
        R.SHARPNESS:-1,
        R.HIGH_ISONR:-1,
        R.CLARITY:-1,
        R.ISO:3200,
        R.XTRANS_VERSION:SR.X_V,
        }

    (perc, name, publisher, website, result) = reciper.check_recipe(exif, recipe)
    fields = [i[1] for i in result]

    assert perc == 100
    assert name == 'RECIPE No. 2'
    assert len(result) == 0
    assert R.DYNAMIC_RANGE not in fields
    assert R.WHITE_BALANCE not in fields
    assert R.WHITE_BALANCE_R not in fields
    assert R.WHITE_BALANCE_B not in fields
    assert R.HIGHLIGHTS not in fields
    assert R.SHADOWS not in fields
    assert R.GRAIN_EFFECT not in fields
    assert R.CCR_EFFECT not in fields
    assert R.CCRFX_BLUE not in fields
    assert R.COLOR not in fields
    assert R.SHARPNESS not in fields
    assert R.HIGH_ISONR not in fields
    assert R.CLARITY not in fields
    assert R.ISO_MIN not in fields
    assert R.ISO_MAX not in fields
    assert R.XTRANS_VERSION not in fields


def test_check_recpipe_failed_fields_color_drp_mode():

    recipe = { 
        R.NAME:'RECIPE No. 3',
        R.PUBLISHER:'Publisher XY',
        R.WEBSITE:'xy.com',
        R.FILMSIMULATION:FS.REALA_ACE, 
        R.DRANGE_PRIORITY:DRP.WEAK,
        R.WHITE_BALANCE:WB.AUTO,
        R.WHITE_BALANCE_R:-1,
        R.WHITE_BALANCE_B:1,
        R.GRAIN_EFFECT:GR.WEAK_LARGE,
        R.CCR_EFFECT:CC.OFF,
        R.CCRFX_BLUE:CC.OFF,
        R.COLOR:0,
        R.SHARPNESS:0,
        R.HIGH_ISONR:0,
        R.CLARITY:0,
        R.ISO_MIN:0,
        R.ISO_MAX:6400,
        R.XTRANS_VERSION:SR.X_V,
        }
    
    exif = {
        R.FILMSIMULATION:FS.CLASSIC_CHROME,
        R.DRANGE_PRIORITY:DRP.STRONG,
        R.WHITE_BALANCE:WB.AMBIENCE_PRIORITY,
        R.WHITE_BALANCE_R:1,
        R.WHITE_BALANCE_B:-1,
        R.GRAIN_EFFECT:GR.STRONG_SMALL,
        R.CCR_EFFECT:CC.STRONG,
        R.CCRFX_BLUE:CC.STRONG,
        R.COLOR:1,
        R.SHARPNESS:1,
        R.HIGH_ISONR:1,
        R.CLARITY:1,
        R.ISO:6500,
        R.XTRANS_VERSION:SR.X_I,
        }

    (perc, name, publisher, website, result) = reciper.check_recipe(exif, recipe)
    fields = [i[1] for i in result]

    assert R.FILMSIMULATION in fields
    assert R.DRANGE_PRIORITY in fields
    assert R.WHITE_BALANCE in fields
    assert R.WHITE_BALANCE_R in fields
    assert R.WHITE_BALANCE_B in fields
    assert R.GRAIN_EFFECT not in fields
    assert R.CCR_EFFECT not in fields
    assert R.CCRFX_BLUE not in fields
    assert R.COLOR in fields
    assert R.SHARPNESS in fields
    assert R.HIGH_ISONR in fields
    assert R.CLARITY not in fields
    assert R.ISO_MIN not in fields
    assert R.ISO_MAX in fields
    assert R.XTRANS_VERSION in fields


def test_check_recpipe_failed_fields_color_dr_mode():

    recipe = { 
        R.NAME:'RECIPE No. 3',
        R.PUBLISHER:'Publisher XY',
        R.WEBSITE:'xy.com',
        R.FILMSIMULATION:FS.REALA_ACE, 
        R.DYNAMIC_RANGE:DR.DR100,
        R.WHITE_BALANCE:WB.AMBIENCE_PRIORITY,
        R.WHITE_BALANCE_R:1,
        R.WHITE_BALANCE_B:-1,
        R.SHADOWS:-1,
        R.HIGHLIGHTS:1,
        R.GRAIN_EFFECT:GR.WEAK_LARGE,
        R.CCR_EFFECT:CC.OFF,
        R.CCRFX_BLUE:CC.OFF,
        R.COLOR:0,
        R.SHARPNESS:0,
        R.HIGH_ISONR:0,
        R.CLARITY:0,
        R.ISO_MIN:3200,
        R.ISO_MAX:6400,
        R.XTRANS_VERSION:SR.X_V,
        }
    
    exif = {
        R.FILMSIMULATION:FS.CLASSIC_CHROME,
        R.DYNAMIC_RANGE:DR.DR200,
        R.WHITE_BALANCE:WB.UNDERWATER,
        R.WHITE_BALANCE_R:9,
        R.WHITE_BALANCE_B:-9,
        R.SHADOWS:-2,
        R.HIGHLIGHTS:2,
        R.GRAIN_EFFECT:GR.STRONG_SMALL,
        R.CCR_EFFECT:CC.STRONG,
        R.CCRFX_BLUE:CC.STRONG,
        R.COLOR:1,
        R.SHARPNESS:1,
        R.HIGH_ISONR:1,
        R.CLARITY:1,
        R.ISO:1600,
        R.XTRANS_VERSION:SR.X_I,
        }

    (perc, name, publisher, website, result) = reciper.check_recipe(exif, recipe)
    fields = [i[1] for i in result]

    assert R.FILMSIMULATION in fields
    assert R.DYNAMIC_RANGE in fields
    assert R.WHITE_BALANCE in fields
    assert R.WHITE_BALANCE_R in fields
    assert R.WHITE_BALANCE_B in fields
    assert R.HIGHLIGHTS in fields
    assert R.SHADOWS in fields
    assert R.GRAIN_EFFECT not in fields
    assert R.CCR_EFFECT not in fields
    assert R.CCRFX_BLUE not in fields
    assert R.COLOR in fields
    assert R.SHARPNESS in fields
    assert R.HIGH_ISONR in fields
    assert R.CLARITY not in fields
    assert R.ISO_MIN in fields
    assert R.ISO_MAX not in fields
    assert R.XTRANS_VERSION in fields

