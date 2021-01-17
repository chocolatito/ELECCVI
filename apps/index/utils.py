def get_index_sumary(queryset, list_url, create_url):

    if queryset.count():
        return [queryset.count(),
                queryset.filter(active=True).count(),
                queryset.filter(active=False).count(),
                list_url, create_url]
    else:
        return [0, create_url]
