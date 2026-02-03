from rest_framework import serializers
from .models import Memos, ArchivosAdjuntos, Validaciones, Status
from users.models import Personas, Usuarios
from users.serializers import PersonaSerializer

class ArchivoAdjuntoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchivosAdjuntos
        fields = '__all__'
class ValidacionSerializer(serializers.ModelSerializer):
    validador_nombre = serializers.CharField(source='fk_validador.nombres', read_only=True)
    estado_descripcion = serializers.CharField(source='fk_status.descripcion', read_only=True)
    class Meta:
        model = Validaciones
        fields = ['id','fecha_validacion','resultado','fk_validador','fk_status', 'fk_memo']

class MemoSerializer(serializers.ModelSerializer):
    archivos = ArchivoAdjuntoSerializer(many=True, read_only=True)
    emisor_data = PersonaSerializer(source='fk_emisor', read_only=True)
    receptor_data = PersonaSerializer(source='fk_receptor', read_only=True)
    
    receptor_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Memos
fields = [
'id', 'titulo', 'contenido', 'fecha_emision', 'estado', 'emisor_data','receptor_data','receptor_id', 'archivos'
     ]
read_only_fields = ['fecha_emision', 'estado', 'fk_emisor', 'fk_receptor']

def create(self, validated_data):
            #aqui extraigo el ID del receptor para asignarlo manualmente
            receptor_id = validated_data.pop('receptor_id')
            memo = Memos.objects.create(**validated_data)
            memo.fk_receptor_id = receptor_id
            memo.save()
            return memo
        