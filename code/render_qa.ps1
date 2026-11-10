$ErrorActionPreference = 'Stop'
$taskRoot = Split-Path -Parent $PSScriptRoot
$qaDirectory = Join-Path $taskRoot 'qa'
New-Item -ItemType Directory -Path $qaDirectory -Force | Out-Null
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    $documentNames = @('Main_Manuscript', 'ESM_1', 'ESM_2')
    if (Test-Path -LiteralPath (Join-Path $taskRoot 'Cover_Letter.docx')) { $documentNames += 'Cover_Letter' }
    foreach ($name in $documentNames) {
        $doc = $word.Documents.Open((Join-Path $taskRoot ($name + '.docx')), $false, $true)
        try {
            $doc.Repaginate()
            $doc.ExportAsFixedFormat((Join-Path $taskRoot ('qa\' + $name + '.pdf')), 17)
            Write-Output ($name + ': ' + $doc.ComputeStatistics(2) + ' pages')
        } finally { $doc.Close(0) }
    }
} finally { $word.Quit() }

Copy-Item -LiteralPath (Join-Path $qaDirectory 'ESM_1.pdf') -Destination (Join-Path $taskRoot 'ESM_1.pdf') -Force

Copy-Item -LiteralPath (Join-Path $qaDirectory 'ESM_2.pdf') -Destination (Join-Path $taskRoot 'ESM_2.pdf') -Force
