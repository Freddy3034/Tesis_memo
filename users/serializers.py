from rest_framework import serializers
from .models import Usuarios, Personas, Departamentos, Cargos
class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamentos
        fields = '__all__'
class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargos
        fields = '__all__'
class PersonaSerializer(serializers.ModelSerializer):
    departamento_info = DepartamentoSerializer(source='fk_departamento', read_only=True)
    cargo_info = CargoSerializer(source='fk_cargo', read_only=True)
    class Meta:
        model = Personas
        fields = ['id', 'nombres','apellidos','cedula','departamento_info','cargo_info']
class UsuarioSerializer(serializers.ModelSerializer):
    Persona_info =PersonaSerializer(source='fk_persona', read_only=True)
    class Meta:
        model= Usuarios
        fields = '__all__'