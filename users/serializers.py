# -*- coding:utf-8 -*-


from django.contrib.auth import get_user_model
from rest_framework import serializers
from collections import OrderedDict
from .models import LoginRecord

User = get_user_model()

class LoginRecordSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(many=False, read_only=True, slug_field='username')
    class Meta:
        model = LoginRecord
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ['user_permissions']

    def to_representation(self, instance):
        ret = super(UserSerializer, self).to_representation(instance)
        if not isinstance(instance, OrderedDict):
            group_instance = instance.groups.first()
            groups = {'id': group_instance.id, 'name': group_instance.name} if group_instance else {}
            ret['groups'] = groups
        return ret

    def create(self, validated_data):
        instance = super(UserSerializer, self).create(validated_data)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if instance.password != password:
            instance.set_password(password)
        return super(UserSerializer, self).update(instance, validated_data)