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
          python3Packages.unicorn
          python3Packages.fonttools
          unicorn
          llvmPackages.clang-unwrapped
          lld
          llvm
          binutils
          squashfsTools
          openssl
          pkg-config
          imagemagick
          graphify
          # test/boot.py: V2.1's demo under user-mode emulation, sandboxed
          qemu-user
          bubblewrap
          # tools/release.py package: the user guide's text check (docs/manual/build.py)
          poppler-utils
        ];

        hardeningDisable = [ "all" ];

        shellHook = ''
          export NIX_HARDENING_ENABLE=""
          # mksquashfs 4.7 refuses SOURCE_DATE_EPOCH beside the times tools/build.py passes; the build
          # takes stock's times, as without Nix.
          unset SOURCE_DATE_EPOCH
          export LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath [ pkgs.stdenv.cc.cc.lib ]}:''${LD_LIBRARY_PATH:-}"
        '';
      };
    };
}
