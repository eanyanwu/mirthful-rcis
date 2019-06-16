from mirthful_rcis.lib import libroom

def test_get_building_manifest(app, room_factory):
    """
    The only thing we can veriy here is the structure of the data
    Additionally, test that when a room gets added, it shows up in the manifest
    """

    with app.app_context():
        manifest = libroom.get_building_manifest()

        assert isinstance(manifest, dict)
        assert len(manifest.keys()) == 0
     
        # Create a room, this should increase the list of keys to 1
        room_factory()

        manifest = libroom.get_building_manifest()

        assert len(manifest.keys()) == 1



def test_get_default_room_areas(app, room_area_factory):
    """
    Test that when a room area gets added, it shows up in the list of room
    areas
    """

    with app.app_context():
        room_areas = libroom.get_default_room_areas()
        
        assert isinstance(room_areas, list)
        assert len(room_areas) == 0

        room_area_factory(name='Test')

        room_areas = libroom.get_default_room_areas()

        assert len(room_areas) == 1
        assert room_areas[0]['room_area_name'] == 'Test'



