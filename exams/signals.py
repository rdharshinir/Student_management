from .models import SystemConfig

def create_system_config(sender, **kwargs):
    if not SystemConfig.objects.exists():
        SystemConfig.objects.create()
