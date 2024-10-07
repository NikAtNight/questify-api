from rest_framework import serializers

from .models import Habit
from .models import UserHabit
from app.external.models import Category
from app.skills.models import Skill


class SlimCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
        ]
        read_only_fields = fields


class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = [
            'id',
            'name',
            'description',
            'points',
            'milestones',
        ]
        read_only_fields = fields


class HabitSerializer(serializers.ModelSerializer):

    difficultyLevel = serializers.CharField(
        source='difficulty_level'
    )
    category = SlimCategorySerializer(
        read_only=True,
        many=True
    )
    milestones = serializers.JSONField(
        default=list,
    )
    skills = SkillSerializer(
        read_only=True,
        many=True
    )

    class Meta:
        model = Habit
        fields = [
            'id',
            'name',
            'category',
            'difficultyLevel',
            'milestones',
            'skills',
            'experience'
        ]
        read_only_fields = fields


class SlimHabitSerializer(serializers.ModelSerializer):

    difficultyLevel = serializers.CharField(
        source='difficulty_level'
    )

    class Meta:
        model = Habit
        fields = [
            'id',
            'name',
            'difficultyLevel',
        ]
        read_only_fields = fields


class UserHabitSerializer(serializers.ModelSerializer):

    habit = SlimHabitSerializer(
        read_only=True
    )
    status = serializers.CharField()
    currentStreak = serializers.IntegerField(
        source='current_streak'
    )
    nextMilestone = serializers.IntegerField(
        source='next_milestone'
    )
    nextSkillUnlock = serializers.CharField(
        source='next_skill_unlock'
    )
    progressPercentage = serializers.FloatField(
        source='progress_percentage'
    )
    notificationsEnabled = serializers.BooleanField(
        source='notifications_enabled'
    )

    class Meta:
        model = UserHabit
        fields = [
            'id',
            'user',
            'habit',
            'status',
            'currentStreak',
            'nextMilestone',
            'nextSkillUnlock',
            'progressPercentage',
            'notificationsEnabled',
        ]
        read_only_fields = [
            'id',
            'user',
            'habit',
            'status',
            'currentStreak',
            'nextMilestone',
            'nextSkillUnlock',
            'progressPercentage',
        ]
