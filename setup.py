from setuptools import setup

setup(
    name='ni-usb-datalogger',
    version='1.0',
    packages=['ni-usb-datalogger'],
    install_requires=['nidaqmx', 'numpy', 'matplotlib'],
    url='https://github.com/chapdbr/NI-USB-DAQ-DATA-LOGGER',
    license='MIT',
    author='Bruno Chapdelaine',
    author_email='bruno.chapdelaine@gmail.com',
    description='This programs reads voltage data from a National Instrument USB-6003 ADC and converts it to F/T using the calibration matrix from ATI for the ATI mini 45 Titanium.',
    include_package_data=True
)
