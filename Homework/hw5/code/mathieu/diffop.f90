module diffop

  use utility, only : dp, pi
  
  implicit none
  
contains

  ! subroutine: diffop_SecondDeriv
  ! purpose: Create second derivative operator over a given (periodic) grid
  ! inputs: x -- Rank 1 array holding grid positions, assumed periodic and equispaced
  ! outputs: D -- Square rank 2 array for the discrete second derivative operator
  subroutine diffop_SecondDeriv(x,D)
    implicit none
    real (dp), intent(in)     :: x(:)
    real (dp), intent(in out) :: D(:,:)
    ! Local variables
    integer :: M, N, i
    real (dp) :: om, dx, k
    real (dp) :: T(size(D,1),size(D,2)), Tinv(size(D,1),size(D,2))
    ! Set sizes and base wavenumber
    M=size(D,1)
    N=size(D,2)
    dx = x(2)-x(1)
    om = 2*pi/(N*dx)
    ! Fill transformation matrices
    T(1,:) = 1.0_dp/N
    Tinv(:,1) = 0.0_dp
    do i=2,M,2
      k = i*om/2
      T(i,:) = 2*cos(k*x)/N
      Tinv(:,i) = -k**2*cos(k*x)
      if (i+1 <= M) then
        T(i+1,:) = 2*sin(k*x)/N
        Tinv(:,i+1) = -k**2*sin(k*x)
      end if
    end do
    if (mod(M,2)==0) then
      T(M,:) = T(M,:)/2.0_dp
    end if
    D = matmul(Tinv,T)
  end subroutine diffop_SecondDeriv

  ! subroutine: diffop_Mathieu
  ! purpose: Create the Mathieu differential operator for a given index over a given
  !          (periodic) grid
  ! inputs: q -- Mathieu index
  !         x -- Rank 1 array holding grid positions, assumed periodic and equispaced
  ! outputs: H -- Square rank 2 array for the discrete Mathieu operator
  subroutine diffop_Mathieu(q, x, H)
    implicit none
    real (dp), intent(in)     :: q
    real (dp), intent(in)     :: x(:)
    real (dp), intent(in out) :: H(:,:)
    ! Local variables
    integer :: N, j
    real (dp) :: V(size(x))
    N = size(x)
    ! Set H to the negative second derivative operator
    call diffop_SecondDeriv(x,H)
    H = -1.0_dp * H
    ! Add the Mathieu potential along the diagonal
    V = 2*q*cos(2*x)
    do j=1,N
      H(j,j) = H(j,j) + V(j)
    end do
  end subroutine diffop_Mathieu

end module diffop
