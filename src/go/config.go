// Package config contains shared constants.
package config

const (
    ApiURL      = "https://api.transistor.fm/v1/episodes"
    ShowID      = "12890"
    CSVFilePath = "./config/go/scotus.csv"
)

// TransistorAPIKey retrieves the API Key from environment variables.
func TransistorAPIKey() string {
    return os.Getenv("TRANSISTOR_API_KEY")
}
