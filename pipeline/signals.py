from django.dispatch import Signal


css_compressed = Signal(providing_args=["package", "version"])
js_compressed = Signal(providing_args=["package", "version"])
