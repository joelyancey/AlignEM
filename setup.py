import setuptools
from setuptools import setup, find_packages
from distutils.extension import Extension
# setup(use_scm_version=True)

long_description = ''
try:
    with open('README.md', 'r') as fh:
        long_description = fh.read()
except:
    print('Could not read README.md')


setup(
    name='AlignEM',
    version='0.6.0',
    author='Joel Yancey,',
    author_email='j.y@ucla.edu',
    description='AlignEM is a GUI for aligning or "registering" electron microscopy images',
    long_description=long_description,
    long_description_content_type='text/markdown',
    platforms=['any'],
    url='https://github.com/mcellteam/swift-ir/tree/development_ng',
    # packages=find_packages(),
    # packages=setuptools.find_packages(where=".", exclude=("./tests","/.docs")),
    # package_dir={'alignem':''},
    packages=['src','src.lib','src.lib.bin_darwin','src.lib.bin_linux','src.lib.bin_tacc'
              'src.resources','src.style','src.ui','src.ui.models','src.utils'],
    ext_package='src.lib',

    ext_modules=[Extension('iavg', ['iavg.c']),
                 Extension('iscale', ['iscale.c']),
                 Extension('iscale2', ['iscale2.c']),
                 Extension('mir', ['mir.c']),
                 Extension('remod', ['remod.c']),
                 Extension('swim', ['swim.c']),
                 ],
    python_requires='>=3.9',
    scripts=['alignem.py'],
    entry_points={
        'console_scripts': [
            'alignem = alignem:main',
        ]
    }
)

if __name__=='__main__':
    setup()