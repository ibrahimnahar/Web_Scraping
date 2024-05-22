# import math
# def find_max(nums):
#     maxn = float(-math.inf)
#     for i in nums:
#         if i > maxn: maxn = i 
#     return maxn

# def does_name_exist(first_names, last_names, full_name):
#     for i in first_names:
#         for c in last_names:
#             if i in full_name and c in full_name:
#                 return True
#     return False

# def get_avg_brand_followers(all_handles, brand_name):
#     a = 0
#     if len(all_handles) > 0:
#         for i in all_handles:
#             for b in i:
#                 if brand_name in b:
#                     a += 1
#         res = a / len(all_handles)
#         return res

# def find_last_name(names_dict:dict, first_name:str):
#         if first_name in names_dict.keys():
#             return names_dict[first_name]
        

# def binary_search(target, arr):
#     minn = 0
#     maxx = len(arr) 

#     while minn < maxx:
#         mid = (minn+maxx)//2
#         if arr[mid] == target:
#             return True
#         elif target < arr[mid]:
#             maxx = mid
#         else:
#             minn = mid +1
#     return False

# def count_names(list_of_lists, target_name):
#     count = 0
#     for i in list_of_lists:
#         for c in i:
#             if c == target_name:
#                 count +=1
#     return count

# def remove_duplicates(nums):
#     nums = set(nums)
#     nums = list(nums)
#     return sorted(nums)

# class Influencer:
#     def __init__(self, num_selfies, num_bio_links):
#         self.num_selfies = num_selfies
#         self.num_bio_links = num_bio_links

#     def __repr__(self):
#         return f"({self.num_selfies}, {self.num_bio_links})"

# # dont touch above this line

# def vanity(influencer):
#     vanity = influencer.num_bio_links * 5 + influencer.num_selfies
#     return vanity


# def vanity_sort(influencers):
#     return sorted(influencers, key=vanity)

# def bubble_sort(nums):
#     swapping = True
#     end = len(nums)
#     while swapping:
#         swapping = False
#         for i in range(1,end):
#             if nums[i-1] > nums[i]:
#                 nums[i], nums[i-1] = nums[i-1], nums[i]
#                 swapping = True
#         end -= 1
#     return nums

# print(bubble_sort([9, 8, 7, 6, 5, 4, 3, 2, 1]))


def merge_sort(A):
    # Base case: if the list has less than 2 elements, it's already sorted
    if len(A) < 2:
        return A

    # Split the list into two halves
    mid = len(A) // 2
    left_half = A[:mid]
    right_half = A[mid:]

    # Recursively sort each half
    sorted_left = merge_sort(left_half)
    sorted_right = merge_sort(right_half)

    # Merge the sorted halves
    return merge(sorted_left, sorted_right)


def merge(first, second):
    final = []
    i, j = 0, 0
    
    # Iterate over both lists
    while i < len(first) and j < len(second):
        if first[i] <= second[j]:
            final.append(first[i])
            i += 1
        else:
            final.append(second[j])
            j += 1
    
    # Add remaining elements from A
    while i < len(first):
        final.append(first[i])
        i += 1
    
    # Add remaining elements from B
    while j < len(second):
        final.append(second[j])
        j += 1
    
    return final
            
    
    
