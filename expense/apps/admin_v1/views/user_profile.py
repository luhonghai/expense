from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q

from libs.decorators import superuser_only
from apps.mobile_api.models import UserProfile, Transaction
from ..constant import TAB_USER_PROFILE, TAB_USER_MANAGEMENT


class ProfileList(ListView):
    model = UserProfile
    template_name = 'user_profile/profile_list.html'
    context_object_name = 'profiles'
    paginate_by = 15
    header_text = ["No",  "Name", "Phone Number", "Balance", "Action"]
    page_size_list = [15, 20, 25]
    active_tab = TAB_USER_PROFILE
    parent_tab = TAB_USER_MANAGEMENT

    def get_queryset(self):
        filter_query = Q()
        try:
            search_key = self.request.GET.get('search_key',)
        except KeyError:
            search_key = None
        if search_key:
            filter_query = filter_query & (Q(email__icontains=search_key) |
                                           Q(name__icontains=search_key) |
                                           Q(phone_number__icontains=search_key)
                                           )
        account_list = UserProfile.objects.filter(filter_query).order_by("-id")
        return account_list

    def get_context_data(self, **kwargs):
        context = super(ProfileList, self).get_context_data(**kwargs)
        context['header_texts'] = self.header_text
        context['page_size_list'] = self.page_size_list
        context['paginate_by'] = int(self.get_paginate_by())
        context['active_tab'] = self.active_tab
        context['parent_tab'] = self.parent_tab
        return context

    def get_paginate_by(self, queryset=None):
        return self.request.GET.get('paginate_by', self.paginate_by)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileList, self).dispatch(*args, **kwargs)

    @method_decorator(superuser_only)
    def post(self, request, *args, **kwargs):
        profile = UserProfile.objects.get(id=request.POST.get("profile_id"))
        try:
            amount = int(request.POST.get("amount"))
            profile.recharge_money(amount=amount)
        except Exception, e:
            pass
        return redirect(reverse('admin_v1:profile_list'))

class ProfileDetailView(ListView):
    model = UserProfile
    template_name = 'user_profile/profile_detail.html'
    context_object_name = 'transactions'
    paginate_by = 15
    header_text = ["No", "Amount", "Description", "Status", "Created at"]
    page_size_list = [15, 20, 25]
    active_tab = TAB_USER_PROFILE
    parent_tab = TAB_USER_MANAGEMENT

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        filter_query = Q(user_id=user_id)
        account_list = Transaction.objects.filter(filter_query).order_by("-modified_at")
        return account_list

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        context['header_texts'] = self.header_text
        context['page_size_list'] = self.page_size_list
        context['paginate_by'] = int(self.get_paginate_by())
        context['active_tab'] = self.active_tab
        context['parent_tab'] = self.parent_tab
        context['user_id'] = self.kwargs.get("user_id")
        context['user_profile'] = UserProfile.objects.get(user_id=self.kwargs.get("user_id"))
        return context

    def get_paginate_by(self, queryset=None):
        return self.request.GET.get('paginate_by', self.paginate_by)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileDetailView, self).dispatch(*args, **kwargs)
