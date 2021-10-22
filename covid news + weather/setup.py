import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup (
	name = "Covid_Daily_Brief",
	version = "0.0.1",
	author = "Harry Collins",
	author_email = "hc697@exeter.ac.uk",
	description = "An app for briefing users about the latest coronavirus data via an alarm",
	license = "MIT",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	url = "",
	packages = setuptools.find_packages(),
	install_requires = [
		'time', 'sched', 'json', 'logging', 'pyttsx3', 'requests', 'flasks', 'uk-covid19', 'datetime',
		],
	classifiers = ["Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
		],
	python_requires = '>=3.9.0',
	)
