from nexus_constructor.filewriter_command_widget import FilewriterCommandWidget


def test_UI_GIVEN_user_presses_disable_start_time_THEN_start_time_line_edit_is_disabled(
    qtbot,
):
    dialog = FilewriterCommandWidget()
    assert dialog.start_time_picker.isEnabled()
    dialog.start_time_enabled.setChecked(False)
    assert not dialog.start_time_picker.isEnabled()


def test_UI_GIVEN_user_presses_disable_stop_time_THEN_stop_time_picker_is_disabled():
    dialog = FilewriterCommandWidget()
    assert not dialog.stop_time_picker.isEnabled()
    dialog.stop_time_enabled.setChecked(False)
    assert not dialog.stop_time_picker.isEnabled()


def test_UI_GIVEN_user_presses_enable_start_time_THEN_start_time_picker_is_enabled():
    dialog = FilewriterCommandWidget()
    assert dialog.start_time_picker.isEnabled()
    dialog.start_time_enabled.setChecked(True)
    assert dialog.start_time_picker.isEnabled()


def test_UI_GIVEN_user_presses_enable_stop_time_THEN_stop_time_picker_is_enabled():
    dialog = FilewriterCommandWidget()
    assert not dialog.stop_time_picker.isEnabled()
    dialog.stop_time_enabled.setChecked(True)
    assert dialog.stop_time_picker.isEnabled()
