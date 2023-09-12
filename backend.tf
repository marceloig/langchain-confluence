terraform {
  cloud {
    organization = "dde"

    workspaces {
      name = "playlist-sync"
    }
  }
}