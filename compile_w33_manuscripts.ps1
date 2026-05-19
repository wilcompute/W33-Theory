param(
    [int]$Passes = 3,
    [switch]$IncludeLegacyW36
)

$ErrorActionPreference = 'Stop'

function Get-LogWarningSummary {
    param([Parameter(Mandatory = $true)][string]$LogPath)

    if (-not (Test-Path $LogPath)) {
        return $null
    }

    $pdfStringWarnings = (Select-String -Path $LogPath -Pattern 'Token not allowed in a PDF string' | Measure-Object).Count
    $duplicateLabels = (Select-String -Path $LogPath -Pattern 'multiply defined' | Measure-Object).Count
    $undefinedRefs = (Select-String -Path $LogPath -Pattern 'undefined references|Reference `.*'' on page .* undefined|Citation `.*'' undefined' | Measure-Object).Count

    $boxWarnings = Select-String -Path $LogPath -Pattern 'Overfull \\hbox|Overfull \\vbox'
    $largestBox = $null
    foreach ($match in $boxWarnings) {
        if ($match.Line -match 'Overfull \\[hv]box \(([0-9.]+)pt') {
            $points = [double]$matches[1]
            if (-not $largestBox -or $points -gt $largestBox.Points) {
                $largestBox = [pscustomobject]@{
                    Points = $points
                    Line   = $match.Line.Trim()
                }
            }
        }
    }

    return [pscustomobject]@{
        PdfStringWarnings = $pdfStringWarnings
        DuplicateLabels   = $duplicateLabels
        UndefinedRefs     = $undefinedRefs
        LargestBox        = $largestBox
    }
}

function Get-MiKTeXTool {
    param([Parameter(Mandatory = $true)][string]$ToolName)

    $candidates = @(
        (Join-Path $env:LOCALAPPDATA 'Programs\MiKTeX\miktex\bin\x64'),
        (Join-Path $env:ProgramFiles 'MiKTeX\miktex\bin\x64'),
        (Join-Path ${env:ProgramFiles(x86)} 'MiKTeX\miktex\bin\x64')
    ) | Where-Object { $_ -and (Test-Path $_) }

    foreach ($dir in $candidates) {
        $toolPath = Join-Path $dir $ToolName
        if (Test-Path $toolPath) {
            return $toolPath
        }
    }

    $command = Get-Command $ToolName -ErrorAction SilentlyContinue
    if ($command) {
        return $command.Source
    }

    throw "Could not locate $ToolName. Install MiKTeX or add it to PATH."
}

$pdflatex = Get-MiKTeXTool -ToolName 'pdflatex.exe'
$initexmf = Get-MiKTeXTool -ToolName 'initexmf.exe'
$bibtex = Get-MiKTeXTool -ToolName 'bibtex.exe'

Write-Host '================================================'
Write-Host ' W(3,3) Manuscript Build'
Write-Host '================================================'
Write-Host "Using pdflatex: $pdflatex"
Write-Host "Using bibtex:   $bibtex"

& $initexmf --enable-installer | Out-Null

$targets = @('w33_paper', 'W33_FOR_EVERYONE')
if ($IncludeLegacyW36) {
    $targets += 'W36_PAPER'
}

foreach ($base in $targets) {
    $texFile = "$base.tex"
    if (-not (Test-Path $texFile)) {
        throw "Missing source file: $texFile"
    }

    Write-Host ''
    Write-Host "Compiling $texFile ..."

    foreach ($pass in 1..$Passes) {
        $logFile = "$base.pass$pass.log"
        & $pdflatex -interaction=nonstopmode -file-line-error $texFile *> $logFile
        if ($LASTEXITCODE -ne 0) {
            throw "pdflatex failed on $texFile pass $pass. See $logFile"
        }
    }

    $auxFile = "$base.aux"
    if (Test-Path $auxFile) {
        $needsBib = Select-String -Path $auxFile -Pattern '\\citation|\\bibdata' -Quiet
        if ($needsBib) {
            $bibLog = "$base.bibtex.log"
            & $bibtex $base *> $bibLog
            if ($LASTEXITCODE -eq 0) {
                foreach ($pass in ($Passes + 1)..($Passes + 2)) {
                    $logFile = "$base.pass$pass.log"
                    & $pdflatex -interaction=nonstopmode -file-line-error $texFile *> $logFile
                    if ($LASTEXITCODE -ne 0) {
                        throw "pdflatex failed on $texFile post-bibtex pass $pass. See $logFile"
                    }
                }
            }
        }
    }

    $pdf = Get-Item "$base.pdf"
    Write-Host ("  -> {0} ({1:N2} KB)" -f $pdf.Name, ($pdf.Length / 1KB))

    $latestLog = "${base}.pass$Passes.log"
    $summary = Get-LogWarningSummary -LogPath $latestLog
    if ($summary) {
        Write-Host ("     warnings: pdf-strings={0}, duplicate-labels={1}, undefined-refs={2}" -f $summary.PdfStringWarnings, $summary.DuplicateLabels, $summary.UndefinedRefs)
        if ($summary.LargestBox) {
            Write-Host ("     largest box: {0}" -f $summary.LargestBox.Line)
        }
    }
}

Write-Host ''
Write-Host 'Done.'

exit 0
