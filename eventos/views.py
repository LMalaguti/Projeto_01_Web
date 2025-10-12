from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Evento, Inscricao

@login_required
def criar_evento(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')  # campo do modelo
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')
        horario = request.POST.get('horario')
        tipo = request.POST.get('tipo')
        descricao = request.POST.get('descricao')
        local = request.POST.get('local')
        quantidade_participantes = request.POST.get('quantidade_participantes')
        organizador = request.user  # usuário logado

        Evento.objects.create(
            titulo=titulo,
            data_inicio=data_inicio,
            data_fim=data_fim,
            horario=horario,
            tipo=tipo,
            descricao=descricao,
            local=local,
            quantidade_participantes=quantidade_participantes,
            organizador=organizador
        )
        return redirect('home')

    return render(request, 'eventos/criar.html')


@login_required
def inscricao(request):
    eventos = Evento.objects.all()
    if request.method == 'POST':
        evento_id = request.POST.get('evento')
        evento = Evento.objects.get(id=evento_id)
        Inscricao.objects.get_or_create(usuario=request.user, evento=evento)
        return redirect('home')
    return render(request, 'eventos/inscricao.html', {'eventos': eventos})
