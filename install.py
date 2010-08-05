from distutils.core import setup, Extension

setup(name='contas', version='1.0', ext_modules=[Extension("contas", ["contasmodule.c"])])
