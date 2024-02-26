from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from rest_framework import serializers

from subscriptions.models import Subscription

User = get_user_model()



class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_subscribed', 'password')
        write_only_fields = ('password',)

    def get_is_subscribed(self, obj):
        if not self.context:
            return False
        user = self.context.get('request').user
        return user.is_authenticated and Subscription.objects.filter(user=user, author=obj).exists()




class PasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate_current_password(self, value):
        user = self.context['request'].user
        if user.check_password(value):
            return value
        raise serializers.ValidationError('Введён неправильный пароль')

    def validate_new_password(self, value):
        user = self.context['request'].user
        try:
            validate_password(value, user)
        except django_exceptions.ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value


#class SubscriptionSerializer(serializers.ModelSerializer):
#    email = serializers.ReadOnlyField(source='author.email')
#    id = serializers.ReadOnlyField(source='author.id')
#    username = serializers.ReadOnlyField(source='author.username')
#    first_name = serializers.ReadOnlyField(source='author.first_name')
#    last_name = serializers.ReadOnlyField(source='author.last_name')
#
#    is_subscribed = serializers.SerializerMethodField()
#    recipes = serializers.SerializerMethodField()
#    recipes_count = serializers.SerializerMethodField()
#
#    class Meta:
#        model = User
#        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed', 'recipes', 'recipes_count')
#
#
#    def get_is_subscribed(self, obj):
#        user = self.context.get('request').user
#        return user.is_authenticated and Subscription.objects.filter(user=user, author=obj).exists()
#
#    def get_recipes_count(self, obj):
#        return obj.recipes.count()
#
#    def get_recipes(self, obj):
#        from recipes.serializers import RecipeSimpleSerializer
#        request = self.context.get('request')
#        limit = request.GET.get('recipes_limit')
#        recipes = obj.recipes.all()
#        if limit and limit.isdigit():
#            recipes = recipes[:int(limit)]
#        return RecipeSimpleSerializer(recipes, many=True).data
#
#
