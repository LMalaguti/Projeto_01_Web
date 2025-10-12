from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from eventos.models import Inscricao

@login_required
def gerar_certificado(request):
    inscricoes = Inscricao.objects.filter(usuario=request.user)
    return render(request, 'certificados/gerar.html', {'inscricoes': inscricoes})
