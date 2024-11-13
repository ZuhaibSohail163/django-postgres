from datetime import timezone

from pydantic import BaseModel, validator
import base64
from django.db import models
from django.core.exceptions import ValidationError
from typing import Optional, List
from enum import Enum
from typing import Type
from pydantic.utils import GetterDict

class IdentityKind(models.TextChoices):
    UNREGISTERED = "unregistered", "Unregistered"
    USER = "user", "User"
    GROUP = "group", "Group"


class DjangoGetterDict(GetterDict):
    def get(self, key: str, default=None):
        res = getattr(self._obj, key, default)
        if isinstance(res, models.Manager):
            return list(res.all())
        return res


class AclIdentity(BaseModel):
    kind: IdentityKind
    uid: str

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash((type(self), str(self)))

    def __str__(self):
        return f"{self.kind}:{self.uid}"

    @classmethod
    def for_group(cls, group_key):
        return cls(kind=IdentityKind.GROUP, uid=str(group_key.id))

    @classmethod
    def for_user(cls, user_key):
        return cls(kind=IdentityKind.USER, uid=str(user_key.id))


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def has_permission(self, permission: str) -> bool:
        # Placeholder implementation
        return True

    def has_class_permission(self, model_class: Type[models.Model], permission_name: str) -> bool:
        # Placeholder implementation
        return True


def get_role_by_name(name: str) -> Role:
    try:
        return Role.objects.get(name=name)
    except Role.DoesNotExist:
        raise ValueError(f"Role '{name}' does not exist")


def permission_exists(permission: str) -> bool:
    # Placeholder for permission check
    return True


def is_system_role_class(role: Role) -> bool:
    # Placeholder check for system role validation
    return True


class AclRule(BaseModel):
    identity: AclIdentity
    roles: list[Role]

    class Config:
        orm_mode = True
        getter_dict = DjangoGetterDict
        extra = "ignore"

    @staticmethod
    def _sort_roles(roles):
        return sorted(roles, key=lambda r: r.name)

    @validator("roles", pre=True)
    def validate_roles_and_ordering(cls, v):
        roles = []
        for item in v:
            if isinstance(item, Role):
                if is_system_role_class(item):
                    roles.append(item)
                else:
                    raise ValueError(f"Role '{item.name}' is not a system role")
            elif isinstance(item, dict) and "name" in item:
                roles.append(get_role_by_name(item["name"]))
            elif isinstance(item, str):
                roles.append(get_role_by_name(item))
        return AclRule._sort_roles(list(set(roles)))

    def __eq__(self, other):
        return self.identity == other.identity and self.roles == other.roles

    def __hash__(self):
        return hash((type(self), self.identity) + tuple(AclRule._sort_roles(self.roles)))

    def contains_named_class_permission(self, model_class: Type[models.Model], permission_name: str) -> bool:
        return any(
            role.has_class_permission(model_class, permission_name)
            or role.has_class_permission(model_class.__base__, permission_name)
            for role in self.roles
        )

    def contains_permission(self, permission: str) -> bool:
        return any(role.has_permission(permission) for role in self.roles)

    def remove_role(self, role: Role):
        self.roles.remove(role)

    def allows(self, identity: AclIdentity, permission: str) -> bool:
        if not isinstance(identity, AclIdentity):
            raise ValueError(f"Identity is not an instance of AclIdentity, '{identity}' received")

        if not permission_exists(permission):
            raise ValueError(f"Permission '{permission}' does not exist in any system role")

        return self.identity == identity and self.contains_permission(permission)


class Key(BaseModel):
    entity: str
    id: str

    def __str__(self):
        return self.path()

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

    def path(self):
        return f"{self.entity}/{self.id}"

    def urlsafe(self):
        return base64.b64encode(self.path().encode("utf8")).decode("utf8")

    @classmethod
    def from_urlsafe(cls, o):
        return cls.from_path(base64.b64decode(o).decode("utf8"))

    @classmethod
    def from_path(cls, path):
        if "/" not in path:
            raise ValueError(f"The path needs to contain a /: '{path}'")
        entity, _id = path.split("/")
        return cls(entity=entity, id=_id)

class AclEntity(models.Model):
    acl_rules = models.JSONField(default=list, blank=True)

    def add_acl_rule(self, rule):
        if rule not in self.acl_rules:
            self.acl_rules.append(rule)
            self.save()

    def remove_acl_rule(self, rule):
        if rule in self.acl_rules:
            self.acl_rules.remove(rule)
            self.save()

    def add_roles(self, identity, roles):
        # Add logic for adding roles to the identity
        pass

    def remove_roles(self, identity, roles=None):
        # Add logic for removing roles from the identity
        pass

    def set_roles(self, identity, roles):
        # Add logic for setting roles for the identity
        pass


class DomainObject(models.Model):
    key = models.OneToOneField(Key, on_delete=models.SET_NULL, null=True, blank=True)
    acl = models.OneToOneField(AclEntity, on_delete=models.SET_NULL, null=True, blank=True)

    def merge(self, keep_none=False, **kwargs):
        for field, value in kwargs.items():
            if keep_none or value is not None:
                setattr(self, field, value)
        self.save()
        return self

    def add_acl_rule(self, rule):
        if not self.acl:
            self.acl = AclEntity.objects.create()
        self.acl.add_acl_rule(rule)

    def add_acl_rules(self, rules: List):
        for rule in rules:
            self.add_acl_rule(rule)

    def remove_acl_rule(self, rule):
        if self.acl:
            self.acl.remove_acl_rule(rule)
            if not self.acl.acl_rules:
                self.acl.delete()
                self.acl = None
                self.save()

    def add_roles(self, identity, roles: List):
        if not self.acl:
            self.acl = AclEntity.objects.create()
        self.acl.add_roles(identity, roles)

    def remove_roles(self, identity, roles: Optional[List] = None):
        if self.acl:
            self.acl.remove_roles(identity, roles)

    def set_roles(self, identity, roles: List):
        if not self.acl:
            self.acl = AclEntity.objects.create()
        self.acl.set_roles(identity, roles)

    def allows(self, user_identity, permission: str) -> bool:
        if not self.acl:
            return False
        return any(self.acl.allows(identity, permission) for identity in user_identity.acl_identities)

    def has_role(self, user_identity, role) -> bool:
        if not self.acl:
            return False
        return any(
            identity_role['name'] == role['name']
            for acl_rule in self.acl.acl_rules
            if acl_rule['identity']['uid'] == user_identity.user_id
            for identity_role in acl_rule['roles']
        )

class LegalMatterKind(DomainObject):
    name: str
    category: str
    description: Optional[str] = None
    intake_form: str
    products: List[str]

class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    PREFER_NOT_TO_ANSWER = "Prefer not to answer"


class State(BaseModel):
    code: str
    name: str

class GroupLabel(str, Enum):
    FIRM_ADMINS = "firm-admins"
    FIRM_ASSIGNERS = "legal-matter-assigners"
    FIRM_CLAIMERS = "legal-matter-claimers"
    FIRM_USERS = "firm-users"
    LEGALFIX_ADMINS = "legalfix-admins"

class Group(models.Model):
    name = models.CharField(max_length=255)
    roles = models.ManyToManyField(Role)  # Assuming Role is a model
    label = models.CharField(
        max_length=50,
        choices=[(tag, tag.value) for tag in GroupLabel],
        null=True, blank=True
    )
    members = models.ManyToManyField(Key)  # Assuming Key is a model (e.g., User or Firm)

    def __str__(self):
        return self.name

    def can(self, permission: str) -> bool:
        """Verifies if the Group has any role that grants the provided permission."""
        return any(role.has_permission(permission) for role in self.roles.all())


class Location(BaseModel):
    state: State
    city: str
    apt_number: Optional[str]
    street: Optional[str]
    zip_code: Optional[str]

class User(models.Model):
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=50, choices=Gender.choices, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    roles = models.ManyToManyField(Role)  # Assuming Role is a model
    groups = models.ManyToManyField(Group)  # Assuming Group is a model
    last_updated_timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} <{self.email}>"

    @property
    def user_id(self) -> str:
        if not self.pk:
            raise ValueError("User has no primary key")
        return str(self.pk)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def acl_identities(self) -> List['AclIdentity']:
        # Assuming AclIdentity and IdentityKind are defined elsewhere
        identities = [AclIdentity(kind=IdentityKind.user, uid=self.pk)]
        for group in self.groups.all():
            identities.append(AclIdentity(kind=IdentityKind.group, uid=group.pk))
        return identities

    def can(self, permission: str) -> bool:
        """Verifies if the User has a role that grants the provided permission."""
        if not permission_exists(permission):
            raise ValueError(f"Permission '{permission}' does not exist in any system role")
        # Checking if any group allows permission
        any_group_allows = any(group.can(permission) for group in self.groups.all())
        if any_group_allows:
            return True
        return any(role.has_permission(permission) for role in self.roles.all())

    def add_to_group(self, group_ref: Key):
        self.groups.add(group_ref)
        return self.groups

    def remove_from_group(self, group_ref: Key):
        self.groups.remove(group_ref)
        return self.groups


class FirmUser(User):
    firm_ref = models.ForeignKey(Key, on_delete=models.CASCADE)  # Assuming Key is another model

    @property
    def _type(self):
        return self.__class__.__name__


class LawyerUser(FirmUser):
    practice_areas = models.JSONField(null=True, blank=True)  # JSONField for the list of practice areas
    number_of_assigned_legal_matters = models.IntegerField(default=0)
    number_of_assigning_legal_matters = models.IntegerField(default=0)


class SubscriberUser(User):
    subscription_active = models.BooleanField(default=False)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)  # Assuming Location is another model
