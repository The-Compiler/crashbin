import pytest
from django import urls

from crashbin_app.models import Bin


pytestmark = pytest.mark.django_db


def test_home(client):
    response = client.get(urls.reverse('home'))
    assert response.status_code == 200
    assert b'Bins you maintain' in response.content


def test_report_list(client, report_obj):
    response = client.get(urls.reverse('report_list'))
    assert response.status_code == 200
    assert b'>testreport<' in response.content
    assert b'href="/report/1/"' in response.content


def test_report_detail(client, report_obj):
    response = client.get(urls.reverse('report_detail', kwargs={'pk': 1}))
    assert response.status_code == 200
    assert b'<h1>testreport</h1>' in response.content
    assert b'<pre>Debug log</pre>' in response.content


def test_bin_list(client, bin_obj):
    response = client.get(urls.reverse('bin_list'))
    assert response.status_code == 200
    print(response.content.decode('utf-8'))
    assert b'>testbin<' in response.content
    assert b'href="/bin/1/"' in response.content


def test_bin_detail(client, bin_obj):
    response = client.get(urls.reverse('bin_detail', kwargs={'pk': 1}))
    assert response.status_code == 200
    assert b'>testbin<' in response.content


def test_bin_new_post(client):
    assert Bin.objects.count() == 0

    response = client.post(urls.reverse('bin_new'), {'name': 'newbin'})

    assert response.status_code == 302
    assert response.url == '/bin/1/'

    assert Bin.objects.count() == 1
    bin_obj = Bin.objects.first()
    assert bin_obj.name == 'newbin'


def test_bin_new_get(client):
    response = client.get(urls.reverse('bin_new'))
    assert response.status_code == 200
    assert b'<form method="POST"' in response.content
    assert b'csrfmiddlewaretoken' in response.content
