import csv
import io

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import forms
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import path
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from apps.models import Model, User


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


@admin.register(Model)
class PostAdmin(admin.ModelAdmin, ExportCsvMixin):
    change_list_template = "admin/change_list.html"
    list_display = ['id', 'custom_title']

    def custom_title(self, obj):
        return ' '.join(obj.title.split()[:4])

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.reader(io_string)
            next(reader)
            result = []
            for row in reader:
                result.append(Model(
                    user_id=int(row[0]),
                    pk=int(row[1]),
                    title=row[2],
                    body=row[3]
                ))

            Model.objects.bulk_create(result)

            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(request, "apps/csv_form.html", payload)

    custom_title.short_description = 'Sarlavha'


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('custom_image', "username", "email", "first_name", "last_name", "is_staff")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", 'image')}),
        (
            _("Permissions"),
            {
                'fields': (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    def custom_image(self, obj: User):
        return mark_safe('<img src="{}"/>'.format(obj.image.url))

    custom_image.short_description = "Image"


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    pass
