@echo off
REM prepare_push.bat <remote-url>
IF "%1"=="" (
  echo No remote URL provided.
  echo Usage: prepare_push.bat https://github.com/username/repo.git
  echo Alternatively run:
  echo   git remote add origin https://github.com/username/repo.git
  echo   git branch -M main
  echo   git push -u origin main
  exit /b 1
)
git remote add origin %1
git branch -M main
git push -u origin main
