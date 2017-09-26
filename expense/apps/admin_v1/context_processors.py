from .constant import *
from apps.mobile_api.models import UserGroup


def global_settings(request):
    tab_expense = {
        "name": TAB_EXPENSE_MANAGEMENT,
        "childs": []
    }
    for user_group in UserGroup.objects.all():
        tab_expense["childs"].append(
            [user_group.id, user_group.name, "admin_v1:user_group_detail", {"group_id": user_group.id}]
        )
    tab_constant = [
        {
            "name": TAB_USER_MANAGEMENT,
            "childs": [
                [TAB_USER_PROFILE, "User Profile", "admin_v1:profile_list"]
            ]
        },
        tab_expense
    ]

    return {
        'TAB_CONSTANTS': tab_constant,
    }
