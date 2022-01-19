import os

import csv
from faker import Faker

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, DeleteView

from .models import *


def get_model(key):
    models_dict = {'1': FullName, '2': Job, '3': Email, '4': DomainName,
                   '5': PhoneNumber, '6': CompanyName, '7': Text, '8': Integer, '9': Address, '10': Date}
    return models_dict[key]


def get_separator(key):
    separator_dict = {'1': ',', '2': ';', '3': '\t', '4': ' ', '5': '|'}
    return separator_dict[key]


class OwnerListView(ListView):
    """ListView sub-class for owned objects"""

    def get_queryset(self):
        qs = super(OwnerListView, self).get_queryset()
        if self.request.user.is_authenticated:
            qs = super(OwnerListView, self).get_queryset()
            return qs.filter(owner=self.request.user)
        else:
            return qs.none()


class OwnerUpdateView(UpdateView, LoginRequiredMixin):
    """
        Sub-class the UpdateView to pass the request to the form and limit the
        queryset to the requesting user.
        """

    def get_queryset(self):
        print('update get_queryset called')
        """ Limit a User to only modifying their own data. """
        qs = super(OwnerUpdateView, self).get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerDeleteView(LoginRequiredMixin, DeleteView):
    """
    Sub-class the DeleteView to restrict a User from deleting other
    user's data.
    """

    def get_queryset(self):
        print('delete get_queryset called')
        qs = super(OwnerDeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)


def parse_instructions(instructions):
    instructions = instructions.split(';')
    res = []
    r_min, r_max = '', ''
    if type(instructions) is list:
        for instruction in instructions:
            ins = instruction.split(',')
            obj = get_model(ins[0]).objects.get(id=ins[1])
            if ins[0] == '7' or ins[0] == '8':
                r_min, r_max = obj.min_range, obj.max_range
            res.append([get_model(ins[0]).objects.get(id=ins[1]).name, ins[0], r_min, r_max])
            r_min, r_max = '', ''
    else:
        ins = instructions.split(',')
        obj = get_model(ins[0]).objects.get(id=ins[1])
        if ins[0] == '8' or ins[0] == '9':
            r_min, r_max = obj.min_range, obj.max_range
        res.append([obj.get(id=ins[1]).name, ins[0], r_min, r_max])
    return res


def save_schema(items, owner, schema=None, update=False):
    # checking if we are creating or updating schema
    if not schema:
        schema = Schema(name=items.get('name'), separator=items.get('separator'),
                        string=items.get('string'),
                        owner=owner, read_instructions='', modified_date=str(datetime.date.today()))
    else:
        schema.read_instructions = ''
        schema.name = items.get('name')
        schema.separator = items.get('separator')
        schema.string = items.get('string')
        schema.modified_date = str(datetime.date.today())

    # getting values in different lists
    names = items.getlist('col-name')
    types = items.getlist('col-select')
    min_values = items.getlist('min-value')
    max_values = items.getlist('max-value')

    for i in range(int(items.get('cols'))):  # Checking type to know whether program need to add min and max or not
        if types[i] == '7' or types[i] == '8':
            item, created = get_model(types[i]).objects.get_or_create(name=names[i],
                                                                      min_range=int(min_values[i]),
                                                                      max_range=int(max_values[i]))
        else:
            item, created = get_model(types[i]).objects.get_or_create(name=names[i])
        item.save()
        if schema.read_instructions:  # Adding read instructions to Schema (mentioned in Schema model)
            schema.read_instructions += ';'
        schema.read_instructions += f'{types[i]},{item.id}'

    path = r'csv_files\\' + str(owner.id)
    schema.file = ''
    schema.save()
    schema.file = os.path.join(path, f'{schema.id}.csv')
    schema.save()
    path = 'media/' + path
    # checking if we need to create new csv of not
    if not update:
        if not os.path.isdir(path):
            os.mkdir(path=path)
        open(os.path.join(path, f'{schema.id}.csv'), 'x').close()


def gen_fake_csv(owner, rows):
    schemas = Schema.objects.filter(owner=owner)
    fake = Faker()

    fake_dict = {'1': fake.name, '2': fake.job, '3': fake.email, '4': fake.domain_name,
                 '5': fake.phone_number, '6': fake.company, '7': fake.paragraph,
                 '8': fake.random_int, '9': fake.address, '10': fake.date}
    for schema in schemas:
        csv_objects = parse_instructions(schema.read_instructions)
        path = r'media\\csv_files/' + str(owner.id)

        with open(os.path.join(path, f'{schema.name}.csv'), 'w+') as f:
            writer = csv.writer(f, delimiter=get_separator(schema.separator))
            writer.writerow([i[0] for i in csv_objects])
            for _ in range(rows):
                data = [fake_dict[i[1]]() if (i[1] not in ["7", "8"]) else
                        fake_dict[i[1]](min=i[2], max=i[3]) if i[1] != '7'
                        else fake_dict[i[1]](fake.random_int(i[2], i[3]), False)
                        for i in csv_objects]
                writer.writerow(data)
        schema.created_date = str(datetime.date.today())


