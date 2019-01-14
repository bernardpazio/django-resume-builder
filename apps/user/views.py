from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect

from .forms import CreateAccountForm


@login_required
def account_edit_view(request):
    """
    Handle a request to update the user's account info or password.
    """
    template_dict = {}

    if request.method == 'POST':
        if 'updateInfo' in request.POST:
            try:
                _handle_update_account_info(request.user, request.POST)
                template_dict['update_info_message'] = 'Account info updated'
            except FormInputError, e:
                template_dict['update_info_error'] = str(e)
        elif 'changePassword' in request.POST:
            try:
                _handle_change_password(request.user, request.POST)
                # Updating the password invalidates all sessions; recreate the
                # current one so the user doesn't have to log in again.
                update_session_auth_hash(request, request.user)
                template_dict['change_password_message'] = 'Password changed'
            except FormInputError, e:
                template_dict['change_password_error'] = str(e)
        else:
            return HttpResponseBadRequest('Unknown account edit type')

    return render(request, 'user/account_edit.html', template_dict)


def account_create_view(request):
    """
    Handle a request to create a new login account.
    """
    template_dict = {}

    if request.method == 'POST':
        form = CreateAccountForm(request.POST)

        if form.is_valid():
            try:
                user = _handle_create_account(request.POST)
                login(request, user)
                return redirect('resumes')
            except FormInputError, e:
                template_dict['error'] = str(e)
    else:
        form = CreateAccountForm()

    template_dict['form'] = form

    return render(request, "user/account_create.html", template_dict)


def _handle_update_account_info(user, post_data):
    """
    Handle account info form input. Either update the user account's info or
    raise an exception with a useful error message.

    :param user: The Django User to update.
    :param post_data: The input form data.
    :raise FormInputError: If the input form data is not valid.
    """
    if 'first_name' not in post_data:
        raise FormInputError('First name is required')
    if 'last_name' not in post_data:
        raise FormInputError('Last name is required')
    if 'email' not in post_data:
        raise FormInputError('Email is required')

    user.first_name = post_data['first_name']
    user.last_name = post_data['last_name']
    user.email = post_data['email']
    user.save()


def _handle_change_password(user, post_data):
    """
    Handle password change form input. Either update the user's password or
    raise an exception with a useful error message.

    :param user: The Django User to update.
    :param post_data: The input form data.
    :raise FormInputError: If the input form data is not valid.
    """
    if 'old_password' not in post_data:
        raise FormInputError('Old password is required')
    if ('password' not in post_data) or ('password2' not in post_data):
        raise FormInputError('Both new passwords must be provided')

    if not user.check_password(post_data['old_password']):
        raise FormInputError('Your old password was entered incorrectly. '
                             'Please enter it again.')

    if post_data['password'] != post_data['password2']:
        raise FormInputError('New passwords do not match')

    user.set_password(post_data['password'])
    user.save()


def _handle_create_account(post_data):
    """
    Handle account creation form input.

    :param post_data: The input form data. 'username' is assumed to have
        already been validated.
    :return: The newly-created Django User object.
    :raise FormInputError: If the input form data is not valid.
    """
    if 'first_name' not in post_data:
        raise FormInputError('First name is required')
    if 'last_name' not in post_data:
        raise FormInputError('Last name is required')
    if ('password' not in post_data) or ('password2' not in post_data):
        raise FormInputError('Both password fields are required')
    if post_data['password'] != post_data['password2']:
        raise FormInputError('Passwords do not match')

    new_user = User.objects.create_user(post_data['username'],
                                        post_data['email'],
                                        post_data['password'])

    new_user.first_name = post_data['first_name']
    new_user.last_name = post_data['last_name']
    new_user.save()

    return new_user


class FormInputError(Exception):
    """
    Indicates an error processing user form input.
    """
    pass
