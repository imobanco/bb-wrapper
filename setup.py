from setuptools import setup

# versioning
import versioneer


with open("README.rst", "r") as fh:
    long_description = fh.read()


setup(
    name="bb_wrapper",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Imobanco",
    description="Cliente não oficial da API do Banco do Brasil",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/imobanco/bb-wrapper/",
    packages=["bb_wrapper", "bb_wrapper.wrapper", "bb_wrapper.models"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Environment :: Web Environment",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: Portuguese (Brazilian)",
        "Operating System :: OS Independent",
        "Topic :: Documentation :: Sphinx",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
        "Topic :: Utilities",
        "",
        "",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.23.0",
        "python-decouple>=3.3",
        "pydantic>=1.7.0",
        "python-barcode>=0.13.1",
        "unidecode>=1.1.2",
        "qrcode>=6.1",
    ],
    keywords="API Banco Brasil BB client wrapper",
    project_urls={
        # "Documentation": "https://bb-wrapper.readthedocs.io",
        "Source": "https://github.com/imobanco/bb-wrapper",
        "Tracker": "https://github.com/imobanco/bb-wrapper/issues",
    },
)
