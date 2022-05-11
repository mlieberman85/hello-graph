{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    nativeBuildInputs = with pkgs; [ 
      python3
      cue
      curl
      rekor-cli
    ];
}
