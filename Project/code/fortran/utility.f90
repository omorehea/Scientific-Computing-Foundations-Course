! File: utility.f90
! Author: Owen Morehead
! Purpose: Define useful constants

module utility
  
  implicit none
  
  integer, parameter :: maxFileLen=50, maxStrLen=200
  integer, parameter :: dp = kind(0.d0)
  real (dp), parameter :: pi = acos(-1.0_dp)

contains

end module utility
