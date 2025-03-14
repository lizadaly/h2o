import json
from test.test_helpers import check_response
from unittest import mock

import pytest
from _pytest.fixtures import FixtureLookupError
from conftest import UserFactory, VerifiedProfessorFactory
from django.template import Variable
from django.urls import reverse

from ..urls import urlpatterns

"""
    This file applies the tests that are attached to each view via the @perms_test decorator.
    A particular test looks like this:

        @perms_test({'method': 'post', 'args': ['casebook'], 'results': {302: ['casebook.testing_editor', 'admin_user'], 403: ['other_user'], 'login': [None]}})
        def some_view(request, casebook): ...

    This means the test should POST to `reverse(some_view, args=[casebook])`, and that casebook.testing_editor and admin_user
    should receive a 302 response; other_user should receive a 403; and non-auth requests should redirect to the login
    form.
"""


def get_permissions_tests():
    """
    This function runs during test collection time. It inspects each route in main.urls, and generates parameters
    for the test_permissions() test below.
    """
    for path in urlpatterns:
        # don't run tests on built-in includes
        if hasattr(path, "urlconf_module") and path.urlconf_module.__name__.startswith("django."):
            continue

        view_func = path.callback

        # don't run tests on anything that's not a pattern (like an include)
        if not hasattr(view_func, "__name__"):
            continue

        # don't run tests on built-in views:
        if view_func.__name__ in ["RedirectView", "TemplateView"]:
            continue

        # retrieve the test config for this view, which will have been attached as view_func.perms_test by the
        # @perms_test decorator
        if not hasattr(view_func, "perms_test") and hasattr(view_func, "view_class"):
            # for class-based views, inspect each request method separately:
            view_class = path.callback.view_class
            to_test = [
                (m.lower(), getattr(getattr(view_class, m.lower()), "perms_test", None))
                for m in view_class()._allowed_methods()
                if m != "OPTIONS"
            ]
        else:
            # just one test config for regular function-based views:
            to_test = [("get", getattr(view_func, "perms_test", None))]

        # yield test_permissions parameters for each test config detected:
        for default_request_method, test_config in to_test:
            if test_config is None:
                yield path, False, None, None, None, None, None
                continue
            for test in test_config:
                request_method = test.get("method", default_request_method)
                url_args = test.get("args", [])
                for status_code, users in test["results"].items():
                    for user_string in users:
                        yield path, True, view_func, url_args, request_method, status_code, user_string


@pytest.mark.parametrize(
    "path, has_tests, view_func, url_args, request_method, status_code, user_string",
    get_permissions_tests(),
)
def test_permissions(
    # regular test fixtures
    client,
    request,
    # parameters from get_permissions_tests()
    path,
    has_tests,
    view_func,
    url_args,
    request_method,
    status_code,
    user_string,
    monkeypatch,
):
    """
    This test function runs a single request on behalf of a single user. The example at the top of this file would
    run this function four separate times.
    """
    # all routes are required to have tests
    if not has_tests:
        raise Exception(
            f"View function or method for path {path} is missing a @perms_test decorator. "
            "Use @no_perms_test if you are sure your view doesn't need tests."
        )

    # Helper method to fetch and return a particular fixture, like 'casebook' or 'casebook.testing_editor'.
    # Values are also stored in the `context` dictionary so they can be reused instead of recreated.
    # The part of `path` before the first period is treated as a pytest fixture, and the remainder is
    # resolved using the Django template language (so lookups like 'casebook.resources.1.some_func'
    # will work).
    def hydrate(context, path):
        if path not in context:
            fixture_name = path.split(".", 1)[0]
            if fixture_name not in context:
                try:
                    context[fixture_name] = request.getfixturevalue(fixture_name)
                except FixtureLookupError:
                    pass  # path may not be a fixture name, like '"some string"'
            context[path] = Variable(path).resolve(context)
        return context[path]

    # Special handling for status code 'login' -- expect a 302, but also check that we redirect to
    # the login page. This lets us differentiate from pages that redirect on success.
    should_redirect_to_login = False
    if status_code == "login":
        status_code = 302
        should_redirect_to_login = True

    # Mock any internals we don't need to test in this scenario
    monkeypatch.setattr("main.models.export_via_aws_lambda", mock.Mock())
    monkeypatch.setattr("main.views.pdf_from_user", mock.Mock())

    # run request
    context = {}
    url = reverse(view_func, args=[hydrate(context, arg) for arg in url_args])
    user = hydrate(context, user_string) if user_string else None
    response = getattr(client, request_method)(url, as_user=user)

    # check response
    check_response(response, status_code=status_code, content_type=None)
    if should_redirect_to_login:
        assert response.url.startswith(reverse("login")), "View failed to redirect to login page"


def test_node_level_viewability(
    full_casebook_parts_with_prof_only_resource, user_factory, verified_professor_factory
):
    """Nodes marked as professor-only should not be considered viewable by non-professors"""
    user = user_factory()
    collaborator = user_factory()
    prof = verified_professor_factory()
    (
        casebook,
        _,
        _,
        private_resource,
        *__,
    ) = full_casebook_parts_with_prof_only_resource
    casebook.add_collaborator(collaborator)

    assert private_resource.viewable_by(prof)
    assert not private_resource.viewable_by(collaborator)
    assert not private_resource.viewable_by(user)


@pytest.mark.parametrize(
    "user_role_factory,part_index,previous_or_next_index,role_specific_ordinals",
    [
        [VerifiedProfessorFactory, 2, 1, [1, 2]],
        [UserFactory, 2, 1, [1, 3]],  # Going 'next' should skip over instructional node r_1_2
        [VerifiedProfessorFactory, 4, 0, [1, 2]],
        [UserFactory, 4, 0, [1, 1]],  # Going 'previous' should skip over instructional node r_1_2
    ],
)
# Given parts: [casebook, s_1, r_1_1, r_1_2 (prof-only), r_1_3, ...]
def test_previous_next_node_visibility(
    user_role_factory,
    part_index,
    previous_or_next_index,
    role_specific_ordinals,
    full_casebook_parts_with_prof_only_resource,
):
    user = user_role_factory()
    public_resource = full_casebook_parts_with_prof_only_resource[
        part_index
    ]  # the base public node

    next_previous = public_resource.get_previous_and_next_nodes(user)

    assert next_previous[previous_or_next_index].ordinals == role_specific_ordinals


@pytest.mark.parametrize(
    "user_role_factory,part_title",
    [
        [VerifiedProfessorFactory, "Instructional material"],
        [UserFactory, "Some Link Name"],
        [lambda: None, "Some Link Name"],  # Not logged in
    ],
)
def test_toc_view(
    full_casebook_parts_with_prof_only_resource, client, user_role_factory, part_title
):
    """The TOC view should respect the user permissions available for specific nodes"""
    casebook = full_casebook_parts_with_prof_only_resource[0]

    user = user_role_factory()
    resp = json.loads(
        client.get(
            reverse("casebook_toc_list", args=[casebook]),
            as_user=user,
            content_type="application/json",
        ).content.decode()
    )
    assert part_title in resp["children"][0]["children"][1]["title"]


def test_export_view(
    full_casebook_parts_with_prof_only_resource, client, user_factory, verified_professor_factory
):
    """The export view should respect the user permissions available for specific nodes"""
    (
        casebook,
        _,
        _,
        private_resource,
        *__,
    ) = full_casebook_parts_with_prof_only_resource
    resp = client.get(
        reverse("export_casebook", kwargs={"node": casebook, "file_type": "html"}),
        as_user=verified_professor_factory(),
    )
    assert private_resource.title in resp.content.decode()

    resp = client.get(
        reverse("export_casebook", kwargs={"node": casebook, "file_type": "html"}),
        as_user=user_factory(),
    )
    assert private_resource.title not in resp.content.decode()


def test_ordinals_never_displayed(full_casebook_parts_with_prof_only_resource):
    """If a node is instructional material, it can never display ordinals"""
    (
        _,
        _,
        public_resource,
        private_resource,
        *__,
    ) = full_casebook_parts_with_prof_only_resource

    assert public_resource.does_display_ordinals
    public_resource.is_instructional_material = True
    public_resource.save()
    public_resource.refresh_from_db()

    assert not public_resource.does_display_ordinals
    assert not private_resource.does_display_ordinals


def test_reorder_ordinals_after_change(full_casebook_parts):
    """When a node is made instructional material, the content tree should reflect its omission from the ordinal list"""

    (
        casebook,
        _,
        _,
        r_1_2,
        r_1_3,
        *__,
    ) = full_casebook_parts
    assert r_1_2.ordinal_string() == "1.2"
    assert r_1_3.ordinal_string() == "1.3"
    assert not r_1_2.is_instructional_material

    r_1_2.is_instructional_material = True
    r_1_2.save()

    casebook.content_tree__repair()
    r_1_2.refresh_from_db()
    r_1_3.refresh_from_db()

    assert r_1_2.ordinal_string() == ""
    assert r_1_3.ordinal_string() == "1.2"
