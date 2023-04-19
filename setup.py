from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-cmd",
    version="0.1.0",
    author="krystian-ai",
    author_email="krystian@toskk.pl",
    description="A command-line tool to execute shell commands based on user input using OpenAI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/krystian-ai/ai-cmd",
    packages=["aicmd"],
    package_data={"aicmd": ["settings.json"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    install_requires=[
        "openai==0.27.0",
        "python-dotenv==0.19.2",
        "setuptools",
        "importlib_resources",
    ],
    entry_points={
        "console_scripts": [
            "ai=aicmd.main:main",
        ],
    },
)
