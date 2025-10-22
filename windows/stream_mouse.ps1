# Load the required .NET assembly
Add-Type -AssemblyName System.Windows.Forms

# Initialize previous position and time
$prevPos = [System.Windows.Forms.Cursor]::Position
$prevTime = Get-Date

while ($true) {
    $pos = [System.Windows.Forms.Cursor]::Position
    $now = Get-Date

    # Calculate distance moved (Pythagorean distance)
    $dx = $pos.X - $prevPos.X
    $dy = $pos.Y - $prevPos.Y
    $distance = [math]::Sqrt(($dx * $dx) + ($dy * $dy))

    # Calculate elapsed time (in seconds)
    $dt = ($now - $prevTime).TotalSeconds
    $speed = if ($dt -ne 0) { $distance / $dt } else { 0 }

    # Display results
    Write-Host ("X: {0}  Y: {1}  Speed: {2,6:N1} px/s" -f $pos.X, $pos.Y, $speed) -NoNewline
    Start-Sleep -Milliseconds 100
    Write-Host "`r" -NoNewline

    # Update previous values
    $prevPos = $pos
    $prevTime = $now
}
