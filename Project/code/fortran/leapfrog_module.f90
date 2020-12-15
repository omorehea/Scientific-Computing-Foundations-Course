! File: leapfrog_module.f90
! Author: Owen Morehead
! Purpose: Holds and updates the solution depending on the given parameters
!          and initial conditions

module leapfrog_module

  use utility, only : dp, pi
  
  implicit none

contains

  !subroutine: leapfrog
  ! inputs: N -- number of masses, alpha -- nonlinear coeficient
  !         K -- spring const, dt -- value of delta t 
  !         tsteps -- (what the pdf calls M) amount of time step solutions to calculate, x -- Rank 2 array
  ! outputs: x -- Rank 2 array now holding time step solutions for all masses in system


  subroutine leapfrog(N, alpha, K, dt, tsteps, x)
    implicit none

    real (dp), intent(in out) :: x(:,:)   !x(row,column) , rows = ith mass from 1 to N , columns = time 
                                          !step solutions for each ith mass 
    integer, intent(in out)   :: N, K, tsteps
    real (dp), intent(in out) :: alpha, dt
    
    
    !Local variables
    integer :: i, nn
    real(dp) :: vinit
    
    do i = 1, tsteps
       x(1,i) = 0    !Dummy masses at both ends of system. Solutions for all time equal 0
       x(N+2,i) = 0  !Amount of rows in x goes as N + 2 because N masses along w/ 2 dummy masses
    end do

    do i = 2, N+1  !Filling in first two time solutions for all masses
       x(i,1) = 0                   !x_i^0 = 0 for all masses
       vinit = sin(((i-1)*pi)/(N+1))
       x(i,2) = dt*vinit        !x_i^1 = x_i^0 + dt*v_i^0 . and x_i^0 = 0 so we calculate second time solution
    end do
    
    do nn = 3, tsteps     !the rest of the time step solutions for each mass:  x_i^nn

       do i = 2, N+1  !calculating the solution for each mass at remaining time steps
         
          x(i,nn) = 2*x(i,nn-1) - x(i,nn-2) + K*(dt**2)*(x(i+1,nn-1) - 2*x(i,nn-1)+ x(i-1,nn-1))* &
          & (1 + alpha*(x(i+1,nn-1) - x(i-1,nn-1)))
         
       end do
    end do
  end subroutine leapfrog
end module leapfrog_module
