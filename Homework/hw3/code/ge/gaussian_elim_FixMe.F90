#define PRINTINFO

program gauss
  implicit none  
  real, allocatable, dimension(:,:) :: A
  real, allocatable, dimension(:) :: b
  integer :: i
  integer, parameter :: N = 3

  !Allocate A and b
  allocate(A(N,N))
  allocate(b(N))  

  ! initialize matrix A and vector b
  A(:,:) = reshape((/2, 4, 7, 3, 7, 10, -1, 1, -4/), (/3,3/))
  b = (/1, 3, 4/)

#ifdef PRINTINFO
  ! print augmented matrix
  do i = 1, size(A,1)           ! i is row
     print *, A(i,:), "|", b(i)
  end do
#endif

#ifdef PRINTINFO  
  print *, ""    ! print a blank line
  print *, "Gaussian elimination........"
#endif
  call gaussian_elimination(A,b)

#ifdef PRINTINFO  
  ! print echelon form
  print *, "***********************"
  do i = 1, size(A,1)
     print *, A(i,:), "|", b(i)
  end do

  print *, ""    ! print a blank line
  print *, "back subs......"
#endif
  call backsubstitution(A,b)

#ifdef PRINTINFO  
  ! print the results
  print *, "***********************"
  do i = 1, size(A,1)
     print *, A(i,:), "|", b(i)
  end do

  print *, ""
  print *, "The solution vector is;"
  do i = 1, size(b)
     print *, b(i)
  end do
#endif


  !Solving the transposed system and reporting solution
  A(:,:) = reshape((/2, 4, 7, 3, 7, 10, -1, 1, -4/), (/3,3/))
  A = transpose(A)
  b = (/1,3,4/)
  call gaussian_elimination(A,b)
  call backsubstitution(A,b)

#ifdef PRINTINFO
  !Pring results
  print *, ""
  print *, "**** Matrix A is now transposed ****"
  print *, "The solution vector is;"
  do i = 1, size(b)
     print *, b(i)
  end do
#endif


contains

  subroutine gaussian_elimination(A,b)

    real, dimension(:,:), intent(INOUT) :: A
    real, dimension(:), intent(INOUT) :: b
    real :: factor
    integer :: i,j

   ! gaussian elimination
    do j = 1, 2           ! j is column
       do i = j+1, 3       ! i is row
          factor = A(i,j)/A(j,j)
          A(i,:) = A(i,:) - factor*A(j,:)
          b(i) = b(i) - factor*b(j)
       end do
    end do
  end subroutine gaussian_elimination


  subroutine backsubstitution(A,b)
    
    real, dimension(:,:), intent(INOUT) :: A
    real, dimension(:), intent(INOUT) :: b
    real :: factor
    integer :: i,j

   ! doing back substitution
    do j = 3, 2, -1             ! j is column
       do i = j-1, 1, -1        ! i is row
          factor = A(i,j)/A(j,j)
          A(i,:) = A(i,:) - factor*A(j,:)
          b(i) = b(i) - factor*b(j)
       end do
    end do

   ! overwrite the solution vector to b
    do i = 1, size(b)
       b(i) = b(i)/A(i,i)
    end do
  end subroutine backsubstitution
 

end program gauss


