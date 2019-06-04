from http import HTTPStatus

import pytest
from rest_framework import test
from django import urls

from crashbin_app.models import Report, Bin


pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client_unauth():
    return test.APIClient()


@pytest.fixture
def api_client(api_client_unauth, admin_user):
    client = api_client_unauth
    client.force_login(user=admin_user)
    return client


@pytest.fixture
def report_detail_url(report_obj):
    return urls.reverse("api-report-detail", kwargs={"pk": report_obj.id})


@pytest.fixture
def bin_detail_url(bin_obj):
    return urls.reverse("api-bin-detail", kwargs={"pk": bin_obj.id})


def test_create_report(api_client_unauth):
    url = urls.reverse("api_report_new")
    r = api_client_unauth.post(url, {"title": "Report", "log": "Hello World"})
    assert r.status_code == HTTPStatus.CREATED
    report = Report.objects.get()
    assert report.title == "Report"
    assert report.log == "Hello World"


def test_delete_report(api_client, report_obj, report_detail_url):
    r = api_client.delete(report_detail_url)
    assert r.status_code == HTTPStatus.NO_CONTENT
    with pytest.raises(Report.DoesNotExist):
        report_obj.refresh_from_db()


def test_delete_report_unauth(api_client_unauth, report_obj, report_detail_url):
    r = api_client_unauth.delete(report_detail_url)
    assert r.status_code == HTTPStatus.FORBIDDEN
    report_obj.refresh_from_db()


def test_bin_archive(api_client, bin_obj, bin_detail_url):
    assert not bin_obj.is_archived
    r = api_client.patch(bin_detail_url, {"is_archived": True}, format="json")
    assert r.status_code == HTTPStatus.OK
    bin_obj.refresh_from_db()
    assert bin_obj.is_archived


def test_bin_archive_unauth(api_client_unauth, bin_obj):
    assert not bin_obj.is_archived
    r = api_client_unauth.patch(bin_detail_url, {"is_archived": True}, format="json")
    assert r.status_code == HTTPStatus.NOT_FOUND
    assert not bin_obj.is_archived


def test_bin_delete(api_client, bin_detail_url, bin_obj):
    r = api_client.delete(bin_detail_url)
    assert r.status_code == HTTPStatus.NO_CONTENT
    with pytest.raises(Bin.DoesNotExist):
        bin_obj.refresh_from_db()


def test_bin_delete_unauth(api_client_unauth, bin_detail_url, bin_obj):
    r = api_client_unauth.delete(bin_detail_url)
    assert r.status_code == HTTPStatus.FORBIDDEN
    bin_obj.refresh_from_db()
