from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.shortcuts import render, redirect
from apps.mobile_api.models import UserProfile, Event, Transaction, UserGroup
from django.urls import reverse
from libs.slack_webhook import SlackWebHook
from ..constant import TAB_USER_PROFILE, TAB_USER_MANAGEMENT, TAB_EXPENSE_MANAGEMENT


@login_required()
def paid_transaction(request, **kwargs):
    data_update = request.POST
    transaction_id = data_update.get("transaction_id")
    redirect_url = data_update.get("redirect_url")
    transaction = Transaction.objects.get(id=transaction_id,status=Transaction.PENDING)
    transaction.paid_user_pending()
    return redirect(redirect_url)

@login_required()
def event_detail(request, **kwargs):
    group_id = kwargs.get("group_id")
    event_id = kwargs.get("event_id")
    event = Event()
    event.group_id = group_id
    group = UserGroup.objects.get(id=group_id)
    if event_id:
        try:
            event = Event.objects.get(id=event_id)
        except Exception, e:
            pass
    if request.method == "POST" and not event_id:
        data_update = request.POST
        has_error = False
        member_joins = data_update.getlist("member_joins")
        if not member_joins:
            has_error = True
            event.member_join_error_message = "Member join empty"
        for member_join in member_joins:
            if not group.members.filter(id=member_join).exists():
                has_error = True
                event.member_join_error_message = "User not belong with group"
        event.member_join = ",".join(member_joins)
        event.description = data_update.get("description")
        if not event.description:
            has_error = True
            event.description_error_message = "Description not empty"
        event.event_type = int(data_update.get("event_type"))
        if event.event_type not in [Event.TYPE_1, Event.TYPE_2]:
            has_error = True
            event.event_type_error_message = "Event invalid"
        event.amount = data_update.get("amount")
        event.source_money = int(data_update.get("source_money"))
        if event.event_type not in [Event.SOURCE_INDIVIDUAL, Event.SOURCE_GROUP]:
            has_error = True
            event.source_money_error_message = "Source money invalid"
        event.amount = data_update.get("amount")
        try:
            event.amount = int(event.amount)
        except Exception, e:
            has_error = True
            event.amount_error_message = "Amount must be integer"
        if not has_error:
            event.save()
            event.collecting_money()
            return redirect(reverse('admin_v1:edit_event', kwargs={"group_id": group_id, "event_id": event.id}))
    header_texts = ["Payer", "Description", "Amount", "Status", "Paid at"]
    context_data = {
        "group_id": group_id,
        "event": event,
        "event_types": Event.EVENT_TYPES,
        "event_source_types": Event.SOURCE_TYPES,
        "event_transactions": event.transactions.all().order_by("-modified_at"),
        "header_texts": header_texts
    }
    return render(request, 'user_group/event_detail.html', context=context_data)

class UserGroupDetailView(ListView):
    model = UserProfile
    template_name = 'user_group/group_detail.html'
    context_object_name = 'events'
    paginate_by = 10
    header_text = ["No", "Description", "Event Type", "Source Money", "Amount",  "Status"]
    page_size_list = [10, 20, 30]
    parent_tab = TAB_EXPENSE_MANAGEMENT

    def get_queryset(self):
        group_id = self.kwargs.get("group_id")
        filter_query = Q(group_id=group_id)
        account_list = Event.objects.filter(filter_query).order_by("-id")
        return account_list

    def get_context_data(self, **kwargs):
        context = super(UserGroupDetailView, self).get_context_data(**kwargs)
        context['header_texts'] = self.header_text
        context['page_size_list'] = self.page_size_list
        context['paginate_by'] = int(self.get_paginate_by())
        context['active_tab'] = int(self.kwargs.get("group_id"))
        context['group_id'] = int(self.kwargs.get("group_id"))
        context['group'] = UserGroup.objects.get(id=self.kwargs.get("group_id"))
        context['parent_tab'] = self.parent_tab
        return context

    def get_paginate_by(self, queryset=None):
        return self.request.GET.get('paginate_by', self.paginate_by)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserGroupDetailView, self).dispatch(*args, **kwargs)