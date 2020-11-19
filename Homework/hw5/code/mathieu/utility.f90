! File: utility.f90
! Author: Ian May
! Purpose: Define useful constants

module utility
  
  implicit none
  
  integer, parameter :: dp = kind(0.d0)
  integer, parameter :: maxFileLen=50, maxStrLen=200
  real (dp), parameter :: pi = acos(-1.0_dp)

contains
  
end module utility
