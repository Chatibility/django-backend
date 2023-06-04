from rest_framework import filters 

class IsOwner(filters.BaseFilterBackend): 

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(user=request.user)