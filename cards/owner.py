from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from cards.models import Confectioner


class ConfectionerRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not Confectioner.objects.filter(user=request.user).exists():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class OwnerCreateView(ConfectionerRequiredMixin, CreateView):
    """
    Sub-class of the CreateView to automatically pass the Request to the Form
    and add the owner to the saved object.
    """

    # Saves the form instance, sets the current object for the view, and redirects to get_success_url().
    def form_valid(self, form):
        print('form_valid called')
        object_ = form.save(commit=False)
        object_.owner = Confectioner.objects.get(user=self.request.user)
        object_.save()
        return super(OwnerCreateView, self).form_valid(form)


class OwnerUpdateView(ConfectionerRequiredMixin, UpdateView):
    """
    Sub-class the UpdateView to pass the request to the form and limit the
    queryset to the requesting user.
    """

    def get_queryset(self):
        print('update get_queryset called')
        """ Limit a User to only modifying their own data. """
        qs = super(OwnerUpdateView, self).get_queryset()
        return qs.filter(owner__user=self.request.user)


class OwnerDeleteView(ConfectionerRequiredMixin, DeleteView):
    """
    Sub-class the DeleteView to restrict a User from deleting other
    user's data.
    """

    def get_queryset(self):
        print('delete get_queryset called')
        qs = super(OwnerDeleteView, self).get_queryset()
        return qs.filter(owner__user=self.request.user)
