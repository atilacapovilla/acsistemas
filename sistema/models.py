from django.db import models

class Sistema(models.Model):
    nome = models.CharField(max_length=30)
    descricao = models.TextField()
    url_app = models.CharField(max_length=100)
    icone_app = models.CharField(max_length=30)
    liberado = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    upfated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome
    
    class Meta:
        ordering = ['nome']
