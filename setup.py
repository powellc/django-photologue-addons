from setuptools import setup, find_packages

setup(
    name='django-photologue-extra-extra-tags',
    version=__import__('photologue_extra_tags').__version__,
    license="BSD",

    install_requires = ['django-photologue',],

    description='An extension to the base photologue template tag set.',
    long_description=open('README.rst').read(),

    author='Colin Powell',
    author_email='colin@onecardinal.com',

    url='http://github.com/powellc/django-photologue-extra-tags',
    download_url='http://github.com/powellc/django-photologue-extra-tags/downloads',

    include_package_data=True,

    packages=['photologue_extra_tags'],

    zip_safe=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
