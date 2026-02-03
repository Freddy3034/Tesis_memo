from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Memos, ArchivosAdjuntos, Validaciones, Status
from .serializers import MemoSerializer, ArchivoAdjuntoSerializer
from users.models import Personas, Usuarios
from django.db.models import Q
from django.db import models
from django.utils import timezone
from rest_framework import viewsets
from rest_framework import permissions

class MemoViewSet(viewsets.ModelViewSet):
    serializer_class = MemoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        
         """
 Filtra los memos según el usuario logueado.- Si es Funcionario: Ve sus borradores y los enviados.- Si es Director: Ve todo lo de su area (esto requeriría lógica de 
deptos), 
por ahora simplificamos a: lo que envió o recibió.
 """
         user = self.request.user
         if not user.fk_persona:
              return Memos.objects.none()
         
         persona_id = user.fk_persona.id

         #Memos donde soy emisor o receptor 
         return Memos.objects.filter(
              Q(fk_emisor_id=persona_id) |
              Q(fk_receptor_id=persona_id)
         ) .order_by('id')
    
    def perform_create(self, serializer):
        """Al crear, asigna automaticamente el emisor y estado inicial"""
        Usuario = self.request.user
        if not Usuario.fk_persona:
             raise serializer.validationError("El usuario no tiene una Persona asociada")   
        
        #estado inicial siempre es BORRADDOR
        serializer.save(
             fk_emisor=Usuario.fk_persona,
             estado='BORRADOR'
        )

        #creamos el registro inicial en validaciones
        memo_instance = serializer.instance
        status_obj = Status.objects.get_or_create(descripcion='BORRADOR')
        Validaciones.objects.create(
             fk_memo=memo_instance,
             fk_status=status_obj,
             fk_validador=Usuario.fk_persona,
             resultado="Creacion del borrador"
        )

          # --- ACCIONES DE FLUJO DE TRABAJO ---

    @action(detail=True, methods=['post'])
    def enviar_a_revision(self, request, pk=None):
         memo = self.get_object()
         if memo.estado != 'BORRADOR':
              return Response({'error': 'Solo borradores pueden enviarse a revision'}, status=400)
         
         nuevo_estado = 'EN_REVISION'
         memo.estado = nuevo_estado
         memo.save()

         self._registrar_validacion(memo, nuevo_estado,request.user.fk_persona, "Enviado para revision")
         return Response({'status': 'Memo enviado a revision'})
    @action(detail=True, methods=['post'])
    def aprobar_envio(self, request, pk=None):
         """Director aprueba y envia el memo"""
         #Validar que sea Director
         if request.user.rol != 'Director':
              return Response({'error': 'Solo directores pueden aprobar'},status=403)
         
         memo = self.get_object()
         if memo.estado != 'EN_REVISION':
              return Response({'error': 'El memo no está en revision'},status=400)
         
         nuevo_estado = 'ENVIADO'
         memo.estado = nuevo_estado
         memo.fecha_emision = timezone.now() #Aqui se "firma"
         memo.save()
         self._registrar_validacion(memo, nuevo_estado,request.user.fk_persona, "Aprobado y Enviado")
         return Response({'status': 'Memo aprobado y enviado'})
    @action(detail=True, methods=['post'])
    def recibir(self, request, pk=None):
         """Director receptor acepta el memo"""
         memo = self.get_object()
         #verificar que quien llama es el receptor
         if request.user.fk_persona != memo.fk_receptor:
              return Response({'error': 'No eres el destinatario'},status=403)
         nuevo_estado = 'RECIBIDO'
         memo.estado = nuevo_estado
         memo.save()

         self._registrar_validacion(memo , nuevo_estado,request.user.fk_persona,"Memo recibido conforme")
         return Response({'status': 'Memo recibido'})
    def _registrar_validacion(self, memo, estado_desc, validador,resultado):
          status_obj, _ = Status.objects.get_or_create(descripcion=estado_desc) 
          Validaciones.objects.create(
              fk_memo=memo,
              fk_status=status_obj,
              fk_validador=validador,
              resultado=resultado
         )

class ArchivoAdjuntoViewSet (viewsets.ModelViewSet):
     queryset = ArchivosAdjuntos.objects.all()
     serializer_class = ArchivoAdjuntoSerializer
     parser_classes = (MultiPartParser, FormParser) #Permite subir Archivos

     def create(self, request, *args, **kwargs):
          #Logica simple para atar archivos a un memo existente
          memo_id = request.data.get('fk_memo')
          if not memo_id:
               return Response({'error': 'fk_memo es requerido'}, status=400)
          return super().create(request, *args, **kwargs)
         

    
    

