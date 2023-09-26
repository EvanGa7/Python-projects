# Evan Gardner
# CS-450 Cyber Security
# Professor Weihao
# September 20, 2023
# Weekly Assignment 2

def to_numbers(text):
    return [ord(char) - ord('A') for char in text]

def to_text(numbers):
    return ''.join([chr(num + ord('A')) for num in numbers])

def rotate_list_left(lst, k):
    print(f"Before rotate_list_left: {lst}, k={k}")
    n = len(lst)
    k = k % n  # In case k is greater than n
    rotated = lst[k:] + lst[:k]
    print(f"After rotate_list_left: {rotated}")
    return rotated

def compress_block(block, running_total):
    print(f"Block: {block}")
    
    # Convert block to numbers
    block_numbers = to_numbers(block)
    print(f"Block numbers: {block_numbers}")
    
    # Initialize 4x4 matrix
    matrix = [[0] * 4 for _ in range(4)]
    
    # Fill the matrix row-wise
    for i in range(4):
        for j in range(4):
            matrix[i][j] = block_numbers[i * 4 + j]
    
    print(f"Initial Matrix: {matrix}")
    
    # Round 1: Add each column mod 26
    for j in range(4):
        col_sum = sum(matrix[i][j] for i in range(4)) % 26
        running_total[j] = (running_total[j] + col_sum) % 26
    
    print(f"Running total after Round 1: {running_total}")
    
    # Round 2: Rotate and Reverse rows
    print("Before Round 2 rotations:")
    for row in matrix:
        print(row)
        
    for i in range(1, 5):  # Starting from 1, going up to 4
        print(f"\nRotating row {i-1} by {i} positions.")  # Access the row with i-1
        rotated_row = rotate_list_left(matrix[i-1], i)  # Perform the rotation by i positions
        print(f"Rotated row {i-1}: {rotated_row}\n")
        matrix[i-1] = rotated_row  # Update the row in the matrix

    print("After Round 2 rotations:")
    for row in matrix:
        print(row)

    matrix[3] = matrix[3][::-1]
    print(f"After reversing last row: {matrix[3]}")
    
    print(f"Matrix after Round 2: {matrix}")

    # Add each column mod 26
    for j in range(4):
        col_sum = sum(matrix[i][j] for i in range(4)) % 26
        running_total[j] = (running_total[j] + col_sum) % 26
    
    print(f"Running total after Round 2: {running_total}")

    return running_total

def tth_hash(message):
    message = ''.join(filter(str.isalpha, message)).upper()
    
    while len(message) % 16 != 0:
        message += 'A'
    
    running_total = [0, 0, 0, 0]
    
    print(f"Initial message: {message}")
    print(f"Initial running total: {running_total}")
    
    for i in range(0, len(message), 16):
        block = message[i:i+16]
        
        print(f"Processing block: {block}")
        
        running_total = compress_block(block, running_total)
        
        print(f"Updated running total: {running_total}\n")
    
    return to_text(running_total)

if __name__ == "__main__":
    message = "I leave twenty million dollars to my friendly cousin Bill."
    messageTest= 'ABCDEFGHI-JKLMNOP'
    hash_value = tth_hash(message)
    print(f"The hash value of the message is {hash_value}")
