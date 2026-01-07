from django.db import models
from users.models import Personas
class ArchivosAdjuntos(models.Model):
    id = models.BigAutoField(primary_key=True)
    fk_memo = models.ForeignKey('Memos', models.DO_NOTHING, db_column='fk_memo', blank=True, null=True)
    nombre_archivo = models.TextField()
    ruta_archivo = models.TextField()
    fecha_subida = models.DateTimeField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'archivos_adjuntos'

class Memos(models.Model):
    id = models.BigAutoField(primary_key=True)
    titulo = models.TextField()
    contenido = models.TextField()
    fecha_emision = models.DateTimeField(blank=True, null=True)
    fk_emisor = models.ForeignKey(Personas, models.DO_NOTHING, db_column='fk_emisor', blank=True, null=True)
    fk_receptor = models.ForeignKey(Personas, models.DO_NOTHING, db_column='fk_receptor', related_name='memos_fk_receptor_set', blank=True, null=True)
    estado = models.TextField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'memos'

class Status(models.Model):
    id = models.BigAutoField(primary_key=True)
    descripcion = models.TextField()

    class Meta:
        #managed = False
        db_table = 'status'

class Validaciones(models.Model):
    id = models.BigAutoField(primary_key=True)
    fk_memo = models.ForeignKey(Memos, models.DO_NOTHING, db_column='fk_memo', blank=True, null=True)
    fk_validador = models.ForeignKey(Personas, models.DO_NOTHING, db_column='fk_validador', blank=True, null=True)
    fecha_validacion = models.DateTimeField(blank=True, null=True)
    resultado = models.TextField(blank=True, null=True)
    fk_status = models.ForeignKey(Status, models.DO_NOTHING, db_column='fk_status', blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'validaciones'