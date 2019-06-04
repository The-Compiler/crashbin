from crashbin_app import signals, models


def test_invalid_incoming_mail(mailbox, mail_factory, caplog):
    mail = mail_factory("Random subject")
    mailbox.process_incoming_message(mail)
    assert caplog.messages == [
        "Got incoming email with unknown subject: Random subject"
    ]
    assert not models.IncomingMessage.objects.exists()


def test_valid_incoming_mail(mailbox, mail_factory, caplog, report_obj):
    mail = mail_factory("qutebrowser report #{}".format(report_obj.id))
    mailbox_message = mailbox.process_incoming_message(mail)
    message = models.IncomingMessage.objects.get()

    assert message.mail == mailbox_message
    assert message.report == report_obj
    assert not caplog.messages


def test_report_saved(mocker, bin_obj):
    mock = mocker.Mock()
    signals.new_report.connect(mock)

    report = models.Report.objects.create(title="testreport 2", bin=bin_obj)
    report.title = "changing title"
    report.save()

    mock.assert_called_once_with(report=report, sender=None, signal=mocker.ANY)
