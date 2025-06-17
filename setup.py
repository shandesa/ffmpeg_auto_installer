from setuptools import setup, find_packages

setup(
    name="ffmpeg_auto_installer",
    version="0.1.0",
    author="Shantanu Desai",
    description="Automatically install and configure ffmpeg in Python for the running session, not permanently",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Windows",
    ],
    python_requires=">=3.7",
)
