package main

import (
    "bufio"
    "encoding/csv"
    "fmt"
    "image"
    "image/color"
    "image/draw"
    "image/png"
    "io"
    "os"
    "path/filepath"

    "golang.org/x/image/font"
    "golang.org/x/image/font/basicfont"
    "golang.org/x/image/math/fixed"
)

func main() {
    // Load CSV file
    csvFile, err := os.Open("./config/scotus.csv")
    if err != nil {
        fmt.Println("Error opening CSV file:", err)
        return
    }
    defer csvFile.Close()

    reader := csv.NewReader(bufio.NewReader(csvFile))

    baseDir := "../2023/"
    graphicPath := "./config/Blank.png"

    for {
        record, err := reader.Read()
        if err == io.EOF {
            break
        }
        if err != nil {
            fmt.Println("Error reading CSV record:", err)
            continue
        }

        title := record[0] // Assuming 'Title' is in the first column
        caseID := record[1] // Assuming 'Case ID' is in the second column

        caseDir := filepath.Join(baseDir, caseID)
        os.MkdirAll(caseDir, os.ModePerm)

        imagesDir := filepath.Join(caseDir, "images")
        os.MkdirAll(imagesDir, os.ModePerm)

        newImagePath := filepath.Join(imagesDir, fmt.Sprintf("%s_cover.png", caseID))
        if _, err := os.Stat(newImagePath); os.IsNotExist(err) {
            img, err := os.Open(graphicPath)
            if err != nil {
                fmt.Println("Error opening image file:", err)
                continue
            }

            src, err := png.Decode(img)
            if err != nil {
                fmt.Println("Error decoding image:", err)
                continue
            }
            img.Close()

            dst := image.NewRGBA(src.Bounds())
            draw.Draw(dst, dst.Bounds(), src, image.Point{}, draw.Src)

            addLabel(dst, 500, 1500, title)

            outFile, err := os.Create(newImagePath)
            if err != nil {
                fmt.Println("Error creating output file:", err)
                continue
            }
            defer outFile.Close()

            png.Encode(outFile, dst)
        } else {
            fmt.Println("Skipping, image already exists:", newImagePath)
        }
    }
}

func addLabel(img *image.RGBA, x, y int, label string) {
    col := color.RGBA{255, 255, 255, 255} // White color
    point := fixed.Point26_6{fixed.Int26_6(x * 64), fixed.Int26_6(y * 64)}

    d := &font.Drawer{
        Dst:  img,
        Src:  image.NewUniform(col),
        Face: basicfont.Face7x13,
        Dot:  point,
    }
    d.DrawString(label)
}
