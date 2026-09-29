import numpy as np

def create_array_from_list():
    return np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

def create_array_with_arange():
    return np.arange(1, 11)

def describe_array(arr):
    print(f"Array            : {arr}")
    print(f"Data type (dtype): {arr.dtype}")
    print(f"Shape            : {arr.shape}")
    print(f"Number of dims   : {arr.ndim}")
    print(f"Size (elements)  : {arr.size}")

if __name__ == "__main__":
    arr1 = create_array_from_list()
    print("Array created with np.array([1, 2, ..., 10]):")
    describe_array(arr1)

    print()
    arr2 = create_array_with_arange()
    print("Array created with np.arange(1, 11):")
    describe_array(arr2)

    print()
    print("Are both arrays equal?", np.array_equal(arr1, arr2))

    print()
    print("Bonus: vectorized operations (applied to every element at once)")
    print(f"arr1 * 2       : {arr1 * 2}")
    print(f"arr1 + 100     : {arr1 + 100}")
    print(f"sum(arr1)      : {arr1.sum()}")
    print(f"mean(arr1)     : {arr1.mean()}")

    print()
    print("Bonus: indexing and slicing")
    print(f"First element  : {arr1[0]}")
    print(f"Last element   : {arr1[-1]}")
    print(f"First 5 values : {arr1[:5]}")
    print(f"Every other    : {arr1[::2]}")
