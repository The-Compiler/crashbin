import pytest

from crashbin_app import models


pytestmark = pytest.mark.django_db


def test_label(label_obj):
    assert str(label_obj) == 'testlabel'


def test_bin(bin_obj):
    assert str(bin_obj) == 'testbin'


def test_report(report_obj):
    assert str(report_obj) == 'testreport'


@pytest.mark.parametrize('subject, error', [
    ('qutebrowser report #1', None),
    ('Re: qutebrowser report #1', None),
    ('Does not match subject',
     'Got incoming email with unknown subject: Does not match subject'),
    ('qutebrowser report #drölfzig',
     'Could not parse report ID from mail subject: qutebrowser report #drölfzig'),
    ('qutebrowser report #666',
     'Could not find report for mail: qutebrowser report #666'),
])
def test_report_for_mail_subject(report_obj, subject, error):
    if error is None:
        report = models.Report.for_mail_subject(subject)
        assert report.id == report_obj.id
    else:
        with pytest.raises(models.InvalidMailError) as excinfo:
            models.Report.for_mail_subject(subject)
        assert str(excinfo.value) == error
