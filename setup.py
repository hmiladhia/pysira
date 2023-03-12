from pathlib import Path

import setuptools

package_name = 'pysira'
long_description = Path('README.md').read_text().strip()
version = Path(package_name).joinpath('VERSION').read_text().strip()

setuptools.setup(
    name=package_name,
    version=version,
    author='Dhia Hmila',
    author_email='dhiahmila@gmail.com',
    description='CLI tool to handle json resume format in python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    packages=['pysira', 'pysira.exporters'],
    include_package_data=True,
    entry_points={
        'console_scripts': ['sira=pysira.__main__:cli'],
    },
    install_requires=[
        'PyYAML>=6.0',
        'Jinja2>=3.0.0',
        'click>=7.1',
    ],
    extras_require={
        'pdfkit': ['pdfkit>=0.6.1'],
        'xhtml2pdf': ['xhtml2pdf>=0.2.9'],
        'pyppdf': ['pyppdf>=0.1.2'],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    keywords=['resume', 'json', 'cli'],
)
