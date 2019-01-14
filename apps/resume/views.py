from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

from .forms import ResumeItemForm, ResumeForm
from .models import ResumeItem, Resume


def get_model_instance(model, user, instance_id):
    """
    Get an instance of a model in a secure way to avoid users getting instances from other users.
    :param model: Model class.
    :param user: Users ID.
    :param instance_id: The ID for the model instance we are looking for.
    :return: Instance of model
    :raises: Http404
    """
    try:
        instance = model.objects\
            .filter(user=user)\
            .get(id=instance_id)
    except model.DoesNotExist:
        raise Http404

    return instance


@login_required
def resume_view(request, resume_id):
    """
    Handle a request to view a user's resume.
    """
    resume = get_model_instance(Resume, request.user, resume_id)

    return render(request, 'resume/resume.html', {'resume': resume})


@login_required
def resume_item_create_view(request, resume_id):
    """
    Handle a request to create a new resume item.
    """
    if request.method == 'POST':
        form = ResumeItemForm(request.POST)

        if form.is_valid():
            new_resume_item = form.save(commit=False)
            new_resume_item.user = request.user
            new_resume_item.resume_set.add(resume_id)

            new_resume_item.save()

            return redirect(resume_item_edit_view, new_resume_item.id)
    else:
        form = ResumeItemForm()

    return render(request, 'resume/resume_item_create.html', {'form': form, 'resume_id': resume_id})


@login_required
def resume_item_edit_view(request, resume_id, resume_item_id):
    """
    Handle a request to edit a resume item.

    :param resume_item_id: The database ID of the ResumeItem to edit.
    """
    resume_item = get_model_instance(ResumeItem, request.user, resume_item_id)

    template_dict = {'resume_id': resume_id}

    if request.method == 'POST':
        if 'delete' in request.POST:
            resume = get_model_instance(Resume, request.user, resume_id)
            resume_item.resume_set.remove(resume)
            return redirect(resume_view, resume_id)

        form = ResumeItemForm(request.POST, instance=resume_item)
        if form.is_valid():
            form.save()
            form = ResumeItemForm(instance=resume_item)
            template_dict['message'] = 'Resume item updated'
    else:
        form = ResumeItemForm(instance=resume_item)

    template_dict['form'] = form

    return render(request, 'resume/resume_item_edit.html', template_dict)


@login_required
def resumes_view(request):
    """
    Handle a request to view all users resumes.
    """
    resumes = Resume.objects.filter(user=request.user)

    return render(request, 'resume/resumes.html', {
        'resumes': resumes
    })


@login_required
def resume_create_view(request):
    """
    Handle a request to create a new resume.
    """
    if request.method == 'POST':
        form = ResumeForm(request.user, request.POST)
        if form.is_valid():
            new_resume = form.save(commit=False)
            new_resume.user = request.user
            new_resume.save()

            for resume_item_id in request.POST['resume_items']:
                resume_item = get_model_instance(ResumeItem, request.user, resume_item_id)
                new_resume.resume_items.add(resume_item)

            new_resume.save()

            return redirect(resume_edit_view, new_resume.id)
    else:
        form = ResumeForm(request.user)

    return render(request, 'resume/resume_create.html', {'form': form})


@login_required
def resume_edit_view(request, resume_id):
    """
    Handle a request to edit a resume.

    :param resume_id: The database ID of the Resume to edit.
    """
    resume = get_model_instance(Resume, request.user, resume_id)

    template_dict = {}

    if request.method == 'POST':
        if 'delete' in request.POST:
            resume.delete()
            return redirect(resumes_view)

        form = ResumeForm(request.user, request.POST, instance=resume)

        if form.is_valid():
            form.save()
            form = ResumeForm(request.user, instance=resume)
            template_dict['message'] = 'Resume updated'
    else:
        form = ResumeForm(request.user, instance=resume)

    template_dict['form'] = form

    return render(request, 'resume/resume_edit.html', template_dict)
