from django.shortcuts import redirect


def user_view(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return redirect('login_page')
            else:
                return view_func(request, *args, **kwargs)

    return wrapper_func


def admin_view(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.is_staff:
                return redirect('login_page')
            else:
                return view_func(request, *args, **kwargs)

    return wrapper_func


def unauthenticated_view(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return redirect('admin_page')
            if not request.user.is_staff:
                return redirect('index')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func
