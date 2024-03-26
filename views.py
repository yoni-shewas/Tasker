from asyncio import taskgroups
from django.shortcuts import render, HttpResponseRedirect
from django import forms
from django.urls import reverse, include
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
            timezone.activate('Africa/Nairobi')
            current_datetime = timezone.now()
            formatted_datetime = timezone.localtime(
                current_datetime).strftime("%Y/%m/%d - %I:%M %p")

            print(formatted_datetime)

            task = form.cleaned_data["task"]

            request.session["tasks"] += [task]
            request.session.setdefault(
                "timeStamp", []).append(formatted_datetime)

            return HttpResponseRedirect(reverse("tasks:index"))

    form = NewTaskForm()
    taskgroups = request.session.get("tasks", [])
    timestamps = request.session.get("timeStamp", [])
    task_data = list(zip(range(len(tasks)), tasks, timestamps))

    if not request.session.get("_session_started", False):
        request.session.flush()
        request.session["_session_started"] = True

    return render(request, "tasks/index.html", {
        "form": form,
        "task_data": task_data
    })


def delete_task(request, task_index):
    if "tasks" in request.session:
        tasks = request.session.get("tasks", [])
        if 0 <= task_index < len(tasks):
            del tasks[task_index]
            request.session["tasks"] = tasks

    return HttpResponseRedirect(reverse("tasks:index"))
