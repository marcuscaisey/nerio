from django.db import IntegrityError


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


class ModelFormIntegrityMixin:
    """
    To be used in conjunction with the ModelFormMixin. Returns the model form
    filled with errors if an IntegrityError is raised whilst saving the
    associated instance. This is a solution to the following problem which is
    caused by a race condition when saving the form:

    1. We have the following model and model form:

       class Foo(Model):
           bar = IntegerField(unique=True)

       class FooForm(ModelForm):
           class Meta:
               model = Foo
               fields = ("bar",)

    2. A page contains FooForm.

    3. At the same time, two users submit FooForm with bar = 2.

    4. Both requests are handled, forms are validated and saved. Only one saves
       successfully though, the other fails and raises an IntegrityError because
       there already exists a Foo with bar = 2.
    """

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except IntegrityError:
            form = self.get_form()
            return self.form_invalid(form)
