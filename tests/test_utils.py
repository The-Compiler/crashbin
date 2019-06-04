import pytest

from crashbin_app import utils


def test_color_from_hex():
    assert utils.Color.from_hex("#112233") == utils.Color(0x11, 0x22, 0x33)


@pytest.mark.parametrize("bg, fg", [("#000000", "white"), ("#ffffff", "black")])
def test_font_color(bg, fg):
    assert utils.Color.from_hex(bg).font_color() == fg


@pytest.fixture
def plugin_path(tmp_path, monkeypatch):
    monkeypatch.setattr(utils.config, "HOMEDIR", tmp_path)
    path = tmp_path / "plugins"
    path.mkdir()
    return path


def test_load_plugins_invalid(plugin_path, caplog):
    py_file = plugin_path / "brokenplugin.py"
    py_file.write_text("import doesnotexist")
    utils.load_plugins()
    assert caplog.messages == ["Exception while loading plugin: brokenplugin"]


def test_load_plugins_success(plugin_path, caplog, capsys):
    py_file = plugin_path / "workingplugin.py"
    py_file.write_text('print("Hello from plugin")')
    utils.load_plugins()

    stdout, stderr = capsys.readouterr()
    assert stdout == "Hello from plugin\n"
    assert not stderr
    assert caplog.messages == ["Loaded plugin: workingplugin"]
