from rest_framework import serializers
from accounts.models import User
from .models import (
    RtImage,
    AiModel,
    Expert,
    ExpertDefect,
    AiDefect,
)


class AiModelCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = AiModel
        fields = [
            'pk',
            'rt_image',
        ]

class RtImageCreateSerializer(serializers.ModelSerializer):
    uploader    = serializers.ReadOnlyField(source='uploader.username')

    class Meta:
        model = RtImage
        fields = [
            'pk',
            'uploader',
            'upload_date',
            'image',
        ]


class AiDefectSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AiDefect
        fields = [
            'pk',
            'ai_model',
            'defect_type',
            'score',
            'xmin',
            'ymin',
            'xmax',
            'ymax',
        ]
    
    def validate_defect_type(self, value):
        valid_defect_types = [
            'slag',
            'porosity',
            'others',
        ]
        if value not in valid_defect_types:
            raise serializers.ValidationError("This is not a valid defect type name.")
        return value


class AiModelListSerializer(serializers.ModelSerializer):
    ai_defect_set = AiDefectSerializer(many=True)
    
    class Meta:
        model = AiModel
        fields = [
            'pk',
            'rt_image',
            'ai_defect_set'
        ]

    def to_representation(self, instance):
        """Custom representation to handle no AiModel case."""
        representation = super().to_representation(instance)
        if not instance.ai_defect_set.exists():
            representation['ai_defect_set'] = []
        return representation


class ExpertDefectSerializer(serializers.ModelSerializer):
    modifier_name = serializers.ReadOnlyField(source='modifier.username')
    
    class Meta:
        model = ExpertDefect
        fields = [
            'pk',
            'expert',
            'modifier',
            'modifier_name',
            'modified_date',
            'defect_type',
            'xmin',
            'ymin',
            'xmax',
            'ymax',
        ]

    def validate_defect_type(self, value):
        valid_defect_types = [
            'slag',
            'porosity',
            'others',
        ]
        if value not in valid_defect_types:
            raise serializers.ValidationError("This is not a valid defect type name.")
        return value


class ExpertListSerializer(serializers.ModelSerializer):
    expert_defect_set = ExpertDefectSerializer(many=True)
    
    class Meta:
        model = Expert
        fields = [
            'pk',
            'rt_image',
            'expert_defect_set',
        ]


class RtImageListSerializer(serializers.ModelSerializer):
    image_name = serializers.SerializerMethodField()
    uploader_name = serializers.ReadOnlyField(source='uploader.username')
    ai_model = AiModelListSerializer()
    expert = ExpertListSerializer()
    
    class Meta:
        model = RtImage
        fields = [
            'pk',
            'image',
            'image_name',
            'uploader',
            'uploader_name',
            'upload_date',
            'ai_model',
            'expert'
        ]

    def get_image_name(self, obj):
        return obj.image.name.split('/')[-1]