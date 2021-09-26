from distutils.core import setup
setup(
  name='TimeNazi',
  packages=['TimeNazi'],
  version='0.1',
  license='MIT',
  description='A simple time tracker with autotagging',
  author='Arthur Franz',
  author_email='af271@protonmail.com',
  url='https://github.com/af271/TimeNazi/tree/af271',
  download_url='https://github.com/af271/TimeNazi/archive/refs/tags/v0.1-alpha.tar.gz',
  keywords=['time tracking', 'time management', 'autotagging'],
  install_requires=[
          'texttable',
          'tkcalendar',
          'datetime',
          'pathlib',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8',
  ],
)