MAKE_PUBLIC_CODENAME = "make_view_public"


def can_make_public(user):
    return user.has_perm(f"data_browser.{MAKE_PUBLIC_CODENAME}")
