! File: utility.f90
! Purpose: Define useful constants

module utility
  
  implicit none
  
  integer, parameter :: dp = kind(0.d0)
  real (dp), parameter :: pi = acos(-1.0_dp)

contains
  
end module utility
