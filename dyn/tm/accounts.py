"""This module contains interfaces for all Account management features of the
REST API
"""
import logging
import dyn.tm.session
from dyn.tm.errors import DynectInvalidArgumentError

__author__ = 'jnappi'
__all__ = ['get_updateusers', 'get_users', 'get_permissions_groups',
           'get_contacts', 'get_notifiers', 'UpdateUser', 'User',
           'PermissionsGroup', 'UserZone', 'Notifier', 'Contact']

session = dyn.tm.session.session


def get_updateusers(search=None):
    """Return a ``list`` of :class:`UpdateUser` objects. If *search* is
    specified, then only :class:`UpdateUsers` who match those search criteria
    will be returned in the list. Otherwise, all :class:`UpdateUsers`'s will be
    returned.

    :param search: A ``dict`` of search criteria. Key's in this ``dict`` much
        map to an attribute a :class:`UpdateUsers` instance and the value mapped
        to by that key will be used as the search criteria for that key when
        searching.
    :return: a ``list`` of :class:`UpdateUser` objects
    """
    uri = '/UpdateUser/'
    api_args = {'detail': 'Y'}
    response = session().execute(uri, 'GET', api_args)
    update_users = []
    for user in response['data']:
        update_users.append(UpdateUser(api=False, **user))
    if search is not None:
        original = update_users
        update_users = []
        for uu in original:
            for key, val in search.items():
                if hasattr(uu, key) and getattr(uu, key) == val:
                    update_users.append(uu)
    return update_users


def get_users(search=None):
    """Return a ``list`` of :class:`User` objects. If *search* is specified,
    then only users who match those search parameters will be returned in the
    list. Otherwise, all :class:`User`'s will be returned.

    :param search: A ``dict`` of search criteria. Key's in this ``dict`` much
        map to an attribute a :class:`User` instance and the value mapped to by
        that key will be used as the search criteria for that key when
        searching.
    :return: a ``list`` of :class:`User` objects
    """
    uri = '/User/'
    api_args = {'detail': 'Y'}
    if search is not None:
        search_string = ''
        for key, val in search.items():
            if search_string != '':
                ' AND '.join([search_string, '{}: "{}"'.format(key, val)])
            else:
                search_string = '{}: "{}"'.format(key, val)
        api_args['search'] = search_string
    response = session().execute(uri, 'GET', api_args)
    users = []
    for user in response['data']:
        user_name = None
        if 'user_name' in user:
            user_name = user['user_name']
            del user['user_name']
        users.append(User(user_name, api=False, **user))
    return users


def get_permissions_groups(search=None):
    """Return a ``list`` of :class:`PermissionGroup` objects. If *search* is
    specified, then only :class:`PermissionGroup`'s that match those search
    criteria will be returned in the list. Otherwise, all
    :class:`PermissionGroup`'s will be returned.

    :param search: A ``dict`` of search criteria. Key's in this ``dict`` much
        map to an attribute a :class:`PermissionGroup` instance and the value
        mapped to by that key will be used as the search criteria for that key
        when searching.
    :return: a ``list`` of :class:`PermissionGroup` objects"""
    uri = '/PermissionGroup/'
    api_args = {'detail': 'Y'}
    response = session().execute(uri, 'GET', api_args)
    groups = []
    for group in response['data']:
        groups.append(PermissionsGroup(None, api=False, **group))
    if search is not None:
        original = groups
        groups = []
        for group in original:
            for key, val in search.items():
                if hasattr(group, key) and getattr(group, key) == val:
                    groups.append(group)
    return groups


def get_contacts(search=None):
    """Return a ``list`` of :class:`Contact` objects. If *search* is specified,
    then only :class:`Contact`'s who match those search criteria will be
    returned in the list. Otherwise, all :class:`Contact`'s will be returned.

    :param search: A ``dict`` of search criteria. Key's in this ``dict`` much
        map to an attribute a :class:`Contact` instance and the value mapped to
        by that key will be used as the search criteria for that key when
        searching.
    :return: a ``list`` of :class:`Contact` objects"""
    uri = '/Contact/'
    api_args = {'detail': 'Y'}
    response = session().execute(uri, 'GET', api_args)
    contacts = []
    for contact in response['data']:
        if 'nickname' in contact:
            contact['_nickname'] = contact['nickname']
            del contact['nickname']
        contacts.append(Contact(None, api=False, **contact))
    if search is not None:
        original = contacts
        contacts = []
        for contact in original:
            for key, val in search.items():
                if hasattr(contact, key) and getattr(contact, key) == val:
                    contacts.append(contact)
    return contacts


def get_notifiers(search=None):
    """Return a ``list`` of :class:`Notifier` objects. If *search* is specified,
    then only :class:`Notifier`'s who match those search criteria will be
    returned in the list. Otherwise, all :class:`Notifier`'s will be returned.

    :param search: A ``dict`` of search criteria. Key's in this ``dict`` much
        map to an attribute a :class:`Notifier` instance and the value mapped to
        by that key will be used as the search criteria for that key when
        searching.
    :return: a ``list`` of :class:`Notifier` objects"""
    uri = '/Notifier/'
    api_args = {'detail': 'Y'}
    response = session().execute(uri, 'GET', api_args)
    notifiers = []
    for notifier in response['data']:
        notifiers.append(Notifier(None, api=False, **notifier))
    if search is not None:
        original = notifiers
        notifiers = []
        for notifier in original:
            for key, val in search.items():
                if hasattr(notifier, key) and getattr(notifier, key) == val:
                    notifiers.append(notifier)
    return notifiers


class UpdateUser(object):
    """:class:`UpdateUser` type objects are a special form of a :class:`User` 
    which are tied to a specific Dynamic DNS services.
    """
    def __init__(self, *args, **kwargs):
        """Create an :class:`UpdateUser` object

        :param user_name: the Username this :class:`UpdateUser` uses or will
            use to log in to the DynECT System. A :class:`UpdateUser`'s
            `user_name` is required for both creating and getting
            :class:`UpdateUser`'s.
        :param nickname: When creating a new :class:`UpdateUser` on the DynECT
            System, this `nickname` will be the System nickname for this
            :class:`UpdateUser`
        :param password: When creating a new :class:`UpdateUser` on the DynECT
            System, this `password` will be the password this
            :class:`UpdateUser` uses to log into the System
        """
        super(UpdateUser, self).__init__()
        self.logger = logging.getLogger(str(self.__class__))
        self.uri = '/UpdateUser/'
        self._password = self._status = self._user_name = self._nickname = None
        if 'api' in kwargs:
            good_args = ('user_name', 'status', 'password')
            for key, val in kwargs.items():
                if key in good_args:
                    setattr(self, '_' + key, val)
            self.uri = '/UpdateUser/{}/'.format(self._user_name)
        elif len(args) + len(kwargs) == 1:
            self._get(*args, **kwargs)
        else:
            self._post(*args, **kwargs)

    def _post(self, nickname, password):
        """Create a new :class:`UpdateUser` on the DynECT System"""
        self._nickname = nickname
        self._password = password
        uri = '/UpdateUser/'
        api_args = {'nickname': self._nickname,
                    'password': self._password}
        response = session().execute(uri, 'POST', api_args)
        self._build(response['data'])
        self.uri = '/UpdateUser/{}/'.format(self._user_name)

    def _get(self, user_name):
        """Get an existing :class:`UpdateUser` from the DynECT System"""
        self._user_name = user_name
        api_args = {}
        self.uri = '/UpdateUser/{}/'.format(self._user_name)
        response = session().execute(self.uri, 'GET', api_args)
        self._build(response['data'])

    def _build(self, data):
        for key, val in data.items():
            setattr(self, '_' + key, val)

    def _update(self, api_args):
        response = session().execute(self.uri, 'PUT', api_args)
        self._build(response['data'])

    @property
    def user_name(self):
        """This :class:`UpdateUser`'s `user_name`. An :class:`UpdateUser`'s
        user_name is a read-only property which can not be updated after the
        :class:`UpdateUser` has been created.
        """
        return self._user_name
    @user_name.setter
    def user_name(self, value):
        pass

    @property
    def nickname(self):
        """This :class:`UpdateUser`s `nickname`. An :class:`UpdateUser`'s
        `nickname` is a read-only property which can not be updated after the
        :class:`UpdateUser` has been created.
        """
        return self._nickname
    @nickname.setter
    def nickname(self, value):
        pass

    @property
    def status(self):
        """The current `status` of an :class:`UpdateUser` will be one of either
        'active' or 'blocked'. Blocked :class:`UpdateUser`'s are unable to log
        into the DynECT System, where active :class:`UpdateUser`'s are.
        """
        return self._status
    @status.setter
    def status(self, value):
        pass
    
    @property
    def password(self):
        """The current `password` for this :class:`UpdateUser`. An
        :class:`UpdateUser`'s `password` may be reassigned."""
        if self._password is None or self._password == u'':
            self._get(self._user_name)
        return self._password
    @password.setter
    def password(self, new_password):
        """Update this :class:`UpdateUser`'s password to be the provided 
        password

        :param new_password: The new password to use
        """
        self._password = new_password
        api_args = {'password': self._password}
        self._update(api_args)

    def block(self):
        """Set the status of this :class:`UpdateUser` to 'blocked'. This will 
        prevent this :class:`UpdateUser` from logging in until they are 
        explicitly unblocked.
        """
        api_args = {'block': True}
        self._update(api_args)

    def unblock(self):
        """Set the status of this :class:`UpdateUser` to 'active'. This will
        re-enable this :class:`UpdateUser` to be able to login if they were
        previously blocked.
        """
        api_args = {'unblock': True}
        self._update(api_args)

    def sync_password(self):
        """Pull in this :class:`UpdateUser` current password from the DynECT
        System, in the unlikely event that this :class:`UpdateUser` object's
        password may have gotten out of sync
        """
        api_args = {'user_name': self._user_name}
        self._update(api_args)

    def delete(self):
        """Delete this :class:`UpdateUser` from the DynECT System. It is
        important to note that this operation may not be undone.
        """
        api_args = {}
        session().execute(self.uri, 'DELETE', api_args)


class User(object):
    """DynECT System User object"""
    def __init__(self, user_name, *args, **kwargs):
        """Create a new :class:`User` object

        :param user_name: This :class:`User`'s system username; used for logging
            into the system
        :param password: Password for this :class:`User` account
        :param email: This :class:`User`'s Email address
        :param first_name: This :class:`User`'s first name
        :param last_name: This :class:`User`'s last name
        :param nickname: The nickname for the `Contact` associated with this
            :class:`User`
        :param organization: This :class:`User`'s organization
        :param phone: This :class:`User`'s phone number. Can be of the form: (0)
            ( country-code ) ( local number ) ( extension ) Only the
            country-code (1-3 digits) and local number (at least 7 digits) are
            required. The extension can be up to 4 digits. Any non-digits are
            ignored.
        :param address: This :class:`User`'s street address
        :param address2: This :class:`User`'s street address, line 2
        :param city: This :class:`User`'s city, part of the user's address
        :param country: This :class:`User`'s country, part of the user's address
        :param fax: This :class:`User`'s fax number
        :param notify_email: Email address where this :class:`User` should
            receive notifications
        :param pager_email: Email address where this :class:`User` should
            receive messages destined for a pager
        :param post_code: Zip code or Postal code
        :param group_name: A list of permission groups this :class:`User`
            belongs to
        :param permission: A list of permissions assigned to this :class:`User`
        :param zone: A list of zones where this :class:`User`'s permissions
            apply
        :param forbid: A list of forbidden permissions for this :class:`User`
        :param status: Current status of this :class:`User`
        :param website: This :class:`User`'s website
        """
        super(User, self).__init__()
        self.logger = logging.getLogger(str(self.__class__))
        self._user_name = user_name
        self.uri = '/User/{}/'.format(self._user_name)
        self._password = self._email = self._first_name = self._last_name = None
        self._nickname = self._organization = self._phone = self._address = None
        self._address_2 = self._city = self._country = self._fax = None
        self._notify_email = self._pager_email = self._post_code = None
        self._group_name = self._permission = self._zone = self._forbid = None
        self._status = self._website = None
        self.permissions = []
        self.permission_groups = []
        self.groups = []
        if 'api' in kwargs:
            del kwargs['api']
            for key, val in kwargs.items():
                if key != '_user_name':
                    setattr(self, '_' + key, val)
                else:
                    setattr(self, key, val)
        elif len(args) == 0 and len(kwargs) == 0:
            self._get()
        else:
            self._post(*args, **kwargs)

    def _post(self, password, email, first_name, last_name, nickname,
              organization, phone, address=None, address_2=None, city=None,
              country=None, fax=None, notify_email=None, pager_email=None,
              post_code=None, group_name=None, permission=None, zone=None,
              forbid=None, status=None, website=None):
        """Create a new :class:`User` object on the DynECT System"""
        self._password = password
        self._email = email
        self._first_name = first_name
        self._last_name = last_name
        self._nickname = nickname
        self._organization = organization
        self._phone = phone
        self._address = address
        self._address_2 = address_2
        self._city = city
        self._country = country
        self._fax = fax
        self._notify_email = notify_email
        self._pager_email = pager_email
        self._post_code = post_code
        self._group_name = group_name
        self._permission = permission
        self._zone = zone
        self._forbid = forbid
        self._status = status
        self._website = website
        response = session().execute(self.uri, 'POST', self)
        for key, val in response['data'].items():
            setattr(self, '_' + key, val)

    def _get(self):
        """Get an existing :class:`User` object from the DynECT System"""
        api_args = {}
        response = session().execute(self.uri, 'GET', api_args)
        for key, val in response['data'].items():
            setattr(self, '_' + key, val)

    def _update(self, api_args):
        response = session().execute(self.uri, 'PUT', api_args)
        for key, val in response['data'].items():
            setattr(self, '_' + key, val)

    @property
    def user_name(self):
        """A :class:`User`'s user_name is a read-only property"""
        return self._user_name
    @user_name.setter
    def user_name(self, value):
        pass

    @property
    def status(self):
        """A :class:`User`'s status is a read-only property. To change you must
        use the :meth:`block`/:meth:`unblock` methods
        """
        return self._status
    @status.setter
    def status(self, value):
        pass

    @property
    def email(self):
        """This :class:`User`'s Email address"""
        return self._email
    @email.setter
    def email(self, value):
        self._email = value
        api_args = {'email': self._email}
        self._update(api_args)

    @property
    def first_name(self):
        """This :class:`User`'s first name"""
        return self._first_name
    @first_name.setter
    def first_name(self, value):
        self._first_name = value
        api_args = {'first_name': self._first_name}
        self._update(api_args)

    @property
    def last_name(self):
        """This :class:`User`'s last name"""
        return self._last_name
    @last_name.setter
    def last_name(self, value):
        self._last_name = value
        api_args = {'last_name': self._last_name}
        self._update(api_args)

    @property
    def nickname(self):
        """The nickname for the `Contact` associated with this :class:`User`"""
        return self._nickname
    @nickname.setter
    def nickname(self, value):
        self._nickname = value
        api_args = {'nickname': self._nickname}
        self._update(api_args)

    @property
    def organization(self):
        """This :class:`User`'s organization"""
        return self._organization
    @organization.setter
    def organization(self, value):
        self._organization = value
        api_args = {'organization': self._organization}
        self._update(api_args)

    @property
    def phone(self):
        """This :class:`User`'s phone number. Can be of the form: (0)
        ( country-code ) ( local number ) ( extension ) Only the country-code
        (1-3 digits) and local number (at least 7 digits) are required. The
        extension can be up to 4 digits. Any non-digits are ignored.
        """
        return self._phone
    @phone.setter
    def phone(self, value):
        self._phone = value
        api_args = {'phone': self._phone}
        self._update(api_args)

    @property
    def address(self):
        """This :class:`User`'s street address"""
        return self._address
    @address.setter
    def address(self, value):
        self._address = value
        api_args = {'address': self._address}
        self._update(api_args)

    @property
    def address_2(self):
        """This :class:`User`'s street address, line 2"""
        return self._address_2
    @address_2.setter
    def address_2(self, value):
        self._address_2 = value
        api_args = {'address_2': self._address_2}
        self._update(api_args)

    @property
    def city(self):
        """This :class:`User`'s city, part of the user's address"""
        return self._city
    @city.setter
    def city(self, value):
        self._city = value
        api_args = {'city': self._city}
        self._update(api_args)

    @property
    def country(self):
        """This :class:`User`'s country, part of the user's address"""
        return self._country
    @country.setter
    def country(self, value):
        self._country = value
        api_args = {'country': self._country}
        self._update(api_args)

    @property
    def fax(self):
        """This :class:`User`'s fax number"""
        return self._fax
    @fax.setter
    def fax(self, value):
        self._fax = value
        api_args = {'fax': self._fax}
        self._update(api_args)

    @property
    def notify_email(self):
        """Email address where this :class:`User` should receive notifications
        """
        return self._notify_email
    @notify_email.setter
    def notify_email(self, value):
        self._notify_email = value
        api_args = {'notify_email': self._notify_email}
        self._update(api_args)

    @property
    def pager_email(self):
        """Email address where this :class:`User` should receive messages
        destined for a pager
        """
        return self._pager_email
    @pager_email.setter
    def pager_email(self, value):
        self._pager_email = value
        api_args = {'pager_email': self._pager_email}
        self._update(api_args)

    @property
    def post_code(self):
        """This :class:`User`'s postal code, part of the user's address"""
        return self._post_code
    @post_code.setter
    def post_code(self, value):
        self._post_code = value
        api_args = {'post_code': self._post_code}
        self._update(api_args)

    @property
    def group_name(self):
        """A list of permission groups this :class:`User` belongs to"""
        return self._group_name
    @group_name.setter
    def group_name(self, value):
        self._group_name = value
        api_args = {'group_name': self._group_name}
        self._update(api_args)

    @property
    def permission(self):
        """A list of permissions assigned to this :class:`User`"""
        return self._permission
    @permission.setter
    def permission(self, value):
        self._permission = value
        api_args = {'permission': self._permission}
        self._update(api_args)

    @property
    def zone(self):
        """A list of zones where this :class:`User`'s permissions apply"""
        return self._zone
    @zone.setter
    def zone(self, value):
        self._zone = value
        api_args = {'zone': self._zone}
        self._update(api_args)

    @property
    def forbid(self):
        """A list of forbidden permissions for this :class:`User`"""
        return self._forbid
    @forbid.setter
    def forbid(self, value):
        """Apply a new list of forbidden permissions for the :class:`User`"""
        self._forbid = value
        api_args = {'forbid': self._forbid}
        self._update(api_args)

    @property
    def website(self):
        """This :class:`User`'s website"""
        return self._website
    @website.setter
    def website(self, value):
        self._website = value
        api_args = {'website': self._website}
        self._update(api_args)

    def block(self):
        """Blocks this :class:`User` from logging in"""
        api_args = {'block': 'True'}
        uri = '/User/{}/'.format(self._user_name)
        response = session().execute(uri, 'PUT', api_args)
        self._status = response['data']['status']

    def unblock(self):
        """Restores this :class:`User` to an active status and re-enables their 
        log-in
        """
        api_args = {'unblock': 'True'}
        uri = '/User/{}/'.format(self._user_name)
        response = session().execute(uri, 'PUT', api_args)
        self._status = response['data']['status']

    def add_permission(self, permission):
        """Add individual permissions to this :class:`User`

        :param permission: the permission to add
        """
        api_args = {}
        self.permissions.append(permission)
        uri = '/UserPermissionEntry/{}/{}/'.format(self._user_name, permission)
        session().execute(uri, 'POST', api_args)

    def replace_permissions(self, permissions=None):
        """Replaces the list of permissions for this :class:`User`

        :param permissions: A list of permissions. Pass an empty list or omit
            the argument to clear the list of permissions of the :class:`User`
        """
        api_args = {}
        if permissions is not None:
            api_args['permissions'] = permissions
            self.permissions = permissions
        else:
            self.permissions = []
        uri = '/UserPermissionEntry/{}/'.format(self._user_name)
        session().execute(uri, 'PUT', api_args)

    def delete_permission(self, permission):
        """Remove this specific permission from the :class:`User`

        :param permission: the permission to remove
        """
        api_args = {}
        if permission in self.permissions:
            self.permissions.remove(permission)
        uri = '/UserPermissionEntry/{}/{}/'.format(self._user_name, permission)
        session().execute(uri, 'DELETE', api_args)

    def add_permissions_group(self, group):
        """Assigns the permissions group to this :class:`User`

        :param group: the permissions group to add to this :class:`User`
        """
        api_args = {}
        self.permission_groups.append(group)
        uri = '/UserGroupEntry/{}/{}/'.format(self._user_name, group)
        session().execute(uri, 'POST', api_args)

    def replace_permissions_group(self, groups=None):
        """Replaces the list of permissions for this :class:`User`

        :param groups: A list of permissions groups. Pass an empty list or omit
            the argument to clear the list of permissions groups of the 
            :class:`User`
        """
        api_args = {}
        if groups is not None:
            api_args['groups'] = groups
            self.groups = groups
        else:
            self.groups = []
        uri = '/UserGroupEntry/{}/'.format(self._user_name)
        session().execute(uri, 'PUT', api_args)

    def delete_permissions_group(self, group):
        """Removes the permissions group from the :class:`User`

        :param group: the permissions group to remove from this :class:`User`
        """
        api_args = {}
        if group in self.permissions:
            self.permission_groups.remove(group)
        uri = '/UserGroupEntry/{}/{}/'.format(self._user_name, group)
        session().execute(uri, 'DELETE', api_args)

    def add_forbid_rule(self, permission, zone=None):
        """Adds the forbid rule to the :class:`User`'s permission group

        :param permission: the permission to forbid from this :class:`User`
        :param zone: A list of zones where the forbid rule applies
        """
        api_args = {}
        if zone is not None:
            api_args['zone'] = zone
        uri = '/UserForbidEntry/{}/{}/'.format(self._user_name, permission)
        session().execute(uri, 'POST', api_args)

    def replace_forbid_rules(self, forbid=None):
        """Replaces the list of forbidden permissions in the :class:`User`'s 
        permissions group with a new list.

        :param forbid: A list of rules to replace the forbidden rules on the 
            :class:`User`'s permission group. If empty or not passed in, the 
            :class:`User`'s forbid list will be cleared
        """
        api_args = {}
        if forbid is not None:
            api_args['forbid'] = forbid
        uri = '/UserForbidEntry/{}/'.format(self._user_name)
        session().execute(uri, 'PUT', api_args)

    def delete_forbid_rule(self, permission, zone=None):
        """Removes a forbid permissions rule from the :class:`User`'s
        permission group

        :param permission: permission
        :param zone: A list of zones where the forbid rule applies
        """
        api_args = {}
        if zone is not None:
            api_args['zone'] = zone
        uri = '/UserForbidEntry/{}/{}/'.format(self._user_name, permission)
        session().execute(uri, 'DELETE', api_args)

    def delete(self):
        """Delete this :class:`User` from the system"""
        api_args = {}
        uri = '/User/{}/'.format(self._user_name)
        session().execute(uri, 'DELETE', api_args)

    def __str__(self):
        """Custom str method"""
        return 'User: <{}>'.format(self.user_name)

    __repr__ = __unicode__ = __str__


class PermissionsGroup(object):
    """A DynECT System Permissions Group object"""
    def __init__(self, group_name, *args, **kwargs):
        """Create a new permissions Group

        :param group_name: The name of the permission group to update
        :param description: A description of the permission group
        :param group_type: The type of the permission group. Valid values: 
            plain or default
        :param all_users: If 'Y', all current users will be added to the group. 
            Cannot be used if user_name is passed in
        :param permission: A list of permissions that the group contains
        :param user_name: A list of users that belong to the permission group
        :param subgroup: A list of groups that belong to the permission group
        :param zone: A list of zones where the group's permissions apply
        """
        super(PermissionsGroup, self).__init__()
        self.logger = logging.getLogger(str(self.__class__))
        self._group_name = group_name
        self._description = self._group_type = self._all_users = None
        self._permission = self._user_name = self._subgroup = self._zone = None
        self.uri = '/PermissionGroup/{}/'.format(self._group_name)
        if 'api' in kwargs:
            del kwargs['api']
            for key, val in kwargs.items():
                setattr(self, '_' + key, val)
        elif len(args) == 0 and len(kwargs) == 0:
            self._get()
        else:
            self._post(*args, **kwargs)

    def _post(self, description, group_type=None, all_users=None,
              permission=None, user_name=None, subgroup=None, zone=None):
        """Create a new :class:`PermissionsGroup` on the DynECT System"""
        self._description = description
        self._group_type = group_type
        self._all_users = all_users
        self._permission = permission
        self._user_name = user_name
        self._subgroup = subgroup
        self._zone = zone
        api_args = {}
        # Any fields that were not explicitly set should not be passed through
        for key, val in self.__dict__.items():
            if val is not None and not hasattr(val, '__call__') and \
                    key.startswith('_'):
                if key is '_group_type':
                    api_args['type'] = val
                else:
                    api_args[key[1:]] = val
        uri = '/PermissionGroup/{}/'.format(self._group_name)
        response = session().execute(uri, 'POST', api_args)
        for key, val in response['data'].items():
            if key == 'type':
                setattr(self, '_group_type', val)
            elif key == 'zone':
                self._zone = []
                for zone in val:
                    self._zone.append(zone['zone_name'])
            else:
                setattr(self, '_' + key, val)

    def _get(self):
        """Get an existing :class:`PermissionsGroup` from the DynECT System"""
        api_args = {}
        response = session().execute(self.uri, 'GET', api_args)
        for key, val in response['data'].items():
            if key == 'type':
                setattr(self, '_group_type', val)
            elif key == 'zone':
                self._zone = []
                for zone in val:
                    self._zone.append(zone['zone_name'])
            else:
                setattr(self, '_' + key, val)

    def _update(self, api_args):
        response = session().execute(self.uri, 'PUT', api_args)
        for key, val in response['data'].items():
            if key == 'type':
                setattr(self, '_group_type', val)
            elif key == 'zone':
                self._zone = []
                for zone in val:
                    self._zone.append(zone['zone_name'])
            else:
                setattr(self, '_' + key, val)

    @property
    def group_name(self):
        """The name of this permission group"""
        return self._group_name
    @group_name.setter
    def group_name(self, value):
        new_group_name = value
        api_args = {'new_group_name': new_group_name,
                    'group_name': self._group_name}
        self._update(api_args)
        self._group_name = new_group_name
        self.uri = '/PermissionGroup/{}/'.format(self._group_name)

    @property
    def description(self):
        """A description of this permission group"""
        return self._description
    @description.setter
    def description(self, value):
        self._description = value
        api_args = {'group_name': self._group_name,
                    'description': self._description}
        self._update(api_args)

    @property
    def group_type(self):
        """The type of this permission group"""
        return self._group_type
    @group_type.setter
    def group_type(self, value):
        self._group_type = value
        api_args = {'type': self._group_type,
                    'group_name': self._group_name}
        self._update(api_args)

    @property
    def all_users(self):
        """If 'Y', all current users will be added to the group. Cannot be
        used if user_name is passed in
        """
        return self._all_users
    @all_users.setter
    def all_users(self, value):
        self._all_users = value
        api_args = {'all_users': self._all_users,
                    'group_name': self._group_name}
        self._update(api_args)

    @property
    def permission(self):
        """A list of permissions that this group contains"""
        return self._permission
    @permission.setter
    def permission(self, value):
        self._permission = value
        api_args = {'permission': self._permission,
                    'group_name': self._group_name}
        self._update(api_args)

    @property
    def user_name(self):
        """A list of users that belong to the permission group"""
        return self._user_name
    @user_name.setter
    def user_name(self, value):
        self._user_name = value
        api_args = {'user_name': self._user_name,
                    'group_name': self._group_name}
        self._update(api_args)

    @property
    def subgroup(self):
        """A list of groups that belong to the permission group"""
        return self._subgroup
    @subgroup.setter
    def subgroup(self, value):
        self._subgroup = value
        api_args = {'subgroup': self._subgroup,
                    'group_name': self._group_name}
        self._update(api_args)

    @property
    def zone(self):
        """A list of users that belong to the permission group"""
        return self._zone
    @zone.setter
    def zone(self, value):
        self._zone = value
        api_args = {'zone': self._zone,
                    'group_name': self._group_name}
        self._update(api_args)

    def delete(self):
        """Delete this permission group"""
        api_args = {}
        uri = '/PermissionGroup/{}/'.format(self._group_name)
        session().execute(uri, 'DELETE', api_args)

    def add_permission(self, permission):
        """Adds individual permissions to the user

        :param permission: the permission to add to this user
        """
        uri = '/PermissionGroupPermissionEntry/{}/{}/'.format(self._group_name, 
                                                              permission)
        session().execute(uri, 'POST', {})
        self._permission.append(permission)

    def replace_permissions(self, permission=None):
        """Replaces a list of individual user permissions for the user

        :param permission: A list of permissions. Pass an empty list or omit 
            the argument to clear the list of permissions of the user
        """
        api_args = {}
        if permission is not None:
            api_args['permission'] = permission
        uri = '/PermissionGroupPermissionEntry/{}/'.format(self._group_name)
        session().execute(uri, 'PUT', api_args)
        if permission:
            self._permission = permission
        else:
            self._permission = []

    def remove_permission(self, permission):
        """Removes the specific permission from the user

        :param permission: the permission to remove
        """
        uri = '/PermissionGroupPermissionEntry/{}/{}/'.format(self._group_name, 
                                                              permission)
        session().execute(uri, 'DELETE', {})
        self._permission.remove(permission)

    def add_zone(self, zone, recurse='Y'):
        """Add a new Zone to this :class:`PermissionsGroup`

        :param zone: The name of the Zone to be added to this
            :class:`PermissionsGroup`
        :param recurse: A flag determining whether or not to add all sub-nodes
            of a Zone to this :class:`PermissionsGroup`
        """
        api_args = {'recurse': recurse}
        uri = '/PermissionGroupZoneEntry/{}/{}/'.format(self._group_name, zone)
        session().execute(uri, 'POST', api_args)
        self._zone.append(zone)

    def add_subgroup(self, name):
        """Add a new Sub group to this :class:`PermissionsGroup`

        :param name: The name of the :class:`PermissionsGroup` to be added to
            this :class:`PermissionsGroup`'s subgroups
        """
        api_args = {}
        uri = '/PermissionGroupSubgroupEntry/{}/{}/'.format(self._group_name, 
                                                            name)
        session().execute(uri, 'POST', api_args)
        self._subgroup.append(name)

    def update_subgroup(self, subgroups):
        """Update the subgroups under this :class:`PermissionsGroup`

        :param subgroups: The subgroups with updated information
        """
        api_args = {'subgroup': subgroups}
        uri = '/PermissionGroupSubgroupEntry/{}/'.format(self._group_name)
        session().execute(uri, 'PUT', api_args)
        self._subgroup = subgroups

    def delete_subgroup(self, name):
        """Remove a Subgroup from this :class:`PermissionsGroup`

        :param name: The name of the :class:`PermissionsGroup` to be remoevd
            from this :class:`PermissionsGroup`'s subgroups
        """
        api_args = {}
        uri = '/PermissionGroupSubgroupEntry/{}/{}/'.format(self._group_name, 
                                                            name)
        session().execute(uri, 'DELETE', api_args)
        self._subgroup.remove(name)


class UserZone(object):
    """A DynECT system UserZoneEntry"""
    def __init__(self, user_name, zone_name, recurse='Y'):
        super(UserZone, self).__init__()
        self.logger = logging.getLogger(str(self.__class__))
        self._user_name = user_name
        self._zone_name = zone_name
        self._recurse = recurse
        api_args = {'recurse': self._recurse}
        uri = '/UserZoneEntry/{}/{}/'.format(self._user_name, self._zone_name)
        respnose = session().execute(uri, 'POST', api_args)
        for key, val in respnose['data'].items():
            setattr(self, '_' + key, val)

    @property
    def user_name(self):
        """User_name property of :class:`UserZone` object is read only"""
        return self._user_name
    @user_name.setter
    def user_name(self, value):
        pass

    @property
    def recurse(self):
        """Indicates whether or not permissions should apply to subnodes of
        the `zone_name` as well
        """
        return self._recurse
    @recurse.setter
    def recurse(self, value):
        self._recurse = value
        api_args = {'recurse': self._recurse, 'zone_name': self._zone_name}
        uri = '/UserZoneEntry/{}/'.format(self._user_name)
        session().execute(uri, 'PUT', api_args)

    def update_zones(self, zone=None):
        """Replacement list zones where the user will now have permissions.
        Pass an empty list or omit the argument to clear the user's zone
        permissions

        :param zone: a list of zone names where the user will now have
            permissions
        """
        if zone is None:
            zone = []
        api_args = {'zone': []}
        for zone_data in zone:
            api_args['zone'].append({'zone_name': zone_data})
        uri = '/UserZoneEntry/{}/'.format(self._user_name)
        respnose = session().execute(uri, 'PUT', api_args)
        for key, val in respnose['data'].items():
            setattr(self, '_' + key, val)

    def delete(self):
        """Delete this :class:`UserZone` object from the DynECT System"""
        api_args = {'recurse': self.recurse}
        uri = '/UserZoneEntry/{}/{}/'.format(self._user_name, self._zone_name)
        session().execute(uri, 'DELETE', api_args)


class Notifier(object):
    """DynECT System Notifier"""
    def __init__(self, *args, **kwargs):
        """Create a new :class:`Notifier` object

        :param label: The label used to identify this :class:`Notifier`
        :param recipients: List of Recipients attached to this :class:`Notifier`
        :param services: List of services attached to this :class:`Notifier`
        :param notifier_id: The system id of this :class:`Notifier`
        """
        super(Notifier, self).__init__()
        self.logger = logging.getLogger(str(self.__class__))
        self._label = self._recipients = self._services = None
        self._notifier_id = self.uri = None
        if 'api' in kwargs:
            del kwargs['api']
            for key, val in kwargs.items():
                setattr(self, '_' + key, val)
            self.uri = '/Notifier/{}/'.format(self._notifier_id)
        elif len(args) + len(kwargs) > 1:
            self._post(*args, **kwargs)
        elif len(kwargs) > 0 or 'label' in kwargs:
            self._post(**kwargs)
        else:
            self._get(*args, **kwargs)

    def _post(self, label=None, recipients=None, services=None):
        """Create a new :class:`Notifier` object on the DynECT System"""
        if label is None:
            raise DynectInvalidArgumentError
        uri = '/Notifier/'
        self._label = label
        self._recipients = recipients
        self._services = services
        response = session().execute(uri, 'POST', self)
        self._build(response['data'])
        self.uri = '/Notifier/{}/'.format(self._notifier_id)

    def _get(self, notifier_id):
        """Get an existing :class:`Notifier` object from the DynECT System"""
        self._notifier_id = notifier_id
        self.uri = '/Notifier/{}/'.format(self._notifier_id)
        api_args = {}
        response = session().execute(self.uri, 'GET', api_args)
        self._build(response['data'])

    def _build(self, data):
        for key, val in data.items():
            setattr(self, '_' + key, val)

    def _update(self, api_args):
        response = session().execute(self.uri, 'PUT', api_args)
        self._build(response['data'])

    @property
    def notifier_id(self):
        """The unique System id for this Notifier"""
        return self._notifier_id
    @notifier_id.setter
    def notifier_id(self, value):
        pass

    @property
    def label(self):
        """The label used to identify this :class:`Notifier`"""
        return self._label
    @label.setter
    def label(self, value):
        self._label = value
        api_args = {'label': self._label}
        self._update(api_args)

    @property
    def recipients(self):
        """List of Recipients attached to this :class:`Notifier`"""
        return self._recipients
    @recipients.setter
    def recipients(self, value):
        self._recipients = value
        api_args = {'recipients': self._recipients}
        self._update(api_args)

    @property
    def services(self):
        """List of services attached to this :class:`Notifier`"""
        return self._services
    @services.setter
    def services(self, value):
        self._services = value
        api_args = {'services': self._services}
        self._update(api_args)

    def delete(self):
        """Delete this :class:`Notifier` from the Dynect System"""
        api_args = {}
        session().execute(self.uri, 'DELETE', api_args)


class Contact(object):
    """A DynECT System Contact"""
    def __init__(self, nickname, *args, **kwargs):
        """Create a :class:`Contact` object

        :param nickname: The nickname for this :class:`Contact`
        :param email: The :class:`Contact`'s email address
        :param first_name: The :class:`Contact`'s first name
        :param last_name: The :class:`Contact`'s last name
        :param organization: The :class:`Contact`'s organization
        :param phone: The :class:`Contact`'s phone number. Can be of the form:
            ( 0 ) ( country-code ) ( local number ) ( extension ) Only the
            country-code (1-3 digits) and local number (at least 7 digits) are
            required. The extension can be up to 4 digits. Any non-digits are
            ignored.
        :param address: The :class:`Contact`'s street address
        :param address2: The :class:`Contact`'s street address, line 2
        :param city: The :class:`Contact`'s city, part of the user's address
        :param country: The :class:`Contact`'s country, part of the
            :class:`Contact`'s address
        :param fax: The :class:`Contact`'s fax number
        :param notify_email: Email address where the :class:`Contact` should
            receive notifications
        :param pager_email: Email address where the :class:`Contact` should
            receive messages destined for a pager
        :param post_code: Zip code or Postal code
        :param state: The :class:`Contact`'s state, part of the
            :class:`Contact`'s address
        :param website: The :class:`Contact`'s website
        """
        super(Contact, self).__init__()
        self.logger = logging.getLogger(str(self.__class__))
        self._nickname = nickname
        self._email = self._first_name = self._last_name = None
        self._organization = self._address = self._address_2 = self._city = None
        self._country = self._fax = self._notify_email = None
        self._pager_email = self._phone = self._post_code = self._state = None
        self._website = None
        self.uri = '/Contact/{}/'.format(self._nickname)
        if 'api' in kwargs:
            del kwargs['api']
            for key, val in kwargs.items():
                if key != '_nickname':
                    setattr(self, '_' + key, val)
                else:
                    setattr(self, key, val)
            self.uri = '/Contact/{}/'.format(self._nickname)
        elif len(args) == 0 and len(kwargs) == 0:
            self._get()
        else:
            self._post(*args, **kwargs)

    def _post(self, email, first_name, last_name, organization, address=None,
              address_2=None, city=None, country=None, fax=None,
              notify_email=None, pager_email=None, phone=None, post_code=None,
              state=None, website=None):
        """Create a new :class:`Contact` on the DynECT System"""
        self._email = email
        self._first_name = first_name
        self._last_name = last_name
        self._organization = organization
        self._address = address
        self._address_2 = address_2
        self._city = city
        self._country = country
        self._fax = fax
        self._notify_email = notify_email
        self._pager_email = pager_email
        self._phone = phone
        self._post_code = post_code
        self._state = state
        self._website = website
        response = session().execute(self.uri, 'POST', self)
        self._build(response['data'])

    def _get(self):
        """Get an existing :class:`Contact` from the DynECT System"""
        api_args = {}
        response = session().execute(self.uri, 'GET', api_args)
        for key, val in response['data'].items():
            setattr(self, '_' + key, val)

    def _build(self, data):
        for key, val in data.items():
            setattr(self, '_' + key, val)

    def _update(self, api_args):
        """Private update method which handles building this :class:`Contact`
        object from the API JSON respnose
        """
        response = session().execute(self.uri, 'PUT', api_args)
        self._build(response['data'])

    @property
    def nickname(self):
        """This :class:`Contact`'s DynECT System Nickname"""
        return self._nickname
    @nickname.setter
    def nickname(self, value):
        self._nickname = value
        api_args = {'new_nickname': self._nickname}
        self._update(api_args)

    @property
    def email(self):
        """This :class:`Contact`'s DynECT System Email address"""
        return self._email
    @email.setter
    def email(self, value):
        self._email = value
        api_args = {'email': self._email}
        self._update(api_args)

    @property
    def first_name(self):
        """The first name of this :class:`Contact`"""
        return self._first_name
    @first_name.setter
    def first_name(self, value):
        self._first_name = value
        api_args = {'first_name': self._first_name}
        self._update(api_args)
    
    @property
    def last_name(self):
        """The last name of this :class:`Contact`"""
        return self._last_name
    @last_name.setter
    def last_name(self, value):
        self._last_name = value
        api_args = {'last_name': self._last_name}
        self._update(api_args)
    
    @property
    def organization(self):
        """The organization this :class:`Contact` belongs to within the DynECT
        System
        """
        return self._organization
    @organization.setter
    def organization(self, value):
        self._organization = value
        api_args = {'organization': self._organization}
        self._update(api_args)
    
    @property
    def phone(self):
        """The phone number associated with this :class:`Contact`"""
        return self._phone
    @phone.setter
    def phone(self, value):
        self._phone = value
        api_args = {'phone': self._phone}
        self._update(api_args)
    
    @property
    def address(self):
        """This :class:`Contact`'s street address"""
        return self._address
    @address.setter
    def address(self, value):
        self._address = value
        api_args = {'address': self._address}
        self._update(api_args)
    
    @property
    def address_2(self):
        """This :class:`Contact`'s street address, line 2"""
        return self._address_2
    @address_2.setter
    def address_2(self, value):
        self._address_2 = value
        api_args = {'address_2': self._address_2}
        self._update(api_args)
    
    @property
    def city(self):
        """This :class:`Contact`'s city"""
        return self._city
    @city.setter
    def city(self, value):
        self._city = value
        api_args = {'city': self._city}
        self._update(api_args)

    @property
    def country(self):
        """This :class:`Contact`'s Country"""
        return self._country
    @country.setter
    def country(self, value):
        self._country = value
        api_args = {'country': self._country}
        self._update(api_args)

    @property
    def fax(self):
        """The fax number associated with this :class:`Contact`"""
        return self._fax
    @fax.setter
    def fax(self, value):
        self._fax = value
        api_args = {'fax': self._fax}
        self._update(api_args)

    @property
    def notify_email(self):
        """Email address where this :class:`Contact` should receive
        notifications
        """
        return self._notify_email
    @notify_email.setter
    def notify_email(self, value):
        self._notify_email = value
        api_args = {'notify_email': self._notify_email}
        self._update(api_args)
    
    @property
    def pager_email(self):
        """Email address where this :class:`Contact` should receive messages
        destined for a pager
        """
        return self._pager_email
    @pager_email.setter
    def pager_email(self, value):
        self._pager_email = value
        api_args = {'pager_email': self._pager_email}
        self._update(api_args)
    
    @property
    def post_code(self):
        """This :class:`Contacts`'s postal code, part of the contacts's address
        """
        return self._post_code
    @post_code.setter
    def post_code(self, value):
        self._post_code = value
        api_args = {'post_code': self._post_code}
        self._update(api_args)

    @property
    def state(self):
        """This :class:`Contact`'s state"""
        return self._state
    @state.setter
    def state(self, value):
        self._state = value
        api_args = {'state': self._state}
        self._update(api_args)

    @property
    def website(self):
        """This :class:`Contact`'s website"""
        return self._website
    @website.setter
    def website(self, value):
        self._website = value
        api_args = {'website': self._website}
        self._update(api_args)

    def delete(self):
        """Delete this :class:`Contact` from the Dynect System"""
        api_args = {}
        session().execute(self.uri, 'DELETE', api_args)