from django.contrib import admin

from users.models import Friendship, Interests, Photo, User, UserTag


class InterestsInline(admin.TabularInline):
    model = Interests
    fields = ["interest"]


class UserTagInline(admin.TabularInline):
    model = UserTag
    fields = ["tag"]


class PhotoInline(admin.TabularInline):
    model = Photo
    fields = ["url", "is_main"]


class FriendshipInline(admin.TabularInline):
    model = Friendship
    fk_name = "user_1"
    fields = ["user_1", "user_2", "request_date", "approve_date"]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "first_name",
        "last_name",
        "city",
        "gender",
        "birthday",
        "mobile_phone",
    ]
    list_filter = ["gender"]
    inlines = [InterestsInline, UserTagInline, PhotoInline, FriendshipInline]
