$ErrorActionPreference = 'Stop'
# Find the TF card by identity (never trust the disk number), then carve p9.
$card = Get-Disk | Where-Object { $_.FriendlyName -eq 'Generic STORAGE DEVICE' -and [int64]$_.Size -eq [int64]62534975488 -and $_.BusType -eq 'USB' }
if (-not $card) { throw 'TF card (Generic STORAGE DEVICE 62.5GB USB) not found' }
$num = $card.Number
Write-Host "TF card at disk $num"
$dev = "\\.\PHYSICALDRIVE$num"
$src = [System.IO.File]::Open($dev, 'Open', 'Read', 'ReadWrite')
$src.Seek(11380736 * 512, 'Begin') | Out-Null
$dst = [System.IO.File]::Create('H:\ugos\base\out\p9-carve.img')
$buf = New-Object byte[] 4194304
$remaining = 1073741824
while ($remaining -gt 0) {
    $n = $src.Read($buf, 0, [Math]::Min($buf.Length, $remaining))
    if ($n -le 0) { break }
    $dst.Write($buf, 0, $n)
    $remaining -= $n
}
$dst.Close(); $src.Close()
Write-Host "carved p9 ok from $dev"
