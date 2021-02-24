from django.conf import settings


def settings_context(_request):
    """Settings available by default to the templates context."""
    # Note: we intentionally do NOT expose the entire settings
    # to prevent accidental leaking of sensitive information
    return {"DEBUG": settings.DEBUG}


def offices_per_user(request):
    context = {}
    # context["offices"] Office.objects.all()
    if request.user.is_authenticated:
        context["default_office"] = request.user.default_office.name
        context["last_office"] = request.session.setdefault(
            "last_office", context["default_office"]
        )

    return context
