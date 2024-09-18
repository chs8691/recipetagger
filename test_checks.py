import pytest
import exifing as ex
import reciping as rp
import reciper
import constants.recipefields as R
import constants.filmsimulations as FS
import constants.grain as GR
import constants.dynamicrange as DR
import constants.drangepriority as DP
import constants.whitebalance as WB
import constants.sensor as SR
import constants.colorchrome as CC
import constants.bwfilter as BWF

import logging

LOGGER = logging.getLogger(__name__)


def test_check_recpipe_full_match_color():

    recipe = { 
        R.FILMSIMULATION:FS.REALA_ACE, 
        R.GRAIN_EFFECT:GR.OFF,
        R.CCR_EFFECT:CC.OFF,
        R.CCRFX_BLUE:CC.OFF,
        R.COLOR:-1,
        R.SHARPNESS:-1,
        R.HIGH_ISONR:-1,
        R.CLARITY:-1,
        }
    
    exif = {
        R.FILMSIMULATION:FS.REALA_ACE,
        R.GRAIN_EFFECT:GR.OFF,
        R.CCR_EFFECT:CC.OFF,
        R.CCRFX_BLUE:CC.OFF,
        R.COLOR:-1,
        R.SHARPNESS:-1,
        R.HIGH_ISONR:-1,
        R.CLARITY:-1,
        }

    (perc, fields) = reciper.check_recipe(exif, recipe)

    assert perc == 100
    assert len(fields) == 0


def test_check_recpipe_full_match_monochromatic():

    recipe = { 
        R.FILMSIMULATION:FS.ACROS, 
        R.GRAIN_EFFECT:GR.STRONG_LARGE,
        R.CCR_EFFECT:CC.OFF,
        R.CCRFX_BLUE:CC.OFF,
        R.BW_COLOR_MC:-1,
        R.BW_COLOR_WC:-1,
        R.SHARPNESS:-1,
        R.HIGH_ISONR:-1,
        R.CLARITY:-1,
        }
    
    exif = {
        R.FILMSIMULATION:FS.ACROS,
        R.GRAIN_EFFECT:GR.STRONG_LARGE,
        R.CCR_EFFECT:CC.OFF,
        R.CCRFX_BLUE:CC.OFF,
        R.BW_COLOR_MC:-1,
        R.BW_COLOR_WC:-1,
        R.SHARPNESS:-1,
        R.HIGH_ISONR:-1,
        R.CLARITY:-1,
        }

    (perc, fields) = reciper.check_recipe(exif, recipe)

    assert perc == 100
    assert len(fields) == 0


def test_check_recpipe_failed_fields_color():

    recipe = { 
        R.FILMSIMULATION:FS.REALA_ACE, 
        R.GRAIN_EFFECT:GR.WEAK_LARGE,
        R.CCR_EFFECT:CC.OFF,
        R.CCRFX_BLUE:CC.OFF,
        R.COLOR:0,
        R.SHARPNESS:0,
        R.HIGH_ISONR:0,
        R.CLARITY:0,
        }
    
    exif = {
        R.FILMSIMULATION:FS.CLASSIC_CHROME,
        R.GRAIN_EFFECT:GR.STRONG_SMALL,
        R.CCR_EFFECT:CC.STRONG,
        R.CCRFX_BLUE:CC.STRONG,
        R.COLOR:1,
        R.SHARPNESS:1,
        R.HIGH_ISONR:1,
        R.CLARITY:1,
        }

    (perc, fields) = reciper.check_recipe(exif, recipe)

    assert R.FILMSIMULATION in fields
    assert R.GRAIN_EFFECT in fields
    assert R.CCR_EFFECT in fields
    assert R.CCRFX_BLUE in fields
    assert R.COLOR in fields
    assert R.SHARPNESS in fields
    assert R.HIGH_ISONR in fields
    assert R.CLARITY in fields

