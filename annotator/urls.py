"Expected api docs at http://docs.annotatorjs.org/en/v1.2.x/storage.html"

from django.conf.urls import url

from . import views

urlpatterns = [
	# storage API
    url(r'^$', views.Root.as_view(), name='annotator.root'),
    url(r'^annotations$', views.AnnotationList.as_view(), name='annotator.index'),
    url(r'^annotations/(?P<pk>[\w\-]+)$', views.AnnotationDetail.as_view(), name='annotator.annotation'),
    url(r'^search$', views.SearchView.as_view(), name='annotation.search'),

    url(r'^token$', views.TokenView.as_view(), name='annotator.token'),

    # # public pages
    # url(r'^document/(?P<doc_id>[\w\-]+)/edit$', views.EditorView.as_view(), name='annotation.editor'),
]
