import pytest

from crashbin_app.models import Label, Bin, Report


@pytest.fixture
def label_obj(db):
    return Label.objects.create(name='testlabel', color='#ff0000')


@pytest.fixture
def bin_obj(db):
    return Bin.objects.create(name='testbin')


@pytest.fixture
def report_obj(db, bin_obj):
    return Report.objects.create(title='testreport', bin=bin_obj, log='Debug log')


@pytest.fixture
def admin_client(client, admin_user):
    client.force_login(user=admin_user)
    return client
