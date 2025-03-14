from django.conf import settings
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.urls import path, register_converter, include
from django.urls.converters import UUIDConverter
from django.views.generic import RedirectView, TemplateView
from rest_framework.urlpatterns import format_suffix_patterns

from .models import Casebook, Section, ContentNode, ContentAnnotation, LegalDocument, SavedImage
from .test.test_permissions_helpers import no_perms_test
from .url_converters import IdSlugConverter, OrdinalSlugConverter, register_model_converter
from .utils import fix_after_rails
from . import views, forms


register_converter(IdSlugConverter, "idslug")
register_converter(OrdinalSlugConverter, "ordslug")
register_model_converter(Casebook)
register_model_converter(Section)
register_model_converter(ContentNode, "resource")
register_model_converter(ContentAnnotation, "annotation")
register_model_converter(LegalDocument)
register_model_converter(SavedImage, name="image_uuid", base=UUIDConverter, field="external_id")

# these patterns will have optional format suffixes added, like '.json'
drf_urlpatterns = [
    # annotations
    path(
        "resources/<resource:resource>/annotations/<annotation:annotation>",
        views.AnnotationDetailView.as_view(),
        name="annotation_detail",
    ),
    path(
        "resources/<resource:resource>/annotations",
        views.AnnotationListView.as_view(),
        name="annotation_list",
    ),
    path(
        "casebook/<idslug:casebook_param>/toc/<idslug:section_id>",
        views.SectionTOCView.as_view(),
        name="toc_list",
    ),
    path(
        "casebook/<idslug:casebook_param>/toc",
        views.CasebookTOCView.as_view(),
        name="casebook_toc_list",
    ),
    path(
        "casebook/<idslug:casebook_param>/info",
        views.CasebookInfoView.as_view(),
        name="casebook_info",
    ),
    path("api/titles/", no_perms_test(views.CommonTitleView.as_view()), name="new_title"),
    path(
        "api/titles/<int:title_id>",
        no_perms_test(views.CommonTitleView.as_view()),
        name="edit_title",
    ),
    path(
        "api/casebooks/<idslug:casebook_param>/export-pdf",
        views.PDFExportView.as_view(),
        name="export_as_pdf",
    ),
    path(
        "casebooks/<idslug:casebook_param>/resources/from_source/",
        views.LegalDocumentResourceView.as_view(),
        name="legal_document_resource_view",
    ),
]

urlpatterns = format_suffix_patterns(drf_urlpatterns) + [
    path("", views.index, name="index"),
    path("casebooks/archived/", views.archived_casebooks, name="archived_casebooks"),
    # users
    path("users/<int:user_id>/", views.dashboard, name="dashboard"),
    path("accounts/new/", views.sign_up, name="sign_up"),
    path("accounts/edit/", views.edit_user, name="edit_user"),
    # built-in Django auth views for login/logout/password update/password reset, with overrides to replace the form or tweak behavior in some views
    path("accounts/password_reset/", no_perms_test(views.reset_password), name="password_reset"),
    path(
        "accounts/reset/<uidb64>/<token>/",
        no_perms_test(
            auth_views.PasswordResetConfirmView.as_view(form_class=forms.SetPasswordForm)
        ),
        name="password_reset_confirm",
    ),
    path("accounts/", include("django.contrib.auth.urls")),
    # author urls
    path("author/<slug:user_slug>/", no_perms_test(views.dashboard), name="pretty_dashboard"),
    path(
        "author/<slug:user_slug>/<slug:title_slug>/",
        no_perms_test(views.pretty_url_dispatch),
        name="pretty_casebook",
    ),
    path(
        "author/<slug:user_slug>/<slug:title_slug>/<ordslug:content_param>",
        no_perms_test(views.pretty_url_dispatch),
        name="pretty_section",
    ),
    # search
    path("search/sources/", views.search_sources, name="search_sources"),
    path("search/<int:source>/", views.search_using, name="search_using"),
    path("search/", views.internal_search, name="internal_search"),
    # legal_docs
    path("documents/fetch/<int:source>/", views.import_from_source, name="from_source"),
    path("documents/<int:legal_doc_id>/", views.display_legal_doc, name="display_legal_doc"),
    path("documents/update/<resource:node>/", views.update_legal_doc, name="update_legal_doc"),
    # resources
    path(
        "casebooks/<idslug:casebook_param>/resources/<ordslug:resource_param>/layout/",
        RedirectView.as_view(pattern_name="resource", permanent=True),
    ),
    path(
        "casebooks/<idslug:casebook_param>/resources/<ordslug:resource_param>/edit/",
        views.edit_resource,
        name="edit_resource",
    ),
    path(
        "casebooks/<idslug:casebook_param>/resources/<ordslug:resource_param>/annotate/",
        views.annotate_resource,
        name="annotate_resource",
    ),
    path(
        "casebooks/<idslug:casebook_param>/resources/<ordslug:resource_param>/",
        views.ResourceView.as_view(),
        name="resource",
    ),
    path(
        "casebooks/<idslug:casebook_param>/resources/<ordslug:resource_param>",
        no_perms_test(views.ResourceView.as_view()),
    ),
    # sections
    path(
        "casebooks/<idslug:casebook_param>/sections/<ordslug:section_param>/layout/",
        views.edit_section,
        name="edit_section",
    ),
    path(
        "casebooks/<idslug:casebook_param>/sections/<ordslug:section_param>/edit/",
        RedirectView.as_view(pattern_name="edit_section", permanent=True),
    ),
    path(
        "casebooks/<idslug:casebook_param>/sections/<ordslug:section_param>/",
        views.SectionView.as_view(),
        name="section",
    ),
    path(
        "casebooks/<idslug:casebook_param>/sections/<ordslug:section_param>",
        no_perms_test(views.SectionView.as_view()),
    ),
    # sections and resources
    path("casebooks/<idslug:casebook_param>/new/section", views.new_section, name="new_section"),
    path("casebooks/<idslug:casebook_param>/new/text", views.new_text, name="new_text"),
    path("casebooks/<idslug:casebook_param>/new/link", views.new_link, name="new_link"),
    path(
        "casebooks/<idslug:casebook_param>/new/legaldoc", views.new_legal_doc, name="new_legal_doc"
    ),
    path(
        "casebooks/<idslug:casebook_param>/new/bulk",
        views.new_from_outline,
        name="new_from_outline",
    ),
    # reordering nodes
    path(
        "casebooks/<idslug:casebook_param>/sections/<ordslug:section_param>/reorder/<ordslug:node_param>",
        views.reorder_node,
        name="reorder_node",
    ),
    path(
        "casebooks/<idslug:casebook_param>/reorder/<ordslug:node_param>",
        views.reorder_node,
        name="reorder_node",
    ),
    # casebooks
    path("casebooks/<idslug:casebook_param>/layout/", views.edit_casebook, name="edit_casebook"),
    path(
        "casebooks/<idslug:casebook_param>/edit/",
        RedirectView.as_view(pattern_name="edit_casebook", permanent=True),
    ),
    path("casebooks/<idslug:casebook_param>/clone/", views.clone_casebook, name="clone"),
    path("casebooks/<idslug:casebook_param>/publish/", views.publish_casebook, name="publish"),
    path(
        "casebooks/<idslug:from_casebook_dict>/sections/<ordslug:from_section_dict>/clone/to/<idslug:to_casebook_dict>/",
        views.clone_casebook_nodes,
        name="clone_nodes",
    ),
    path(
        "casebooks/<idslug:casebook_param>/create_draft/", views.create_draft, name="create_draft"
    ),
    path("casebooks/<idslug:casebook_param>/credits/", views.show_credits, name="show_credits"),
    path(
        "casebooks/<idslug:casebook_param>/settings/",
        views.casebook_settings,
        name="casebook_settings",
    ),
    path(
        "casebooks/<idslug:casebook_param>/history/",
        views.casebook_history,
        name="casebook_history",
    ),
    path(
        "casebooks/<idslug:casebook_param>/outline/",
        views.casebook_outline,
        name="casebook_outline",
    ),
    path(
        "casebooks/<idslug:casebook_param>/follow/", views.follow_casebook, name="follow_casebook"
    ),
    path(
        "casebooks/<idslug:casebook_param>/search/", views.casebook_search, name="casebook_search"
    ),
    # TODO: we temporarily need to list with and without trailing slash, to handle POSTs without slashes
    path("casebooks/<idslug:casebook_param>/", views.CasebookView.as_view(), name="casebook"),
    path("casebooks/<idslug:casebook_param>", no_perms_test(views.CasebookView.as_view())),
    path("casebooks/new", views.new_casebook, name="new_casebook"),
    # export
    path("casebooks/<casebook:node>/export.<file_type>", views.export, name="export_casebook"),
    path("sections/<section:node>/export.<file_type>", views.export, name="export_section"),
    path("resources/<resource:node>/export.<file_type>", views.export, name="export_resource"),
    # Reading mode
    path(
        "casebooks/<idslug:casebook_param>/as-printable-html/",
        views.as_printable_html,
        name="as_printable_html",
    ),
    path(
        "casebooks/<idslug:casebook_param>/as-printable-html/<int:page>/",
        views.as_printable_html,
        name="as_printable_html",
    ),
    path(
        "casebooks/<idslug:casebook_param>/as-printable-html/all/",
        views.as_printable_html,
        {"whole_book": True},
        name="printable_all",
    ),
    path(
        "casebooks/<idslug:casebook_param>/as-printable-html/pdf/",
        views.as_printable_html,
        {"whole_book": True, "as_pdf": True},
        name="printable_pdf",
    ),
    # images
    path("image/", no_perms_test(views.upload_image), name="upload_image"),
    path("image/<image_uuid>", no_perms_test(views.view_image), name="image_url"),
    # canonical paths for static pages
    path(
        "featured/",
        TemplateView.as_view(template_name="pages/featured_casebooks.html"),
        name="featured",
    ),
    path("pages/about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
    path(
        "pages/privacy-policy/",
        TemplateView.as_view(template_name="pages/privacy-policy.html"),
        name="privacy-policy",
    ),
    path(
        "pages/terms-of-service/",
        TemplateView.as_view(template_name="pages/terms-of-service.html"),
        name="terms-of-service",
    ),
    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="robots.txt",
            content_type="text/plain",
            extra_context={
                "excluded_casebooks": lambda: Casebook.objects.filter(listed_publicly=False),
            },
        ),
        name="robots_txt",
    ),
    # redirects
    path(
        "subscribe",
        no_perms_test(
            lambda request: redirect(
                "https://opencasebook.us1.list-manage.com/subscribe?u=894c9c0d9d7d7c5f8de8d76aa&id=89f2a23e12",
                permanent=True,
            )
        ),
    ),
    path(
        "pages/faq/",
        no_perms_test(lambda request: redirect(settings.FAQ_URL, permanent=True)),
        name="faq",
    ),
    path("django-admin/reporting/", include("reporting.urls")),
]
fix_after_rails("some routes don't have end slashes for rails compatibility")

# debugging routes to see error pages
# for example, http://localhost:8000/404 triggers an actual 404
# and http://localhost:8000/404.html shows the 404 template
if settings.DEBUG or settings.TESTING:
    from .test import views as test_views

    urlpatterns += [
        path(error_page, TemplateView.as_view(template_name=error_page), name=error_page)
        for error_page in ("400.html", "403.html", "403_csrf.html", "404.html", "500.html")
    ]
    urlpatterns += [
        path(error_page, no_perms_test(getattr(test_views, f"raise_{error_page}")), name=error_page)
        for error_page in ("400", "403", "403_csrf", "404", "500")
    ]
