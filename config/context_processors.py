from .constants import COMPANY_NAME, SYSTEM_FULL_NAME, SYSTEM_NAME


def site_constants(request):
    return {
        "SYSTEM_NAME": SYSTEM_NAME,
        "SYSTEM_FULL_NAME": SYSTEM_FULL_NAME,
        "COMPANY_NAME": COMPANY_NAME,
    }
