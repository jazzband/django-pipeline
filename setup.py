from setuptools import find_packages, setup

setup(
    name="django-pipeline",
    use_scm_version={"version_scheme": "post-release"},
    setup_requires=["setuptools_scm"],
    description="Pipeline is an asset packaging library for Django.",
    long_description=(
        open("README.rst", encoding="utf-8").read()
        + "\n\n"
        + open("HISTORY.rst", encoding="utf-8").read()
    ),
    author="Timothée Peignier",
    author_email="timothee.peignier@tryphon.org",
    url="https://github.com/jazzband/django-pipeline",
    license="MIT",
    packages=find_packages(exclude=["tests", "tests.tests"]),
    zip_safe=False,
    include_package_data=True,
    keywords=("django pipeline asset compiling concatenation compression" " packaging"),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Utilities",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)
