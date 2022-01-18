import csv


def create_csv(objects):
    for column_object in objects:
        if column_object[0] == 'csrfmiddlewaretoken':
            continue
