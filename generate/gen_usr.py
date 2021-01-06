import string
from django.contrib.auth.models import User


def generate_tuple(name, number):
    return(name,
           (name+(number*4)[:4]+name),
           name+'@example.com')


user_list = [leter*4 for leter in string.ascii_lowercase]
account_tuple = [generate_tuple(user_list[i], str(i)) for i in range(len(user_list))]

print(account_tuple)

us = [User.objects.create(username=obj[0], password=obj[1], email=obj[2])
      for obj in account_tuple]
[us[i].set_password(account_tuple[i][1]) for i in range(len(us))]
[us[i].save() for i in range(len(us))]
