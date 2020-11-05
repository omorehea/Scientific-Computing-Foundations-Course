!/hw3/code/pi/pi.f90
! Author: Owen Morehead
! Purpose: Estimate pi using a direct method and compare to true value

program pi
  use pimod
  implicit none  
  real (dp), dimension(4) :: thresh  !All threshold values used
  real (dp) ::  pi_appx, diff
  integer :: N_Max, N, j
  N_Max = 50
  thresh = (/1.0d-4,1.0d-8,1.0d-12,1.0d-16/)
   
  do j = 1,size(thresh)
     
     call pi_estimate(thresh(j),N_Max,pi_appx,diff,N)
     print *, "Number of terms required for a threshold of",thresh(j),"is : ", N
     print *, "Calculated value of pi: ", pi_appx
  enddo

end program
