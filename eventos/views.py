from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Evento, Inscricao

@login_required
def criar_evento(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        data = request.POST.get('data')
        Evento.objects.create(nome=nome, data=data)
        return redirect('home')
    return render(request, 'eventos/criar_evento.html')

@login_required
def inscricao(request):
    eventos = Evento.objects.all()
    if request.method == 'POST':
        evento_id = request.POST.get('evento')
        evento = Evento.objects.get(id=evento_id)
        Inscricao.objects.get_or_create(usuario=request.user, evento=evento)
        return redirect('home')
    return render(request, 'eventos/inscricao.html', {'eventos': eventos})
