package main

import (
    "bufio"
    "encoding/csv"
    "encoding/json"
    "fmt"
    "io"
    "net/http"
    "os"
)

type EpisodeData struct {
    Title   string `json:"title"`
    Summary string `json:"summary"`
}

type EpisodeResponse struct {
    Data struct {
        ID string `json:"id"`
    } `json:"data"`
}

func createDraftEpisode(data EpisodeData, apiURL, apiKey, showID string) (*EpisodeResponse, error) {
    payload := map[string]interface{}{
        "episode": map[string]string{
            "show_id":     showID,
            "title":       data.Title,
            "description": data.Summary,
        },
    }

    jsonData, err := json.Marshal(payload)
    if err != nil {
        return nil, err
    }

    client := &http.Client{}
    req, err := http.NewRequest("POST", apiURL, bytes.NewBuffer(jsonData))
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

    var response EpisodeResponse
    err = json.NewDecoder(resp.Body).Decode(&response)
    return &response, err
}

func processCSV(csvPath, apiURL, apiKey, showID string) error {
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

    updatedRows := make([][]string, 0, len(rows))
    updatedRows = append(updatedRows, append(rows[0], "Episode ID")) // Add header

    for _, row := range rows[1:] {
        episodeData := EpisodeData{
            Title:   row[0], // Assuming 'Title' is the first column
            Summary: row[1], // Assuming 'Summary' is the second column
        }

        response, err := createDraftEpisode(episodeData, apiURL, apiKey, showID)
        if err != nil {
            fmt.Println("Error creating draft episode:", err)
            continue
        }

        updatedRow := append(row, response.Data.ID)
        updatedRows = append(updatedRows, updatedRow)
    }

    outputFile, err := os.Create(csvPath)
    if err != nil {
        return err
    }
    defer outputFile.Close()

    writer := csv.NewWriter(outputFile)
    writer.WriteAll(updatedRows)
    writer.Flush()

    return nil
}

func main() {
    csvFilePath := "./config/scotus.csv"
    transistorAPIURL := "https://api.transistor.fm/v1/episodes"
    transistorAPIKey := os.Getenv("TRANSISTOR_API_KEY")
    transistorShowID := os.Getenv("TRANSISTOR_SHOW_ID")

    if err := processCSV(csvFilePath, transistorAPIURL, transistorAPIKey, transistorShowID); err != nil {
        fmt.Println("Error processing CSV file:", err)
    }
}
