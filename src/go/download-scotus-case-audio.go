package main

import (
    "bufio"
    "encoding/csv"
    "fmt"
    "io"
    "os"
    "os/exec"
    "path/filepath"
    "strings"
)

func main() {
    // Load the CSV file
    file, err := os.Open("./config/scotus.csv") // Replace with your actual file path
    if err != nil {
        fmt.Println("Error opening CSV file:", err)
        return
    }
    defer file.Close()

    reader := csv.NewReader(bufio.NewReader(file))

    // Base directory for the year
    baseDir := "../2023/"

    // Iterate over each row to generate and execute the curl commands
    for {
        record, err := reader.Read()
        if err == io.EOF {
            break
        }
        if err != nil {
            fmt.Println("Error reading CSV record:", err)
            continue
        }

        // Assuming 'Case ID' is in the first column
        caseID := strings.TrimSpace(record[0])

        // Full path for the case directory
        caseDir := filepath.Join(baseDir, caseID)

        // Create directory for the case if it doesn't exist
        audioDir := filepath.Join(caseDir, "audio")
        if err := os.MkdirAll(audioDir, os.ModePerm); err != nil {
            fmt.Println("Error creating directory:", err)
            continue
        }

        // Generate the curl command
        curlCommand := fmt.Sprintf("curl https://www.supremecourt.gov/media/audio/mp3files/%s.mp3 --output %s/audio/%s.mp3", caseID, caseDir, caseID)

        // Check if the file already exists
        filePath := filepath.Join(audioDir, fmt.Sprintf("%s.mp3", caseID))
        if _, err := os.Stat(filePath); os.IsNotExist(err) {
            // File doesn't exist, execute the curl command
            cmd := exec.Command("bash", "-c", curlCommand)
            if err := cmd.Run(); err != nil {
                fmt.Println("Error executing curl command:", err)
            }
        } else {
            // File already exists, skip downloading
            fmt.Println("Skipping download, file already exists:", filePath)
        }
    }
}
