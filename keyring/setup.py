from cx_Freeze import setup, Executable

setup(name = "Crypt",
      version = "0.1",
      description = "encrypts and decrypts main system keyring",
      executables = [Executable("crypt.py")])