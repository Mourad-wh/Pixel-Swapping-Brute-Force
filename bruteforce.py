import os
import numpy as np
from PIL import Image

#clearing the terminal:
def clear_screen():
    """Clear the terminal screen."""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

clear_screen()


def image_decrypter(image_path, block_size, output_path, encryption_key):
    """Decrypt the image by reversing the block shuffling process."""
    # Open the encrypted image and convert it to a numpy array
    encrypted_image = Image.open(image_path)
    encrypted_image_array = np.array(encrypted_image)

    # Get image dimensions
    height, width = encrypted_image_array.shape[:2]  # Ensure height and width are correctly extracted
    channels = encrypted_image_array.shape[2] if encrypted_image_array.ndim == 3 else 1  # Handle grayscale images

    # Ensure the image dimensions are divisible by the block size
    height = (height // block_size) * block_size
    width = (width // block_size) * block_size
    encrypted_image_array = encrypted_image_array[:height, :width, :]

    # Create a list to hold the blocks
    blocks = []

    # Divide the encrypted image into blocks
    for i in range(0, height, block_size):
        for j in range(0, width, block_size):
            block = encrypted_image_array[i:i+block_size, j:j+block_size, :]
            blocks.append(block)

    # Flatten the blocks list into a single array
    flat_blocks = np.array(blocks).reshape(-1, block_size * block_size * channels)

    # Generate the same permutation key using the encryption key
    np.random.seed(int(encryption_key))  # Use the same seed as in the encryption process
    original_indices = np.random.permutation(len(flat_blocks))

    # Initialize an array to hold the decrypted blocks
    decrypted_blocks = np.zeros_like(flat_blocks)

    # Re-arrange the blocks back to their original positions
    for i, original_index in enumerate(original_indices):
        decrypted_blocks[original_index] = flat_blocks[i]

    # Reshape the decrypted blocks back to the original block format
    decrypted_blocks = decrypted_blocks.reshape(-1, block_size, block_size, channels)

    # Create an empty array to hold the decrypted image
    decrypted_image = np.zeros_like(encrypted_image_array)

    # Reconstruct the image with the decrypted blocks
    block_index = 0
    for i in range(0, height, block_size):
        for j in range(0, width, block_size):
            decrypted_image[i:i + block_size, j:j + block_size, :] = decrypted_blocks[block_index]
            block_index += 1

    # Save the decrypted image
    decrypted_img = Image.fromarray(decrypted_image.astype('uint8'))  # Ensure data type is 'uint8' for saving
    decrypted_img.save(output_path)

    print(f"Decrypted image saved as {output_path}")

def brute_force(image_path):

    # Specify the directory for decrypted images
    file_path = r"C:/Force Brute Photos"  # Adjust this path as necessary

    # Ensure the directory exists before attempting to write
    if not os.path.exists(file_path):
        os.makedirs(file_path)  # Create the directory if it doesn't exist

    # Iterate over block sizes and encryption keys to attempt decryption
    for i in range(1, 100):  # Block sizes from 1 to 99

        # Specify the directory for decrypted images
        file_path = rf"C:/Force Brute Photos/combinaison_{i}"  # Adjust this path as necessary

        # Ensure the directory exists before attempting to write
        if not os.path.exists(file_path):
            os.makedirs(file_path)  # Create the directory if it doesn't exist


        for j in range(0, 250):  # Encryption keys from 0 to 249
            output_path = os.path.join(file_path, f"decrypted_image_{i}_{j}.png")  # Save images with unique names
            image_decrypter(image_path, i, output_path, j)

# Main execution
image_path = input("Insert the encrypted image path: ")
brute_force(image_path)
