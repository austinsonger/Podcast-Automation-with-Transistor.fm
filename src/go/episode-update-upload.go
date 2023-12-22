package main

import (
    "bufio"
    "bytes"
    "encoding/csv"
    "encoding/json"
    "fmt"
    "io/ioutil"
    "mime/multipart"
    "net/http"
    "os"
    "path/filepath"
)

const (
    transistorAPIURL = "https://api.transistor.fm/v1/episodes"
    imgurAPIURL      = "https://api.imgur.com/3/upload"
    caseBasePath     = "../2023/"
    dryRun           = true
)

type EpisodeData struct {
    Title       string `json:"title"`
    Summary     string `json:"summary"`
    AudioURL    string `json:"audio_url,omitempty"`
    ImageURL    string `json:"image_url,omitempty"`
}

func findFirstFileInDirectory(directoryPath string, fileTypes []string) (string, error) {
    for _, fileType := range fileTypes {
        files, err := filepath.Glob(filepath.Join(directoryPath, fmt.Sprintf("*.%s", fileType)))
        if err != nil {
            return "", err
        }
        if len(files) > 0 {
            return files[0], nil
        }
    }
    return "", fmt.Errorf("no files found")
}

func authorizeAndUploadAudio(episodeID, audioFilePath string) (string, error) {
    // Step 1: Authorize Audio Upload
    authURL := fmt.Sprintf("%s/%s/audio_upload", transistorAPIURL, episodeID)
    req, err := http.NewRequest("POST", authURL, nil)
    if err != nil {
        return "", err
    }
    req.Header.Set("x-api-key", os.Getenv("TRANSISTOR_API_KEY"))
    req.Header.Set("Content-Type", "application/json")

    client := &http.Client{}
    authResp, err := client.Do(req)
    if err != nil {
        return "", err
    }
    defer authResp.Body.Close()

    var authResponse map[string]interface{}
    err = json.NewDecoder(authResp.Body).Decode(&authResponse)
    uploadURL, ok := authResponse["data"].(map[string]interface{})["url"].(string)
    if !ok {
        return "", fmt.Errorf("authorization failed")
    }

    // Step 2: Upload Audio File
    audioFile, err := os.Open(audioFilePath)
    if err != nil {
        return "", err
    }
    defer audioFile.Close()

    uploadResp, err := http.Post(uploadURL, "audio/mpeg", audioFile)
    if err != nil {
        return "", err
    }
    defer uploadResp.Body.Close()

    if uploadResp.StatusCode != http.StatusOK {
        return "", fmt.Errorf("error uploading audio file: %s", uploadResp.Status)
    }

    return uploadURL, nil
}

func authorizeAndUploadImage(episodeID, imageFilePath string) (string, error) {
    // Step 1: Prepare image file
    imageFile, err := os.Open(imageFilePath)
    if err != nil {
        return "", err
    }
    defer imageFile.Close()

    body := &bytes.Buffer{}
    writer := multipart.NewWriter(body)
    part, err := writer.CreateFormFile("image", filepath.Base(imageFilePath))
    if err != nil {
        return "", err
    }
    _, err = io.Copy(part, imageFile)
    if err != nil {
        return "", err
    }
    writer.Close()

    // Step 2: Upload Image
    req, err := http.NewRequest("POST", imgurAPIURL, body)
    if err != nil {
        return "", err
    }
    req.Header.Set("Authorization", fmt.Sprintf("Client-ID %s", os.Getenv("IMGUR_CLIENT_ID")))
    req.Header.Set("Content-Type", writer.FormDataContentType())

    client := &http.Client{}
    uploadResp, err := client.Do(req)
    if err != nil {
        return "", err
    }
    defer uploadResp.Body.Close()

    var uploadResponse map[string]interface{}
    err = json.NewDecoder(uploadResp.Body).Decode(&uploadResponse)
    imageURL, ok := uploadResponse["data"].(map[string]interface{})["link"].(string)
    if !ok {
        return "", fmt.Errorf("image upload failed")
    }

    return imageURL, nil
}

func updateEpisode(episodeID, caseID string, data EpisodeData) (json.RawMessage, error) {
    if dryRun {
        fmt.Printf("Dry run: Would update episode %s with data: %v\n", episodeID, data)
        return json.RawMessage(`{"message": "Dry run, no update made"}`), nil
    }

    payload, err := json.Marshal(map[string]EpisodeData{"episode": data})
    if err != nil {
        return nil, err
    }

    updateURL := fmt.Sprintf("%s/%s", transistorAPIURL, episodeID)
    req, err := http.NewRequest("PATCH", updateURL, bytes.NewBuffer(payload))
    if err != nil {
        return nil, err
    }
    req.Header.Set("x-api-key", os.Getenv("TRANSISTOR_API_KEY"))
    req.Header.Set("Content-Type", "application/json")

    client := &http.Client{}
    updateResp, err := client.Do(req)
    if err != nil {
        return nil, err
    }
    defer updateResp.Body.Close()

    var response json.RawMessage
    err = json.NewDecoder(updateResp.Body).Decode(&response)
    return response, err
}

func processCSV(csvPath string) error {
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
        episodeID := row[0] // Assuming 'Episode ID' is the first column
        caseID := row[1]   // Assuming 'Case ID' is the second column

        audioFile, err := findFirstFileInDirectory(filepath.Join(caseBasePath, caseID, "audio"), []string{"mp3"})
        if err != nil {
            fmt.Println("Error finding audio file:", err)
            continue
        }
        imageFile, err := findFirstFileInDirectory(filepath.Join(caseBasePath, caseID, "images"), []string{"jpg", "jpeg", "png"})
        if err != nil {
            fmt.Println("Error finding image file:", err)
            continue
        }

        audioURL, err := authorizeAndUploadAudio(episodeID, audioFile)
        if err != nil {
            fmt.Println("Error uploading audio:", err)
            continue
        }
        imageURL, err := authorizeAndUploadImage(episodeID, imageFile)
        if err != nil {
            fmt.Println("Error uploading image:", err)
            continue
        }

        episodeData := EpisodeData{
            Title:    row[2], // Assuming 'Title' is the third column
            Summary:  row[3], // Assuming 'Summary' is the fourth column
            AudioURL: audioURL,
            ImageURL: imageURL,
        }

        response, err := updateEpisode(episodeID, caseID, episodeData)
        if err != nil {
            fmt.Println("Error updating episode:", err)
            continue
        }
        fmt.Printf("Episode updated: %s\n", string(response))
    }
    return nil
}

func main() {
    csvFilePath := "./config/scotus.csv"

    if err := processCSV(csvFilePath); err != nil {
        fmt.Println("Error processing CSV file:", err)
    }
}
