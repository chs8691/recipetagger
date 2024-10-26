import pytest
from customs import read_template
from customs import create_custom
from customs import search_tag
from customs import map_drpriority
from customs import map_dynamicrange
from customs import map_filmsimulation
from customs import map_whitebalance
from constants import recipefields as R
from constants import dynamicrange as DR
from constants import recipefields as R
from constants import grain as GR
from constants import colorchrome as CC
from constants import whitebalance as WB
from constants import filmsimulations as FS
from constants import whitebalance as WB
from constants import drangepriority as DP
from constants import customfields as C

from os import path

import logging

LOGGER = logging.getLogger(__name__)


# Names for building the path the test images. 
# See README file in testdata for more information.
X_T50 = 'X-T50'
X_S10 = 'X-S10'
cameras = [X_T50, X_S10]

# #############################################################################
# Compares X Raw Studio file content with created content.
# #############################################################################

@pytest.mark.parametrize("cam", cameras)
def test_min(cam):
        
    template_file = path.join('testdata', 'customs', cam, 'test-decimals.FP1')
    if not path.exists(template_file):
        LOGGER.warning(f'Missing template customs: {template_file}')
        return
    
    exp_file = path.join('testdata', 'customs', cam, 'test-min.FP1')
    if not path.exists(exp_file):
        LOGGER.warning(f'Missing destination customs: {exp_file}')
        return
    
    
    (tcam, tlines) = read_template(template_file)

    recipe = {R.NAME:'test-min',
              R.DYNAMIC_RANGE:DR.DR100,
              R.DRANGE_PRIORITY:DP.WEAK,
              R.FILMSIMULATION:FS.PROVIA,
              R.BW_COLOR_WC:'-18',
              R.BW_COLOR_MC:'-18',
              R.GRAIN_EFFECT:GR.WEAK_LARGE,
              R.CCR_EFFECT:CC.WEAK,
              R.CCRFX_BLUE:CC.STRONG,
              R.WHITE_BALANCE:WB.KELVIN,
              R.WHITE_BALANCE_R:'-1',
              R.WHITE_BALANCE_B:'1',
              R.KELVIN:'7010',
              R.GRAIN_EFFECT:GR.OFF,
              R.CCR_EFFECT:CC.OFF,
              R.CCRFX_BLUE:CC.OFF,
              R.WHITE_BALANCE:WB.KELVIN,
              R.KELVIN:'2500',
              R.HIGHLIGHTS:'-2',
              R.SHADOWS:'-2',
              R.COLOR:'-4',
              R.SHARPNESS:'-4',
              R.HIGH_ISONR:'-4',
              R.CLARITY:'-5',
              }

    act = create_custom(recipe, tlines)

    (exp_cam, exp_lines) = read_template(exp_file)

    assert tcam == cam
    
    field = R.DYNAMIC_RANGE
    tag = C.DYNAMIC_RANGE
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    assert exp_count == 1
    assert exp_value == map_dynamicrange(recipe[field])
    
    field = R.DRANGE_PRIORITY
    tag = C.WIDE_D_RANGE
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    assert exp_count == 1
    assert exp_value == map_drpriority(recipe[field])

    field = R.FILMSIMULATION
    tag = C.FILM_SIMULATION
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    assert exp_count == 1
    assert exp_value == map_filmsimulation(recipe[field])

    field = R.BW_COLOR_WC
    tag = C.BLACK_IMAGE_TONE
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    assert exp_count == 1
    assert exp_value == recipe[field]

    field = R.BW_COLOR_MC
    tag = C.MONOCHROMATIC_COLOR_RG
    ((exp_count, exp_index, exp_value)) = search_tag(tag, exp_lines)
    assert exp_count == 1
    assert exp_value == recipe[field]


