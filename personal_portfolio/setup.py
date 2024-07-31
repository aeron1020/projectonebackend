from setuptools import setup, find_packages

setup(
    name='personal_portfolio',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django>=4.2.5',
        'djangorestframework',
        'djangorestframework-simplejwt',
        'django-cors-headers',
        'whitenoise',
        'python-dotenv',
        'psycopg2-binary',
    ],
    entry_points={
        'console_scripts': [
            'manage.py = manage:main',
        ],
    },
)
