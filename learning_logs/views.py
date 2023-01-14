from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.

def index(request):
    # The home page for learning log
    return render(request, "learning_logs/index.html")

def check_topic_owner(topic, request):
    if topic.owner != request.user:
        raise Http404

@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics':topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(topic, request)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):

    # add new topic
    if request.method != 'POST':
        # create a blank form
        form = TopicForm()
    else:
        # POST form submitted, process data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
        return redirect('learning_logs:topics')

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(topic, request)
    
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
        return redirect('learning_logs:topic', topic_id=topic_id)

    context = {'topic': topic, 'form': form }
    return render(request, 'learning_logs/new_entry.html/', context)

@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(topic, request)

    if request.method != 'POST':
        #pre-fill the field with current entry
        form=EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
        return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry':entry, 'topic':topic, 'form':form}
    return render(request, 'learning_logs/edit_entry.html', context)

@login_required
def delete_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(topic, request)

    if request.method == 'POST':
        topic.delete()
        return redirect('learning_logs:topics')

    context = {'topic':topic}
    return render(request, 'learning_logs/delete_topic.html', context)

@login_required
def delete_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(topic, request)

    if request.method == 'POST':
        entry.delete()
        return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'topic': topic, 'entry': entry}
    return render(request, 'learning_logs/delete_entry.html', context)