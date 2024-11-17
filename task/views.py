from django.shortcuts import render, redirect
from .models import task
from .forms import taskForm

tasks=[
    {id:1,'name':'do homework'},
    {id:2,'name':'do dishes'},
]
# Create your views here.
def taskManager(request):
    tasks=task.objects.all()
    form=taskForm()
    if request.method=='POST':
        form=taskForm(request.POST)
        if form.is_valid():
            form.save()
    context={'tasks':tasks, 'form': form}
    return render(request,'task/task.html',context)

def completed(request, pk):
    tasks=task.objects.get(id=pk)
    tasks.completed = not tasks.completed  # Toggle the completed status
    tasks.save()
    return redirect('tasks')

def delete(request, pk):
    tasks=task.objects.get(id=pk)
    tasks.delete()
    return redirect('tasks')