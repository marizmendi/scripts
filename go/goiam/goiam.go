package main

import (
	"io/ioutil"
	"os"

	"github.com/aws/aws-sdk-go/aws"

	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/iam"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func main() {
	sess := session.Must(session.NewSessionWithOptions(session.Options{
		SharedConfigState: session.SharedConfigEnable,
	}))

	svc := iam.New(sess)

	input := &iam.CreateAccessKeyInput{
		UserName: aws.String("manuel"),
	}

	result, err := svc.CreateAccessKey(input)
	check(err)

	string := "[default]" + "\n" +
		"aws_access_key_id=" + *result.AccessKey.AccessKeyId + "\n" +
		"aws_secret_access_key=" + *result.AccessKey.SecretAccessKey + "\n"
	creds := []byte(string)
	err = ioutil.WriteFile(os.Getenv("HOME")+"/.aws/credentials_2", creds, 0644)
	check(err)
}
