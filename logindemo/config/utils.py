from django.contrib.auth import login
from django.utils.timezone import now

def handle_login(request, user):
    right_now = now()
    previous_login = user.last_login or right_now
    previous_login_days = (previous_login - right_now).days

    request.session['previous_login'] = previous_login.strftime("%Y/%m/%d %H:%M:%S")
    request.session['previous_login_days'] = f'{previous_login_days} days ago' if previous_login_days > 0 else 'Today'
    
    login(request, user)

    user.last_login = right_now
    user.login_count += 1
    user.save(update_fields = [
        "last_login", 
        "login_count"
    ])
    