from rest_framework.throttling import UserRateThrottle

class EventListThrottle(UserRateThrottle):
    scope = 'event_list'

class RegistrationThrottle(UserRateThrottle):
    scope = 'registration'
