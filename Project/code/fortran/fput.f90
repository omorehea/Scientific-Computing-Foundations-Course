! File: fput.f90
! Author: Owen Morehead
! Purpose: Main driver routine which calls appropriate routines from...

program fput

  use utility, only : dp, pi
  use leapfrog_module, only : leapfrog
  use setup_module, only : N, alpha, C, problemsetup_Init, outFile
 !use output_module

  implicit none

  !Problem Data

  real(dp), allocatable  ::  x(:,:)
 ! real(dp), allocatable  ::  vs(:)
  integer :: K, tsteps
  real(dp) :: tf = 10*pi
  real(dp) :: dt
  integer :: i,j
  
  !Read the input file
  call problemsetup_Init('fput.init')
  print *, 'N=', N, 'alpha=', alpha, 'C=', C
  
  !Initialize problem parameters
  K = 4*((N+1)**2)
  tsteps = ceiling((tf*K**(0.5))/C)
  dt = tf/tsteps

  !Allocate arrays to match problem size
  allocate(x(N+2, tsteps))
  
  call leapfrog(N, alpha, K, dt, tsteps,  x)
 ! print *, "Matrix of masses and their time series values: "
 ! print *, x

  open(20,file=outFile,status="replace")
  do i = 1, N+2
     write(20,*) (x(i,j), j=1,tsteps)
  end do
  close(20)

  deallocate(x)

end program fput
