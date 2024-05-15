from setuptools import setup, find_packages, find_namespace_packages

setup(
    name='torgi_gov_ru',
    version='0.0.1',
    install_requires=[
        'Scrapy>=2.11.2',
    ],
    packages=find_packages(
        # All keyword arguments below are optional:
        where='.',  # '.' by default
        include=['torgi_gov_ru'],  # ['*'] by default
        exclude=['torgi_gov_ru.sandbox'],  # empty by default
    ),
    # package_dir = {
    #     'torgi_gov_ru': 'torgi_gov_ru',
    #     },
    include_package_data=True,
    entry_points = {'scrapy': ['settings = torgi_gov_rue.settings']},
)