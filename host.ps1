$predictionUrl = "https://tf2023.cognitiveservices.azure.com/customvision/v3.0/Prediction/4d43e701-bbc8-4397-b8c4-c456f82719ea/classify/iterations/Iteration3/image"
$predictionKey = "50fa53c6982c4c58b3a42bb13f71946a"

# Path to the image file
$imagePath = "C:/Users/abhyu/Documents/TF/dataset/test/test/AppleScab2.JPG"
$imageName = [System.IO.Path]::GetFileName($imagePath)

# Read the image file as bytes
$imageBytes = [System.IO.File]::ReadAllBytes($imagePath)



# Create headers
$headers = @{
    "Prediction-Key" = $predictionKey
    "Content-Type"   = "application/octet-stream"
}



write-host "Analyzing image: $imagename"
try {
    $result = Invoke-RestMethod -Method Post -Uri $predictionUrl -Headers $headers -Body $imageBytes
    if ($result.predictions -ne $null) {
        # Sort predictions by probability in descending order
        $sortedPredictions = $result.predictions | Sort-Object -Property probability -Descending
        Write-Host "Top Prediction:"
        Write-Host ("Tag: $($sortedPredictions[0].tagName), Confidence: $($sortedPredictions[0].probability*100)%")
    }
    else {
        Write-Host "No predictions generated for the image."
    }
}
catch {
    Write-Host "Error: $_"
}
