from django.shortcuts import render


def index_page(request):
    template = 'main/index.html'
    context = {
        'status': 'ok',
    }
    return render(request, template, context)
