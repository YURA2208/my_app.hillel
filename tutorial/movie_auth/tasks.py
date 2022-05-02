from celery import shared_task
from movie_auth.models import MyUser

@shared_task
def notify_task_user():
    false_status_users = MyUser.objects.filter(is_notified=False)
    for user in false_status_users:
        if not user.is_notified:
            user.is_notified = True
            user.save()
        print(f'User {user.name} is notified')
    return "All users are notified"