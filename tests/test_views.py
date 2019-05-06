import pytest
from django import urls

from crashbin_app.models import Bin


pytestmark = pytest.mark.django_db


def test_home(admin_client):
    response = admin_client.get(urls.reverse('home'))
    assert response.status_code == 200
    assert b'Bins you maintain' in response.content


def test_report_list(admin_client, report_obj):
    response = admin_client.get(urls.reverse('report_list'))
    assert response.status_code == 200
    assert b'>testreport<' in response.content
    assert b'href="/report/1/"' in response.content


def test_report_detail(admin_client, report_obj):
    response = admin_client.get(
        urls.reverse('report_detail', kwargs={'pk': report_obj.id}))
    assert response.status_code == 200
    assert b'<h1>testreport</h1>' in response.content
    assert b'<pre>Debug log</pre>' in response.content


def test_bin_list(admin_client, bin_obj):
    response = admin_client.get(urls.reverse('bin_list'))
    assert response.status_code == 200
    print(response.content.decode('utf-8'))
    assert b'>testbin<' in response.content
    assert b'href="/bin/1/"' in response.content


def test_bin_detail(admin_client, bin_obj):
    response = admin_client.get(
        urls.reverse('bin_detail', kwargs={'pk': bin_obj.id}))
    print(response.content.decode())
    assert response.status_code == 200
    assert b'>testbin<' in response.content


def test_bin_new_post(admin_client):
    response = admin_client.post(urls.reverse('bin_new'), {'name': 'newbin'})

    assert response.status_code == 302

    bin_obj = Bin.objects.get(name='newbin')
    assert bin_obj.name == 'newbin'
    assert response.url == urls.reverse('bin_detail',
                                        kwargs={'pk': bin_obj.id})


def test_bin_new_get(admin_client):
    response = admin_client.get(urls.reverse('bin_new'))
    assert response.status_code == 200
    assert b'<form method="POST"' in response.content
    assert b'csrfmiddlewaretoken' in response.content


def test_logged_out(client):
    response = client.get(urls.reverse('home'))
    assert response.status_code == 302
    assert response.url == urls.reverse('login') + '?next=/'
