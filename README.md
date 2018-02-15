# Work In Progress

# Dnote Server

Python Flask server to sync notes from [dnote-cli](https://github.com/dnote-io/cli)

# Why?

I have started this to understand what is happening when we sync the notes with a backend server, which is at the moment provided as a paid option by the developer. I am not sure if the developer would be releasing the source for the backend server to self-host. Until then this is the option I'll be going with.

# How?

## Pre-requisites

* Golang is setup on local machine.
* Clone [dnote-cli](https://github.com/dnote-io/cli) to `$GOPATH/src` and checkout to a stable release.
* Download stable release of [go-dep](https://github.com/golang/dep/releases) and make sure it is available in the `$PATH`. Probably rename it to `dep` so its easier.
* `cd` into the cloned dnote-cli directory and run `dep ensure` to install all necessary dependencies.
* Run `go install -ldflags "-X main.apiEndpoint=http://127.0.0.1:5000"` which would build, change api endpoint for syncing and place the executable in `$GOPATH/bin`.

**Note:** Use this modified version of dnote-cli further.

## Install Flask 

**Note:** Use a virtual environment.

```
git clone <this_repo> dnote-server
cd dnote-server
pip install -r requirements.txt
python app.py
```
Flask should be running at http://0.0.0.0:5000. 

## Test the setup

With flask server running,

* Create a new note with `<dnote-cli> add js`
* `<dnote-cli> sync`
* You should see the deserialized output on the server console

Playaround with the setup as you like.
