{ pkgs ? import <nixpkgs> { } }:
pkgs.poetry2nix.mkPoetryApplication {
  poetrylock = ./poetry.lock;
  pyproject = ./pyproject.toml;
  python = pkgs.python3;
  src = pkgs.lib.cleanSource ./.;
}
