import datetime
from celery import shared_task
from accounts.models.user import CustomUser



@shared_task
def delete_abandon_users():
    users = CustomUser.objects.filter(created_date__lte=(datetime.now - datetime.timedelta(days=31)))
    counter = 0
    for user in users:
        print(f"trying to delete user({user}) ")
        user.delete()
        counter +=1
        
    if counter > 0 :
        print(f"ATTENTION!, {counter} of Users just got removed due to not getting verified during last month!.")
    else:
        print('users are good')
