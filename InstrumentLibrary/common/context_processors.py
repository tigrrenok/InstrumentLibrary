def get_context_menu(request):
    menu_items = [{'title': "О сайте", 'url_name': 'about'},
                  {'title': "Добавить статью", 'url_name': 'add_page'},
                  {'title': "Обратная связь", 'url_name': 'contact'},
                  {'title': "Войти", 'url_name': 'users:login', 'title2': "Регистрация", 'url_name2': 'users:register'},
                  ]
    if request.user.is_authenticated:
        menu_items[-1] = {'title': request.user.username, 'url_name': 'users:profile', 'title2': "Выйти", 'url_name2': 'users:logout'}

    return {'menu': menu_items}