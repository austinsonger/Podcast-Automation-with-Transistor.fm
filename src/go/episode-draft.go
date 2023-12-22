package main

import (
	"bufio"
	"bytes"
	"encoding/csv"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
)

type Config struct {
	CSVFilePath        string
	TRANSISTOR_API_URL string
	TRANSISTOR_API_KEY string
	TRANSISTOR_SHOW_ID string
}

func LoadConfig() Config {
	return Config{
		CSVFilePath:        "./config/go/scotus.csv",
		TRANSISTOR_API_URL: "https://api.transistor.fm/v1/episodes",
		TRANSISTOR_API_KEY: os.Getenv("TRANSISTOR_API_KEY"),
		TRANSISTOR_SHOW_ID: "12890",
	}
}

type EpisodeData struct {
	Title   string `json:"title"`
	Summary string `json:"summary"`
}

type EpisodeResponse struct {
	Data struct {
		ID string `json:"id"`
	} `json:"data"`
}

func createDraftEpisode(data EpisodeData, TRANSISTOR_API_URL, TRANSISTOR_API_KEY, TRANSISTOR_SHOW_ID string) (*EpisodeResponse, error) {
	payload := map[string]interface{}{
		"episode": map[string]string{
			"show_id":     TRANSISTOR_SHOW_ID,
			"title":       data.Title,
			"description": data.Summary,
		},
	}

	jsonData, err := json.Marshal(payload)
	if err != nil {
		return nil, err
	}

	client := &http.Client{}
	req, err := http.NewRequest("POST", TRANSISTOR_API_URL, bytes.NewBuffer(jsonData))
	if err != nil {
		return nil, err
	}
	req.Header.Set("x-api-key", TRANSISTOR_API_KEY)
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

func processCSV(csvPath, TRANSISTOR_API_URL, TRANSISTOR_API_KEY, TRANSISTOR_SHOW_ID string) error {
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

		response, err := createDraftEpisode(episodeData, TRANSISTOR_API_URL, TRANSISTOR_API_KEY, TRANSISTOR_SHOW_ID)
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
	if err := processCSV(csvFilePath, TRANSISTOR_API_URL, TRANSISTOR_API_KEY, TRANSISTOR_SHOW_ID); err != nil {
		fmt.Println("Error processing CSV file:", err)
	}
}
