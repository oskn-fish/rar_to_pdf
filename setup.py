from setuptools import setup 


setup(
    install_requires = ["patool", "img2pdf"],
    entry_points = {
        "console_scripts":["rar_to_pdf = rar_to_pdf:main"]
    }
)