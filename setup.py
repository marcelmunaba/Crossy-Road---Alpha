import cx_Freeze

executables = [cx_Freeze.Executable("Crossy Road - Marcel.py", icon = "icon.ico", base = "Win32GUI")]

cx_Freeze.setup(
    name="Crossy Road - Marcel",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["background.png", "player.png", "enemy.png", "treasure.png", "README.TXT"]}},
    executables = executables

    )
