package main

import (
    "bufio"
    "bytes"
    "encoding/csv"
    "encoding/json"
    "fmt"
    "net/http"
    "os"
    "regexp"
    "time"
)

const (
    apiURL           = "https://api.transistor.fm/v1/episodes"
    showID           = "12890"
    csvFilePath      = "./config/scotus.csv"
)

var TRANSISTOR_API_KEY = os.Getenv("TRANSISTOR_API_KEY")

type Episode struct {
    Title    string
    Summary  string
}

func createDraftEpisodesFromCSV(filePath string) ([]Episode, error) {
    file, err := os.Open(filePath)
    if err != nil {
        return nil, err
    }
    defer file.Close()

    var episodes []Episode
    reader := csv.NewReader(bufio.NewReader(file))
    for {
        record, err := reader.Read()
        if err != nil {
            if err == io.EOF {
                break
            }
            return nil, err
        }

        if len(record) < 2 {
            continue
        }

        episodes = append(episodes, Episode{
            Title:   record[0],
            Summary: record[1],
        })
    }
    return episodes, nil
}

func createDraftEpisodeInTransistor(episode Episode) (string, error) {
    episodeData := map[string]string{
        "episode[show_id]":   showID,
        "episode[title]":     episode.Title,
        "episode[summary]":   episode.Summary,
    }

    jsonData, err := json.Marshal(episodeData)
    if err != nil {
        return "", err
    }

    req, err := http.NewRequest("POST", fmt.Sprintf("%s/publish", apiURL), bytes.NewBuffer(jsonData))
    if err != nil {
        return "", err
    }
    req.Header.Set("x-api-key", TRANSISTOR_API_KEY)
    req.Header.Set("Content-Type", "application/json")

    client := &http.Client{}
    resp, err := client.Do(req)
    if err != nil {
        return "", err
    }
    defer resp.Body.Close()

    if resp.StatusCode != 201 {
        return "", fmt.Errorf("failed to create episode: status code %d", resp.StatusCode)
    }

    var response map[string]interface{}
    json.NewDecoder(resp.Body).Decode(&response)
    episodeID, ok := response["id"].(string)
    if !ok {
        return "", fmt.Errorf("invalid response format")
    }

    return episodeID, nil
}

func updateEpisodePublishDate(episodeID, publishedDate string) error {
    endpoint := fmt.Sprintf("%s/%s", apiURL, episodeID)
    episodeData := map[string]string{
        "episode[published_at]": publishedDate,
    }

    jsonData, err := json.Marshal(episodeData)
    if err != nil {
        return err
    }

    req, err := http.NewRequest("PATCH", endpoint, bytes.NewBuffer(jsonData))
    if err != nil {
        return err
    }
    req.Header.Set("x-api-key", TRANSISTOR_API_KEY)
    req.Header.Set("Content-Type", "application/json")

    client := &http.Client{}
    resp, err := client.Do(req)
    if err != nil {
        return err
    }
    defer resp.Body.Close()

    if resp.StatusCode != 200 {
        return fmt.Errorf("failed to update episode: status code %d", resp.StatusCode)
    }

    return nil
}

func processEpisodes() error {
    episodes, err := createDraftEpisodesFromCSV(csvFilePath)
    if err != nil {
        return err
    }

    argumentDateRegex := regexp.MustCompile(`\[Arg:\s(\d{2}\.\d{2}\.\d{4})\]`)
    for _, episode := range episodes {
        episodeID, err := createDraftEpisodeInTransistor(episode)
        if err != nil {
            fmt.Printf("Failed to create episode '%s': %v\n", episode.Title, err)
            continue
        }

        matches := argumentDateRegex.FindStringSubmatch(episode.Title)
        if len(matches) > 1 {
            argumentDate, err := time.Parse("01.02.2006", matches[1])
            if err != nil {
                fmt.Printf("Error parsing argument date for episode '%s': %v\n", episode.Title, err)
                continue
            }
            publishedDate := argumentDate.Format(time.RFC3339)

            err = updateEpisodePublishDate(episodeID, publishedDate)
            if err != nil {
                fmt.Printf("Failed to update publish date for episode '%s': %v\n", episode.Title, err)
            } else {
                fmt.Printf("Publish date updated for episode '%s'\n", episode.Title)
            }
        } else {
            fmt.Printf("Argument date not found for episode '%s'\n", episode.Title)
        }
    }

    return nil
}

func main() {
    if err := processEpisodes(); err != nil {
        fmt.Println("Error processing episodes:", err)
    }
}
