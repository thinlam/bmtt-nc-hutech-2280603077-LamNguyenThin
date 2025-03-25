def dem_so_lan_xuat_hien(lst):
    count_dict = {}
    for num in lst:
        if num in count_dict:
            count_dict[num] += 1
        else:
            count_dict[num] = 1
    return count_dict
input_string = input("Nhập danh sách các từ, cách nhau bằng dấu cách:")
world_list = input_string.split()
so_lan_xuat_hien = dem_so_lan_xuat_hien(world_list)
print("Số lần xuất hiện của các phẩn tử:", so_lan_xuat_hien)