# Long running tests on image files
import pytest
import reciper
import constants.recipefields as R
import constants.sensor as SR
from os import path

import logging

LOGGER = logging.getLogger(__name__)


# Names for building the path the test images. 
# See README file in testdata for more information.
X_T50 = 'X-T50'
X_S10 = 'X-S10'
cameras = [X_T50, X_S10]

@pytest.mark.parametrize("cam", cameras)
def test_non_recipe_report(cam):
    """Check gather report. Most value of this test is to proof that gather() 
    is callable for all images."""
        
    name = f'testdata/{cam}/{cam}-Automodus.JPG'
    if not path.exists(name):
        LOGGER.warning(f'Missing test image: {name}')
        return
    
    act = reciper.read_file(name)
    exifdata = reciper.gather(act)

    for (k, v) in exifdata:
        assert act[k] == v
