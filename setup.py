from setuptools import setup, find_packages


setup(
	name="smapi",
	version="1.0",
	url="https://github.com/pykpt/smapi",
	author="pykpt",
	packages=find_packages(),
	description="API враппер для school.mosreg.ru",
	install_requires=["requests"],
	long_description=open("README.md", encoding="utf-8").read()
)