from rest_framework import serializers
from .models import Certificado

class CertificateSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    event = serializers.StringRelatedField()
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Certificado
        fields = ['id','user','event','issued_at','file_url']

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None
