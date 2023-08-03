from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from .models import Card
from cards.forms import SearchForm, ConfectionerForm, UserForm
from cards.owner import OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from django.utils.translation import gettext_lazy as _
from django.db.models import Q


class CardListView(generic.ListView):
    template_name = "cards/index.html"

    def get_queryset(self):
        return Card.objects.order_by("-created_at")[:5]

    def get(self, request, **kwargs):
        product = request.GET.get("product")
        confectioner = request.GET.get("confectioner")
        fillings = request.GET.getlist("fillings", None)
        area = request.GET.get("area")
        min_price = request.GET.get("min_price")
        max_price = request.GET.get("max_price")
        query = Q()
        if product:
            query.add(Q(product=product), Q.AND)
        if confectioner:
            query.add(Q(owner=confectioner), Q.AND)
        if area:
            query.add(Q(owner__area=area), Q.AND)
        if min_price:
            query.add(Q(price__gte=min_price), Q.AND)
        if max_price:
            query.add(Q(price__lte=max_price), Q.AND)
        print(query)
        query_set = Card.objects.filter(query)
        if fillings:
            for filling in fillings:
                sub_query = query & Q(fillings=filling)
                sub_query_set = Card.objects.filter(sub_query)
                query_set = query_set.intersection(sub_query_set)
        form = SearchForm(request.GET)
        ctx = {"form": form, "card_list": query_set}
        return render(request, self.template_name, ctx)


class CardDetailView(generic.DetailView):
    template_name = "cards/detail.html"
    model = Card


class CardCreateView(OwnerCreateView):
    model = Card
    template_name = "cards/create.html"
    fields = ["product", "fillings", "price", "name", "description"]
    success_url = reverse_lazy('cards:all')


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        confectioner_form = ConfectionerForm(request.POST, instance=request.user.confectioner)
        if user_form.is_valid() and confectioner_form.is_valid():
            user_form.save()
            confectioner_form.save()
            messages.success(request, _('Ваш профиль успешно обновлен!'))
            return redirect('cards:all')
        else:
            messages.error(request, _('Пожалуйста, исправьте ошибки.'))
    else:
        user_form = UserForm(instance=request.user)
        confectioner_form = ConfectionerForm(instance=request.user.confectioner)
    return render(request, 'confectioners/confectioner.html', {
        'user_form': user_form,
        'confectioner_form': confectioner_form
    })
