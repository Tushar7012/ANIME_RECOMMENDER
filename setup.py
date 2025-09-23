from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="ANIME_RECOMMENDER",
    version="0.1",
    author="Tushar7012",
    packages=find_packages(),
    install_requires = requirements,
)