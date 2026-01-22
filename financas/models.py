from django.db import models
from django.contrib.auth.models import User

class Transacao(models.Model):
    TIPO_CHOICES = (
        ('E', 'Entrada'),
        ('S', 'Saída'),
    )
    
    descricao = models.CharField("Descrição", max_length=100)
    valor = models.DecimalField("Valor (R$)", max_digits=10, decimal_places=2)
    data = models.DateField("Data da Transação")
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES, default='S')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) # O campo mais importante
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data', '-criado_em']
        verbose_name = "Transação"
        verbose_name_plural = "Transações"

    def __str__(self):
        return f"{self.descricao} - {self.valor}"