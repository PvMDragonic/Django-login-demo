from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.shortcuts import render

@login_required
def dashboard_start(request):
    user = request.user
    user.dashboard_reloads += 1
    user.save(update_fields = ["dashboard_reloads"])

    days_since_signup = (now() - request.user.signup_date).days

    return render(request, 'dashboard/start.html', {
        'signup_date': request.user.signup_date.strftime("%Y/%m/%d %H:%M:%S"),
        'days_since_signup': f'{days_since_signup} days ago' if days_since_signup > 0 else 'Today',
        'previous_login': request.session['previous_login'],
        'previous_login_days': request.session['previous_login_days']
    })