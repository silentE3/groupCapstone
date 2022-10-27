from operator import truediv
from random import randint
from app import generate
from app.algorithm import models


def grouping_algorithm(user_records: list[generate.UserRecord], group_size: int) -> list[models.Group]:
    groups: list[models.Group] = []

    group_count = len(user_records) // group_size
    for idx in range(group_count):
        group = models.Group(str(idx))
        for _ in range(group_size):
            group.members.append(user_records.pop(
                randint(0, len(user_records)-1)))
        groups.append(group)

    for g in groups:
        print()
        print(f"meets availability: {g.meets_availability_requirement()}")
        print(
            f"meets dislike requirement: {models.meets_dislike_requirement(g.members)}")
        for u in g.members:
            print(u.asurite)
    print('===========================')

    check_groups(groups)

    # for _ in range(100000):
    #     idx = rand_idx(group_count-1)
    #     swap_member(groups[idx[0]], groups[idx[1]])
    return groups


def swap_member(group_a: models.Group, group_b: models.Group):
    member_idx = randint(
        0, min(len(group_a.members)-1, len(group_b.members)-1))
    if group_a.is_user_compatible(group_b.members[member_idx], member_idx) and group_b.is_user_compatible(group_a.members[member_idx], member_idx):
        member_a = group_a.members.pop(member_idx)
        member_b = group_b.members.pop(member_idx)
        group_a.members.append(member_b)
        group_b.members.append(member_a)


def rand_idx(count):
    while True:
        idx_a = randint(0, count)
        idx_b = randint(0, count)
        if idx_a != idx_b:
            return [idx_a, idx_b]


def check_groups(groups: list[models.Group]):
    for g in groups:
        check_group(g)


def check_group(group: models.Group):
    
    if group.meets_availability_requirement():
        print("meets availabiliy requirements")
        return True

    if models.meets_dislike_requirement(group.members):
        print("met the dislike requirement")
