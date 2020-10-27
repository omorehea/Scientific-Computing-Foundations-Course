! File: dft.f90
! Author: Ian May
! Purpose: Find real Fourier cosine series using a direct method

program dft
  use utility, only : dp, pi
  use dftmod
  implicit none
  ! Size of transform
  integer, parameter :: N =80            ! Number of grid points to use
  ! Problem data
  real (dp) :: dx = 2*pi/N               ! Grid point spacing in physical domain
  real (dp), dimension(N) :: x, k        ! Physical domain, wave domain
  real (dp), dimension(N) :: u, f, ft    ! Solution, forcing, transformed forcing
  real (dp), dimension(N,N) :: T, Tinv   ! Transformation matrices
  ! Loop variables
  integer :: i
  !!! === 1. Set up physical domain
  do i = 1,N
    x(i) = (i-1)*dx
  enddo  
  !!! === 2. Fill in the forcing vector
  f = forcing(x)

  !!! === 3. Fill in k and T
  call dft_TransMat(x,k,T)

  !!! === 4. Fill in Tinv 
  call dft_InvTransMat(x,k,Tinv)

  !!! === 5. Set ft = T*f using matvecprod
  ft = matvecprod(T,f)

  !!! === 6. Apply wavenumber scaling
  ft = ft/(1+k**2)
  
  !!! === 7. Set u = Tinv*ft using matvecprod
  u = matvecprod(Tinv,ft)

  !!! === Reports the maximum error and writes out the data file
  write(*,*) "Err: ", maxval( abs(u - exactsol(x) ) )
  ! Open the output file and write the columns
  open(20,file="out.dat",status="replace")
  do i=1,N
    write(20,*) x(i), u(i), f(i), ft(i)
  end do
  close(20)

contains

  !! Forcing function for the given boundary value problem
  real (dp) elemental function forcing(x)
    real (dp), intent(in) :: x
    forcing = exp(sin(x))*(1+sin(x)-cos(x)**2) + &
        9*exp(cos(3*x))*(-1._dp/9._dp+sin(3*x)**2-cos(3*x))
  end function forcing
  
  !! Exact solution for the BVP
  real (dp) elemental function exactsol(x)
    real (dp), intent(in) :: x
    exactsol = exp(sin(x))-exp(cos(3*x))
  end function exactsol
  
end program dft
