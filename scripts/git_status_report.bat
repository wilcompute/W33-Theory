@echo off
setlocal
set OUT=git_status_report.txt
cd /d "%~dp0.."
> %OUT% echo ==== git status --porcelain ====
git status --porcelain -u >> %OUT%
>> %OUT% echo.
>> %OUT% echo ==== git log -1 --pretty=format:%%H %%an %%ad %%s --date=iso ====
git log -1 --pretty=format:"%%H %%an %%ad %%s" --date=iso >> %OUT%
>> %OUT% echo.
>> %OUT% echo ==== git log -1 --stat ====
git log -1 --stat >> %OUT%
>> %OUT% echo.
>> %OUT% echo ==== git show --name-only --pretty=format:"" HEAD ====
git show --name-only --pretty=format:"" HEAD >> %OUT%
>> %OUT% echo.
type %OUT%
endlocal
