from django.dispatch import Signal

css_filtered = Signal(providing_args=["package", "version"])
js_filtered = Signal(providing_args=["package", "version"])
