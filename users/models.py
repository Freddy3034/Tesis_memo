from django.db import models
from django.contrib.auth.models import AbstractUser
class Cargos(models.Model):
    id = models.BigAutoField(primary_key=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'cargos'

class Departamentos(models.Model):
    codigo = models.TextField(primary_key=True)
    descripcion = models.TextField(blank=True, null=True)
    codigo_padre = models.ForeignKey('self', models.DO_NOTHING, db_column='codigo_padre', blank=True, null=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True)
    fecha_actualizacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'departamentos'

class Personas(models.Model):
    id = models.BigAutoField(primary_key=True)
    fk_tipo_nacionalidad = models.ForeignKey('TipoNacionalidad', models.DO_NOTHING, db_column='fk_tipo_nacionalidad', blank=True, null=True)
    fk_departamento = models.ForeignKey(Departamentos, models.DO_NOTHING, db_column='fk_departamento', blank=True, null=True)
    fk_cargo = models.ForeignKey(Cargos, models.DO_NOTHING, db_column='fk_cargo', blank=True, null=True)
    nombres = models.TextField()
    apellidos = models.TextField()
    cedula = models.BigIntegerField(unique=True)
    firma_url = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'personas'

class TipoNacionalidad(models.Model):
    id = models.BigAutoField(primary_key=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True)
    fecha_actualizacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'tipo_nacionalidad'  

class Usuarios(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    username = models.TextField(unique=True)
    #password = models.TextField(db_column='password_hash')
    fk_persona = models.ForeignKey(Personas, models.DO_NOTHING, db_column='fk_persona', blank=True, null=True)
    rol = models.TextField(blank=True, null=True)
    USERNAME_FIELD= 'username'
    #REQUIRED_FIELDS= ['username']
    class Meta:
        #managed = False
        db_table = 'usuarios'             