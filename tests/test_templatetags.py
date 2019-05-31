import attr
import pytest

from crashbin_app.templatetags import utils


def test_label_style(label_obj):
    expected = 'background-color: #ff0000; color: white;'
    assert utils.label_style(label_obj) == expected


@attr.s
class FakeRequest:

    path: str = attr.ib()


@pytest.mark.parametrize('name, path, active', [
    ('home', '/', True),
    ('bins', '/bins', True),
    ('bins', '/bin/23/settings', True),
    ('reports', '/reports', True),
    ('reports', '/report/23/settings', True),
    ('labels', '/labels', True),
    ('labels', '/label/23', True),

    ('home', '/foo', False),
    ('bins', '/foo', False),
    ('reports', '/foo', False),
    ('labels', '/foo', False),
])
def test_active_class(name, path, active):
    context = {'request': FakeRequest(path)}
    expected = 'active' if active else ''
    assert utils.active_class(context, name) == expected
