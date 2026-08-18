from django.shortcuts import render, redirect, get_object_or_404
from .models import Note
from .forms import NoteForm


def note_list(request):
    notes = Note.objects.all()
    return render(request, "notes/note_list.html", {"notes": notes})


def note_create(request):
    if request.method == "POST":
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("note_list")
    else:
        form = NoteForm()
    return render(request, "notes/note_form.html", {"form": form})


def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == "POST":
        note.delete()
    return redirect("note_list")

def note_create(request):

    note = Note(user=request.user, title=title, content=content)
    note.save()
