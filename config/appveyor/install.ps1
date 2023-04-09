# Script to set up tests on AppVeyor Windows.

$Dependencies = ""
$Dependencies = ${Dependencies} -split " "

# Use cmd here since Invoke-Expression will raise NativeCommandError and want
# stdout and stderr to not buffer until command completion.
cmd /c "git clone https://github.com/log2timeline/l2tdevtools.git ..\l2tdevtools 2>&1"

If ($env:APPVEYOR_REPO_BRANCH -eq "main")
{
	$Track = "stable"
}
Else
{
	$Track = $env:APPVEYOR_REPO_BRANCH
}
New-Item -ItemType "directory" -Name "dependencies"

$env:PYTHONPATH = "..\l2tdevtools"

# Use cmd here since Invoke-Expression will raise NativeCommandError and want
# stdout and stderr to not buffer until command completion.
cmd /c "& '${env:PYTHON}\python.exe' ..\l2tdevtools\tools\update.py --download-directory dependencies --machine-type ${env:MACHINE_TYPE} --msi-targetdir ${env:PYTHON} --track ${env:L2TBINARIES_TRACK} ${Dependencies} 2>&1"

