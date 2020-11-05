!hw3/code/pi/pimod.f90

module pimod

  implicit none
  integer, parameter :: dp = kind(0.d0)
  real(dp), parameter :: pi_ref = acos(-1.d0)  !Needs -1.d0 for full precision

contains

  subroutine pi_estimate(thresh,N_Max,pi_appx,diff,N)
    !Compute a numerical value of pi and compares to pi_ref
    implicit none
    real(dp), intent(in) :: thresh
    integer,  intent(in) :: N_Max
    real(dp), intent(out) :: pi_appx, diff
    integer, intent(out) :: N
    integer :: i

    pi_appx = 0.d0
    diff = abs(pi_appx - pi_ref)
    N = 0    
    do i = 0,N_Max
       pi_appx = pi_appx + (16.**(-i) * (4./(8.*i + 1.) - 2./(8.*i+4.) - 1./(8.*i+5.) - 1./(8.*i+6.)))
       diff = abs(pi_appx - pi_ref) 
       N = N + 1
       if (diff < thresh) then
          exit
       endif
    enddo
  
  end subroutine pi_estimate

end module pimod

       
  
