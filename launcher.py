from kings_and_pigs import game


# need this file because PyInstaller doesn't support executables packages
# see https://github.com/pyinstaller/pyinstaller/issues/2560

if __name__ == "__main__":
    game.run()
