from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .forms import UserUpdateForm, EmailVerificationForm
from .models import EmailVerification

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)

        if u_form.is_valid():
            u_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form,
    }
    return render(request, 'users/profile.html', context)

@login_required
def verify_email(request):
    # Check if email is already verified
    if request.user.profile.email_verified:
        messages.info(request, 'Your email is already verified.')
        return redirect('profile')

    if request.method == 'POST':
        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            entered_code = form.cleaned_data['code']

            try:
                verification = EmailVerification.objects.get(user=request.user)
                if verification.code == entered_code:
                    # Mark email as verified
                    request.user.profile.email_verified = True
                    request.user.profile.save()

                    # Delete verification code
                    verification.delete()

                    messages.success(request, 'Your email has been successfully verified!')
                    return redirect('profile')
                else:
                    messages.error(request, 'Invalid verification code. Please try again.')
            except EmailVerification.DoesNotExist:
                messages.error(request, 'Verification code not found. Please request a new one.')
    else:
        form = EmailVerificationForm()

    return render(request, 'users/verify_email.html', {'form': form})

@login_required
def send_verification_email(request):
    # Check if email is already verified
    if request.user.profile.email_verified:
        messages.info(request, 'Your email is already verified.')
        return redirect('profile')

    # Generate verification code
    code = EmailVerification.generate_code()

    # Save or update verification code
    verification, created = EmailVerification.objects.update_or_create(
        user=request.user,
        defaults={'code': code}
    )

    # Send email with verification code
    subject = 'Email Verification Code'
    html_message = render_to_string('users/email_verification.html', {
        'user': request.user,
        'code': code
    })
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = request.user.email

    try:
        send_mail(
            subject,
            plain_message,
            from_email,
            [to_email],
            html_message=html_message,
            fail_silently=False
        )
        messages.success(request, f'Verification code has been sent to {to_email}')
    except Exception as e:
        messages.error(request, f'Failed to send verification email: {str(e)}')

    return redirect('verify_email')
