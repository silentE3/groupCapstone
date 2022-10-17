"""
entrypoint to the application
"""

from app import generate

def start():
    """
    serves as the entrypoint for this application
    """
    print("made it here")

    userRecords = generate.generate_random_dataset(50)

    


start()
