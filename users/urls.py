from django.urls import path
from .views import (
    register_view,
    login_view,
    # logout_view,
    # supervisor_view,
    # reviewer_view
)

urlpatterns = [
    path("register", register_view, name="register"),
    path("login", login_view, name="login"),
    # path("logout", logout_view, name="logout"),
    # path("supervisors", supervisor_view, name="supervisors"),
    # path("reviewers", reviewer_view, name="reviewers"),
]
