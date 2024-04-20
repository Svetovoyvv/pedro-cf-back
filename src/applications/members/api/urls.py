from rest_framework.routers import SimpleRouter

from applications.members.api import views

router = SimpleRouter()

router.register(r'user', views.UserViewSet)
router.register(r'tag', views.TagViewSet)
router.register(r'position', views.WorkPositionViewSet)

urlpatterns = router.urls