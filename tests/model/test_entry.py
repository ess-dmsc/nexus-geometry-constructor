from nexus_constructor.model.entry import Entry
from nexus_constructor.model.instrument import Instrument, SAMPLE_NAME, INSTRUMENT_NAME


def test_entry_as_dict_contains_sample_and_instrument():
    test_entry = Entry()
    test_entry.instrument = Instrument()
    dictionary_output = test_entry.as_dict()

    child_names = [child["name"] for child in dictionary_output["children"]]
    assert SAMPLE_NAME in child_names
    assert INSTRUMENT_NAME in child_names