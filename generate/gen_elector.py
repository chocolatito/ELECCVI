from django.contrib.auth.models import User
from apps.core.models import Elector


def generate_tuple(name, number, user):
    return(((number+'0')*4)[:8],
           name,
           (name*2).upper(),
           user)


user_list = [us for us in User.objects.filter(is_superuser=0)]

elector_list = [generate_tuple(user_list[i].username, str(i+1), user_list[i])
                for i in range(len(user_list))]

[Elector.objects.create(dni=elector[0],
                        names=elector[1],
                        surnames=elector[2],
                        user=elector[3]) for elector in elector_list]
