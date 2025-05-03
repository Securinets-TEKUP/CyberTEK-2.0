package main

import (
	"context"
	"flag"
	"log"

	"github.com/minio/minio-go/v7"
	"github.com/minio/minio-go/v7/pkg/credentials"
)

var (
	Cfg = struct {
		EndPoint        string
		AccessKeyID     string
		SecretAccessKey string
		UseSSL          bool
	}{}
	BucketName string
	Location   string
)

func main() {
	//flags
	flag.StringVar(&Cfg.EndPoint, "endpoint", "", "MinIO server endpoint")
	flag.StringVar(&Cfg.AccessKeyID, "access-key", "", "MinIO access key ID")
	flag.StringVar(&Cfg.SecretAccessKey, "secret-key", "", "MinIO secret access key")
	flag.BoolVar(&Cfg.UseSSL, "use-ssl", false, "Use SSL for connection")
	flag.StringVar(&BucketName, "bucket", "", "Bucket name")
	flag.StringVar(&Location, "location", "us-west-1", "Bucket location")

	filePath := flag.String("file", "", "file to be uploaded")
	objectName := flag.String("object", "", "object name")
	contentType := flag.String("content-type", "application/octet-stream", "content type")

	flag.Parse()

	// validate
	if Cfg.EndPoint == "" || Cfg.AccessKeyID == "" || Cfg.SecretAccessKey == "" {
		log.Fatalln("Error: endpoint, access-key and secret-key are required parameters")
	}
	if *filePath == "" || *objectName == "" {
		log.Fatalln("Error: file and obj-name are required parameters")
	}

	ctx := context.Background()

	// init minio client
	minioClient, err := minio.New(Cfg.EndPoint, &minio.Options{
		Creds:  credentials.NewStaticV4(Cfg.AccessKeyID, Cfg.SecretAccessKey, ""),
		Secure: Cfg.UseSSL,
	})
	if err != nil {
		log.Fatalln("Failed to initialize MinIO client:", err)
	}

	info, err := minioClient.FPutObject(ctx, BucketName, *objectName, *filePath, minio.PutObjectOptions{ContentType: *contentType})
	if err != nil {
		log.Fatalln("Failed to upload file:", err)
	}

	log.Printf("Successfully uploaded %s of size %d bytes\n", *objectName, info.Size)
}