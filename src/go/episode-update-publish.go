package main

import (
    "bufio"
    "encoding/csv"
    "encoding/json"
    "fmt"
    "net/http"
    "os"
    "time"
)

type Config struct {
    CSVFilePath       string
    TransistorAPIURL  string
    TransistorAPIKey  string
}

func LoadConfig() Config {
    return Config{
        CSVFilePath:       "./config/scotus.csv",
        TransistorAPIURL:  "https://api.transistor.fm/v1/episodes",
        TransistorAPIKey:  os.Getenv("TRANSISTOR_API_KEY"),
    }
}

func publishEpisode(episodeID, apiURL, apiKey string) (json.RawMessage, error) {
    url := fmt.Sprintf("%s/%s/publish", apiURL, episodeID)

    client := &http.Client{}
    req, err := http.NewRequest("POST", url, nil)
    if err != nil {
        return nil, err
    }
    req.Header.Set("x-api-key", apiKey)
    req.Header.Set("Content-Type", "application/json")

    resp, err := client.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()

    var response json.RawMessage
    err = json.NewDecoder(resp.Body).Decode(&response)
    return response, err
}

func processCSV(csvPath, apiURL, apiKey string) error {
    file, err := os.Open(csvPath)
    if err != nil {
        return err
    }
    defer file.Close()

    reader := csv.NewReader(bufio.NewReader(file))
    rows, err := reader.ReadAll()
    if err != nil {
        return err
    }

    for _, row := range rows[1:] {
        argumentDate, err := time.Parse("2006-01-02", row[1]) // Assuming 'Argument Date' is the second column
        if err != nil {
            fmt.Println("Error parsing date:", err)
            continue
        }

        if row[2] != "" && argumentDate.Before(time.Now()) && row[3] != "yes" { // Assuming 'Published' is the fourth column
            response, err := publishEpisode(row[2], apiURL, apiKey) // Assuming 'Episode ID' is the third column
            if err != nil {
                fmt.Println("Error publishing episode:", err)
                continue
            }
            fmt.Printf("Episode %s published: %s\n", row[2], string(response))
        }
    }
    return nil
}

func main() {
    config := LoadConfig()

    if err := processCSV(config.CSVFilePath, config.TransistorAPIURL, config.TransistorAPIKey); err != nil {
        fmt.Println("Error processing CSV file:", err)
    }
}
