from rest_framework.routers import SimpleRouter

from applications.matches.api import views

router = SimpleRouter()


router.register(r'match', views.MatchViewSet)
router.register('meeting', views.MeetingViewSet)


urlpatterns = router.urls