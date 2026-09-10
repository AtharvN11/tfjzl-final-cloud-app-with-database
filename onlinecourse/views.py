from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Submission


def index(request):
    course = Course.objects.first()

    if course is None:
        return render(
            request,
            "onlinecourse/course_details_bootstrap.html",
            {"course": None}
        )

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
    questions = course.questions.all()

    return render(
        request,
        "onlinecourse/exam.html",
        {
            "course": course,
            "questions": questions,
        }
    )


def submit(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    total_score = 0
    selected_choices = []

    for question in course.questions.all():
        selected_choice_id = request.POST.get(
            f"question_{question.id}"
        )

        if selected_choice_id:
            try:
                choice = question.choices.get(
                    id=selected_choice_id
                )

                selected_choices.append(choice)

                if choice.is_correct:
                    total_score += question.grade

            except question.choices.model.DoesNotExist:
                pass

    from .models import Learner

    learner, created = Learner.objects.get_or_create(
        user=request.user,
        defaults={
            "occupation": "",
            "social_link": "",
        }
    )

    submission = Submission.objects.create(
        learner=learner,
        exam=course,
        total_score=total_score,
    )

    submission.choices.set(selected_choices)

    return redirect(
        "show_exam_result",
        submission_id=submission.id
    )


def show_exam_result(request, submission_id):
    submission = get_object_or_404(
        Submission,
        id=submission_id
    )

    max_score = sum(
        question.grade
        for question in submission.exam.questions.all()
    )

    return render(
        request,
        "onlinecourse/exam_result.html",
        {
            "submission": submission,
            "max_score": max_score,
        }
    )