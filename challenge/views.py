import os

from django.core.serializers import serialize
from django.shortcuts import redirect
from django.views.generic import CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .owner import OwnerListView, OwnerUpdateView, OwnerDeleteView, parse_instructions, save_schema


class SchemaCreateView(LoginRequiredMixin, CreateView):
    model = Schema
    fields = ['name', 'separator', 'string']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['names'] = serialize("json", Schema.objects.filter(owner=self.request.user))
        context['separator'] = None
        context['string'] = None
        context['objects'] = None
        return context

    def post(self, request, **kwargs):
        owner = request.user
        items = request.POST

        save_schema(items, owner)

        return redirect('fakecsv:main')


class SchemaListView(OwnerListView):
    model = Schema


class SchemaDeleteView(OwnerDeleteView):
    model = Schema

    def post(self, request, *args, **kwargs):
        path = r'csv_files\\' + str(self.request.user.id) + '/' + f'{self.get_object().id}.csv'
        os.remove(path)
        return super().post(request)


class SchemaUpdateView(OwnerUpdateView):
    model = Schema
    fields = ['name', 'separator', 'string']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = str(self.get_object().name)
        context['separator'] = self.get_object().separator
        context['string'] = self.get_object().string
        objects = parse_instructions(self.get_object().read_instructions)
        context['objects'] = objects
        context['names'] = serialize("json", Schema.objects.filter(owner=self.request.user))
        return context

    def post(self, request, **kwargs):
        owner = request.user
        items = request.POST

        save_schema(items, owner, schema=self.get_object(), update=True)

        return redirect('fakecsv:main')
