import pytest
import email
import textwrap
from datetime import datetime, timezone

from django_mailbox.models import Mailbox
from crashbin_app.models import (
    Label,
    Bin,
    Report,
    IncomingMessage,
    OutgoingMessage,
    NoteMessage,
)


@pytest.fixture
def label_obj(db):
    return Label.objects.create(name="testlabel", color="#ff0000")


@pytest.fixture
def bin_obj(db):
    return Bin.objects.create(name="testbin")


@pytest.fixture
def report_obj(db, bin_obj):
    return Report.objects.create(title="testreport", bin=bin_obj, log="Debug log")


TIMESTAMP = datetime.fromtimestamp(0, tz=timezone.utc)


@pytest.fixture
def mail_factory():
    def create(subject):
        return email.message_from_string(
            textwrap.dedent(
                f"""
                Date: Tue, 28 May 2019 15:05:40 +0200
                From: Florian Bruhin <me@the-compiler.org>
                To: me@the-compiler.org
                Subject: {subject}
                Message-ID: <20190528130540.h6mfwjmegnlloy4k@hooch.localdomain>
                MIME-Version: 1.0
                Content-Type: text/plain; charset=us-ascii
                Content-Disposition: inline
                User-Agent: NeoMutt/20180716

                Incoming message
                """.strip("\n")
            )
        )

    return create


@pytest.fixture
def mailbox(db):
    return Mailbox.objects.create(name="testmailbox")


@pytest.fixture
def incoming_msg_obj(db, mailbox, report_obj, mail_factory):
    mail = mail_factory("crashbin test email")
    mail_obj = mailbox.process_incoming_message(mail)
    assert mail_obj.subject == "crashbin test email"
    return IncomingMessage.objects.create(
        report=report_obj, mail=mail_obj, created_at=TIMESTAMP
    )


@pytest.fixture
def outgoing_msg_obj(db, report_obj, admin_user):
    return OutgoingMessage.objects.create(
        report=report_obj,
        text="Outgoing message",
        created_at=TIMESTAMP,
        author=admin_user,
    )


@pytest.fixture
def note_msg_obj(db, report_obj, admin_user):
    return NoteMessage.objects.create(
        report=report_obj, text="Note message", created_at=TIMESTAMP, author=admin_user
    )


@pytest.fixture
def admin_client(client, admin_user):
    client.force_login(user=admin_user)
    return client
