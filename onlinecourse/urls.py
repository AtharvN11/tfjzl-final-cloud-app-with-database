from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path(
        "course/<int:course_id>/",
        views.course_details,
        name="course_details"
    ),

    path(
        "course/<int:course_id>/exam/",
        views.exam,
        name="exam"
    ),

   path(
    "course/<int:course_id>/submission/<int:submission_id>/result/",
    views.show_exam_result,
    name="show_exam_result"
),

    path(
        "exam/result/<int:submission_id>/",
        views.show_exam_result,
        name="show_exam_result"
    ),
]
