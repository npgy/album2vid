// AUTHOR: Nicholas Preston (npgy) and Alexis Masson (Aveheuzed)

package main

import (
	"flag"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"sort"
	"strconv"
	"strings"

	"github.com/npgy/album2vid/internal/ffmpegbin"
)

var ffmpegBin string
var ffprobeBin string

func extractEmbedded(tmpd string) (string, string) {
	ffmpegName := "ffmpeg"
	ffprobeName := "ffprobe"
	if runtime.GOOS == "windows" {
		ffmpegName = "ffmpeg.exe"
		ffprobeName = "ffprobe.exe"
	}

	ffmpegPath := filepath.Join(tmpd, ffmpegName)
	ffprobePath := filepath.Join(tmpd, ffprobeName)

	if err := os.WriteFile(ffmpegPath, ffmpegbin.FFmpeg, 0755); err != nil {
		throwError("Failed to extract ffmpeg: " + err.Error())
	}
	if err := os.WriteFile(ffprobePath, ffmpegbin.FFprobe, 0755); err != nil {
		throwError("Failed to extract ffprobe: " + err.Error())
	}

	return ffmpegPath, ffprobePath
}

func getRuntime(filename string) (float64, error) {
	cmd := exec.Command(ffprobeBin,
		"-v", "quiet",
		"-show_entries", "format=duration",
		"-of", "csv=p=0",
		filename,
	)
	out, err := cmd.Output()
	if err != nil {
		return 0, err
	}
	return strconv.ParseFloat(strings.TrimSpace(string(out)), 64)
}

func getTimestamp(seconds float64) string {
	h := int(seconds) / 3600
	m := (int(seconds) % 3600) / 60
	s := int(seconds) % 60
	return fmt.Sprintf("%02d:%02d:%02d", h, m, s)
}

func throwError(text string) {
	fmt.Fprintln(os.Stderr, "ERROR: "+text)
	os.Exit(1)
}

func cleanup(tempDir string) {
	os.RemoveAll(tempDir)
}

func preprocessFiles(infiles []string, tmpd string) []string {
	outfiles := make([]string, len(infiles))
	for i, inf := range infiles {
		base := filepath.Base(inf)
		name := strings.TrimSuffix(base, filepath.Ext(base)) + ".m4a"
		outf, _ := filepath.Abs(filepath.Join(tmpd, name))
		outfiles[i] = outf

		cmd := exec.Command(ffmpegBin,
			"-i", inf,
			"-map", "0",
			"-map", "-v?",
			"-map", "-V?",
			"-acodec", "aac",
			"-b:a", "320k",
			outf,
		)
		cmd.Stdout = os.Stdout
		cmd.Stderr = os.Stderr
		cmd.Run()
	}
	return outfiles
}

func genFilelist(infiles []string, tmpd string) string {
	filename := filepath.Join(tmpd, "files.txt")
	f, err := os.Create(filename)
	if err != nil {
		throwError("Could not create filelist: " + err.Error())
	}
	defer f.Close()

	for _, file := range infiles {
		escaped := strings.ReplaceAll(file, "'", "'\\''")
		fmt.Fprintf(f, "file '%s'\n", escaped)
	}
	return filename
}

func genTracklist(infiles []string, outfile string) {
	f, err := os.Create(outfile)
	if err != nil {
		throwError("Could not create tracklist: " + err.Error())
	}
	defer f.Close()

	currTime := 0.0
	for _, file := range infiles {
		stem := strings.TrimSuffix(filepath.Base(file), filepath.Ext(file))
		fmt.Fprintf(f, "%s -- %s\n", stem, getTimestamp(currTime))
		if runtime, err := getRuntime(file); err == nil {
			currTime += runtime
		}
	}
}

func getcover(srcdir string) string {
	for _, name := range []string{"cover.jpg", "cover.png"} {
		candidate := filepath.Join(srcdir, name)
		if _, err := os.Stat(candidate); err == nil {
			return candidate
		}
	}
	throwError("The cover photo could not be found")
	return ""
}

func getSrcFiles(srcdir string) []string {
	exts := map[string]bool{
		".wav": true, ".mp3": true, ".m4a": true, ".ogg": true, ".flac": true,
	}

	entries, err := os.ReadDir(srcdir)
	if err != nil {
		throwError("Could not read directory: " + err.Error())
	}

	var files []string
	for _, e := range entries {
		if e.IsDir() {
			continue
		}
		if exts[strings.ToLower(filepath.Ext(e.Name()))] {
			abs, _ := filepath.Abs(filepath.Join(srcdir, e.Name()))
			files = append(files, abs)
		}
	}

	if len(files) == 0 {
		throwError("The audio files could not be found")
	}

	sort.Slice(files, func(i, j int) bool {
		si := strings.TrimSuffix(filepath.Base(files[i]), filepath.Ext(files[i]))
		sj := strings.TrimSuffix(filepath.Base(files[j]), filepath.Ext(files[j]))
		return si < sj
	})

	return files
}

func mainFfmpegCall(filelist, cover string, totalDuration float64, outfile string) {
	cmd := exec.Command(ffmpegBin,
		"-hwaccel", "auto",
		"-y",
		"-loop", "1",
		"-framerate", "1",
		"-i", cover,
		"-f", "concat",
		"-safe", "0",
		"-i", filelist,
		"-tune", "stillimage",
		"-t", fmt.Sprintf("%.2f", totalDuration),
		"-vf", "format=yuv420p",
		"-s", "1080x1080",
		"-b:a", "320k",
		outfile,
	)
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	cmd.Run()
}

func getTotalDuration(infiles []string) float64 {
	total := 0.0
	for _, file := range infiles {
		if runtime, err := getRuntime(file); err == nil {
			total += runtime
		}
	}
	return total
}

func main() {
	fast := flag.Bool("f", false, "Enables fast mode, may cause rendering errors")
	flag.BoolVar(fast, "fast", false, "Enables fast mode, may cause rendering errors")
	flag.Usage = func() {
		fmt.Fprintf(os.Stderr, "Usage: album2vid [options] <path>\n")
		flag.PrintDefaults()
	}
	flag.Parse()

	if flag.NArg() < 1 {
		flag.Usage()
		os.Exit(1)
	}

	srcPath := flag.Arg(0)
	info, err := os.Stat(srcPath)
	if err != nil || !info.IsDir() {
		throwError("The directory could not be found")
	}

	tempDir, err := os.MkdirTemp("", "album2vid")
	if err != nil {
		throwError("Could not create temp directory: " + err.Error())
	}
	defer cleanup(tempDir)
	ffmpegBin, ffprobeBin = extractEmbedded(tempDir)
	fmt.Println("Welcome to album2vid!")

	sourceFiles := getSrcFiles(srcPath)
	cover := getcover(srcPath)

	var ppfiles []string
	if *fast {
		ppfiles = make([]string, len(sourceFiles))
		copy(ppfiles, sourceFiles)
	} else {
		ppfiles = preprocessFiles(sourceFiles, tempDir)
	}

	filelist := genFilelist(ppfiles, tempDir)
	totalDuration := getTotalDuration(ppfiles)
	genTracklist(sourceFiles, filepath.Join(srcPath, "tracklist.txt"))
	mainFfmpegCall(filelist, cover, totalDuration, filepath.Join(srcPath, "out.mp4"))
}
