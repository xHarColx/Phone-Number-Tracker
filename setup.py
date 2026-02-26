from setuptools import setup, find_packages

setup(
    name="PhoneTrackerPro",
    version="5.0.0",
    author="Vishal Rao",
    author_email="",
    description="Advanced Phone Intelligence & OSINT Framework",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Vishal-HaCkEr1910/PhoneTrackerPro",
    py_modules=["phone_tracker"],
    python_requires=">=3.9",
    install_requires=[
        "phonenumbers>=8.13.0",
        "opencage>=2.0.0",
        "folium>=0.14.0",
        "requests>=2.31.0",
        "colorama>=0.4.6",
        "rich>=13.0.0",
        "beautifulsoup4>=4.12.0",
        "lxml>=4.9.0",
        "python-dotenv>=1.0.0",
        "flask>=3.0.0",
        "tqdm>=4.65.0",
        "fake-useragent>=1.4.0",
        "httpx>=0.25.0",
    ],
    entry_points={
        "console_scripts": [
            "phonetracker=phone_tracker:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
    ],
    keywords="osint phone-tracker intelligence recon cybersecurity",
)
