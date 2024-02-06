from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='easy_whisper',
      version='1.0.0',
      description="An easy to use adaption of OpenAI's Whisper, with both CLI and (tkinter) GUI, faster processing of long audio files even on CPU, txt output with timestamps.",
      long_description=readme(),
      classifiers=[
        'Development Status ::  Alpha',
        'Programming Language :: Python :: 3.10',
        'Topic :: Multimedia :: Sound/Audio :: Speech',
      ],
      keywords='audio transcribe translate ',
      url='https://github.com/iamsamkhan/whisper.git',
      author='shamshad ahmed',
      author_email='smshad0001@gmail.com',
      license='Apache License ',
      packages=['easy_whisper'],
      install_requires=[
          'pydub',
          'openai-whisper'
      ],
      entry_points={
        "console_scripts": [
            "whisper=app.__main__:main"
        ]
      },
      include_package_data=True,
      zip_safe=False)