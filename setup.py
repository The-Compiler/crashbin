import setuptools

setuptools.setup(
    name='crashbin',
    version='0.0.0',
    url='https://github.com/The-Compiler/crashbin/',
    description='Crash collecting and reporting',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Bug Tracking',
    ],
    install_requires=[
        'django',
        'django-crispy-forms',
        'djangorestframework',
        'django-mailbox',
        'django-fieldsignals',
    ]
)
