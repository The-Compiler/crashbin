import pytest
from django.db.utils import IntegrityError

from crashbin_app import models, signals


pytestmark = pytest.mark.django_db


class TestLabel:

    def test_str(self, label_obj):
        assert str(label_obj) == 'testlabel'

    def test_name_is_unique(self, label_obj):
        with pytest.raises(IntegrityError):
            models.Label.objects.create(name=label_obj.name, color='#ff0000')


class TestBin:

    def test_str(self, bin_obj):
        assert str(bin_obj) == 'testbin'

    def test_name_is_unique(self, bin_obj):
        with pytest.raises(IntegrityError):
            models.Bin.objects.create(name=bin_obj.name)


class TestReport:

    def test_str(self, report_obj):
        assert str(report_obj) == 'testreport'

    def test_all_messages(self, report_obj, incoming_msg_obj, outgoing_msg_obj, note_msg_obj):
        messages = report_obj.all_messages()
        assert len(messages) == 3

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
    def test_for_mail_subject(self, report_obj, subject, error):
        if error is None:
            report = models.Report.for_mail_subject(subject)
            assert report.id == report_obj.id
        else:
            with pytest.raises(models.InvalidMailError) as excinfo:
                models.Report.for_mail_subject(subject)
            assert str(excinfo.value) == error

    def test_assign_to_bin(self, report_obj, bin_obj, admin_user, mocker):
        new_bin = models.Bin.objects.create(name='testbin 2')
        mock = mocker.Mock()
        signals.bin_assigned.connect(mock)

        report_obj.assign_to_bin(new_bin, user=admin_user)

        mock.assert_called_with(report=report_obj, old_bin=bin_obj, new_bin=new_bin,
                                user=admin_user, signal=mocker.ANY, sender=mocker.ANY)
        report_obj.refresh_from_db()
        assert report_obj.bin == new_bin


class TestIncomingMessage:

    def test_str(self, incoming_msg_obj):
        expected = 'Message from me@the-compiler.org at Thu Jan  1 00:00:00 1970'
        assert str(incoming_msg_obj) == expected

    def test_author_str(self, incoming_msg_obj):
        assert incoming_msg_obj.author_str() == 'me@the-compiler.org'

    def test_contents(self, incoming_msg_obj):
        assert incoming_msg_obj.contents() == 'Incoming message'


class TestNoteMessage:

    def test_str(self, note_msg_obj):
        expected = 'Note from admin at Thu Jan  1 00:00:00 1970'
        assert str(note_msg_obj) == expected

    def test_author_str(self, note_msg_obj):
        assert note_msg_obj.author_str() == 'admin'

    def test_author_str_unset(self, note_msg_obj):
        note_msg_obj.author = None
        assert note_msg_obj.author_str() == '<unknown>'

    def test_contents(self, note_msg_obj):
        assert note_msg_obj.contents() == 'Note message'


class TestOutgoingMessage:

    def test_str(self, outgoing_msg_obj):
        expected = 'Reply from admin at Thu Jan  1 00:00:00 1970'
        assert str(outgoing_msg_obj) == expected

    def test_author_str(self, outgoing_msg_obj):
        assert outgoing_msg_obj.author_str() == 'admin'

    def test_author_str_unset(self, outgoing_msg_obj):
        outgoing_msg_obj.author = None
        assert outgoing_msg_obj.author_str() == '<unknown>'

    def test_contents(self, outgoing_msg_obj):
        assert outgoing_msg_obj.contents() == 'Outgoing message'
