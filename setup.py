from setuptools import setup, find_packages

setup(
    name='flask_etl_app',
    version='1.0.0',
    description='A Flask ETL pipeline application with MongoDB and PostgreSQL integrations',
    author='Nishant Nayak',
    author_email='nishant.pintu@gmail.com',
    #url='https://github.com/your-repo-url',  # Optional, add if hosted on GitHub or other platforms
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy',
        'Flask-PyMongo',
        'dagster',
        'dagit',
        'pandas',
        'plotly',
        'psycopg-binary',
        'dnspython',  # Required for PyMongo with MongoDB Atlas
        'SQLAlchemy',
        'gunicorn',   # Optional, for deploying the app on production
    ],
    entry_points={
        'console_scripts': [
            'flask_etl_app=run:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
