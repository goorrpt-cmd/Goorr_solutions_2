# # utils.py
# def get_user_role(user):
#     if not user.is_authenticated:
#         return None

#     profile = getattr(user, "userprofile", None)
#     if profile and profile.role:
#         return profile.role.name.upper()

#     return None



# from django.shortcuts import redirect

# def goorr_login_redirect(request):
#     user = request.user
#     if user.is_staff:
#         return redirect("/admin/")
#     return redirect("/dashboard/")


from django.shortcuts import redirect

def goorr_login_redirect(request):
    user = request.user
    if user.is_staff:
        return redirect("/admin/")
    return redirect("/dashboard/")


# def get_user_role(user):
#     """
#     Returns the user's role name in uppercase.
#     Works only if UserProfile has OneToOne with User.
#     """
#     # If user has no profile, return None
#     if not hasattr(user, "userprofile"):
#         return None

#     profile = user.userprofile

#     # If profile has no role, return None
#     if not hasattr(profile, "role") or profile.role is None:
#         return None

#     return profile.role.name.upper()

def get_user_role(user):
    if not user.is_authenticated:
        return None

    profile = getattr(user, "userprofile", None)
    if not profile:
        return None

    role = getattr(profile, "role", None)
    if not role:
        return None

    return role.name.upper()
