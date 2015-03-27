from django.db.models.fields import *

__author__ = 'wachs'

from django.db import models

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def get_field_value(model_object, property):
    last_obj = model_object
    for prop_chain in property.split('__'):
        last_obj = last_obj.__getattribute__(prop_chain)
    return last_obj


class Entity():
    def __init__(self, model, insertion_list, lookup_key_names):
        self.model = model
        self.lookup_key_names = lookup_key_names
        self.insertion_list = insertion_list
        self.do_insertions()

    def check_data_exists(self, filled_model):

        if type(self.lookup_key_names) is not list:
            k = str(self.lookup_key_names)
            v = filled_model.__getattribute__(str(self.lookup_key_names))
            print("\tChecking with " + bcolors.OKBLUE + k + "='" + v + "'" + bcolors.ENDC),
            kw = {k: v}
        else:
            kw = {}
            print("\tChecking with: "),
            last = len(self.lookup_key_names)-1
            for k in self.lookup_key_names:
                v = get_field_value(filled_model, k)
                kw[k] = v
                print(bcolors.OKBLUE + k + "='" + v + "'" + bcolors.ENDC + ("," if last > 0 else "")),
                last -= 1

        exists = self.model.objects.filter(**kw).exists()
        print (bcolors.OKGREEN + "[EXISTS]" if exists else bcolors.FAIL + "[NOT EXISTS]" + bcolors.ENDC)

        return exists

    def do_insertions(self):
        print("\nChecking the Presense of data of entity " + bcolors.OKBLUE + self.model._meta.object_name + bcolors.ENDC + " on database")
        if hasattr(self.insertion_list, '__iter__'):
            for obj in self.insertion_list:
                if not self.check_data_exists(obj):
                    self.insert(obj)
        else:
            if not self.check_data_exists(self.insertion_list):
                    self.insert(self.insertion_list)

    def insert(self, filled_model):
        entity = self.model()
        fields = filled_model._meta.fields
        print(bcolors.WARNING + "\t\tInserting into table " + bcolors.OKBLUE + entity._meta.db_table + bcolors.ENDC),
        for f in fields:
            if type(f) is models.ForeignKey:
                first_name = f.name.split('_')[0]
                foreign_model = type(filled_model.__getattribute__(first_name))

                foreign_key = [s for s in self.lookup_key_names if s.startswith(first_name+'__')]
                prop_value_key = foreign_key[0] if len(foreign_key) > 0 else None
                foreign_key = foreign_key[0].split('__')[1] if len(foreign_key) > 0 else None

                if foreign_key:
                    results = foreign_model.objects.filter(**{foreign_key: get_field_value(filled_model, prop_value_key)})
                    if len(results) == 1:
                        entity.__setattr__(f.name, results.first())
                    else:
                        print(bcolors.FAIL + "\t[ERROR] FK NOT FOUND!" + bcolors.ENDC)
                        return
            else:
                entity.__setattr__(f.name, filled_model.__getattribute__(f.name))
        try:
            entity.save()
            print(bcolors.OKGREEN + "\t[INSERTED]")
        except Exception as e:
            print(bcolors.FAIL + "\t[ERROR]")
            print("\t\t" + str(e))
        finally:
            print(bcolors.ENDC),


