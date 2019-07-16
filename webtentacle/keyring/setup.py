from cx_Freeze import setup, Executable

options = {
    'build_exe': '../../.code/keyring'
}
setup(name = "Crypt",
      version = "0.1",
      description = "",
      options={"build_exe": options},
      executables = [Executable("crypt.py")])