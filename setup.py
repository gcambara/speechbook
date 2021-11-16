from setuptools import setup, find_packages

setup(
    name='speechbook',
    packages = find_packages(),
    version='latest',
    description='Speech Recognition Cook Book',
    author='Guillermo Cambara',
    author_email='guillermocambara@gmail.com',
    url='https://github.com/gcambara/speechbook',
    install_requires=[
        'torch>=1.10.0',
    ],
    keywords=['speech_recognition', 'asr', 'speech_processing'],
    python_requires='>=3.6'
)