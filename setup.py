# pip install cx_freeze
import cx_Freeze

executaveis = [
    cx_Freeze.Executable(
        script="main.py",
        icon="bases/icone.ico",
        target_name="HomerSimpsonRun.exe"
    )
]

cx_Freeze.setup(
    name="The Simpsons - Corrida em Springfield",
    options={
        "build_exe": {
            "packages": ["pygame", "pyttsx3"],
            "include_files": ["bases", "Recursos"]
        }
    },
    executables=executaveis
)

# Comando para gerar executavel:
# python setup.py build
