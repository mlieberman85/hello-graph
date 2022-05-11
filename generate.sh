#!/usr/bin/env bash

# Nix Path is just a path to a build or nix-store
NIX_PATH=$1
COSIGN_EXPERIMENTAL=1
COSIGN_PASSWORD=""

rm drvmod/*
rm attestations/*

nix show-derivation -r $1 > build.json

python get_data.py

pushd drvmod
cue import -p main -l "_drv:" -f
for f in *.cue; do
    cue eval ../drv2slsa.cue $f --out json >../attestations/$f.json
done
popd

pushd attestations
for f in *.json; do
    for h in $(cat $f | jq .subject[].digest.sha256 | tr -d '"'); do
        PREDICATE=$(cat $f | jq .predicate)
    #gpg --batch --yes --passphrase "foo" --output attestation.sig --detach-sig $f
    #rekor-cli upload --artifact $f --artifact-hash $ARTIFACT_HASH --public-key ../tpm.pub --signature attestation.sig
        COSIGN_EXPERIMENTAL=1 COSIGN_PASSWORD="" ~/go/bin/cosign attest-blob --key ../cosign.key --predicate <(echo $PREDICATE) --type slsaprovenance --hash $h $f
    done
done
popd
