# Authorization with Guardian and Django-Tastypie
# 
# modified from airtonix
# https://gist.github.com/airtonix/54764553

from tastypie.authorization import DjangoAuthorization
from tastypie.exceptions import Unauthorized

from guardian.core import ObjectPermissionChecker

import logging
logger = logging.getLogger(__name__)


class GuardianAuthorization( DjangoAuthorization ):

    def base_check(self, object_list, bundle):
        klass = self.base_checks(bundle.request, object_list.model)
        if klass is False:
            raise Unauthorized("You are not allowed to access that resource.")
        return True

    def item_check(self, object_list, bundle, permission):
        if not self.base_check(object_list, bundle):
            raise Unauthorized("You are not allowed to access that resource.")
        checker = ObjectPermissionChecker(bundle.request.user)
        if not checker.has_perm(permission, bundle.obj):
            raise Unauthorized("You are not allowed to access that resource.")
        return True

    def list_check(self, object_list, bundle, permission):
        if not self.base_check(object_list, bundle):
            raise Unauthorized("You are not allowed to access that resource.")
        checker = ObjectPermissionChecker( bundle.request.user )
        read_list = []
        for obj in object_list:
            if checker.has_perm( permission, obj ):
                read_list.append( obj )
        return read_list

    # List Checks
    def create_list(self, object_list, bundle):
        klass = self.base_checks(bundle.request, object_list.model)
        permission = 'add_%s' % (klass._meta.module_name)
        return self.list_check( object_list, bundle, permission )

    def read_list(self, object_list, bundle):
        klass = self.base_checks(bundle.request, object_list.model)
        permission = 'view_%s' % (klass._meta.module_name)
        return self.list_check( object_list, bundle, permission )

    def update_list(self, object_list, bundle):
        klass = self.base_checks(bundle.request, object_list.model)
        permission = 'change_%s' % (klass._meta.module_name)
        return self.list_check( object_list, bundle, permission )

    def delete_list(self, object_list, bundle):
        klass = self.base_checks(bundle.request, object_list.model)
        permission = 'delete_%s' % (klass._meta.module_name)
        return self.list_check( object_list, bundle, permission )

    # Item Checks
    def create_detail(self, object_list, bundle):
        klass = self.base_checks(bundle.request, bundle.obj.__class__)
        permission = 'add_%s' % (klass._meta.module_name)
        return self.item_check( object_list, bundle, permission )

    def read_detail(self, object_list, bundle):
        klass = self.base_checks(bundle.request, bundle.obj.__class__)
        permission = 'view_%s' % (klass._meta.module_name)
        return self.item_check( object_list, bundle, permission )

    def update_detail(self, object_list, bundle):
        klass = self.base_checks(bundle.request, bundle.obj.__class__)
        permission = 'change_%s' % (klass._meta.module_name)
        return self.item_check( object_list, bundle, permission )

    def delete_detail(self, object_list, bundle):
        klass = self.base_checks(bundle.request, bundle.obj.__class__)
        permission = 'delete_%s' % (klass._meta.module_name)
        return self.item_check( object_list, bundle, permission )

