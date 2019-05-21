import pytest
from django import urls

from crashbin_app.models import Bin


pytestmark = pytest.mark.django_db


def test_home(admin_client):
    response = admin_client.get(urls.reverse('home'))
    assert response.status_code == 200
    assert b'Bins you maintain' in response.content


@pytest.mark.parametrize('query, matches', [
    (None, True),
    ('test', True),
    ('Test', True),
    ('', True),
    ('blah', False),
])
def test_report_list(admin_client, report_obj, query, matches):
    url = urls.reverse('report_list')
    if query is not None:
        url += '?q={}'.format(query)

    response = admin_client.get(url)
    assert response.status_code == 200
    assert (b'>testreport<' in response.content) == matches
    assert (b'href="/report/1/"' in response.content) == matches


def test_report_detail(admin_client, report_obj):
    response = admin_client.get(
        urls.reverse('report_detail', kwargs={'pk': report_obj.id}))
    assert response.status_code == 200
    assert b'>testreport<' in response.content
    assert b'>Debug log<' in response.content


@pytest.mark.parametrize('query, matches', [
    (None, True),
    ('test', True),
    ('Test', True),
    ('', True),
    ('blah', False),
])
def test_bin_list(admin_client, bin_obj, query, matches):
    url = urls.reverse('bin_list')
    if query is not None:
        url += '?q={}'.format(query)

    response = admin_client.get(url)
    assert response.status_code == 200
    assert (b'>testbin<' in response.content) == matches


@pytest.mark.parametrize('scope', ['Reports', 'Bins'])
def test_search_dispatch(admin_client, bin_obj, report_obj, scope):
    url = urls.reverse('search_dispatch') + '?q=foo&scope={}'.format(scope)
    message = 'No {} found'.format(scope.lower())

    response = admin_client.get(url)

    assert response.status_code == 200
    assert message in response.content.decode()


def test_bin_detail(admin_client, bin_obj):
    response = admin_client.get(
        urls.reverse('bin_detail', kwargs={'pk': bin_obj.id}))
    assert response.status_code == 200
    assert b'>testbin<' in response.content


def test_bin_new_post(admin_client):
    response = admin_client.post(urls.reverse('bin_new_edit'), {'name': 'newbin'})

    assert response.status_code == 302

    bin_obj = Bin.objects.get(name='newbin')
    assert bin_obj.name == 'newbin'
    assert response.url == urls.reverse('bin_detail',
                                        kwargs={'pk': bin_obj.id})


def test_bin_new_get(admin_client):
    response = admin_client.get(urls.reverse('bin_new_edit'))
    assert response.status_code == 200
    assert b'<form method="POST"' in response.content
    assert b'csrfmiddlewaretoken' in response.content


def test_logged_out(client):
    response = client.get(urls.reverse('home'))
    assert response.status_code == 302
    assert response.url == urls.reverse('login') + '?next=/'
