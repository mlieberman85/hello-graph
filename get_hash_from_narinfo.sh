#!/usr/bin/env bash

NAR_LOOKUP=$(echo $1 | xargs basename | sed 's/-.*//')
# FIXME: Some nix hashes are not sha256. This ends up giving incorrect hash in many cases
curl https://cache.nixos.org/$NAR_LOOKUP.narinfo | grep NarHash | sed 's/^.*://' | xargs nix-hash --to-base16 --type sha256
