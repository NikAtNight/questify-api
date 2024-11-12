from rest_framework import serializers

from .models import (
    Habit,
    UserHabit,
    HabitLog,
)
from app.external.models import Category
from app.milestones.models import Milestone
from app.users.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from zoneinfo import ZoneInfo
from app.core.enums import HabitStatusEnum


class SlimCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
        ]
        read_only_fields = fields


class MilestoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Milestone
        fields = [
            'id',
            'name',
            'day',
            'points',
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
    milestones = MilestoneSerializer(
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


class NextMilestoneMixin:
    def get_next_milestone(self, obj):
        if not hasattr(obj, '_next_milestone'):
            next_milestone = obj.habit.milestones.filter(
                day__gt=obj.current_streak
            ).order_by('day').first()

            obj._next_milestone = next_milestone.day if next_milestone else 0

        return obj._next_milestone


class UserHabitSerializer(NextMilestoneMixin, serializers.ModelSerializer):

    habit = SlimHabitSerializer(
        read_only=True
    )
    status = serializers.CharField()
    currentStreak = serializers.IntegerField(
        source='current_streak'
    )
    progressPercentage = serializers.FloatField(
        source='progress_percentage'
    )
    nextMilestone = serializers.SerializerMethodField(
        method_name='get_next_milestone'
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
            'progressPercentage',
        ]
        read_only_fields = [
            'id',
            'user',
            'habit',
            'status',
            'currentStreak',
            'nextMilestone',
            'progressPercentage',
        ]


class UserHabitCreateSerializer(serializers.ModelSerializer):

    habit = serializers.PrimaryKeyRelatedField(
        queryset=Habit.objects.all(),
        write_only=True,
        required=True,
    )

    def create(self, validated_data):
        habit = validated_data.pop('habit')

        user_habit = UserHabit.objects.create(
            user=self.context['request'].user,
            habit=habit,
            start_date=timezone.now()
        )
        return user_habit

    class Meta:
        model = UserHabit
        fields = [
            'habit',
        ]


class MilestoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Milestone
        fields = [
            'name',
            'day',
            'points',
        ]


class SlimRetrieveHabitSerializer(serializers.ModelSerializer):

    difficultyLevel = serializers.CharField(
        source='difficulty_level'
    )
    milestones = MilestoneSerializer(
        read_only=True,
        many=True
    )

    class Meta:
        model = Habit
        fields = [
            'id',
            'name',
            'difficultyLevel',
            'milestones',
        ]
        read_only_fields = fields


class UserHabitRetrieveSerializer(NextMilestoneMixin, serializers.ModelSerializer):

    habit = SlimRetrieveHabitSerializer(
        read_only=True
    )
    startDate = serializers.DateTimeField(
        source='start_date'
    )
    completionDate = serializers.DateTimeField(
        source='completion_date'
    )
    status = serializers.CharField()
    currentStreak = serializers.IntegerField(
        source='current_streak'
    )
    bestStreak = serializers.IntegerField(
        source='best_streak'
    )
    totalDaysCompleted = serializers.IntegerField(
        source='total_days_completed'
    )
    progressPercentage = serializers.FloatField(
        source='progress_percentage'
    )
    nextMilestone = serializers.SerializerMethodField(
        method_name='get_next_milestone'
    )

    class Meta:
        model = UserHabit
        fields = [
            'id',
            'habit',
            'startDate',
            'completionDate',
            'status',
            'currentStreak',
            'bestStreak',
            'totalDaysCompleted',
            'nextMilestone',
            'progressPercentage',
        ]
        read_only_fields = fields


class UserHabitUpdateSerializer(serializers.ModelSerializer):

    status = serializers.CharField()

    def update(self, instance, validated_data):
        status = validated_data.get('status', None)

        if status is not None:
            instance.status = status

        instance.save()
        return instance

    class Meta:
        model = UserHabit
        fields = [
            'status',
        ]


class HabitLogSerializer(serializers.ModelSerializer):
    createdAt = serializers.DateTimeField(
        source='created_at'
    )

    class Meta:
        model = HabitLog
        fields = [
            'createdAt',
        ]


class HabitLogCreateSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        required=True,
    )
    habit = serializers.PrimaryKeyRelatedField(
        queryset=Habit.objects.all(),
        write_only=True,
        required=True,
    )
    timezone = serializers.CharField(
        write_only=True,
        required=True,
    )

    def create(self, validated_data):
        tz = validated_data.pop('timezone')
        try:
            user_tz = ZoneInfo(tz)
            user_local_date = timezone.now().astimezone(user_tz).date()

            print(timezone.now().astimezone(user_tz))

            logs = HabitLog.objects.filter(
                user=validated_data['user'],
                habit=validated_data['habit'],
                created_at__date=user_local_date,
            )

            if logs.count() > 0:
                raise serializers.ValidationError('Already logged this habit today')

            habit_log = HabitLog.objects.create(
                **validated_data,
                created_at=timezone.now().astimezone(user_tz)
            )

            user_habit = UserHabit.objects.get(
                user=validated_data['user'],
                habit=validated_data['habit'],
            )

            last_log = HabitLog.objects.filter(
                user=validated_data['user'],
                habit=validated_data['habit'],
                created_at__date__lt=user_local_date
            ).order_by('-created_at').first()

            user_habit.total_days_completed += 1

            if last_log:
                days_between = (user_local_date - last_log.created_at.astimezone(user_tz).date()).days
                if days_between == 1:
                    user_habit.current_streak += 1
                else:
                    user_habit.current_streak = 1
                    user_habit.progress_percentage = 0.0
            else:
                user_habit.current_streak = 1
                user_habit.progress_percentage = 0.0
            if user_habit.current_streak > user_habit.best_streak:
                user_habit.best_streak = user_habit.current_streak

            milestones = validated_data['habit'].milestones.all().order_by('-day')
            if milestones.exists():
                final_milestone_day = milestones.first().day
                if final_milestone_day > 0:
                    user_habit.progress_percentage = (user_habit.current_streak / final_milestone_day) * 100
                    user_habit.progress_percentage = min(user_habit.progress_percentage, 100.0)

                    # TODO: When complete, update user experience
                    if user_habit.current_streak >= final_milestone_day:
                        user_habit.status = HabitStatusEnum.COMPLETED.name
                        user_habit.completion_date = timezone.now()
            else:
                user_habit.progress_percentage = 0.0

            user_habit.save()

        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

        return habit_log

    class Meta:
        model = HabitLog
        fields = [
            'user',
            'habit',
            'timezone',
        ]
