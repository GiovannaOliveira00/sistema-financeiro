from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib import messages
from .models import Transacao
from .forms import TransacaoForm

@login_required
def dashboard(request):
    # Filtra apenas as transações do usuário logado
    transacoes = Transacao.objects.filter(usuario=request.user)
    
    # Cálculos de Somatório
    total_entradas = transacoes.filter(tipo='E').aggregate(Sum('valor'))['valor__sum'] or 0
    total_saidas = transacoes.filter(tipo='S').aggregate(Sum('valor'))['valor__sum'] or 0
    saldo = total_entradas - total_saidas

    context = {
        'transacoes': transacoes,
        'entradas': total_entradas,
        'saidas': total_saidas,
        'saldo': saldo
    }
    return render(request, 'financas/dashboard.html', context)

@login_required
def adicionar_transacao(request):
    if request.method == 'POST':
        form = TransacaoForm(request.POST)
        if form.is_valid():
            transacao = form.save(commit=False)
            transacao.usuario = request.user # Associa transação ao usuário
            transacao.save()
            return redirect('dashboard')
    else:
        form = TransacaoForm()
    
    return render(request, 'financas/form.html', {'form': form})

@login_required
def adicionar_transacao(request):
    if request.method == 'POST':
        form = TransacaoForm(request.POST)
        if form.is_valid():
            transacao = form.save(commit=False)
            transacao.usuario = request.user
            transacao.save()
            messages.success(request, 'Movimentação registrada com sucesso!')
            return redirect('dashboard')
        else:
            # Se o formulário for inválido, o Django envia os erros dentro do objeto 'form'
            messages.error(request, 'Erro ao salvar. Verifique os campos abaixo.') # Msg Erro Global
    else:
        form = TransacaoForm()
    
    return render(request, 'financas/form.html', {'form': form})

@login_required
def excluir_transacao(request, id):
    # Garante que o usuário só exclua as suas transações
    transacao = get_object_or_404(Transacao, id=id, usuario=request.user)
    transacao.delete()
    return redirect('dashboard')