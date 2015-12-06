class VkApiError(Exception):
    pass


class AccessError(VkApiError):
    pass


class AccessTokenRequired(VkApiError):
    pass
