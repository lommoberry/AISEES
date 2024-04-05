from django.urls import path, include
from . import views
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
	path("", views.home, name='home'),
	path('post_list/', views.post_list, name='post_list'),
	path('add_post/', views.add_post, name='add_post'),
	# path('register/', views.add_researcher, name='register'),
	path('memberlist/', views.memberlist, name='memberlist'),
	path('accounts/', include('django.contrib.auth.urls')), #login and logout django
	path('success/', views.success, name='success'),
	# path('signup/', SignUpView.as_view(), name='signup'),
	path('register/', views.register, name='register'),
	path("admin/", admin.site.urls),
	path('upload/', views.upload_research_item, name='upload_research_item'),
	path('search_results/', views.search_research_items, name='search_results'),
	path('research-item/<int:pk>/', views.research_item_detail, name='research_item_detail'),
	path('activate/<uidb64>/<token>/', views.activate, name='activate'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
