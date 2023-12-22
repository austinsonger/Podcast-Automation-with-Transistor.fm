// Package config contains shared constants.
package config

import "os"

const (
	TRANSISTOR_API_URL = "https://api.transistor.fm/v1/episodes"
	TRANSISTOR_SHOW_ID = "12890"
	TRANSISTOR_API_KEY = os.Getenv("TRANSISTOR_API_KEY")
	imgurAPIURL        = "https://api.imgur.com/3/upload"
	caseBasePath       = "/2023/"
	CSVFilePath        = "./config/go/scotus.csv"
)
