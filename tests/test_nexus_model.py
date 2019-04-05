from nexus_constructor.nexus_model import (
    NexusModel,
    get_nx_class_for_component,
    create_group,
    ComponentType,
)
import h5py

sample_name = "NXsample"
detector_name = "NXdetector"
monitor_name = "NXmonitor"
source_name = "NXsource"
slit_name = "NXslit"
moderator_name = "NXmoderator"
chopper_name = "NXdisk_chopper"
instrument_name = "NXinstrument"
entry_name = "NXentry"


def test_GIVEN_detector_WHEN_get_nx_class_THEN_returns_correct_component_name():
    component = ComponentType.DETECTOR
    assert get_nx_class_for_component(component) == detector_name


def test_GIVEN_sample_WHEN_get_nx_class_THEN_returns_correct_component_name():
    component = ComponentType.SAMPLE
    assert get_nx_class_for_component(component) == sample_name


def test_GIVEN_monitor_WHEN_get_nx_class_THEN_returns_correct_component_name():
    component = ComponentType.MONITOR
    assert get_nx_class_for_component(component) == monitor_name


def test_GIVEN_source_WHEN_get_nx_class_THEN_returns_correct_component_name():
    component = ComponentType.SOURCE
    assert get_nx_class_for_component(component) == source_name


def test_GIVEN_slit_WHEN_get_nx_class_THEN_returns_correct_component_name():
    component = ComponentType.SLIT
    assert get_nx_class_for_component(component) == slit_name


def test_GIVEN_moderator_WHEN_get_nx_class_THEN_returns_correct_component_name():
    component = ComponentType.MODERATOR
    assert get_nx_class_for_component(component) == moderator_name


def test_GIVEN_chopper_WHEN_get_nx_class_THEN_returns_correct_component_name():
    component = ComponentType.DISK_CHOPPER
    assert get_nx_class_for_component(component) == chopper_name


def test_GIVEN_nothing_WHEN_creating_nexus_model_THEN_creates_entry_group_with_correct_nx_class():
    model = NexusModel()
    assert model.getEntryGroup().attrs["NX_class"] == entry_name


def test_GIVEN_another_variable_WHEN_setting_entry_group_THEN_variable_does_not_change():
    model = NexusModel()
    original = model.getEntryGroup()
    model.setEntryGroup("test")
    assert original == model.getEntryGroup()


def test_GIVEN_nonstandard_nxclass_WHEN_creating_group_THEN_group_is_still_created():
    name = "test"
    nx_class = "NXarbitrary"
    nexus_file = h5py.File(name, driver="core", backing_store=False)
    create_group(name, nx_class, nexus_file)

    assert nexus_file[name].attrs["NX_class"] == nx_class
