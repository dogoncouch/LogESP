
def get_pageless_path(request):
    return {'current_path': request.get_full_path()[:-7] }
