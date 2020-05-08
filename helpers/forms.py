class PlaceholdersMixin:
    """
    Sets the placeholders on a Form's widgets. Add a "placeholders" dict to the
    Meta options, which maps field names to placeholder texts.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = getattr(self.Meta, "placeholders", {})
        for field, placeholder in placeholders.items():
            self.fields[field].widget.attrs["placeholder"] = placeholder
