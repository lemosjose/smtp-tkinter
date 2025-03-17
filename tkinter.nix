{ pkgs ? import <nixpkgs> {} }:
(pkgs.buildFHSUserEnv {
  name = "tkinter test";
  targetPkgs = pkgs: (with pkgs; [
    python313Full
    poetry
    python313Packages.pip
    python313Packages.tkinter
    tk
  ]);
  runScript = "bash";
}).env
