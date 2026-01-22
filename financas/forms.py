from django import forms
from .models import Transacao
from datetime import date

class TransacaoForm(forms.ModelForm):
    class Meta:
        model = Transacao
        fields = ['descricao', 'valor', 'data', 'tipo']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Salário, Mercado...'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'max': str(date.today())}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
        }

    # Validação personalizada para o campo DATA
    def clean_data(self):
        data_transacao = self.cleaned_data.get('data')
        
        # Verifica se a data existe
        if not data_transacao:
            return data_transacao

        # Regra de Negócio: Não permitir futuro
        if data_transacao > date.today():
            raise forms.ValidationError("Não é permitido lançamentos futuros.")
            
        return data_transacao

    # Validação personalizada para o campo VALOR
    def clean_valor(self):
        valor = self.cleaned_data.get('valor')
        
        if valor is not None and valor <= 0:
           raise forms.ValidationError("O valor deve ser positivo.")
        
        return valor