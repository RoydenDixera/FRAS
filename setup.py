import subprocess

# List of dependencies
dependencies = [
    'opencv-python',
    'Pillow',
    'numpy',
    'pandas',
    'opencv-contrib-python',
]

# Install each dependency using pip
for dependency in dependencies:
    subprocess.call(['pip', 'install', dependency])
