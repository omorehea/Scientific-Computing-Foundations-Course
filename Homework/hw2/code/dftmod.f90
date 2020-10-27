 module dftmod

  use utility, only : dp, pi
  
  implicit none
  
contains

  !!! ==== Add your matvecprod function here ==== !!!                                                         
  function matvecprod(A,x) result(y)
    implicit none   
    real(dp), intent(in) :: A(:,:)
    real(dp), intent(in) :: x(:)
    real(dp), dimension(size(A,1)) :: y
    !Local variables                                                                                             
    integer :: i, j                                                                                     
    do i = 1, size(A,1)
       y(i) = 0.
       do j = 1, size(A,1)
          y(i) = y(i) + A(i,j)*x(j)
       enddo
    enddo
  end function matvecprod
  
  ! subroutine: dft_TransMat
  ! purpose: Fill transformation matrix for a discrete Fourier transform
  !          on a given domain
  subroutine dft_TransMat(x,k,T)
    implicit none
    real (dp), intent(in)     :: x(:)
    real (dp), intent(out)    :: k(:)
    real (dp), intent(in out) :: T(:,:)
    ! Local variables
    integer :: M, N, i
    real (dp) :: om, dx
    ! Set sizes and base wavenumber
    M=size(T,1)
    N=size(T,2)
    dx = x(2)-x(1)
    om = 2*pi/(N*dx)
    ! Set wavenumbers
    k(1) = 0.0_dp
    do i=2,M,2
      k(i) = i*om/2
      if (i+1<=M) then
        k(i+1) = k(i)
      end if
    end do
    !!! ==== Add your code to fill T here ==== !!!
    T(1,:) = 1/N
    do i = 2,size(T,1)
      if (mod(i,2)==0) then
        T(i,:) = 2*cos(k(i)*x)/N
      elseif (mod(i,2)>0) then
        T(i,:) = 2*sin(k(i)*x)/N
      endif
    enddo

    
    
  end subroutine dft_TransMat

  
  !!! ==== Add your dft_InvTransMat subroutine here ==== !!!
  subroutine dft_InvTransMat(x,k,Tinv)
    implicit none
    real (dp), intent(in)     :: x(:)
    real (dp), intent(in)     :: k(:)
    real (dp), intent(in out) :: Tinv(:,:)
    integer :: j
    Tinv(:,1) = 1
    do j = 2,size(Tinv,2)
      if (mod(j,2)==0) then
        Tinv(:,j) = cos(k(j)*x)
      elseif (mod(j,2)>0) then
        Tinv(:,j) = sin(k(j)*x)
      endif
    enddo 
  end subroutine dft_InvTransMat

end module dftmod
