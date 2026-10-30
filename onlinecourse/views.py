from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Submission, Learner, Enrollment


def index(request):
    course = Course.objects.first()

    return render(
        request,
        "onlinecourse/course_details_bootstrap.html",
        {"course": course}
    )


def course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    return render(
        request,
        "onlinecourse/course_details_bootstrap.html",
        {"course": course}
    )


def exam(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    return render(
        request,
        "onlinecourse/exam.html",
        {
            "course": course,
            "questions": course.questions.all(),
        }
    )


def submit(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    learner, created = Learner.objects.get_or_create(
        user=request.user
    )

    enrollment, created = Enrollment.objects.get_or_create(
        learner=learner,
        course=course
    )

    submission = Submission.objects.create(
        enrollment=enrollment
    )

    total_score = 0
    selected_choices = []

    for question in course.questions.all():
        selected_ids = request.POST.getlist(
            f"question_{question.id}"
        )

        if question.is_get_score(selected_ids):
            total_score += question.grade

        for choice_id in selected_ids:
            choice = question.choices.filter(
                id=choice_id
            ).first()

            if choice:
                selected_choices.append(choice)

    submission.choices.set(selected_choices)
    submission.total_score = total_score
    submission.save()

    return redirect(
        "show_exam_result",
        course_id=course.id,
        submission_id=submission.id
    )


def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, id=course_id)

    submission = get_object_or_404(
        Submission,
        id=submission_id,
        enrollment__course=course
    )

    max_score = sum(
        question.grade
        for question in course.questions.all()
    )

    return render(
        request,
        "onlinecourse/exam_result.html",
        {
            "course": course,
            "submission": submission,
            "max_score": max_score,
            "total_score": submission.total_score,
        }
    )
