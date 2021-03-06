from http import HTTPStatus

import pytest
from django import urls

from crashbin_app.models import Bin, OutgoingMessage, NoteMessage, Label


pytestmark = pytest.mark.django_db


def test_home(admin_client):
    response = admin_client.get(urls.reverse("home"))
    assert response.status_code == HTTPStatus.OK
    assert b"Bins you maintain" in response.content


@pytest.mark.parametrize(
    "query, matches",
    [(None, True), ("test", True), ("Test", True), ("", True), ("blah", False)],
)
def test_report_list(admin_client, report_obj, query, matches):
    url = urls.reverse("report_list")
    if query is not None:
        url += f"?q={query}"

    response = admin_client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert (b">testreport<" in response.content) == matches
    assert (b'href="/report/1/"' in response.content) == matches


@pytest.fixture
def report_detail_url(report_obj):
    return urls.reverse("report_detail", kwargs={"pk": report_obj.id})


def test_detail(admin_client, report_obj, report_detail_url):
    response = admin_client.get(report_detail_url)
    assert response.status_code == HTTPStatus.OK
    assert b">testreport<" in response.content
    assert b">Debug log<" in response.content


class TestReportReply:
    @pytest.fixture
    def report_reply_url(self, report_obj):
        return urls.reverse("report_reply", kwargs={"pk": report_obj.id})

    @pytest.mark.parametrize(
        "typ, klass, fragment",
        [("Reply", OutgoingMessage, "#reply-1"), ("Note", NoteMessage, "#note-1")],
    )
    def test_reply(
        self,
        admin_client,
        report_obj,
        report_reply_url,
        report_detail_url,
        typ,
        klass,
        fragment,
    ):
        text = "test text"

        assert not report_obj.all_messages()
        response = admin_client.post(report_reply_url, {"typ": typ, "text": text})

        assert response.status_code == HTTPStatus.FOUND
        assert response.url == report_detail_url + fragment

        messages = report_obj.all_messages()
        assert len(messages) == 1
        message = messages[0]
        assert isinstance(message, klass)
        assert message.text == text

    def test_invalid_type(self, admin_client, report_obj, report_reply_url):
        response = admin_client.post(
            report_reply_url, {"typ": "blabla", "text": "test text"}
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert not report_obj.all_messages()

    def test_get(self, admin_client, report_reply_url):
        response = admin_client.get(report_reply_url)
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED


@pytest.mark.parametrize(
    "query, matches",
    [(None, True), ("test", True), ("Test", True), ("", True), ("blah", False)],
)
@pytest.mark.parametrize(
    "view, match", [("bin_list", ">testbin<"), ("label_list", ">testlabel<")]
)
def test_lists(admin_client, bin_obj, label_obj, view, query, match, matches):
    url = urls.reverse(view)
    if query is not None:
        url += f"?q={query}"

    response = admin_client.get(url)
    assert response.status_code == HTTPStatus.OK
    content = response.content.decode("utf-8")
    assert (match in content) == matches


class TestSearchDispatch:
    @pytest.fixture
    def search_dispatch_url(self):
        return urls.reverse("search_dispatch")

    @pytest.mark.parametrize("scope", ["Reports", "Bins", "Labels"])
    def test_search_dispatch(
        self, search_dispatch_url, admin_client, bin_obj, report_obj, scope
    ):
        response = admin_client.get(
            search_dispatch_url, {"q": "foo&bar", "scope": scope}
        )

        assert response.status_code == HTTPStatus.FOUND

        response2 = admin_client.get(response.url)
        content = response2.content.decode()

        assert f"No {scope.lower()} found" in content
        assert f'{scope} matching "foo&amp;bar"' in content

    def test_invalid_scope(
        self, search_dispatch_url, admin_client, bin_obj, report_obj
    ):
        response = admin_client.get(
            search_dispatch_url, {"q": "foo", "scope": "blabla"}
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.fixture
def bin_detail_url(bin_obj):
    return urls.reverse("bin_detail", kwargs={"pk": bin_obj.id})


@pytest.fixture
def inbox_bin():
    return Bin.get_inbox()


def test_bin_detail(admin_client, bin_detail_url):
    response = admin_client.get(bin_detail_url)
    assert response.status_code == HTTPStatus.OK
    assert b">testbin<" in response.content


class TestBinNewEdit:
    @pytest.fixture
    def bin_new_url(self):
        return urls.reverse("bin_new_edit")

    @pytest.fixture
    def bin_edit_url(self, bin_obj):
        return urls.reverse("bin_new_edit", kwargs={"pk": bin_obj.id})

    def test_new_post(self, admin_client, bin_new_url):
        response = admin_client.post(bin_new_url, {"name": "newbin"})
        assert response.status_code == HTTPStatus.FOUND

        new_bin_obj = Bin.objects.get(name="newbin")
        assert new_bin_obj.name == "newbin"
        assert not new_bin_obj.description

        assert response.url == urls.reverse("bin_detail", kwargs={"pk": new_bin_obj.id})

    def test_edit_post(self, admin_client, bin_obj, bin_edit_url, bin_detail_url):
        data = {"name": bin_obj.name, "description": "Bin description"}
        response = admin_client.post(bin_edit_url, data)

        assert response.status_code == HTTPStatus.FOUND
        assert response.url == bin_detail_url

        bin_obj.refresh_from_db()
        assert bin_obj.description == "Bin description"

    def test_new_get(self, admin_client, bin_new_url):
        response = admin_client.get(bin_new_url)

        assert response.status_code == HTTPStatus.OK
        content = response.content.decode("utf-8")
        assert '<form method="POST"' in content
        assert "csrfmiddlewaretoken" in content
        assert "New bin" in content
        assert "Delete bin" not in content

    def test_edit_get(self, admin_client, bin_edit_url, bin_obj):
        response = admin_client.get(bin_edit_url)

        assert response.status_code == HTTPStatus.OK
        content = response.content.decode("utf-8")
        assert '<form method="POST"' in content
        assert "csrfmiddlewaretoken" in content
        assert "Edit bin" in content
        assert "Delete bin" in content
        assert bin_obj.name in content
        assert bin_obj.description in content

    def test_edit_inbox(self, admin_client, inbox_bin):
        url = urls.reverse("bin_new_edit", kwargs={"pk": inbox_bin.id})
        response = admin_client.get(url)

        assert response.status_code == HTTPStatus.OK
        content = response.content.decode("utf-8")
        assert "Delete bin" not in content
        assert f'value="{inbox_bin.name}"' not in content

    def test_edit_inbox_post(self, admin_client, inbox_bin):
        data = {"name": "New name", "description": "Bin description"}
        url = urls.reverse("bin_new_edit", kwargs={"pk": inbox_bin.id})
        response = admin_client.post(url, data)

        assert response.status_code == HTTPStatus.FOUND

        inbox_bin.refresh_from_db()
        assert inbox_bin.name == "Inbox"

    @pytest.mark.parametrize(
        "back_url, is_valid",
        {("/", True), ("/reports", True), ("https://evil.example.com/", False)},
    )
    def test_back_url(
        self, admin_client, bin_obj, bin_edit_url, bin_detail_url, back_url, is_valid
    ):
        bin_edit_url += f"?back={back_url}"
        data = {"name": bin_obj.name, "description": bin_obj.description}
        response = admin_client.post(bin_edit_url, data)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == (back_url if is_valid else bin_detail_url)


class TestLabelNewEdit:
    @pytest.fixture
    def label_new_url(self):
        return urls.reverse("label_new_edit")

    @pytest.fixture
    def label_edit_url(self, label_obj):
        return urls.reverse("label_new_edit", kwargs={"pk": label_obj.id})

    @pytest.fixture
    def label_list_url(self):
        return urls.reverse("label_list")

    def test_new_post(self, admin_client, label_new_url):
        response = admin_client.post(
            label_new_url, {"name": "newlabel", "color": "#424242"}
        )
        assert response.status_code == HTTPStatus.FOUND

        new_label_obj = Label.objects.get(name="newlabel")
        assert new_label_obj.name == "newlabel"
        assert new_label_obj.color == "#424242"
        assert not new_label_obj.description

        assert response.url == urls.reverse("label_list")

    def test_edit_post(self, admin_client, label_obj, label_edit_url, label_list_url):
        data = {
            "name": label_obj.name,
            "description": "Label description",
            "color": "#424242",
        }
        response = admin_client.post(label_edit_url, data)

        assert response.status_code == HTTPStatus.FOUND
        assert response.url == label_list_url

        label_obj.refresh_from_db()
        assert label_obj.description == "Label description"
        assert label_obj.color == "#424242"

    def test_new_get(self, admin_client, label_new_url):
        response = admin_client.get(label_new_url)

        assert response.status_code == HTTPStatus.OK
        content = response.content.decode("utf-8")
        assert '<form method="POST"' in content
        assert "csrfmiddlewaretoken" in content
        assert "New label" in content
        assert "Delete label" not in content

    def test_edit_get(self, admin_client, label_edit_url, label_obj):
        response = admin_client.get(label_edit_url)

        assert response.status_code == HTTPStatus.OK
        content = response.content.decode("utf-8")
        assert '<form method="POST"' in content
        assert "csrfmiddlewaretoken" in content
        assert "Edit label" in content
        assert "Delete label" in content
        assert label_obj.name in content
        assert label_obj.description in content

    @pytest.mark.parametrize(
        "back_url, is_valid",
        {("/", True), ("/reports", True), ("https://evil.example.com/", False)},
    )
    def test_back_url(
        self,
        admin_client,
        label_obj,
        label_edit_url,
        label_list_url,
        back_url,
        is_valid,
    ):
        label_edit_url += f"?back={back_url}"
        data = {
            "name": label_obj.name,
            "description": label_obj.description,
            "color": label_obj.color,
        }
        response = admin_client.post(label_edit_url, data)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == (back_url if is_valid else label_list_url)


def test_subscribe(bin_obj, admin_user, admin_client):
    url = urls.reverse("bin_subscribe", kwargs={"pk": bin_obj.id})
    assert admin_user not in bin_obj.subscribers.all()

    response = admin_client.post(url)
    assert response.status_code == HTTPStatus.OK
    assert admin_user in bin_obj.subscribers.all()

    response = admin_client.post(url)
    assert response.status_code == HTTPStatus.OK
    assert admin_user not in bin_obj.subscribers.all()


class TestSettings:
    def _get_url(self, obj, setting):
        view = "bin_settings" if isinstance(obj, Bin) else "report_settings"
        return urls.reverse(view, kwargs={"setting": setting, "pk": obj.id})

    # Getting settings

    def test_get_bin_maintainer(self, bin_obj, admin_client):
        url = self._get_url(bin_obj, "maintainer")
        response = admin_client.get(url)
        content = response.content.decode("utf-8")
        assert ">Maintainers for testbin<" in content
        assert 'type="checkbox"' in content
        assert ">admin<" in content

    def test_get_bin_label(self, bin_obj, label_obj, admin_client):
        url = self._get_url(bin_obj, "label")
        response = admin_client.get(url)
        content = response.content.decode("utf-8")
        assert ">Labels for testbin<" in content
        assert 'type="checkbox"' in content
        assert ">testlabel<" in content

    def test_get_report_label(self, report_obj, label_obj, admin_client):
        url = self._get_url(report_obj, "label")
        response = admin_client.get(url)
        content = response.content.decode("utf-8")
        assert ">Labels for testreport<" in content
        assert 'type="checkbox"' in content
        assert ">testlabel<" in content

    def test_get_bin_related(self, bin_obj, admin_client):
        url = self._get_url(bin_obj, "related")
        response = admin_client.get(url)
        content = response.content.decode("utf-8")
        assert ">Related to testbin<" in content
        assert 'type="checkbox"' in content
        assert ">testbin<" not in content  # Bin can't relate to itself

    def test_get_report_bin(self, report_obj, bin_obj, admin_client):
        url = self._get_url(report_obj, "bin")
        response = admin_client.get(url)
        content = response.content.decode("utf-8")
        assert ">Bin for testreport<" in content
        assert 'type="radio"' in content
        assert ">testbin<" in content

    def test_get_invalid(self, report_obj, admin_client):
        url = self._get_url(report_obj, "blabla")
        response = admin_client.get(url)
        assert response.status_code == HTTPStatus.BAD_REQUEST

    # Setting settings

    def test_set_bin_maintainer(
        self, bin_obj, bin_detail_url, admin_client, admin_user
    ):
        assert not bin_obj.maintainers.exists()

        url = self._get_url(bin_obj, "maintainer")
        response = admin_client.post(url, {"maintainer": admin_user.id})

        assert response.status_code == HTTPStatus.FOUND
        assert response.url == bin_detail_url
        assert bin_obj.maintainers.get() == admin_user

    def test_set_bin_label(self, bin_obj, label_obj, bin_detail_url, admin_client):
        assert not bin_obj.labels.exists()

        url = self._get_url(bin_obj, "label")
        response = admin_client.post(url, {"label": label_obj.id})

        assert response.status_code == HTTPStatus.FOUND
        assert response.url == bin_detail_url
        assert bin_obj.labels.get() == label_obj

    def test_set_report_label(
        self, report_detail_url, report_obj, label_obj, admin_client
    ):
        assert not report_obj.labels.exists()

        url = self._get_url(report_obj, "label")
        response = admin_client.post(url, {"label": label_obj.id})

        assert response.status_code == HTTPStatus.FOUND
        assert response.url == report_detail_url
        assert report_obj.labels.get() == label_obj

    def test_set_bin_related(self, bin_obj, bin_detail_url, admin_client):
        assert not bin_obj.related_bins.exists()
        new_bin = Bin.objects.create(name="related bin")

        url = self._get_url(bin_obj, "related")
        response = admin_client.post(url, {"related": new_bin.id})

        assert response.status_code == HTTPStatus.FOUND
        assert response.url == bin_detail_url
        assert bin_obj.related_bins.get() == new_bin
        assert new_bin.related_bins.get() == bin_obj

    def test_set_report_bin(
        self, report_detail_url, report_obj, bin_obj, inbox_bin, admin_client
    ):
        assert report_obj.bin == bin_obj

        url = self._get_url(report_obj, "bin")
        response = admin_client.post(url, {"bin": inbox_bin.id})

        assert response.url == report_detail_url
        assert response.status_code == HTTPStatus.FOUND
        report_obj.refresh_from_db()
        assert report_obj.bin == inbox_bin

    def test_set_invalid(self, report_obj, admin_client):
        url = self._get_url(report_obj, "blabla")
        response = admin_client.post(url)
        assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.parametrize(
    "view, kwargs",
    [
        ("home", {}),
        ("search_dispatch", {}),
        ("report_list", {}),
        ("report_detail", {"pk": 1}),
        ("report_reply", {"pk": 1}),
        ("report_settings", {"pk": 1, "setting": "label"}),
        ("bin_list", {}),
        ("bin_new_edit", {}),
        ("bin_detail", {"pk": 1}),
        ("bin_subscribe", {"pk": 1}),
        ("bin_settings", {"pk": 1, "setting": "label"}),
        ("label_list", {}),
        ("label_new_edit", {}),
    ],
)
def test_logged_out(client, view, kwargs):
    view_url = urls.reverse(view, kwargs=kwargs)
    response = client.get(view_url)
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == urls.reverse("login") + "?next=" + view_url


@pytest.mark.parametrize(
    "view, method",
    [
        ("report_detail", "get"),
        ("bin_detail", "get"),
        ("bin_new_edit", "get"),
        ("bin_new_edit", "post"),
        ("bin_subscribe", "post"),
        ("label_new_edit", "get"),
        ("label_new_edit", "post"),
        ("report_reply", "post"),
    ],
)
def test_404(admin_client, view, method):
    url = urls.reverse(view, kwargs={"pk": 1337})
    func = getattr(admin_client, method)
    response = func(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
