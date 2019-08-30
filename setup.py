import sys
py_version = sys.version_info[:2]

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

install_requires = [
    "selenium",
    "ipython",
    "python-dateutil",
    "pyobjc"
]

setup(name='AutoTimer',
      version='1.0',
      description='Tracking the desktop applications in real time and time spent on each application.',
      author='KalleHallden',
      author_email='gward@python.net',
      packages=find_packages(exclude=['ez_setup']),
      install_requires=install_requires,
      url='https://github.com/KalleHallden/AutoTimer',
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      )
