from django.shortcuts import render
from django.views.generic import View


class OrgListView(View):
    """课程机构"""
    def get(self, request, *args, **kwargs):
        """显示"""
        return render(request, 'org-list.html')
