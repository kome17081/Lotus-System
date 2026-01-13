import numpy as np
def main():
    data = np.random.rand(10)
    matrix = np.random.rand(10, 10)
    result = np.dot(data, matrix)
    print(f"Lotus Output: {result.tolist()}")

if __name__ == "__main__":
    main()
