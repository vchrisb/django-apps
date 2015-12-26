from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from django.contrib.auth.models import User
from candidate.models import Candidate
from rest_framework import routers, serializers, viewsets

import newsletter.views
import candidate.views
import mytwitter.views

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Serializers define the API representation.
class CandidateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Candidate
        fields = ('first_name', 'last_name', 'photo', 'secure_photo')

# ViewSets define the view behavior.
class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'candidates', CandidateViewSet)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    # Examples:
    url(r'^api/', include(router.urls)),
    url(r'^$', newsletter.views.home, name='home'),
    url(r'^contact/$', newsletter.views.contact, name='contact'),
    #url(r'^logout/$', newsletter.views.logout_view, name='logout'),
    #url(r'^login/$', newsletter.views.login_view, name='login'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^candidate/$', candidate.views.create, name='candidate-create'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # Url Entries for allauth
    url(r'^accounts/', include('allauth.urls')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    # Url Entries for social auth
    #url('', include('social.apps.django_app.urls', namespace='social')),
    # Url Entries for django administration
    #url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^primes$', newsletter.views.primes, name='primes'),
    url(r'^tweet/$', mytwitter.views.tweet, name='tweet'),
]

# just for testing!
if settings.DEBUG:
#     urlpatterns += static (settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
