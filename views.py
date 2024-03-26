from django.shortcuts import render, HttpResponseRedirect
from django import forms
from django.urls import reverse
from django.utils import timezone


class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")


def index(request):
    if "tasks" not in request.session:
        request.session["tasks"] = []
    if "timeStamp" not in request.session:
        request.session["timeStamp"] = []

    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            current_datetime = timezone.now()
            formatted_datetime = timezone.localtime(
                # 12-hour format with AM/PM
                current_datetime).strftime("%I:%M %p")
            task = form.cleaned_data["task"]

            request.session["tasks"] += [task]
            request.session.setdefault(
                "timeStamp", []).append(formatted_datetime)

            return HttpResponseRedirect(reverse("tasks:index"))

    form = NewTaskForm()
    tasks = request.session.get("tasks", [])
    timestamps = request.session.get("timeStamp", [])
    task_data = zip(tasks, timestamps)

    # Clear session on new opening
    if not request.session.get("_session_started", False):
        request.session.flush()
        request.session["_session_started"] = True

    return render(request, "tasks/index.html", {
        "form": form,
        "task_data": task_data
    })
