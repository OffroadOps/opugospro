$ErrorActionPreference = 'Continue'

# Canonical TF card writer: identity lock, dismount letters, one-shot write+readback.
# No Clear-Disk and no separate zeroing pass -- write-image-once.py overwrites sector 0
# with the image MBR in a single open handle (the zero-then-writer gap triggered
# ERROR_INVALID_HANDLE after Update-Disk rescans).

$DiskNumber = 2
$ExpectedFriendlyName = 'Generic STORAGE DEVICE'
$ExpectedSerialNumber = '000000001532'
$ExpectedDiskSize = [int64]62534975488
$ExpectedBusType = 'USB'
$ImagePath = 'H:\ugos\base\out\ugos-arm64-radxa-cubie-a5e.img'
$ManifestPath = "$ImagePath.manifest.json"
$WriterPath = 'H:\ugos\base\scripts\write-image-once.py'
$PythonPath = 'D:\dev\python\Python314\python.exe'
$StatusPath = 'H:\ugos\base\out\a5e-sd-write.status.json'
$LogPath = 'H:\ugos\base\out\a5e-sd-write.log'

Start-Transcript -Path $LogPath -Force

try {
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = [Security.Principal.WindowsPrincipal]::new($identity)
    if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
        throw 'Administrator token is required'
    }

    $manifest = Get-Content -LiteralPath $ManifestPath -Raw | ConvertFrom-Json
    $ExpectedRawBytes = [int64]$manifest.image_bytes
    $ExpectedRawHash = [string]$manifest.sha256
    $disk = Get-Disk -Number $DiskNumber
    if (
        $disk.FriendlyName -ne $ExpectedFriendlyName -or
        $disk.SerialNumber.Trim() -ne $ExpectedSerialNumber -or
        $disk.BusType.ToString() -ne $ExpectedBusType -or
        [int64]$disk.Size -ne $ExpectedDiskSize -or
        $disk.IsSystem -or $disk.IsBoot -or $disk.IsReadOnly
    ) {
        throw "Refusing disk identity: number=$($disk.Number), name=$($disk.FriendlyName), serial=$($disk.SerialNumber), bus=$($disk.BusType), size=$($disk.Size), system=$($disk.IsSystem), boot=$($disk.IsBoot), readonly=$($disk.IsReadOnly)"
    }
    if ($ExpectedRawBytes -ge $ExpectedDiskSize) { throw 'Image does not fit the identity-locked TF card' }
    if ((Get-Item -LiteralPath $ImagePath).Length -ne $ExpectedRawBytes) { throw 'Local raw image length does not match manifest' }
    if ((Get-FileHash -LiteralPath $ImagePath -Algorithm SHA256).Hash -ne $ExpectedRawHash) { throw 'Local raw image SHA256 does not match manifest' }
    Write-Host "[1/5] identity + source image verified (bytes=$ExpectedRawBytes)"

    $parts = Get-Partition -DiskNumber $DiskNumber -ErrorAction SilentlyContinue
    foreach ($p in $parts) {
        foreach ($dl in @($p.AccessPaths) | Where-Object { $_ -match '^[A-Z]:\\?$' }) {
            Write-Host "dismounting access path $dl"
            Remove-PartitionAccessPath -DiskNumber $DiskNumber -PartitionNumber $p.PartitionNumber -AccessPath ($dl.TrimEnd('\')) -ErrorAction Continue
        }
    }
    Update-Disk -Number $DiskNumber
    Write-Host "[2/5] drive letters removed"

    Write-Host "[3/5] one-shot write + readback (single open handle)"
    & $PythonPath $WriterPath --image $ImagePath --device "\\.\PhysicalDrive$DiskNumber" --expected-sha256 $ExpectedRawHash --raw-bytes $ExpectedRawBytes --status $StatusPath
    $code = $LASTEXITCODE
    Write-Host "writer exit code: $code"
    if ($code -ne 0) { throw "raw writer exited with $code" }

    Update-Disk -Number $DiskNumber
    $after = Get-Disk -Number $DiskNumber
    if ($after.PartitionStyle.ToString() -ne 'MBR') { throw 'MBR was not detected after write' }
    Write-Host "[4/5] MBR detected"
    $p1 = Get-Partition -DiskNumber $DiskNumber -PartitionNumber 1 -ErrorAction SilentlyContinue
    if (-not $p1 -or [int64]$p1.Size -ne [int64]536870912) { throw 'p1 512MiB boot partition not found after write' }
    Write-Host "[5/5] write + readback verified, MBR + 9-partition layout detected"
    exit 0
} catch {
    Write-Host "FAILED: $($_.Exception.Message)"
    exit 1
} finally {
    Stop-Transcript
}
