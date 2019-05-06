import pytest

from crashbin_app.models import Label, Bin, Report


pytestmark = pytest.mark.django_db


@pytest.fixture
def label_obj():
    return Label.objects.create(name='testlabel', color='#ff0000')


@pytest.fixture
def bin_obj():
    return Bin.objects.create(name='testbin')


@pytest.fixture
def report_obj(bin_obj):
    return Report.objects.create(title='testreport', bin=bin_obj)


def test_label(label_obj):
    assert str(label_obj) == 'testlabel'


def test_bin(bin_obj):
    assert str(bin_obj) == 'testbin'


def test_report(report_obj):
    assert str(report_obj) == 'testreport'
