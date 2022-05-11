# Nix2SLSA POC

Do not actually use in this state. It is configured to my personal setup and requires some changes.

It assumes you have:
* Cosign installed. Assumes using code based on this PR: https://github.com/sigstore/cosign/pull/1265
* In order to build a graph out of this you can follow: https://github.com/mlieberman85/scq -- also still in POC.
* It might require nix experimental commands?

## Use (only for dev/testing out)

```
./generate.sh <nix_store_path>
```

This will take a while.
