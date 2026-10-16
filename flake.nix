{
  description = "Q2 Pod firmware build and development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs =
    { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
    in
    {
      devShells.${system}.default = (pkgs.mkShell.override { stdenv = pkgs.multiStdenv; }) {
        packages = with pkgs; [
          python3
          llvmPackages.clang-unwrapped
          lld
          llvm
          binutils
          squashfsTools
          openssl
          pkg-config
          graphify
        ];

        hardeningDisable = [ "all" ];

        shellHook = ''
          export NIX_HARDENING_ENABLE=""
        '';
      };
    };
}
