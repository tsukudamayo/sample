# FROM golang:1.20-bullseye AS builder

# ENV GO111MODULE=on
#     && go get -u golang.org/x/tools/cmd/goimports \
#     && go get -u golang.org/x/tools/cmd/godoc \
#     && go get -u golang.org/x/lint/golint \
#     && go get -u github.com/stamblerre/gocode \
#     && go get -u github.com/rogpeppe/godef \
#     && go get -u github.com/jstemmer/gotags \
#     && go get -u github.com/kisielk/errcheck \
#     && go get github.com/go-delve/delve/cmd/dlv 

FROM golang:1.20-bullseye
ENV GO111MODULE=on
ENV PATH $PATH:/usr/local/go/bin
ENV GOPATH /go
ENV PATH $GOPATH/bin:$PATH
# COPY --from=builder /go/bin/gopls /go/bin/gopls

RUN apt-get update \
    && apt-get install -y git \
    gnupg \
    curl \
    software-properties-common \
    # && go get -u golang.org/x/tools/gopls \
    && go install golang.org/x/tools/gopls@latest \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /go

EXPOSE 8080

CMD ["/bin/bash"]
