import os
import logging

from django.conf import settings
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, HttpRequest
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import login as login_view
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.contrib.auth.views import redirect_to_login

# Configure instant2fa with your access key and access secret. You can get
# these credentials at https://developer.dashboard.instant2fa.com
# See docs.instant2fa.com for more
import instant2fa
instant2fa.access_key = os.environ['ACCESS_KEY']
instant2fa.access_secret = os.environ['ACCESS_SECRET']


# Helpers
def get_user_distinct_id(user):
    return str(user.id)


def get_session_distinct_id(session):
    return session.get('distinct_id')


def redirect_to_user_settings():
    return redirect(settings.LOGIN_REDIRECT_URL)


def do_login(request):
    """
    Log the user whose distinct_id is stored in the session and clear the
    request session.
    """
    distinct_id = request.session.pop('distinct_id')
    user = User.objects.get(id=distinct_id)
    login(request, user)
    return redirect_to_user_settings()


# Views
def index(request):
    return render(request, 'index.html', {})


@login_required
def user_settings(request):
    distinct_id = get_user_distinct_id(request.user)
    hosted_url = instant2fa.create_settings(distinct_id)
    context = {'user': request.user, 'url': hosted_url}
    return TemplateResponse(request, 'user/settings.html', context)


@require_http_methods(['POST'])
@never_cache
def two_factor_verification(request):
    token = request.POST['instant2faToken']
    distinct_id = get_session_distinct_id(request.session)
    try:
        confirmed = instant2fa.confirm_verification(distinct_id, token)
    except instant2fa.errors.VerificationMismatch:
        logging.debug('The distinct_id in the session does not match.')
        return HttpResponseRedirect('/login/two-factor/')
    except instant2fa.errors.VerificationFailed:
        logging.debug(
            'The verification request timed out or was tried too many times.'
        )
        return redirect_to_login(settings.LOGIN_REDIRECT_URL)

    return do_login(request)


def two_factor_login(request):
    if request.user.is_authenticated:
        return redirect_to_user_settings()
    distinct_id = get_session_distinct_id(request.session)
    if not distinct_id:
        return redirect_to_login(settings.LOGIN_REDIRECT_URL)
    try:
        hosted_url = instant2fa.create_verification(distinct_id)
    except instant2fa.errors.MFANotEnabled:
        # user has not turned on Instant2FA so login as usual
        return do_login(request)
    return TemplateResponse(
        request, 'registration/two-factor.html', context={'url': hosted_url}
    )


@sensitive_post_parameters()
@never_cache
def login_entrypoint(request, authentication_form=AuthenticationForm):
    """
    Display the login form. If the user has turned on Instant2FA, verify the
    two factor code. Otherwise, login as usual.
    """
    if request.user.is_authenticated:
        return redirect_to_user_settings()

    if request.method == 'GET':
        return login_view(request)

    # authenticate the user
    form = authentication_form(request, data=request.POST)

    # store the user's id in the session so you can perform Instant2FA check
    if form.is_valid():
        user = form.get_user()
        request.session['distinct_id'] = get_user_distinct_id(user)
        return HttpResponseRedirect('/login/two-factor/')
    else:
        logging.debug("User did not provide valid authentication credentials.")
        return login_view(request)
