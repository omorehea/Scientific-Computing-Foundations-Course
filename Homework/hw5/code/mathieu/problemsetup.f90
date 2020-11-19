! File: problemsetup.f90
! Author: Ian May
! Purpose: Define problem specific information
! Comments: The read_initFile* subroutines were taken from Prof. Lee's
!           Newton's method example code

module problemsetup

  use utility, only : dp, maxFileLen, maxStrLen
  
  implicit none
  
  integer, save :: Npts    ! Number of grid points to use in the discretization
  real (dp), save :: qIdx  ! Index of Mathieu functions we are looking for
  character(len=maxStrLen), save :: runName, outFile ! Name of the run and the output file the code should write

contains

  ! subroutine: problemsetup_Init
  ! purpose: Set module variables to values defined in an input file
  ! inputs: inFile -- String with name of input file to be read
  ! outputs: <none>
  subroutine problemsetup_Init(inFile)
    implicit none
    character(len=*), intent(in) :: inFile
    ! Fill in default values
    Npts = 31
    qIdx = 36.0_dp
    ! Read problem resolution
    call read_initFileInt(inFile,'num_points',Npts)
    ! Read the Mathieu index
    call read_initFileReal(inFile,'q_index',qIdx)
    ! Set the name of the run
    call read_initFileChar(inFile,'run_name',runName)
    print *, 'Running problem: ', runName
    ! Set the output file, note that // does string concatenation
    outFile = 'data/' // trim(runName) // '.dat'
  end subroutine problemsetup_Init

  ! subroutine: read_initFileReal
  ! purpose: Pull one real value from an input file
  ! inputs: inFile -- String holding the name of the input file
  !         varName -- String that names the variable, this must be first entry on a line
  ! outputs: varValue -- Real value that will hold the result from the input file
  subroutine read_initFileReal(inFile,varName,varValue)

    implicit none
    character(len=*),intent(IN) :: inFile,varName
    real (dp), intent(OUT)      :: varValue

    integer :: i,openStatus,inputStatus
    real :: simInitVars
    character(len=maxStrLen) :: simCharVars
    integer :: pos1,pos2

    open(unit = 10, file=inFile, status='old',IOSTAT=openStatus,FORM='FORMATTED',ACTION='READ')

    do i=1,maxFileLen
      read(10, FMT = 100, IOSTAT=inputStatus) simCharVars
      pos1 = index(simCharVars,varName)
      pos2 = pos1+len_trim(varName)
      if (pos2 > len_trim(varName)) then
        read(simCharVars(pos2+1:),*)simInitVars
        !print*,varName,len_trim(varName)
        !print*,simCharVars
        !print*,pos1,pos2,simCharVars(pos2+1:),simInitVars;stop
        varValue = simInitVars
      endif
    end do

    close(10)

100 FORMAT(A, 1X, F3.1)

  end subroutine read_initFileReal

  ! subroutine: read_initFileInt
  ! purpose: Pull one integer value from an input file
  ! inputs: inFile -- String holding the name of the input file
  !         varName -- String that names the variable, this must be first entry on a line
  ! outputs: varValue -- Integer value that will hold the result from the input file
  subroutine read_initFileInt(inFile,varName,varValue)

    implicit none
    character(len=*),intent(IN) :: inFile,varName
    integer, intent(OUT) :: varValue

    integer :: i,openStatus,inputStatus
    integer :: simInitVars
    character(len=maxStrLen) :: simCharVars
    integer :: pos1,pos2

    open(unit = 11, file=inFile, status='old',IOSTAT=openStatus,FORM='FORMATTED',ACTION='READ')

    do i=1,maxFileLen
      read(11, FMT = 101, IOSTAT=inputStatus) simCharVars
      pos1 = index(simCharVars,varName)
      pos2 = pos1+len_trim(varName)
      if (pos2 > len_trim(varName)) then
        read(simCharVars(pos2+1:),*)simInitVars
        varValue = simInitVars
      endif
    end do

    close(11)

101 FORMAT(A, 1X, I5)

  end subroutine read_initFileInt

  ! subroutine: read_initFileChar
  ! purpose: Pull one string with no spaces from an input file
  ! inputs: inFile -- String holding the name of the input file
  !         varName -- String that names the variable, this must be first entry on a line
  ! outputs: varValue -- String that will hold the result from the input file
  subroutine read_initFileChar(inFile,varName,varValue)

    implicit none
    character(len=*),intent(IN)  :: inFile,varName
    character(len=*),intent(OUT) :: varValue

    integer :: i,openStatus,inputStatus
    character(len=maxStrLen) :: simInitVars
    character(len=maxStrLen) :: simCharVars
    integer :: pos1,pos2

    open(unit = 13, file=inFile, status='old',IOSTAT=openStatus,FORM='FORMATTED',ACTION='READ')

    do i=1,maxFileLen
      read(13, FMT = 103, IOSTAT=inputStatus) simCharVars
      pos1 = index(simCharVars,varName)
      pos2 = pos1+len_trim(varName)

      if (pos2 > len_trim(varName)) then
        read(simCharVars(pos2+1:),*)simInitVars
        varValue = simInitVars
      endif
    end do

    close(13)

103 FORMAT(A, 1X, A)

  end subroutine read_initFileChar

end module problemsetup
