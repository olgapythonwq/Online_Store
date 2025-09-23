from django.core.exceptions import PermissionDenied

class GroupRequiredMixin:
    group_required = None  # Строка или список

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied("Вы не авторизованы.")

        if isinstance(self.group_required, str):
            groups = [self.group_required]
        else:
            groups = self.group_required or []

        if not request.user.groups.filter(name__in=groups).exists():
            raise PermissionDenied("У вас нет доступа к этому разделу.")

        return super().dispatch(request, *args, **kwargs)
