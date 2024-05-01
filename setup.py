import subprocess

# List of dependencies
dependencies = [
    'opencv-python',
    'Pillow',
    'numpy',
    'pandas',
    'opencv-contrib-python',
    'tk',
]

def install_dependencies():
    for dependency in dependencies:
        subprocess.call(['pip', 'install', dependency])
        print("Installed:",dependencies)

def uninstall_dependencies():
    for dependency in dependencies:
        subprocess.call(['pip', 'uninstall', '-y', dependency])
        print("Uninstalled:",dependencies)

def reinstall_dependencies():
    print("Reinstalling:",dependencies)

    uninstall_dependencies()
    print("Uninstalled:",dependencies)

    install_dependencies()
    print("Installed:",dependencies)

def train():
    subprocess.call(['python', 'train.py'])

def main():
    while True:
        print("Commands: ")
        print("`install` - Install dependencies")
        print("`uninstall` - Uninstall dependencies")
        print("`reinstall` - Reinstall dependencies")
        print("`train` - Run main program (train.py)")
        print("`exit` - Exit program")
        
        choice = input("CLI > ").lower()
        if choice == 'install':
            install_dependencies()
        elif choice == 'uninstall':
            uninstall_dependencies()
        elif choice == 'reinstall':
            reinstall_dependencies()
        elif choice == 'train':
            train()
        elif choice == 'exit':
            print("Quitting!")
            break
        else:
            print("Invalid command. Please try again or check for typo.")

if __name__ == "__main__":
    main()