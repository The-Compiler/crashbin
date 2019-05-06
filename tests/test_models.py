import pytest

pytestmark = pytest.mark.django_db


def test_label(label_obj):
    assert str(label_obj) == 'testlabel'


def test_bin(bin_obj):
    assert str(bin_obj) == 'testbin'


def test_report(report_obj):
    assert str(report_obj) == 'testreport'
