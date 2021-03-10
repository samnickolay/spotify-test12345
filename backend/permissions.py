# # from rest_framework import permissions

# from django.contrib.auth.models import Group


# def remove_clear_delete_group(group):
#     # removes all users from the group
#     # group.clear()
#     for user in group.user_set.all():
#         group.user_set.remove(user)
#     # removes all permissions from the group
#     group.permissions.clear()
#     # deletes the group
#     group.delete()


# def get_team_admin_group(team):
#     group_name = 'team' + ' ' + 'admin' + ' ' + str(team.id)
#     group, created = Group.objects.get_or_create(name=group_name)
#     return group


# def get_team_member_group(team):
#     group_name = 'team' + ' ' + 'member' + ' ' + str(team.id)
#     group, created = Group.objects.get_or_create(name=group_name)
#     return group


# def get_room_admin_group(room):
#     group_name = 'room' + ' ' + 'admin' + ' ' + str(room.team.id) + ' ' + str(room.id)
#     group, created = Group.objects.get_or_create(name=group_name)
#     return group


# def get_room_member_group(room):
#     group_name = 'room' + ' ' + 'member' + ' ' + str(room.team.id) + ' ' + str(room.id)
#     group, created = Group.objects.get_or_create(name=group_name)
#     return group


# def filter_groups_for_team(groups, team):
#     filtered_groups = []
#     for group in groups:
#         group_name_parts = group.name.split(' ')
#         if len(group_name_parts) > 2 and group_name_parts[2] == str(team.id):
#             filtered_groups.append(group)

#     return filtered_groups
