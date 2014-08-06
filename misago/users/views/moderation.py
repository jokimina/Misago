from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.shortcuts import redirect, render
from django.utils.translation import ugettext as _

from misago.acl import add_acl
from misago.core.decorators import require_POST
from misago.core.shortcuts import get_object_or_404, validate_slug
from misago.core.utils import clean_return_path
from misago.markup import Editor

from misago.users.avatars.dynamic import set_avatar as set_dynamic_avatar
from misago.users import warnings
from misago.users.bans import get_user_ban
from misago.users.decorators import deny_guests
from misago.users.forms.rename import ChangeUsernameForm
from misago.users.forms.modusers import (BanForm, ModerateAvatarForm,
                                         ModerateSignatureForm, WarnUserForm)
from misago.users.models import Ban
from misago.users.permissions.moderation import (allow_rename_user,
                                                 allow_moderate_avatar,
                                                 allow_moderate_signature,
                                                 allow_ban_user,
                                                 allow_lift_ban)
from misago.users.permissions.warnings import (allow_warn_user,
                                               allow_see_warnings,
                                               allow_cancel_warning,
                                               allow_delete_warning)
from misago.users.permissions.delete import allow_delete_user
from misago.users.signatures import set_user_signature
from misago.users.sites import user_profile


def user_moderation_view(required_permission=None):
    def wrap(f):
        @deny_guests
        @transaction.atomic
        def decorator(request, *args, **kwargs):
            queryset = get_user_model().objects.select_for_update()
            user_id = kwargs.pop('user_id')

            kwargs['user'] = get_object_or_404(queryset, id=user_id)
            validate_slug(kwargs['user'], kwargs.pop('user_slug'))
            add_acl(request.user, kwargs['user'])

            if required_permission:
                required_permission(request.user, kwargs['user'])

            return f(request, *args, **kwargs)
        return decorator
    return wrap


def moderation_return_path(request, user):
    return_path = clean_return_path(request)
    if not return_path:
        return reverse(user_profile.get_default_link(),
                       kwargs={'user_slug': user.slug, 'user_id': user.pk})
    return return_path


@user_moderation_view(allow_warn_user)
def warn(request, user, reason=None):
    return_path = moderation_return_path(request, user)

    if warnings.is_user_warning_level_max(user):
        message = _("%(username)s has maximum warning "
                    "level and can't be warned.")
        message = message % {'username': user.username}
        messages.info(request, message)

        return redirect(return_path)

    form = WarnUserForm(initial={'reason': reason})
    if request.method == 'POST':
        form = WarnUserForm(request.POST)
        if form.is_valid():
            warnings.warn_user(request.user, user, form.cleaned_data['reason'])

            message = _("%(username)s has been warned.")
            message = message % {'username': user.username}
            messages.success(request, message)

            return redirect(return_path)

    warning_levels = warnings.get_warning_levels()
    current_level = warning_levels[user.warning_level]
    next_level = warning_levels[user.warning_level + 1]

    return render(request, 'misago/modusers/warn.html', {
        'profile': user,
        'form': form,
        'return_path': return_path,
        'current_level': current_level,
        'next_level': next_level
    })


def warning_moderation_view(required_permission=None):
    def wrap(f):
        @deny_guests
        @transaction.atomic
        def decorator(request, *args, **kwargs):
            queryset = kwargs['user'].warnings
            warning_id = kwargs.pop('warning_id')

            kwargs['warning'] = get_object_or_404(queryset, id=warning_id)
            add_acl(request.user, kwargs['warning'])

            required_permission(request.user, kwargs['warning'])

            response = f(request, *args, **kwargs)

            if response:
                return response
            else:
                return_path = moderation_return_path(request, kwargs['user'])
                return redirect(return_path)
        return decorator
    return wrap


@user_moderation_view(allow_see_warnings)
@warning_moderation_view(allow_cancel_warning)
def cancel_warning(request, user, warning):
    warnings.cancel_warning(request.user, user, warning)

    message = _("%(username)s's warning has been canceled.")
    message = message % {'username': user.username}
    messages.success(request, message)


@user_moderation_view(allow_see_warnings)
@warning_moderation_view(allow_delete_warning)
def delete_warning(request, user, warning):
    warnings.delete_warning(request.user, user, warning)

    message = _("%(username)s's warning has been deleted.")
    message = message % {'username': user.username}
    messages.success(request, message)


@user_moderation_view(allow_rename_user)
def rename(request, user):
    form = ChangeUsernameForm(user=user)
    if request.method == 'POST':
        old_username = user.username
        form = ChangeUsernameForm(request.POST, user=user)
        if form.is_valid():
            try:
                form.change_username(changed_by=user)
                message = _("%(old_username)s's username has been changed.")
                message = message % {'old_username': old_username}
                messages.success(request, message)

                return redirect(user_profile.get_default_link(),
                                user_slug=user.slug, user_id=user.pk)
            except IntegrityError:
                message = _("Error changing username. Please try again.")
                messages.error(request, message)

    return render(request, 'misago/modusers/rename.html',
                  {'profile': user, 'form': form})


@user_moderation_view(allow_moderate_avatar)
def moderate_avatar(request, user):
    avatar_locked = user.is_avatar_locked
    form = ModerateAvatarForm(instance=user)

    if request.method == 'POST':
        form = ModerateAvatarForm(request.POST, instance=user)
        if form.is_valid():
            if not avatar_locked and form.cleaned_data['is_avatar_locked']:
                set_dynamic_avatar(user)

            user.save(update_fields=(
                'is_avatar_locked',
                'avatar_lock_user_message',
                'avatar_lock_staff_message'
            ))

            message = _("%(username)s's avatar has been moderated.")
            message = message % {'username': user.username}
            messages.success(request, message)

            if 'stay' not in request.POST:
                return redirect(user_profile.get_default_link(),
                                user_slug=user.slug, user_id=user.pk)

    return render(request, 'misago/modusers/avatar.html',
                  {'profile': user, 'form': form})


@user_moderation_view(allow_moderate_signature)
def moderate_signature(request, user):
    form = ModerateSignatureForm(instance=user)

    if request.method == 'POST':
        form = ModerateSignatureForm(request.POST, instance=user)
        if form.is_valid():
            set_user_signature(user, form.cleaned_data['signature'])
            user.save(update_fields=(
                'signature',
                'signature_parsed',
                'signature_checksum',
                'is_signature_locked',
                'signature_lock_user_message',
                'signature_lock_staff_message'
            ))

            message = _("%(username)s's signature has been moderated.")
            message = message % {'username': user.username}
            messages.success(request, message)

            if 'stay' not in request.POST:
                return redirect(user_profile.get_default_link(),
                                user_slug=user.slug, user_id=user.pk)

    acl = user.acl
    editor = Editor(form['signature'],
                    allow_blocks=acl['allow_signature_blocks'],
                    allow_links=acl['allow_signature_links'],
                    allow_images=acl['allow_signature_images'])

    return render(request, 'misago/modusers/signature.html',
                  {'profile': user, 'form': form, 'editor': editor})


@user_moderation_view(allow_ban_user)
def ban_user(request, user):
    form = BanForm(user=user)
    if request.method == 'POST':
        form = BanForm(request.POST, user=user)
        if form.is_valid():
            form.ban_user()

            message = _("%(username)s has been banned.")
            messages.success(request, message % {'username': user.username})

            return redirect(user_profile.get_default_link(),
                            user_slug=user.slug, user_id=user.pk)

    return render(request, 'misago/modusers/ban.html',
                  {'profile': user, 'form': form})


@require_POST
@user_moderation_view(allow_lift_ban)
def lift_user_ban(request, user):
    user_ban = get_user_ban(user).ban
    user_ban.lift()
    user_ban.save()

    Ban.objects.invalidate_cache()

    message = _("%(username)s's ban has been lifted.")
    messages.success(request, message % {'username': user.username})

    return redirect(user_profile.get_default_link(),
                    user_slug=user.slug, user_id=user.pk)


@require_POST
@user_moderation_view(allow_delete_user)
def delete(request, user):
    user.delete(delete_content=True)

    message = _("User %(username)s has been deleted.")
    messages.success(request, message % {'username': user.username})
    return redirect('misago:index')