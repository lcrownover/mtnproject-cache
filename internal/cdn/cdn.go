package cdn

import (
	"errors"
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
)

type CDNLinkHandler struct {
	Name string
	URL  string
}

func NewCDNLinkHandler(imageName, imageURL string) *CDNLinkHandler {
	return &CDNLinkHandler{imageName, imageURL}
}

func (h CDNLinkHandler) getFilename() string {
	res_parts := strings.Split(h.URL, "/")
	resource := res_parts[len(res_parts)-1]
	f_parts := strings.Split(resource, ".")
	filename := f_parts[0]
	ext := f_parts[1]
	return fmt.Sprintf("%s_%s.%s", filename, h.Name, ext)
}

func (h CDNLinkHandler) SaveImage() error {
	fileName := h.getFilename()

	resp, err := http.Get(h.URL)
	if err != nil {
		return err
	}

	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		return errors.New("Received non-200 response code")
	}

	file, err := os.Create(fileName)
	if err != nil {
		return err
	}

	defer file.Close()

	_, err = io.Copy(file, resp.Body)
	if err != nil {
		return err
	}

	return nil
}
