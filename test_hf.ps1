for ($i=0; $i -lt 30; $i++) {
    try {
        $res = Invoke-RestMethod -Uri "https://fathiarasy-smartwaste.hf.space/api/debug-files" -Method Get -TimeoutSec 10
        if ($res.cwd) {
            $res | ConvertTo-Json -Depth 10
            exit 0
        }
    } catch {
        Write-Host "Waiting..."
    }
    Start-Sleep -Seconds 10
}
