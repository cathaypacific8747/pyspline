# derived from: https://github.com/scipy/scipy/blob/main/scipy/meson.build
project(
  'pyspline', 'c',
  version: run_command(['pyspline/_version.py'], check: true).stdout().strip(),
  license: 'Apache-2.0',
  meson_version: '>= 1.5.0',
  default_options: [
    'buildtype=debugoptimized',
    'b_ndebug=if-release',
    'c_std=c99'
  ]
)

add_languages('fortran', native: false)
ff = meson.get_compiler('fortran')
cc = meson.get_compiler('c')

py3 = import('python').find_installation(pure: false)
py3_dep = py3.dependency()

incdir_numpy = run_command(py3,
  ['-c', 'import os; os.chdir(".."); import numpy; print(numpy.get_include())'],
  check: true
).stdout().strip()
inc_np = include_directories(incdir_numpy)

incdir_f2py = incdir_numpy / '..' / '..' / 'f2py' / 'src'
inc_f2py = include_directories(incdir_f2py)
fortranobject_c = incdir_f2py / 'fortranobject.c'

# share this object across multiple modules
fortranobject_lib = static_library('_fortranobject',
  fortranobject_c,
  dependencies: py3_dep,
  include_directories: [inc_np, inc_f2py],
  gnu_symbol_visibility: 'hidden',
)
fortranobject_dep = declare_dependency(
  link_with: fortranobject_lib,
  include_directories: [inc_np, inc_f2py],
)

f2py = find_program('f2py')
f2py_version = run_command([py3, '-m', 'numpy.f2py', '-v'], check: true).stdout().strip()
message(f'f2py version: @f2py_version@')

cc_args = cc.get_supported_arguments(
  '-O2',
  '-fPIC',
  '-std=c99',
)

# ignore fortran warning flags
_fflag_Wno_maybe_uninitialized = ff.get_supported_arguments('-Wno-maybe-uninitialized')
_fflag_Wno_unused_dummy_argument = ff.get_supported_arguments('-Wno-unused-dummy-argument')
_fflag_Wno_unused_label = ff.get_supported_arguments('-Wno-unused-label')
_fflag_Wno_unused_variable = ff.get_supported_arguments('-Wno-unused-variable')
_fflag_Wno_tabs = ff.get_supported_arguments('-Wno-tabs')

fortran_ignore_warnings = ff.get_supported_arguments(
  _fflag_Wno_maybe_uninitialized,
  _fflag_Wno_unused_dummy_argument,
  _fflag_Wno_unused_label,
  _fflag_Wno_unused_variable,
  _fflag_Wno_tabs
)
fortran_args = ff.get_supported_arguments(
  '-std=f2008',
  '-fPIC',
  '-O2',
  '-fdefault-real-8',
  '-r8', # intel ifx
)

#
# libspline
#

spline_src = files(
  'src/precision.f90',
  'src/adtProjections.F90',
  'src/evaluations.f90',
  'src/basis.f90',
  'src/knots.f90',
  'src/insertKnot.f90',
  'src/getBasisPt.f90',
  'src/parameterizations.f90',
  'src/findSpan.f90',
  'src/compute_curve.f90',
  'src/compute_surface.f90',
  'src/compute_volume.f90',
  'src/eval_curve.f90',
  'src/eval_surface.f90',
  'src/eval_volume.f90',
  'src/projections.F90',
  'src/tfi2d.f90',
)

spline_lib = static_library('spline',
  spline_src,
  fortran_args: fortran_ignore_warnings + fortran_args,
)

# f2py requires f2cmap to be in the current working directory
# see https://github.com/mdolab/pyspline/blob/746e1191840461de9a7e7335cc2070a5ebdd39fb/src/f2py/Makefile#L35-L36
spline_copy_f2cmap = custom_target('copy f2cmap',
  input: 'src/f2py/f2py_f2cmap.ref',
  output:  '.f2py_f2cmap',
  command: ['cp', '@INPUT@', '@OUTPUT@'],
  install: false,
  build_by_default: true
)

spline_c_wrapper = custom_target('libsplinemodule.c', 
  input: 'src/f2py/pyspline.pyf',
  output: ['libsplinemodule.c', 'libspline-f2pywrappers2.f90'],
  command: [f2py, '@INPUT@', '--f2cmap', files('src/f2py/f2py_f2cmap.ref')],
  depends: spline_copy_f2cmap,
)

py3.extension_module('libspline',
  spline_c_wrapper,
  link_with: [spline_lib],
  c_args: cc_args,
  dependencies: [fortranobject_dep],
  link_language: 'fortran',
  subdir: 'pyspline',
  install: true
)

py3.install_sources(
  [
    'pyspline/__init__.py',
    'pyspline/pyCurve.py',
    'pyspline/pySurface.py',
    'pyspline/pyVolume.py',
    'pyspline/utils.py',
  ],
  subdir: 'pyspline'
)