def can_make_public(user):
    return user.has_perm("data_browser.make_view_public")
