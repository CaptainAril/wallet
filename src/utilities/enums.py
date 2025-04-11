from django.db.models import TextChoices


class Currency(TextChoices):
    NGN = 'NGN', 'Naira'


class DocumentTypes(TextChoices):
    PASSPORT = 'PASSPORT', 'Passport'
    DRIVERS_LICENSE = 'DRIVERS_LICENSE', 'Driver\'s License'
    VOTER_CARD = 'VOTER_CARD', 'Voter\'s Card'
    NATIONAL_ID = 'NATIONAL_ID', 'National ID Card'
    NIN = 'NIN', 'National Identification Number'
    OTHER = 'OTHER', 'Other' 


class NextOfKinRelationship(TextChoices):
    FATHER = 'FATHER', 'Father'
    MOTHER = 'MOTHER', 'Mother'
    BROTHER = 'BROTHER', 'Brother'
    SISTER = 'SISTER', 'Sister'
    UNCLE = 'UNCLE', 'Uncle'
    AUNT = 'AUNT', 'Aunt'
    COUSIN = 'COUSIN', 'Cousin'
    NEPHEW = 'NEPHEW', 'Nephew'
    NIECE = 'NIECE', 'Niece'
    SON = 'SON', 'Son'
    DAUGHTER = 'DAUGHTER', 'Daughter'