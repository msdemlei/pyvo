'''
The first service in operation the annotates query responses in the fly is Vizier
https://cds/viz-bin/mivotconesearch/VizierParams
Data are mapped on the mango:EpochPropagtion class as it is implemented in the current code.
This test case is based on 2 VOTables:
Both tests check the generation of SkyCoord instances from the MivotInstances buil
for the output of this service.
'''
import pytest
from pyvo.mivot.version_checker import check_astropy_version
from pyvo.mivot.viewer.mivot_instance import MivotInstance
from pyvo.mivot.features.sky_coord_builder import SkyCoordBuilder
from pyvo.mivot.utils.exceptions import NoMatchingDMType

# annotations generated by Vizier as given to the MivotInstance
vizier_dict = {
    "dmtype": "mango:EpochPosition",
    "longitude": {
        "dmtype": "ivoa:RealQuantity",
        "value": 52.26722684,
        "unit": "deg",
        "ref": "RAICRS",
    },
    "latitude": {
        "dmtype": "ivoa:RealQuantity",
        "value": 59.94033461,
        "unit": "deg",
        "ref": "DEICRS",
    },
    "pmLongitude": {
        "dmtype": "ivoa:RealQuantity",
        "value": -0.82,
        "unit": "mas/yr",
        "ref": "pmRA",
    },
    "pmLatitude": {
        "dmtype": "ivoa:RealQuantity",
        "value": -1.85,
        "unit": "mas/yr",
        "ref": "pmDE",
    },
    "epoch": {
        "dmtype": "ivoa:RealQuantity",
        "value": 1991.25,
        "unit": "yr",
        "ref": None,
    },
    "coordSys": {
        "dmtype": "coords:SpaceSys",
        "dmid": "SpaceFrame_ICRS",
        "dmrole": "coords:Coordinate.coordSys",
        "spaceRefFrame": {
            "dmtype": "coords:SpaceFrame",
            "value": "ICRS",
            "unit": None,
            "ref": None,
        },
    },
}
# The same edited by hand (parallax added and FK5 + Equinox frame)
vizier_equin_dict = {
    "dmtype": "mango:EpochPosition",
    "longitude": {
        "dmtype": "ivoa:RealQuantity",
        "value": 52.26722684,
        "unit": "deg",
        "ref": "RAICRS",
    },
    "latitude": {
        "dmtype": "ivoa:RealQuantity",
        "value": 59.94033461,
        "unit": "deg",
        "ref": "DEICRS",
    },
    "pmLongitude": {
        "dmtype": "ivoa:RealQuantity",
        "value": -0.82,
        "unit": "mas/yr",
        "ref": "pmRA",
    },
    "pmLatitude": {
        "dmtype": "ivoa:RealQuantity",
        "value": -1.85,
        "unit": "mas/yr",
        "ref": "pmDE",
    },
    "parallax": {
        "dmtype": "ivoa:RealQuantity",
        "value": 0.6,
        "unit": "mas",
        "ref": "parallax",
    },
    "epoch": {
        "dmtype": "ivoa:RealQuantity",
        "value": 1991.25,
        "unit": "yr",
        "ref": None,
    },
    "coordSys": {
        "dmtype": "coords:SpaceSys",
        "dmid": "SpaceFrame_ICRS",
        "dmrole": "coords:Coordinate.coordSys",
        "spaceRefFrame": {
            "dmtype": "coords:SpaceFrame.spaceRefFrame",
            "value": "FK5",
            "unit": None,
            "ref": None,
        },
        "equinox": {
            "dmtype": "coords:SpaceFrame.equinox",
            "value": "2012",
            "unit": "yr",
        },
    },
}

# The same edited mapped on a dummy class
vizier_dummy_type = {
    "dmtype": "mango:DumyType",
    "longitude": {
        "dmtype": "ivoa:RealQuantity",
        "value": 52.26722684,
        "unit": "deg",
        "ref": "RAICRS",
    },
    "latitude": {
        "dmtype": "ivoa:RealQuantity",
        "value": 59.94033461,
        "unit": "deg",
        "ref": "DEICRS",
    },
    "pmLongitude": {
        "dmtype": "ivoa:RealQuantity",
        "value": -0.82,
        "unit": "mas/yr",
        "ref": "pmRA",
    },
    "pmLatitude": {
        "dmtype": "ivoa:RealQuantity",
        "value": -1.85,
        "unit": "mas/yr",
        "ref": "pmDE",
    },
    "parallax": {
        "dmtype": "ivoa:RealQuantity",
        "value": 0.6,
        "unit": "mas",
        "ref": "parallax",
    },
    "epoch": {
        "dmtype": "ivoa:RealQuantity",
        "value": 1991.25,
        "unit": "yr",
        "ref": None,
    },
    "coordSys": {
        "dmtype": "coords:SpaceSys",
        "dmid": "SpaceFrame_ICRS",
        "dmrole": "coords:Coordinate.coordSys",
        "spaceRefFrame": {
            "dmtype": "coords:SpaceFrame.spaceRefFrame",
            "value": "FK5",
            "unit": None,
            "ref": None,
        },
        "equinox": {
            "dmtype": "coords:SpaceFrame.equinox",
            "value": "2012",
            "unit": "yr",
        },
    },
}


def test_no_matching_mapping():
    """
    Test that a NoMatchingDMType is raised not mapped on mango:EpochPosition
    """
    with pytest.raises(NoMatchingDMType):
        mivot_instance = MivotInstance(**vizier_dummy_type)
        scb = SkyCoordBuilder(mivot_instance.to_dict())
        scb.build_sky_coord()


@pytest.mark.skipif(not check_astropy_version(), reason="need astropy 6+")
def test_vizier_output():
    """ Test the SkyCoord issued from the Vizier response
    """
    mivot_instance = MivotInstance(**vizier_dict)
    scb = SkyCoordBuilder(mivot_instance.to_dict())
    scoo = scb.build_sky_coord()
    assert (str(scoo).replace("\n", "").replace("  ", "")
            == "<SkyCoord (ICRS): (ra, dec) in deg(52.26722684, 59.94033461) "
               "(pm_ra_cosdec, pm_dec) in mas / yr(-0.82, -1.85)>")
    scoo = mivot_instance.get_SkyCoord()
    assert (str(scoo).replace("\n", "").replace("  ", "")
            == "<SkyCoord (ICRS): (ra, dec) in deg(52.26722684, 59.94033461) "
               "(pm_ra_cosdec, pm_dec) in mas / yr(-0.82, -1.85)>")

    vizier_dict["coordSys"]["spaceRefFrame"]["value"] = "Galactic"
    mivot_instance = MivotInstance(**vizier_dict)
    scoo = mivot_instance.get_SkyCoord()
    assert (str(scoo).replace("\n", "").replace("  ", "")
            == "<SkyCoord (Galactic): (l, b) in deg(52.26722684, 59.94033461) "
               "(pm_l_cosb, pm_b) in mas / yr(-0.82, -1.85)>")

    vizier_dict["coordSys"]["spaceRefFrame"]["value"] = "QWERTY"
    mivot_instance = MivotInstance(**vizier_dict)
    scoo = mivot_instance.get_SkyCoord()
    assert (str(scoo).replace("\n", "").replace("  ", "")
            == "<SkyCoord (ICRS): (ra, dec) in deg(52.26722684, 59.94033461) "
               "(pm_ra_cosdec, pm_dec) in mas / yr(-0.82, -1.85)>")


@pytest.mark.skipif(not check_astropy_version(), reason="need astropy 6+")
def test_vizier_output_with_equinox_and_parallax():
    """Test the SkyCoord issued from the modofier Vizier response *
    (parallax added and FK5 + Equinox frame)
    """
    mivot_instance = MivotInstance(**vizier_equin_dict)
    scb = SkyCoordBuilder(mivot_instance.to_dict())
    scoo = scb.build_sky_coord()
    assert (str(scoo).replace("\n", "").replace("  ", "")
            == "<SkyCoord (FK5: equinox=J2012.000): (ra, dec, distance) in "
               "(deg, deg, pc)(52.26722684, 59.94033461, 600.) "
               "(pm_ra_cosdec, pm_dec) in mas / yr(-0.82, -1.85)>")

    vizier_equin_dict["coordSys"]["spaceRefFrame"]["value"] = "FK4"
    mivot_instance = MivotInstance(**vizier_equin_dict)
    scoo = mivot_instance.get_SkyCoord()
    assert (str(scoo).replace("\n", "").replace("  ", "")
            == "<SkyCoord (FK4: equinox=B2012.000, obstime=J1991.250): (ra, dec, distance) in "
               "(deg, deg, pc)(52.26722684, 59.94033461, 600.) "
               "(pm_ra_cosdec, pm_dec) in mas / yr(-0.82, -1.85)>")
